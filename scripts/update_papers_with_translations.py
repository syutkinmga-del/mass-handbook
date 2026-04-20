#!/usr/bin/env python3
"""
Скрипт для обновления существующих статей с переводами и ключевыми выводами.
"""
import os
import re
import logging
from pathlib import Path
from openai import OpenAI
import yaml

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def translate_to_russian(text: str) -> str:
    """
    Переводит текст на русский язык используя OpenAI API.
    """
    if not text or len(text.strip()) < 10:
        return ""
    
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a professional translator. Translate the following academic abstract to Russian. Maintain technical terms and scientific accuracy."},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.warning(f"Ошибка при переводе текста: {e}")
        return ""

def generate_key_findings(abstract: str) -> str:
    """
    Генерирует ключевые выводы из аннотации используя OpenAI API.
    """
    if not abstract or len(abstract.strip()) < 50:
        return ""
    
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are an expert in summarizing academic papers. Extract 3-5 key findings from the abstract. Format as a bullet list. Be concise and specific."},
                {"role": "user", "content": f"Abstract: {abstract}"}
            ],
            temperature=0.3,
            max_tokens=300
        )
        findings = response.choices[0].message.content.strip()
        # Ensure it's formatted as bullet points
        if not findings.startswith('-'):
            findings = '- ' + findings.replace('\n', '\n- ')
        return findings
    except Exception as e:
        logger.warning(f"Ошибка при генерации ключевых выводов: {e}")
        return ""

def clean_abstract_text(text: str) -> str:
    """
    Очищает текст аннотации от XML тегов и форматирования.
    """
    # Удаляем XML теги
    text = re.sub(r'<[^>]+>', '', text)
    # Удаляем лишние пробелы
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_frontmatter(content: str) -> tuple:
    """
    Извлекает frontmatter из markdown файла.
    Возвращает (frontmatter_dict, body_content)
    """
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

def extract_abstract_from_body(body: str) -> str:
    """
    Извлекает аннотацию из body markdown файла.
    """
    # Ищем текст между "## Аннотация (оригинал)" и следующим заголовком
    match = re.search(r'## Аннотация \(оригинал\)\n\n(.*?)\n\n##', body, re.DOTALL)
    if match:
        abstract = match.group(1).strip()
        # Проверяем, что это не плейсхолдер
        if abstract and not abstract.startswith('_'):
            return clean_abstract_text(abstract)
    
    return ""

def update_paper_file(filepath: str) -> bool:
    """
    Обновляет файл статьи с переводом и ключевыми выводами.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Извлекаем frontmatter и body
        frontmatter, body = extract_frontmatter(content)
        
        # Проверяем, есть ли уже перевод
        if frontmatter.get('abstract_ru') and frontmatter.get('key_findings') and frontmatter.get('abstract_ru') != '':
            if not frontmatter.get('abstract_ru').startswith('_'):
                logger.info(f"✓ {filepath} уже содержит перевод и ключевые выводы")
                return False
        
        # Получаем оригинальную аннотацию из frontmatter или body
        abstract_en = frontmatter.get('abstract_en', '')
        if not abstract_en:
            abstract_en = extract_abstract_from_body(body)
        
        if not abstract_en:
            logger.warning(f"✗ {filepath} не содержит оригинальную аннотацию")
            return False
        
        logger.info(f"Обновляю {filepath}...")
        
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
        
        # Обновляем body (заменяем плейсхолдеры на реальные значения)
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
    """
    Основная функция.
    """
    papers_dir = "docs/papers"
    
    if not os.path.exists(papers_dir):
        logger.error(f"Директория {papers_dir} не найдена")
        return
    
    # Находим все файлы статей
    paper_files = sorted(Path(papers_dir).glob("paper_*.md"))
    
    if not paper_files:
        logger.warning(f"Статьи не найдены в {papers_dir}")
        return
    
    logger.info(f"Найдено {len(paper_files)} статей для обновления")
    
    updated_count = 0
    for filepath in paper_files:
        if update_paper_file(str(filepath)):
            updated_count += 1
    
    logger.info(f"\n✓ Обновлено {updated_count} из {len(paper_files)} статей")

if __name__ == "__main__":
    main()
