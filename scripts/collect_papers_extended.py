#!/usr/bin/env python3
"""
Скрипт сбора и обработки научных статей.
Поддерживает поиск по ключевым словам и прямую загрузку по DOI.
"""
import os
import json
import sqlite3
import hashlib
import requests
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
import re

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def escape_mdx_content(text: str) -> str:
    """
    Экранирует специальные символы для безопасности MDX парсинга в Docusaurus.
    """
    if not text:
        return ""
    
    # Экранируем фигурные скобки
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    
    # Экранируем обратные слэши (но не двойные)
    text = re.sub(r'(?<!\\)\\(?!\\)', r'\\\\', text)
    
    return text

def sanitize_frontmatter(data: Dict) -> Dict:
    """
    Очищает frontmatter от проблемных символов.
    """
    sanitized = {}
    for key, value in data.items():
        if isinstance(value, str):
            # Экранируем кавычки в строках
            sanitized[key] = value.replace('"', '\\"').replace("'", "\\'")
        elif isinstance(value, list):
            sanitized[key] = [str(v).replace('"', '\\"').replace("'", "\\'") for v in value]
        else:
            sanitized[key] = value
    return sanitized

def generate_markdown_safe(paper_data: Dict, output_path: str) -> bool:
    """
    Генерирует Markdown файл с безопасным экранированием MDX.
    """
    try:
        # Подготовка безопасных данных для frontmatter
        safe_data = sanitize_frontmatter(paper_data)
        
        # Экранирование контента
        abstract_en = escape_mdx_content(paper_data.get('abstract_en', ''))
        abstract_ru = escape_mdx_content(paper_data.get('abstract_ru', ''))
        key_findings = escape_mdx_content(paper_data.get('key_findings', ''))
        
        # Формирование frontmatter
        frontmatter = "---\n"
        for key, value in safe_data.items():
            if key in ['abstract_en', 'abstract_ru', 'key_findings']:
                continue
            if isinstance(value, list):
                # Исправленная генерация списка: кавычки внутри f-строки
                items_str = ", ".join(f'"{item}"' for item in value)
                frontmatter += f'{key}: [{items_str}]\n'
            else:
                frontmatter += f'{key}: "{value}"\n'
        frontmatter += "---\n\n"
        
        # Формирование контента
        content = f"""# {escape_mdx_content(paper_data.get('title', 'Unknown'))}

**Авторы:** {escape_mdx_content(paper_data.get('authors', 'Unknown'))}
**Год:** {paper_data.get('year', 'N/A')}
**Источник:** {paper_data.get('source', 'Unknown')}
**DOI:** {paper_data.get('doi', 'N/A')}
**arXiv ID:** {paper_data.get('arxiv_id', 'N/A')}

## Аннотация (оригинал)

{abstract_en if abstract_en else '_Аннотация недоступна_'}

## Аннотация (русский перевод)

{abstract_ru if abstract_ru else '_Перевод недоступен_'}

## Ключевые выводы

{key_findings if key_findings else '- Статья добавлена автоматически'}

## Оценка применимости (TRL)

**TRL {paper_data.get('trl_level', 3)}** - {paper_data.get('trl_description', 'Экспериментальное подтверждение концепции')}

## Ссылки

"""
        
        # Добавляем ссылки
        links = []
        if paper_data.get('doi') and paper_data.get('doi') != 'N/A':
            links.append(f"- [Полный текст на CrossRef](https://doi.org/{paper_data['doi']})")
        if paper_data.get('url') and paper_data.get('url') != 'N/A':
            links.append(f"- [Источник]({paper_data['url']})")
        if paper_data.get('arxiv_id') and paper_data.get('arxiv_id') != 'N/A':
            links.append(f"- [arXiv](https://arxiv.org/abs/{paper_data['arxiv_id']})")
        
        if links:
            content += "\n".join(links)
        else:
            content += "- _Ссылки недоступны_"
            
        # Запись в файл
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter + content)
            
        return True
        
    except Exception as e:
        logger.error(f"✗ Ошибка при создании файла {output_path}: {e}")
        return False

def is_doi(query: str) -> bool:
    """
    Проверяет, является ли строка DOI.
    DOI обычно начинается с '10.' и содержит слэш.
    """
    return bool(re.match(r'^10\.\d{4,9}/[-._;()/:A-Z0-9]+$', query, re.IGNORECASE))

def fetch_paper_by_doi(doi: str, email: str) -> List[Dict]:
    """
    Получает конкретную статью из CrossRef по DOI.
    """
    url = f"https://api.crossref.org/works/{doi}"
    
    params = {
        'mailto': email
    }
    
    try:
        logger.info(f"Запрос статьи по DOI: {doi}")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        item = data.get('message', {})
        
        if not item:
            logger.warning(f"Статья с DOI {doi} не найдена")
            return []
            
        paper = {
            'title': item.get('title', ['Unknown'])[0],
            'authors': ', '.join([f"{a.get('given', '')} {a.get('family', '')}".strip() 
                                for a in item.get('author', [])[:3]]) or 'Unknown',
            'year': item.get('published-online', {}).get('date-parts', [[None]])[0][0] or 'N/A',
            'doi': item.get('DOI', 'N/A'),
            'abstract_en': item.get('abstract', ''),
            'source': 'crossref',
            'url': item.get('URL', ''),
            'arxiv_id': 'N/A'
        }
        
        logger.info(f"✓ Успешно получена статья по DOI: {doi}")
        return [paper]
        
    except Exception as e:
        logger.error(f"✗ Ошибка при получении статьи по DOI {doi}: {e}")
        return []

def fetch_papers_crossref(query: str, email: str, max_papers: int = 20) -> List[Dict]:
    """
    Получает статьи из CrossRef API по поисковому запросу.
    """
    papers = []
    url = "https://api.crossref.org/works"
    
    params = {
        'query': query,
        'rows': min(max_papers, 100),
        'mailto': email
    }
    
    try:
        logger.info(f"Поиск в CrossRef по запросу: '{query}'")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        for item in data.get('message', {}).get('items', [])[:max_papers]:
            paper = {
                'title': item.get('title', ['Unknown'])[0],
                'authors': ', '.join([f"{a.get('given', '')} {a.get('family', '')}".strip() 
                                    for a in item.get('author', [])[:3]]) or 'Unknown',
                'year': item.get('published-online', {}).get('date-parts', [[None]])[0][0] or 'N/A',
                'doi': item.get('DOI', 'N/A'),
                'abstract_en': item.get('abstract', ''),
                'source': 'crossref',
                'url': item.get('URL', ''),
                'arxiv_id': 'N/A'
            }
            papers.append(paper)
        
        logger.info(f"✓ Получено {len(papers)} статей из CrossRef")
        
    except Exception as e:
        logger.error(f"✗ Ошибка при получении статей из CrossRef: {e}")
    
    return papers

def fetch_papers_arxiv(query: str, max_papers: int = 20) -> List[Dict]:
    """
    Получает статьи из arXiv API.
    """
    papers = []
    url = "http://export.arxiv.org/api/query"
    
    # arXiv API требует особого форматирования для длинных запросов
    # Заменяем пробелы на +AND+ для строгого поиска
    arxiv_query = query.replace(" ", "+AND+")
    
    # Для arXiv лучше искать в абстрактах (abs) или названиях (ti), а не везде (all)
    # Если запрос длинный, all часто возвращает мусор
    search_query = f"search_query=abs:{arxiv_query}&start=0&max_results={max_papers}&sortBy=submittedDate&sortOrder=descending"
    
    try:
        logger.info(f"Поиск в arXiv по запросу: '{query}'")
        response = requests.get(f"{url}?{search_query}", timeout=10)
        response.raise_for_status()
        
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.content)
        
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
            authors_elems = entry.findall('{http://www.w3.org/2005/Atom}author')
            summary_elem = entry.find('{http://www.w3.org/2005/Atom}summary')
            arxiv_id_elem = entry.find('{http://www.w3.org/2005/Atom}id')
            published_elem = entry.find('{http://www.w3.org/2005/Atom}published')
            
            paper = {
                'title': title_elem.text if title_elem is not None else 'Unknown',
                'authors': ', '.join([author.find('{http://www.w3.org/2005/Atom}name').text 
                                    for author in authors_elems[:3] 
                                    if author.find('{http://www.w3.org/2005/Atom}name') is not None]),
                'year': published_elem.text.split('-')[0] if published_elem is not None else 'N/A',
                'doi': 'N/A',
                'abstract_en': summary_elem.text if summary_elem is not None else '',
                'source': 'arxiv',
                'url': arxiv_id_elem.text if arxiv_id_elem is not None else '',
                'arxiv_id': arxiv_id_elem.text.split('/abs/')[-1] if arxiv_id_elem is not None else 'N/A'
            }
            papers.append(paper)
        
        logger.info(f"✓ Получено {len(papers)} статей из arXiv")
        
    except Exception as e:
        logger.error(f"✗ Ошибка при получении статей из arXiv: {e}")
    
    return papers

def main():
    """
    Главная функция.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Сбор и обработка научных статей')
    parser.add_argument('--query', default='maritime autonomous collision avoidance', help='Поисковый запрос (ключевые слова или DOI)')
    parser.add_argument('--max-papers', type=int, default=20, help='Максимальное количество статей')
    parser.add_argument('--email', required=True, help='Email для CrossRef API')
    parser.add_argument('--output-dir', default='docs/papers', help='Директория для сохранения')
    parser.add_argument('--use-openai', action='store_true', help='Использовать OpenAI для обработки')
    
    args = parser.parse_args()
    
    # Создаем директорию
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Собираем статьи
    all_papers = []
    
    # Очистка запроса от лишних пробелов и переносов строк
    # Заменяем переносы строк на пробелы, удаляем лишние пробелы
    query = " ".join(args.query.replace("\n", " ").replace("\r", " ").split())
    
    # Проверяем, является ли запрос DOI
    if is_doi(query):
        logger.info(f"Обнаружен DOI: {query}")
        all_papers.extend(fetch_paper_by_doi(query, args.email))
    else:
        # Если не DOI, ищем по ключевым словам
        logger.info(f"Поиск по ключевым словам: {query}")
        all_papers.extend(fetch_papers_crossref(query, args.email, args.max_papers // 2))
        all_papers.extend(fetch_papers_arxiv(query, args.max_papers // 2))
    
    if not all_papers:
        logger.warning("Статьи не найдены. Проверьте запрос.")
        return
        
    # Генерируем Markdown файлы
    for idx, paper in enumerate(all_papers, 1):
        paper['sidebar_position'] = idx
        paper['tags'] = ['Research', 'Maritime', 'Autonomous']
        paper['trl_level'] = 3
        paper['trl_description'] = 'Экспериментальное подтверждение концепции'
        
        source_prefix = paper['source'][:3].upper()
        filename = f"paper_{idx:04d}_{source_prefix.lower()}.md"
        output_path = os.path.join(args.output_dir, filename)
        
        generate_markdown_safe(paper, output_path)
    
    logger.info(f"\n✓ Обработано {len(all_papers)} статей")
    logger.info(f"✓ Файлы сохранены в {args.output_dir}")

if __name__ == '__main__':
    main()



