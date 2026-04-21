#!/usr/bin/env python3
"""
update_glossary.py — Автоматическое обновление глоссария MASS Handbook.

Алгоритм:
1. Сканирует все статьи в docs/papers/ и собирает уникальные теги
2. Сравнивает с существующим глоссарием (glossary-data.json)
3. Для новых тегов запрашивает LLM для генерации определений
4. Перегенерирует glossary.md (краткий) и glossary-extended.md (подробный)
"""

import os
import re
import json
import glob
import logging
import argparse
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ─── LLM helper ────────────────────────────────────────────────────────────────

def call_llm(prompt: str, model: str = "gpt-4.1-mini") -> str:
    """Вызов LLM через OpenAI-совместимый API."""
    try:
        from openai import OpenAI
        client = OpenAI()
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=800,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.warning(f"LLM недоступен: {e}")
        return ""

# ─── Сбор тегов из статей ──────────────────────────────────────────────────────

def collect_tags_from_papers(papers_dir: str) -> dict:
    """
    Собирает все теги из статей и возвращает словарь:
    {tag: [список файлов статей, где встречается тег]}
    """
    tag_to_papers = {}
    paper_files = sorted(glob.glob(os.path.join(papers_dir, "*.md")))

    for filepath in paper_files:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()

        # Извлекаем теги из frontmatter
        m = re.search(r'^tags:\s*\[(.+?)\]', content, re.MULTILINE)
        if not m:
            continue

        raw = m.group(1)
        tags_in_file = []
        for t in re.findall(r'"([^"]+)"|([^,\s"][^,"]*[^,\s"])', raw):
            tag = (t[0] or t[1]).strip().strip('"').strip()
            if tag:
                tags_in_file.append(tag)

        # Извлекаем название статьи из frontmatter
        title_m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
        paper_title = title_m.group(1).strip() if title_m else os.path.basename(filepath)

        # Извлекаем DOI
        doi_m = re.search(r'^doi:\s*(.+?)\s*$', content, re.MULTILINE)
        doi = doi_m.group(1).strip() if doi_m else ""

        paper_info = {
            "file": os.path.basename(filepath),
            "title": paper_title,
            "doi": doi,
        }

        for tag in tags_in_file:
            if tag not in tag_to_papers:
                tag_to_papers[tag] = []
            # Избегаем дубликатов
            if paper_info not in tag_to_papers[tag]:
                tag_to_papers[tag].append(paper_info)

    logger.info(f"Найдено {len(tag_to_papers)} уникальных тегов в {len(paper_files)} статьях")
    return tag_to_papers

# ─── Загрузка / сохранение базы данных глоссария ──────────────────────────────

def load_glossary_db(db_path: str) -> dict:
    """Загружает базу данных глоссария из JSON-файла."""
    if os.path.exists(db_path):
        with open(db_path, encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_glossary_db(db: dict, db_path: str):
    """Сохраняет базу данных глоссария в JSON-файл."""
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    logger.info(f"База данных глоссария сохранена: {db_path}")

# ─── Генерация определений через LLM ──────────────────────────────────────────

def generate_term_definition(tag: str, papers: list) -> dict:
    """
    Генерирует определение термина через LLM.
    Возвращает словарь с полями: definition_ru, definition_en, context, related_terms, examples
    """
    # Формируем контекст из статей
    paper_titles = [p["title"][:80] for p in papers[:3]]
    papers_context = "\n".join(f"- {t}" for t in paper_titles)

    prompt = f"""Ты эксперт в области морских автономных надводных судов (MASS).
Напиши краткую энциклопедическую статью для глоссария по термину: "{tag}"

Контекст: этот термин встречается в следующих научных статьях по MASS:
{papers_context}

Верни ответ строго в формате JSON (без markdown-блоков):
{{
  "definition_ru": "Краткое определение на русском (1-2 предложения)",
  "definition_en": "Brief definition in English (1-2 sentences)",
  "context": "Контекст применения в MASS (2-3 предложения на русском)",
  "related_terms": ["список", "связанных", "терминов"],
  "examples": ["Пример использования 1", "Пример использования 2"]
}}"""

    result = call_llm(prompt)
    if not result:
        return {
            "definition_ru": f"Термин, используемый в контексте морских автономных надводных судов (MASS).",
            "definition_en": f"Term used in the context of Maritime Autonomous Surface Ships (MASS).",
            "context": "Применяется в системах автономного управления судами.",
            "related_terms": ["MASS"],
            "examples": [],
        }

    # Парсим JSON
    try:
        # Убираем возможные markdown-блоки
        result = re.sub(r'^```json\s*', '', result, flags=re.MULTILINE)
        result = re.sub(r'^```\s*$', '', result, flags=re.MULTILINE)
        return json.loads(result)
    except json.JSONDecodeError:
        logger.warning(f"Не удалось распарсить JSON для термина '{tag}': {result[:100]}")
        return {
            "definition_ru": result[:200] if result else f"Термин из области MASS.",
            "definition_en": "",
            "context": "",
            "related_terms": [],
            "examples": [],
        }

# ─── Обновление базы данных глоссария ─────────────────────────────────────────

def update_glossary_db(db: dict, tag_to_papers: dict) -> tuple[dict, list]:
    """
    Обновляет базу данных глоссария:
    - Добавляет новые термины с определениями от LLM
    - Обновляет список статей для существующих терминов
    Возвращает (обновленная_база, список_новых_тегов)
    """
    new_tags = []

    for tag, papers in tag_to_papers.items():
        if tag not in db:
            # Новый термин — генерируем определение
            logger.info(f"Новый термин: '{tag}' — генерирую определение...")
            definition = generate_term_definition(tag, papers)
            db[tag] = {
                "tag": tag,
                "definition_ru": definition.get("definition_ru", ""),
                "definition_en": definition.get("definition_en", ""),
                "context": definition.get("context", ""),
                "related_terms": definition.get("related_terms", []),
                "examples": definition.get("examples", []),
                "papers": papers,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }
            new_tags.append(tag)
        else:
            # Существующий термин — обновляем список статей
            existing_files = {p["file"] for p in db[tag].get("papers", [])}
            for paper in papers:
                if paper["file"] not in existing_files:
                    db[tag]["papers"].append(paper)
                    existing_files.add(paper["file"])
            db[tag]["updated_at"] = datetime.now().isoformat()

    return db, new_tags

# ─── Генерация glossary.md (краткий) ──────────────────────────────────────────

def generate_basic_glossary(db: dict) -> str:
    """Генерирует краткий глоссарий glossary.md."""
    lines = [
        "---",
        "sidebar_position: 3",
        "---",
        "# Глоссарий MASS",
        "",
        "Краткий справочник ключевых терминов и аббревиатур, используемых в области морских автономных надводных судов (MASS).",
        "",
        f"> Глоссарий содержит **{len(db)} терминов**. Последнее обновление: {datetime.now().strftime('%d.%m.%Y')}.",
        "",
        "Подробные определения, примеры и перекрестные ссылки доступны в [Расширенном глоссарии](./glossary-extended).",
        "",
    ]

    # Группируем по первой букве
    sorted_tags = sorted(db.keys(), key=lambda x: x.upper())
    current_letter = ""

    for tag in sorted_tags:
        entry = db[tag]
        first_letter = tag[0].upper()
        if first_letter != current_letter:
            current_letter = first_letter
            lines.append(f"## {current_letter}")
            lines.append("")

        definition = entry.get("definition_ru", "").strip()
        if not definition:
            definition = entry.get("definition_en", "Термин из области MASS.").strip()

        lines.append(f"### {tag}")
        lines.append(definition)
        lines.append("")

    return "\n".join(lines)

# ─── Генерация glossary-extended.md (подробный) ───────────────────────────────

def generate_extended_glossary(db: dict) -> str:
    """Генерирует расширенный глоссарий glossary-extended.md."""
    lines = [
        "---",
        "sidebar_position: 4",
        "---",
        "# Расширенный глоссарий MASS",
        "",
        "Подробное описание ключевых терминов, концепций и технологий, используемых в разработке морских автономных надводных судов.",
        "Каждый термин включает определение, контекст применения, связанные концепции и примеры использования.",
        "",
        f"> Глоссарий содержит **{len(db)} терминов**. Последнее обновление: {datetime.now().strftime('%d.%m.%Y')}.",
        "",
    ]

    sorted_tags = sorted(db.keys(), key=lambda x: x.upper())

    for tag in sorted_tags:
        entry = db[tag]

        lines.append(f"---")
        lines.append(f"")
        lines.append(f"### {tag}")
        lines.append("")

        # Определение
        if entry.get("definition_ru"):
            lines.append(f"**Определение:** {entry['definition_ru']}")
            lines.append("")

        if entry.get("definition_en"):
            lines.append(f"**Definition (EN):** {entry['definition_en']}")
            lines.append("")

        # Контекст применения
        if entry.get("context"):
            lines.append(f"**Контекст применения в MASS:**")
            lines.append("")
            lines.append(entry["context"])
            lines.append("")

        # Связанные термины
        related = entry.get("related_terms", [])
        if related:
            lines.append("**Связанные термины:**")
            lines.append("")
            for rt in related:
                # Создаем ссылку, если термин есть в базе
                anchor = rt.lower().replace(" ", "-").replace("(", "").replace(")", "")
                if rt in db:
                    lines.append(f"- [{rt}](#{anchor})")
                else:
                    lines.append(f"- {rt}")
            lines.append("")

        # Примеры
        examples = entry.get("examples", [])
        if examples:
            lines.append("**Примеры использования:**")
            lines.append("")
            for ex in examples:
                lines.append(f"- {ex}")
            lines.append("")

        # Статьи по теме
        papers = entry.get("papers", [])
        if papers:
            lines.append("**Статьи по теме:**")
            lines.append("")
            for p in papers:
                title = p.get("title", p.get("file", ""))
                file_base = p.get("file", "").replace(".md", "")
                doi = p.get("doi", "")
                if file_base:
                    lines.append(f"- [{title}](./papers/{file_base})")
                elif doi:
                    lines.append(f"- [{title}](https://doi.org/{doi})")
                else:
                    lines.append(f"- {title}")
            lines.append("")

    return "\n".join(lines)

# ─── Основная функция ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Автоматическое обновление глоссария MASS Handbook")
    parser.add_argument("--papers-dir", default="docs/papers", help="Директория со статьями")
    parser.add_argument("--output-dir", default="docs", help="Директория для записи глоссариев")
    parser.add_argument("--db-path", default="scripts/glossary-data.json", help="Путь к базе данных глоссария")
    parser.add_argument("--force-regenerate", action="store_true", help="Перегенерировать все определения")
    args = parser.parse_args()

    # 1. Сканируем статьи
    logger.info("=== Шаг 1: Сканирование статей ===")
    tag_to_papers = collect_tags_from_papers(args.papers_dir)

    # 2. Загружаем базу данных
    logger.info("=== Шаг 2: Загрузка базы данных глоссария ===")
    db = {} if args.force_regenerate else load_glossary_db(args.db_path)
    logger.info(f"Загружено {len(db)} существующих терминов")

    # 3. Обновляем базу данных
    logger.info("=== Шаг 3: Обновление базы данных ===")
    db, new_tags = update_glossary_db(db, tag_to_papers)

    if new_tags:
        logger.info(f"Добавлено {len(new_tags)} новых терминов: {', '.join(new_tags)}")
    else:
        logger.info("Новых терминов не обнаружено")

    # 4. Сохраняем базу данных
    logger.info("=== Шаг 4: Сохранение базы данных ===")
    os.makedirs(os.path.dirname(args.db_path), exist_ok=True)
    save_glossary_db(db, args.db_path)

    # 5. Генерируем файлы глоссария
    logger.info("=== Шаг 5: Генерация файлов глоссария ===")
    os.makedirs(args.output_dir, exist_ok=True)

    basic_path = os.path.join(args.output_dir, "glossary.md")
    with open(basic_path, "w", encoding="utf-8") as f:
        f.write(generate_basic_glossary(db))
    logger.info(f"✓ Краткий глоссарий: {basic_path}")

    extended_path = os.path.join(args.output_dir, "glossary-extended.md")
    with open(extended_path, "w", encoding="utf-8") as f:
        f.write(generate_extended_glossary(db))
    logger.info(f"✓ Расширенный глоссарий: {extended_path}")

    logger.info(f"\n✅ Готово! Глоссарий содержит {len(db)} терминов.")
    if new_tags:
        logger.info(f"   Новые термины: {', '.join(new_tags)}")

if __name__ == "__main__":
    main()
