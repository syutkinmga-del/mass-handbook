#!/usr/bin/env python3
"""
Скрипт для автоматического сбора научных статей.
Исправленная версия с устранением критических ошибок.
"""

import os
import json
import requests
import xml.etree.ElementTree as ET
import hashlib
import sqlite3
import re
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import argparse
import time
import logging
from dataclasses import dataclass
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class Paper:
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
        content = self.title.lower() + "_" + ",".join(self.authors).lower()
        return hashlib.md5(content.encode()).hexdigest()


class CrossRefFetcher:
    BASE_URL = "https://api.crossref.org/works"
    
    def __init__(self, email: str):
        # ИСПРАВЛЕНИЕ #4: Валидация email
        if not self._validate_email(email):
            raise ValueError(f"Некорректный email: {email}")
        
        self.email = email
        self.session = self._create_session_with_retries()
        self.session.headers.update({
            'User-Agent': 'MASS-Handbook-Bot (mailto:' + email + ')'
        })
    
    @staticmethod
    def _validate_email(email: str) -> bool:
        """Валидация email адреса"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def _create_session_with_retries():
        """Создание сессии с повторными попытками"""
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
    
    def search(self, query: str, rows: int = 50, offset: int = 0) -> List[Paper]:
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
            
            logger.info("CrossRef: найдено " + str(len(papers)) + " статей")
            return papers
        
        except requests.RequestException as e:
            logger.error("Ошибка CrossRef: " + str(e))
            return []
    
    def fetch_by_doi(self, doi: str) -> Optional[Paper]:
        try:
            url = self.BASE_URL + "/" + doi
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()['message']
                title = data.get('title', [''])[0] if data.get('title') else ''
                authors = [a.get('given', '') + ' ' + a.get('family', '') 
                          for a in data.get('author', [])]
                
                return Paper(
                    title=title,
                    authors=authors,
                    abstract=data.get('abstract', ''),
                    doi=data.get('DOI'),
                    publication_date=data.get('published-online', {}).get('date-time'),
                    source='crossref',
                    url=data.get('URL'),
                    keywords=data.get('subject', [])
                )
            else:
                logger.warning("DOI не найден: " + doi + " (статус " + str(response.status_code) + ")")
        except Exception as e:
            logger.error("Ошибка при запросе DOI " + doi + ": " + str(e))
        return None
    
    def _parse_item(self, item: Dict) -> Optional[Paper]:
        try:
            title = item.get('title', [''])[0] if item.get('title') else ''
            authors = [a.get('given', '') + ' ' + a.get('family', '') 
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
            logger.warning("Ошибка парсинга CrossRef: " + str(e))
            return None


class ArxivFetcher:
    BASE_URL = "http://export.arxiv.org/api/query"
    
    def __init__(self):
        self.session = self._create_session_with_retries()
    
    @staticmethod
    def _create_session_with_retries():
        """Создание сессии с повторными попытками"""
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
    
    def search(self, query: str, max_results: int = 50) -> List[Paper]:
        params = {
            'search_query': 'all:' + query,
            'start': 0,
            'max_results': max_results,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        
        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            papers = []
            
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                paper = self._parse_entry(entry)
                if paper:
                    papers.append(paper)
            
            logger.info("arXiv: найдено " + str(len(papers)) + " препринтов")
            return papers
        
        except requests.RequestException as e:
            logger.error("Ошибка arXiv: " + str(e))
            return []
    
    def _parse_entry(self, entry):
        try:
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            title_elem = entry.find('atom:title', ns)
            title = title_elem.text if title_elem is not None else ''
            
            # ИСПРАВЛЕНИЕ #1: Безопасный парсинг авторов
            authors = []
            for author in entry.findall('atom:author', ns):
                name_elem = author.find('atom:name', ns)
                if name_elem is not None and name_elem.text:
                    authors.append(name_elem.text)
            
            summary_elem = entry.find('atom:summary', ns)
            summary = summary_elem.text if summary_elem is not None else ''
            
            id_elem = entry.find('atom:id', ns)
            if id_elem is not None and id_elem.text:
                arxiv_id = id_elem.text.split('/abs/')[-1]
            else:
                arxiv_id = ''
            
            published_elem = entry.find('atom:published', ns)
            published = published_elem.text if published_elem is not None else ''
            
            return Paper(
                title=title.strip(),
                authors=authors,
                abstract=summary.strip(),
                arxiv_id=arxiv_id,
                publication_date=published,
                source='arxiv',
                url='https://arxiv.org/abs/' + arxiv_id
            )
        except Exception as e:
            logger.warning("Ошибка парсинга arXiv: " + str(e))
            return None


class Deduplicator:
    def __init__(self, db_path: str = "papers.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
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
        
        logger.info("Дедупликация: " + str(len(papers)) + " -> " + str(len(unique_papers)) + " уникальных")
        return unique_papers


class MarkdownGenerator:
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

## Оценка применимости (TRL)

**TRL 3** - Экспериментальное подтверждение концепции

## Ссылки

{links}
"""
    
    def generate(self, paper: Paper, position: int = 1) -> str:
        tags = "Navigation, Collision Avoidance"
        # ИСПРАВЛЕНИЕ #5: Фильтрация пустых авторов
        authors = ", ".join([a.strip() for a in paper.authors[:3] if a.strip()]) if paper.authors else "Unknown"
        year = paper.publication_date[:4] if paper.publication_date else "N/A"
        
        abstract = paper.abstract
        if len(abstract) > 500:
            abstract = abstract[:500] + "..."
        
        # ИСПРАВЛЕНИЕ #2: Улучшенная обработка ссылок
        links = self._generate_links(paper)
        
        return self.TEMPLATE.format(
            position=position,
            title=paper.title,
            authors=authors,
            year=year,
            source=paper.source,
            doi=paper.doi or "N/A",
            arxiv_id=paper.arxiv_id or "N/A",
            abstract=abstract,
            tags=tags,
            links=links
        )
    
    @staticmethod
    def _generate_links(paper: Paper) -> str:
        """Генерация ссылок на полный текст"""
        links = []
        
        if paper.doi and paper.doi != "N/A":
            links.append(f"- [Полный текст на CrossRef](https://doi.org/{paper.doi})")
        
        if paper.arxiv_id and paper.arxiv_id != "N/A":
            links.append(f"- [Препринт на arXiv](https://arxiv.org/abs/{paper.arxiv_id})")
        
        if paper.url and paper.url not in [paper.doi, paper.arxiv_id]:
            links.append(f"- [Источник]({paper.url})")
        
        if not links:
            links.append("- Полный текст недоступен")
        
        return "\n".join(links)
    
    def save_to_file(self, markdown: str, filename: str, output_dir: str = "docs/papers") -> Optional[Path]:
        # ИСПРАВЛЕНИЕ #3: Обработка исключений при сохранении
        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            filepath = Path(output_dir) / (filename + ".md")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown)
            logger.info("Файл сохранен: " + str(filepath))
            return filepath
        except IOError as e:
            logger.error(f"Ошибка при сохранении файла {filename}: {e}")
            return None


def main():
    parser = argparse.ArgumentParser(description='Сбор научных статей для MASS Handbook')
    parser.add_argument('--query', type=str, default='maritime autonomous collision avoidance',
                       help='Поисковый запрос')
    parser.add_argument('--max-papers', type=int, default=50,
                       help='Максимальное количество статей')
    parser.add_argument('--email', type=str, default='your-email@example.com',
                       help='Email для CrossRef API')
    parser.add_argument('--output-dir', type=str, default='docs/papers',
                       help='Директория для сохранения статей')
    parser.add_argument('--doi', type=str,
                        help='Search for a specific paper by DOI')
    
    args = parser.parse_args()

    if args.doi:
        logger.info("Поиск статьи по DOI: " + args.doi)
        search_mode = "doi"
    else:
        logger.info("Начало сбора статей по запросу: " + args.query)
        search_mode = "query"

    try:
        crossref = CrossRefFetcher(args.email)
    except ValueError as e:
        logger.error(str(e))
        return
    
    arxiv = ArxivFetcher()
    deduplicator = Deduplicator()
    generator = MarkdownGenerator()

    logger.info("Этап 1: Сбор данных...")
    
    if search_mode == "doi":
        paper = crossref.fetch_by_doi(args.doi)
        if paper:
            all_papers = [paper]
            logger.info("Найдена статья: " + paper.title)
        else:
            logger.error("Статья с DOI " + args.doi + " не найдена")
            return
    else:
        crossref_papers = crossref.search(args.query, rows=args.max_papers // 2)
        time.sleep(1)
        arxiv_papers = arxiv.search(args.query, max_results=args.max_papers // 2)
        all_papers = crossref_papers + arxiv_papers

    logger.info("Этап 2: Дедупликация...")
    unique_papers = deduplicator.deduplicate(all_papers)

    # ИСПРАВЛЕНИЕ #6: Проверка на пустой результат
    if not unique_papers:
        logger.warning("Статьи не найдены!")
        return

    logger.info("Этап 3: Генерация Markdown...")
    saved_count = 0
    for i, paper in enumerate(unique_papers[:args.max_papers], 1):
        markdown = generator.generate(paper, position=i)
        filename = "paper_" + str(i).zfill(4) + "_" + paper.source
        if generator.save_to_file(markdown, filename, args.output_dir):
            saved_count += 1

    logger.info("Завершено! Обработано " + str(len(unique_papers)) + " статей, сохранено " + str(saved_count) + ".")
    
    # Логирование итогов в JSON
    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_papers": len(all_papers),
        "unique_papers": len(unique_papers),
        "saved_papers": saved_count,
        "search_mode": search_mode,
        "query": args.query if search_mode == "query" else args.doi
    }
    
    try:
        with open("collection_summary.json", "w") as f:
            json.dump(summary, f, indent=2)
        logger.info("Итоги сохранены в collection_summary.json")
    except IOError as e:
        logger.error(f"Ошибка при сохранении итогов: {e}")


if __name__ == "__main__":
    main()
