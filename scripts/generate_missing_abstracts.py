#!/usr/bin/env python3
"""
Скрипт для автоматического генерирования недостающих аннотаций используя OpenAI API.
"""
import os
import re
import logging
import yaml
from pathlib import Path
from openai import OpenAI

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_abstract(title: str) -> str:
    """Генерирует аннотацию на основе названия статьи используя OpenAI API."""
    if not title or len(title.strip()) < 10:
        return ""
    
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": """You are an expert academic writer specializing in maritime autonomous systems and robotics. 
Generate a professional, detailed abstract (150-200 words) for a research paper based on the given title. 
The abstract should:
1. Clearly state the problem/motivation
2. Describe the proposed approach or methodology
3. Highlight key contributions
4. Mention results or implications
Write in formal academic English, suitable for a peer-reviewed journal."""},
                {"role": "user", "content": f"Generate an abstract for this paper title: {title}"}
            ],
            temperature=0.7,
            max_tokens=400
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Ошибка при генерировании аннотации: {e}")
        return ""

def translate_to_russian(text: str) -> str:
    """Переводит текст на русский язык используя OpenAI API."""
    if not text or len(text.strip()) < 10:
        return ""
    
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a professional translator. Translate the following academic abstract to Russian. Maintain technical terms and scientific accuracy. Keep the same structure and length."},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Ошибка при переводе текста: {e}")
        return ""

def generate_key_findings(abstract: str) -> str:
    """Генерирует ключевые выводы из аннотации используя OpenAI API."""
    if not abstract or len(abstract.strip()) < 50:
        return ""
    
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are an expert in summarizing academic papers. Extract 3-5 key findings from the abstract. Format as a bullet list with clear, concise statements. Be specific and technical."},
                {"role": "user", "content": f"Abstract: {abstract}"}
            ],
            temperature=0.3,
            max_tokens=300
        )
        findings = response.choices[0].message.content.strip()
        # Убеждаемся, что каждая строка начинается с '-'
        lines = findings.split('\n')
        formatted_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('-'):
                formatted_lines.append(f"- {line}")
            elif line:
                formatted_lines.append(line)
        return '\n'.join(formatted_lines)
    except Exception as e:
        logger.error(f"Ошибка при генерации ключевых выводов: {e}")
        return ""

def extract_frontmatter(content: str) -> tuple:
    """Извлекает frontmatter из markdown файла."""
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        return {}, content
    
    frontmatter_str = match.group(1)
    body = match.group(2)
    
    try:
        frontmatter = yaml.safe_load(frontmatter_str)
        return frontmatter or {}, body
    except Exception as e:
        logger.warning(f"Ошибка при парсинге frontmatter: {e}")
        return {}, content

def update_paper_file(filepath: str) -> bool:
    """Обновляет файл статьи с автоматически сгенерированной аннотацией."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Извлекаем frontmatter и body
        frontmatter, body = extract_frontmatter(content)
        
        # Проверяем, есть ли уже перевод
        if frontmatter.get('abstract_ru') and frontmatter.get('abstract_ru') != '':
            if not frontmatter.get('abstract_ru').startswith('_'):
                logger.info(f"✓ {filepath} уже содержит перевод")
                return False
        
        # Получаем название статьи
        title = frontmatter.get('title', '')
        if not title:
            logger.warning(f"✗ {filepath} не содержит названия")
            return False
        
        logger.info(f"Генерирую аннотацию для: {title[:60]}...")
        
        # Генерируем аннотацию
        abstract_en = generate_abstract(title)
        if not abstract_en:
            logger.warning(f"✗ Не удалось сгенерировать аннотацию для {filepath}")
            return False
        
        logger.info(f"Генерирую перевод и выводы...")
        
        # Генерируем перевод и ключевые выводы
        abstract_ru = translate_to_russian(abstract_en)
        key_findings = generate_key_findings(abstract_en)
        
        if not abstract_ru or not key_findings:
            logger.warning(f"✗ Не удалось сгенерировать перевод или выводы для {filepath}")
            return False
        
        # Обновляем frontmatter
        frontmatter['abstract_en'] = abstract_en
        frontmatter['abstract_ru'] = abstract_ru
        frontmatter['key_findings'] = key_findings
        
        # Генерируем новый frontmatter
        new_frontmatter = "---\n"
        for key, value in frontmatter.items():
            if isinstance(value, list):
                items_str = ", ".join(f'"{item}"' for item in value)
                new_frontmatter += f'{key}: [{items_str}]\n'
            else:
                # Экранируем кавычки
                value_str = str(value).replace('"', '\\"')
                new_frontmatter += f'{key}: "{value_str}"\n'
        new_frontmatter += "---\n"
        
        # Обновляем body
        new_body = body
        
        # Заменяем аннотацию оригинал
        new_body = re.sub(
            r'## Аннотация \(оригинал\)\n\n.*?\n\n',
            f'## Аннотация (оригинал)\n\n{abstract_en}\n\n',
            new_body,
            flags=re.DOTALL
        )
        
        # Заменяем перевод
        new_body = re.sub(
            r'## Аннотация \(русский перевод\)\n\n.*?\n\n',
            f'## Аннотация (русский перевод)\n\n{abstract_ru}\n\n',
            new_body,
            flags=re.DOTALL
        )
        
        # Заменяем ключевые выводы
        new_body = re.sub(
            r'## Ключевые выводы\n\n.*?\n\n',
            f'## Ключевые выводы\n\n{key_findings}\n\n',
            new_body,
            flags=re.DOTALL
        )
        
        # Записываем обновленный файл
        new_content = new_frontmatter + new_body
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        logger.info(f"✓ Успешно обновлен {filepath}")
        return True
        
    except Exception as e:
        logger.error(f"✗ Ошибка при обновлении {filepath}: {e}")
        return False

def main():
    """Основная функция."""
    papers_dir = "docs/papers"
    
    if not os.path.exists(papers_dir):
        logger.error(f"Директория {papers_dir} не найдена")
        return
    
    # Находим все файлы статей
    paper_files = sorted(Path(papers_dir).glob("paper_*.md"))
    
    if not paper_files:
        logger.warning(f"Статьи не найдены в {papers_dir}")
        return
    
    logger.info(f"Найдено {len(paper_files)} статей для проверки")
    
    updated_count = 0
    for filepath in paper_files:
        if update_paper_file(str(filepath)):
            updated_count += 1
    
    logger.info(f"\n✓ Обновлено {updated_count} из {len(paper_files)} статей")

if __name__ == "__main__":
    main()
