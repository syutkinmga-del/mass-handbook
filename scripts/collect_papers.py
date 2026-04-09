#!/usr/bin/env python3
"""
Скрипт для автоматического сбора научных статей и их обработки с помощью OpenAI.
Использует CrossRef и arXiv API для поиска релевантных статей.

Использование:
    python scripts/collect_papers.py --query "maritime autonomous collision avoidance" --max-papers 50
"""

import os
import json
import requests
import xml.etree.ElementTree as ET
import hashlib
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import argparse
import time
import logging
from dataclasses import dataclass, asdict

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class Paper:
    """Класс для представления научной статьи"""
    title: str
    authors: List[str]
    abstract: str
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    publication_date: Optional[str] = None
    source: str = "unknown"
    url: Optional[str] = None
    keywords: List[str] = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
    
    def get_hash(self) -> str:
        """Генерирует хеш для дедупликации"""
        content = f"{self.title}_{','.join(self.authors)}".lower()
        return hashlib.md5(content.encode()).hexdigest()


class CrossRefFetcher:
    """Получение данных из CrossRef API"""
    
    BASE_URL = "https://api.crossref.org/works"
    
    def __init__(self, email: str):
        self.email = email
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': f'MASS-Handbook-Bot (mailto:{email})'
        })
    
    def search(self, query: str, rows: int = 50, offset: int = 0) -> List[Paper]:
        """Поиск статей в CrossRef"""
        params = {
            'query': query,
            'rows': rows,
            'offset': offset,
            'mailto': self.email
        }
        
        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            papers = []
            for item in data.get('message', {}).get('items', []):
                paper = self._parse_item(item)
                if paper:
                    papers.append(paper)
            
            logger.info(f"CrossRef: найдено {len(papers)} статей")
            return papers
        
        except requests.RequestException as e:
            logger.error(f"Ошибка CrossRef: {e}")
            return []
    
    def _parse_item(self, item: Dict) -> Optional[Paper]:
        """Парсинг элемента из ответа CrossRef"""
        try:
            title = item.get('title', [''])[0] if item.get('title') else ''
            authors = [f"{a.get('given', '')} {a.get('family', '')}".strip() 
                      for a in item.get('author', [])]
            
            return Paper(
                title=title,
                authors=authors,
                abstract=item.get('abstract', ''),
                doi=item.get('DOI'),
                publication_date=item.get('published-online', {}).get('date-time'),
                source='crossref',
                url=item.get('URL'),
                keywords=item.get('keywords', [])
            )
        except Exception as e:
            logger.warning(f"Ошибка парсинга CrossRef: {e}")
            return None


class ArXivFetcher:
    """Получение данных из arXiv API"""
    
    BASE_URL = "http://export.arxiv.org/api/query"
    
    def search(self, query: str, max_results: int = 50) -> List[Paper]:
        """Поиск препринтов в arXiv"""
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            papers = []
            
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                paper = self._parse_entry(entry)
                if paper:
                    papers.append(paper)
            
            logger.info(f"arXiv: найдено {len(papers)} препринтов")
            return papers
        
        except requests.RequestException as e:
            logger.error(f"Ошибка arXiv: {e}")
            return []
    
    def _parse_entry(self, entry: ET.Element) -> Optional[Paper]:
        """Парсинг элемента из Atom ответа arXiv"""
        try:
            ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
            
            title = entry.find('atom:title', ns).text if entry.find('atom:title', ns) is not None else ''
            authors = [author.find('atom:name', ns).text 
                      for author in entry.findall('atom:author', ns)]
            summary = entry.find('atom:summary', ns).text if entry.find('atom:summary', ns) is not None else ''
            arxiv_id = entry.find('atom:id', ns).text.split('/abs/')[-1] if entry.find('atom:id', ns) is not None else ''
            published = entry.find('atom:published', ns).text if entry.find('atom:published', ns) is not None else ''
            
            return Paper(
                title=title.strip(),
                authors=authors,
                abstract=summary.strip(),
                arxiv_id=arxiv_id,
                publication_date=published,
                source='arxiv',
                url=f'https://arxiv.org/abs/{arxiv_id}'
            )
        except Exception as e:
            logger.warning(f"Ошибка парсинга arXiv: {e}")
            return None


class Deduplicator:
    """Удаление дубликатов и фильтрация статей"""
    
    def __init__(self, db_path: str = "papers.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS papers (
                id INTEGER PRIMARY KEY,
                hash TEXT UNIQUE,
                title TEXT,
                doi TEXT,
                arxiv_id TEXT,
                source TEXT,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def deduplicate(self, papers: List[Paper]) -> List[Paper]:
        """Удаление дубликатов из списка статей"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        unique_papers = []
        
        for paper in papers:
            paper_hash = paper.get_hash()
            
            cursor.execute('SELECT id FROM papers WHERE hash = ?', (paper_hash,))
            if cursor.fetchone() is None:
                unique_papers.append(paper)
                
                cursor.execute('''
                    INSERT INTO papers (hash, title, doi, arxiv_id, source)
                    VALUES (?, ?, ?, ?, ?)
                ''', (paper_hash, paper.title, paper.doi, paper.arxiv_id, paper.source))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Дедупликация: {len(papers)} -> {len(unique_papers)} уникальных")
        return unique_papers


class MarkdownGenerator:
    """Генерация Markdown файлов для Docusaurus"""
    
    TEMPLATE = """---
sidebar_position: {position}
tags: [{tags}]
---

# {title}

**Авторы:** {authors}
**Год:** {year}
**Источник:** {source}
**DOI:** {doi}
**arXiv ID:** {arxiv_id}

## Аннотация

{abstract}

## Ключевые выводы

- Статья добавлена автоматически
- Требуется ручная обработка для полного описания

## Оценка применимости (TRL)

**TRL 3** - Экспериментальное подтверждение концепции

## Ссылки

- [Полный текст](https://doi.org/{doi})
"""
    
    def generate(self, paper: Paper, position: int = 1) -> str:
        """Генерация Markdown для одной статьи"""
        tags = "Navigation, Collision Avoidance"
        authors = ", ".join(paper.authors[:3]) if paper.authors else "Unknown"
        year = paper.publication_date[:4] if paper.publication_date else "N/A"
        
        markdown = self.TEMPLATE.format(
            position=position,
            title=paper.title,
            authors=authors,
            year=year,
            source=paper.source,
            doi=paper.doi or "N/A",
            arxiv_id=paper.arxiv_id or "N/A",
            abstract=paper.abstract[:500] + "..." if len(paper.abstract) > 500 else paper.abstract,
            tags=tags
        )
        
        return markdown
    
    def save_to_file(self, markdown: str, filename: str, output_dir: str = "docs/papers"):
        """Сохранение Markdown в файл"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        filepath = Path(output_dir) / f"{filename}.md"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown)
        
        logger.info(f"Файл сохранен: {filepath}")
        return filepath


def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(description='Сбор научных статей для MASS Handbook')
    parser.add_argument('--query', type=str, default='maritime autonomous collision avoidance',
                       help='Поисковый запрос')
    parser.add_argument('--max-papers', type=int, default=50,
                       help='Максимальное количество статей')
    parser.add_argument('--email', type=str, default='your-email@example.com',
                       help='Email для CrossRef API')
    parser.add_argument('--output-dir', type=str, default='docs/papers',
                       help='Директория для сохранения статей')
    
    args = parser.parse_args()
    
    logger.info(f"Начало сбора статей по запросу: '{args.query}'")
    
    # Инициализация компонентов
    crossref = CrossRefFetcher(args.email)
    arxiv = ArXivFetcher()
    deduplicator = Deduplicator()
    generator = MarkdownGenerator()
    
    # Сбор данных
    logger.info("Этап 1: Сбор данных...")
    crossref_papers = crossref.search(args.query, rows=args.max_papers // 2)
    time.sleep(1)  # Задержка между запросами
    arxiv_papers = arxiv.search(args.query, max_results=args.max_papers // 2)
    all_papers = crossref_papers + arxiv_papers
    
    # Дедупликация
    logger.info("Этап 2: Дедупликация...")
    unique_papers = deduplicator.deduplicate(all_papers)
    
    # Генерация Markdown
    logger.info("Этап 3: Генерация Markdown...")
    for i, paper in enumerate(unique_papers[:args.max_papers], 1):
        markdown = generator.generate(paper, position=i)
        filename = f"paper_{i:04d}_{paper.source}"
        generator.save_to_file(markdown, filename, args.output_dir)
    
    logger.info(f"Завершено! Обработано {len(unique_papers)} статей.")


if __name__ == "__main__":
    main()
