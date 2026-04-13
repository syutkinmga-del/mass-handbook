#!/usr/bin/env python3
"""
Расширенный скрипт для автоматического сбора и обработки научных статей.
Включает интеграцию с OpenAI для перевода, анализа и оценки TRL.

Использование:
    python collect_papers_extended.py --query "maritime autonomous" --use-openai --sources crossref,arxiv
"""

import os
import json
import requests
import xml.etree.ElementTree as ET
import hashlib
import sqlite3
import re
import time
import logging
import argparse
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Импорт модулей обработки
try:
    from openai_processor import OpenAIPaperProcessor, ProcessedPaper
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    ProcessedPaper = None

try:
    from additional_sources import (
        get_fetcher, RECOMMENDED_SOURCES, IEEEXploreFetcher, 
        COREFetcher, Paper
    )
    ADDITIONAL_SOURCES_AVAILABLE = True
except ImportError:
    ADDITIONAL_SOURCES_AVAILABLE = False

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class EnhancedPaper:
    """Расширенная структура для научной статьи с обработанными данными"""
    title: str
    authors: List[str]
    abstract: str
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    publication_date: Optional[str] = None
    source: str = "unknown"
    url: Optional[str] = None
    keywords: List[str] = None
    
    # Поля, добавленные OpenAI
    translated_abstract: Optional[str] = None
    key_findings: Optional[List[str]] = None
    trl_level: Optional[int] = None
    trl_assessment: Optional[str] = None
    tags: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
        if self.tags is None:
            self.tags = []
    
    def get_hash(self) -> str:
        content = self.title.lower() + "_" + ",".join(self.authors).lower()
        return hashlib.md5(content.encode()).hexdigest()


class CrossRefFetcher:
    BASE_URL = "https://api.crossref.org/works"
    
    def __init__(self, email: str):
        if not self._validate_email(email):
            raise ValueError(f"Некорректный email: {email}")
        
        self.email = email
        self.session = self._create_session_with_retries()
        self.session.headers.update({
            'User-Agent': 'MASS-Handbook-Bot (mailto:' + email + ')'
        })
    
    @staticmethod
    def _validate_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def _create_session_with_retries():
        session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
    
    def search(self, query: str, rows: int = 50) -> List[EnhancedPaper]:
        params = {
            'query': query,
            'rows': rows,
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
    
    def _parse_item(self, item: Dict) -> Optional[EnhancedPaper]:
        try:
            title = item.get('title', [''])[0] if item.get('title') else ''
            authors = [a.get('given', '') + ' ' + a.get('family', '') for a in item.get('author', [])]
            
            return EnhancedPaper(
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


class ArxivFetcher:
    BASE_URL = "http://export.arxiv.org/api/query"
    
    def __init__(self):
        self.session = self._create_session_with_retries()
    
    @staticmethod
    def _create_session_with_retries():
        session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
    
    def search(self, query: str, max_results: int = 50) -> List[EnhancedPaper]:
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
            
            logger.info(f"arXiv: найдено {len(papers)} препринтов")
            return papers
        
        except requests.RequestException as e:
            logger.error(f"Ошибка arXiv: {e}")
            return []
    
    def _parse_entry(self, entry) -> Optional[EnhancedPaper]:
        try:
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            title_elem = entry.find('atom:title', ns)
            title = title_elem.text if title_elem is not None else ''
            
            authors = []
            for author in entry.findall('atom:author', ns):
                name_elem = author.find('atom:name', ns)
                if name_elem is not None and name_elem.text:
                    authors.append(name_elem.text)
            
            summary_elem = entry.find('atom:summary', ns)
            summary = summary_elem.text if summary_elem is not None else ''
            
            id_elem = entry.find('atom:id', ns)
            arxiv_id = id_elem.text.split('/abs/')[-1] if id_elem is not None and id_elem.text else ''
            
            published_elem = entry.find('atom:published', ns)
            published = published_elem.text if published_elem is not None else ''
            
            return EnhancedPaper(
                title=title.strip(),
                authors=authors,
                abstract=summary.strip(),
                arxiv_id=arxiv_id,
                publication_date=published,
                source='arxiv',
                url='https://arxiv.org/abs/' + arxiv_id
            )
        except Exception as e:
            logger.warning(f"Ошибка парсинга arXiv: {e}")
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
    
    def deduplicate(self, papers: List[EnhancedPaper]) -> List[EnhancedPaper]:
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

## Аннотация (оригинал)

{abstract}

## Аннотация (русский перевод)

{translated_abstract}

## Ключевые выводы

{key_findings}

## Оценка применимости (TRL)

**TRL {trl_level}** - {trl_assessment}

## Ссылки

{links}
"""
    
    def generate(self, paper: EnhancedPaper, position: int = 1) -> str:
        tags = ", ".join(paper.tags) if paper.tags else "Navigation, Collision Avoidance"
        authors = ", ".join([a.strip() for a in paper.authors[:3] if a.strip()]) if paper.authors else "Unknown"
        year = paper.publication_date[:4] if paper.publication_date else "N/A"
        
        abstract = paper.abstract
        if len(abstract) > 500:
            abstract = abstract[:500] + "..."
        
        translated_abstract = paper.translated_abstract or abstract
        
        key_findings = ""
        if paper.key_findings:
            key_findings = "\n".join([f"- {finding}" for finding in paper.key_findings])
        else:
            key_findings = "- Статья добавлена автоматически"
        
        trl_level = paper.trl_level or 3
        trl_assessment = paper.trl_assessment or "Экспериментальное подтверждение концепции"
        
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
            translated_abstract=translated_abstract,
            key_findings=key_findings,
            trl_level=trl_level,
            trl_assessment=trl_assessment,
            tags=tags,
            links=links
        )
    
    @staticmethod
    def _generate_links(paper: EnhancedPaper) -> str:
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
        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            filepath = Path(output_dir) / (filename + ".md")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown)
            logger.info(f"Файл сохранен: {filepath}")
            return filepath
        except IOError as e:
            logger.error(f"Ошибка при сохранении файла {filename}: {e}")
            return None


def main():
    parser = argparse.ArgumentParser(description='Расширенный сбор научных статей для MASS Handbook')
    parser.add_argument('--query', type=str, default='maritime autonomous collision avoidance',
                       help='Поисковый запрос')
    parser.add_argument('--max-papers', type=int, default=50,
                       help='Максимальное количество статей')
    parser.add_argument('--email', type=str, default='your-email@example.com',
                       help='Email для CrossRef API')
    parser.add_argument('--output-dir', type=str, default='docs/papers',
                       help='Директория для сохранения статей')
    parser.add_argument('--use-openai', action='store_true',
                       help='Использовать OpenAI для обработки статей')
    parser.add_argument('--sources', type=str, default='crossref,arxiv',
                       help='Источники для поиска (crossref,arxiv,ieee,core)')
    
    args = parser.parse_args()
    
    logger.info(f"Начало сбора статей по запросу: {args.query}")
    logger.info(f"Используемые источники: {args.sources}")
    
    # Инициализация компонентов
    crossref = CrossRefFetcher(args.email)
    arxiv = ArxivFetcher()
    deduplicator = Deduplicator()
    generator = MarkdownGenerator()
    
    openai_processor = None
    if args.use_openai:
        if not OPENAI_AVAILABLE:
            logger.warning("OpenAI модуль не доступен. Установите: pip install openai")
        else:
            try:
                openai_processor = OpenAIPaperProcessor()
                logger.info("OpenAI процессор инициализирован")
            except ValueError as e:
                logger.error(f"Ошибка инициализации OpenAI: {e}")
    
    # Сбор данных
    logger.info("Этап 1: Сбор данных...")
    all_papers = []
    
    sources = [s.strip() for s in args.sources.split(',')]
    
    if 'crossref' in sources:
        crossref_papers = crossref.search(args.query, rows=args.max_papers // 2)
        all_papers.extend(crossref_papers)
        time.sleep(1)
    
    if 'arxiv' in sources:
        arxiv_papers = arxiv.search(args.query, max_results=args.max_papers // 2)
        all_papers.extend(arxiv_papers)
    
    # Дедупликация
    logger.info("Этап 2: Дедупликация...")
    unique_papers = deduplicator.deduplicate(all_papers)
    
    if not unique_papers:
        logger.warning("Статьи не найдены!")
        return
    
    # Обработка с OpenAI
    if openai_processor:
        logger.info("Этап 3: Обработка с OpenAI...")
        for paper in unique_papers[:args.max_papers]:
            processed = openai_processor.process_paper(paper.title, paper.abstract)
            if processed:
                paper.translated_abstract = processed.translated_abstract
                paper.key_findings = processed.key_findings
                paper.trl_level = processed.trl_level
                paper.trl_assessment = processed.trl_assessment
                paper.tags = processed.tags
            time.sleep(0.5)  # Задержка между запросами к OpenAI
    
    # Генерация Markdown
    logger.info("Этап 4: Генерация Markdown...")
    saved_count = 0
    for i, paper in enumerate(unique_papers[:args.max_papers], 1):
        markdown = generator.generate(paper, position=i)
        filename = f"paper_{i:04d}_{paper.source}"
        if generator.save_to_file(markdown, filename, args.output_dir):
            saved_count += 1
    
    # Итоговая статистика
    logger.info(f"Завершено! Обработано {len(unique_papers)} статей, сохранено {saved_count}.")
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_papers": len(all_papers),
        "unique_papers": len(unique_papers),
        "saved_papers": saved_count,
        "sources": sources,
        "query": args.query,
        "openai_enabled": openai_processor is not None
    }
    
    try:
        with open("collection_summary.json", "w") as f:
            json.dump(summary, f, indent=2)
        logger.info("Итоги сохранены в collection_summary.json")
    except IOError as e:
        logger.error(f"Ошибка при сохранении итогов: {e}")


if __name__ == "__main__":
    main()
