#!/usr/bin/env python3
"""
Скрипт сбора и обработки научных статей.
Поддерживает поиск по ключевым словам и прямую загрузку по DOI.
Накапливает статьи, не перезаписывая существующие.
Автоматически генерирует специфичные теги на основе содержимого.
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
import glob
from openai import OpenAI

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Словарь ключевых слов для автоматического тегирования
TAG_KEYWORDS = {
    # ===== АЛГОРИТМЫ И МОДЕЛИ =====
    'Dynamic Window Approach': ['dynamic window', 'dwa', 'velocity obstacle'],
    'Deep Reinforcement Learning': ['deep reinforcement learning', 'drl', 'q-learning', 'policy gradient'],
    'Model Predictive Control': ['model predictive control', 'mpc', 'predictive'],
    'Path Planning': ['path planning', 'route planning', 'trajectory planning', 'motion planning'],
    'Machine Learning': ['machine learning', 'neural network', 'classification', 'regression'],
    'Fuzzy Logic': ['fuzzy', 'fuzzy inference', 'fuzzy logic'],
    'Genetic Algorithm': ['genetic algorithm', 'evolutionary', 'ga'],
    'Particle Swarm': ['particle swarm', 'pso'],
    'Reinforcement Learning': ['reinforcement learning', 'reward', 'markov'],
    'Neural Networks': ['neural network', 'cnn', 'lstm', 'rnn', 'deep learning'],
    'Optimization Algorithm': ['optimization', 'optimal control', 'convex optimization'],
    
    # ===== АРХИТЕКТУРА MASS - PERCEPTION (ВОСПРИЯТИЕ) =====
    'Perception': ['perception', 'sensor', 'lidar', 'radar', 'camera', 'sonar', 'detection', 'object detection'],
    'Sensor Fusion': ['sensor fusion', 'data fusion', 'multi-sensor'],
    'Image Processing': ['image processing', 'computer vision', 'visual', 'video processing'],
    
    # ===== АРХИТЕКТУРА MASS - DECISION MAKING (ПРИНЯТИЕ РЕШЕНИЙ) =====
    'Decision Making': ['decision making', 'decision support', 'decision system', 'planning'],
    'Behavior Planning': ['behavior planning', 'behavior tree', 'state machine'],
    'Trajectory Planning': ['trajectory planning', 'motion planning', 'path planning'],
    
    # ===== АРХИТЕКТУРА MASS - CONTROL (УПРАВЛЕНИЕ) =====
    'Control System': ['control system', 'controller', 'autopilot', 'steering', 'propulsion'],
    'Adaptive Control': ['adaptive control', 'pid controller', 'feedback control'],
    'Nonlinear Control': ['nonlinear control', 'robust control', 'sliding mode'],
    
    # ===== АРХИТЕКТУРА MASS - COLLISION AVOIDANCE (ИЗБЕЖАНИЕ СТОЛКНОВЕНИЙ) =====
    'Collision Avoidance': ['collision avoidance', 'collision detection', 'avoid collision', 'anti-collision', 'cpa', 'tcpa'],
    'Obstacle Avoidance': ['obstacle avoidance', 'obstacle detection', 'avoidance maneuver'],
    'COLREGs': ['colregs', 'international regulations', 'collision prevention', 'rules of the road', 'imca'],
    
    # ===== АРХИТЕКТУРА MASS - SITUATIONAL AWARENESS (СИТУАЦИОННАЯ ОСВЕДОМЛЕННОСТЬ) =====
    'Situational Awareness': ['situational awareness', 'situation awareness', 'awareness', 'maritime awareness'],
    'Knowledge Representation': ['knowledge map', 'knowledge graph', 'ontology', 'semantic', 'knowledge base'],
    'Environment Modeling': ['environment model', 'world model', 'scene understanding'],
    
    # ===== АРХИТЕКТУРА MASS - COMMUNICATION & DATA MANAGEMENT (КОММУНИКАЦИЯ И УПРАВЛЕНИЕ ДАННЫМИ) =====
    'Communication': ['communication', 'network', 'wireless', 'connectivity', 'v2x', 'maritime communication'],
    'Data Management': ['data management', 'database', 'data storage', 'data processing'],
    'Cloud Computing': ['cloud', 'edge computing', 'fog computing', 'distributed'],
    
    # ===== АРХИТЕКТУРА MASS - HUMAN MACHINE INTERACTION (ВЗАИМОДЕЙСТВИЕ ЧЕЛОВЕКА И МАШИНЫ) =====
    'Human Machine Interaction': ['human machine interaction', 'hmi', 'human interaction', 'user interface', 'teleoperation'],
    'User Interface': ['user interface', 'ui', 'dashboard', 'visualization'],
    'Remote Control': ['remote control', 'teleoperation', 'remote operation'],
    
    # ===== АРХИТЕКТУРА MASS - CYBERSECURITY (КИБЕРБЕЗОПАСНОСТЬ) =====
    'Cybersecurity': ['cybersecurity', 'cyber security', 'security', 'encryption', 'authentication', 'intrusion detection'],
    'Network Security': ['network security', 'firewall', 'ddos', 'attack'],
    'Data Protection': ['data protection', 'privacy', 'confidentiality'],
    
    # ===== АРХИТЕКТУРА MASS - SYSTEM HEALTH MANAGEMENT (УПРАВЛЕНИЕ ЗДОРОВЬЕМ СИСТЕМЫ) =====
    'System Health Management': ['system health', 'health management', 'diagnostics', 'fault detection', 'prognostics'],
    'Fault Tolerance': ['fault tolerance', 'redundancy', 'reliability', 'availability'],
    'Maintenance': ['maintenance', 'predictive maintenance', 'condition monitoring'],
    
    # ===== АРХИТЕКТУРА MASS - DIGITAL TWIN SUPPORT (ПОДДЕРЖКА ЦИФРОВЫХ ДВОЙНИКОВ) =====
    'Digital Twin': ['digital twin', 'virtual ship', 'simulation', 'virtual environment', 'digital model'],
    'Simulation': ['simulation', 'simulator', 'virtual environment', 'digital twin'],
    'Testing': ['testing', 'validation', 'verification', 'experiment', 'benchmark'],
    
    # ===== COMPLIANCE & REGULATORY LAYER (СООТВЕТСТВИЕ И НОРМАТИВНЫЙ СЛОЙ) =====
    'Safety': ['safety', 'risk assessment', 'hazard', 'safety analysis', 'fail-safe'],
    'Compliance': ['compliance', 'regulatory', 'regulation', 'standard'],
    'IMO': ['imo', 'international maritime', 'maritime regulations', 'maritime law'],
    'MASS': ['mass', 'maritime autonomous', 'autonomous surface ship'],
}

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

def generate_tags_from_content(paper_data: Dict) -> List[str]:
    """
    Автоматически генерирует теги на основе содержимого статьи.
    Анализирует заголовок и аннотацию.
    """
    tags = set()
    
    # Объединяем текст для анализа
    text_to_analyze = f"{paper_data.get('title', '')} {paper_data.get('abstract_en', '')}".lower()
    
    # Проходим по словарю ключевых слов
    for tag, keywords in TAG_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text_to_analyze:
                tags.add(tag)
                break  # Нашли совпадение для этого тега, переходим к следующему
    
    # Если теги не найдены, добавляем базовый тег
    if len(tags) == 0:
        tags.add('MASS')
    
    return sorted(list(tags))

def get_existing_dois_and_arxiv_ids(output_dir: str) -> tuple[set, set]:
    """
    Читает все существующие markdown файлы и извлекает из них DOI и arXiv ID,
    чтобы избежать дублирования статей.
    """
    existing_dois = set()
    existing_arxiv_ids = set()
    
    if not os.path.exists(output_dir):
        return existing_dois, existing_arxiv_ids
        
    for filepath in glob.glob(os.path.join(output_dir, "paper_*.md")):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Ищем DOI
                doi_match = re.search(r'^doi:\s*"?([^"\n]+)"?', content, re.MULTILINE)
                if doi_match and doi_match.group(1) != 'N/A':
                    existing_dois.add(doi_match.group(1).strip())
                    
                # Ищем arXiv ID
                arxiv_match = re.search(r'^arxiv_id:\s*"?([^"\n]+)"?', content, re.MULTILINE)
                if arxiv_match and arxiv_match.group(1) != 'N/A':
                    existing_arxiv_ids.add(arxiv_match.group(1).strip())
        except Exception as e:
            logger.warning(f"Не удалось прочитать файл {filepath} для проверки дубликатов: {e}")
            
    return existing_dois, existing_arxiv_ids

def get_next_paper_id(output_dir: str) -> int:
    """
    Находит следующий доступный номер для файла статьи.
    """
    max_id = 0
    
    if not os.path.exists(output_dir):
        return 1
        
    for filepath in glob.glob(os.path.join(output_dir, "paper_*.md")):
        filename = os.path.basename(filepath)
        # Извлекаем число из имени файла paper_XXXX_source.md
        match = re.search(r'paper_(\d+)_', filename)
        if match:
            current_id = int(match.group(1))
            if current_id > max_id:
                max_id = current_id
                
    return max_id + 1

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
            links.append(f"- [Полный текст на CrossRef](https://doi.org/{paper_data['doi']} )")
        if paper_data.get('url') and paper_data.get('url') != 'N/A':
            links.append(f"- [Источник]({paper_data['url']})")
        if paper_data.get('arxiv_id') and paper_data.get('arxiv_id') != 'N/A':
            links.append(f"- [arXiv](https://arxiv.org/abs/{paper_data['arxiv_id']} )")
        
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
        logger.info(f"Запрос статьи по DOI: {doi}" )
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        item = data.get('message', {})
        
        if not item:
            logger.warning(f"Статья с DOI {doi} не найдена")
            return []
            
        abstract_en = item.get('abstract', '')
        abstract_ru = translate_to_russian(abstract_en) if abstract_en else ''
        key_findings = generate_key_findings(abstract_en) if abstract_en else ''
        
        paper = {
            'title': item.get('title', ['Unknown'])[0],
            'authors': ', '.join([f"{a.get('given', '')} {a.get('family', '')}" .strip() 
                                for a in item.get('author', [])[:3]]) or 'Unknown',
            'year': item.get('published-online', {}).get('date-parts', [[None]])[0][0] or 'N/A',
            'doi': item.get('DOI', 'N/A'),
            'abstract_en': abstract_en,
            'abstract_ru': abstract_ru,
            'key_findings': key_findings,
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
        'rows': min(max_papers, 100 ),
        'mailto': email
    }
    
    try:
        logger.info(f"Поиск в CrossRef по запросу: '{query}'")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        for item in data.get('message', {}).get('items', [])[:max_papers]:
            abstract_en = item.get('abstract', '')
            abstract_ru = translate_to_russian(abstract_en) if abstract_en else ''
            key_findings = generate_key_findings(abstract_en) if abstract_en else ''
            
            paper = {
                'title': item.get('title', ['Unknown'])[0],
                'authors': ', '.join([f"{a.get('given', '')} {a.get('family', '')}" .strip() 
                                    for a in item.get('author', [])[:3]]) or 'Unknown',
                'year': item.get('published-online', {}).get('date-parts', [[None]])[0][0] or 'N/A',
                'doi': item.get('DOI', 'N/A'),
                'abstract_en': abstract_en,
                'abstract_ru': abstract_ru,
                'key_findings': key_findings,
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
    
    arxiv_query = query.replace(" ", "+AND+" )
    search_query = f"search_query=abs:{arxiv_query}&start=0&max_results={max_papers}&sortBy=submittedDate&sortOrder=descending"
    
    try:
        logger.info(f"Поиск в arXiv по запросу: '{query}'")
        response = requests.get(f"{url}?{search_query}", timeout=10)
        response.raise_for_status()
        
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.content)
        
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry' ):
            title_elem = entry.find('{http://www.w3.org/2005/Atom}title' )
            authors_elems = entry.findall('{http://www.w3.org/2005/Atom}author' )
            summary_elem = entry.find('{http://www.w3.org/2005/Atom}summary' )
            arxiv_id_elem = entry.find('{http://www.w3.org/2005/Atom}id' )
            published_elem = entry.find('{http://www.w3.org/2005/Atom}published' )
            
            paper = {
                'title': title_elem.text if title_elem is not None else 'Unknown',
                'authors': ', '.join([author.find('{http://www.w3.org/2005/Atom}name' ).text 
                                    for author in authors_elems[:3] 
                                    if author.find('{http://www.w3.org/2005/Atom}name' ) is not None]),
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
    
    query = " ".join(args.query.replace("\n", " ").replace("\r", " ").split())
    
    if is_doi(query):
        logger.info(f"Обнаружен DOI: {query}")
        all_papers.extend(fetch_paper_by_doi(query, args.email))
    else:
        logger.info(f"Поиск по ключевым словам: {query}")
        all_papers.extend(fetch_papers_crossref(query, args.email, args.max_papers // 2))
        all_papers.extend(fetch_papers_arxiv(query, args.max_papers // 2))
    
    if not all_papers:
        logger.warning("Статьи не найдены. Проверьте запрос.")
        return
        
    # Получаем уже существующие DOI и arXiv ID, чтобы не добавлять дубликаты
    existing_dois, existing_arxiv_ids = get_existing_dois_and_arxiv_ids(args.output_dir)
    logger.info(f"Найдено {len(existing_dois)} существующих DOI и {len(existing_arxiv_ids)} arXiv ID в базе")
    
    # Получаем следующий свободный номер для файла
    next_id = get_next_paper_id(args.output_dir)
    logger.info(f"Новые статьи будут нумероваться начиная с {next_id}")
    
    # Фильтруем дубликаты и генерируем Markdown файлы
    added_count = 0
    skipped_count = 0
    
    for paper in all_papers:
        # Проверка на дубликаты
        doi = paper.get('doi', 'N/A')
        arxiv_id = paper.get('arxiv_id', 'N/A')
        
        if doi != 'N/A' and doi in existing_dois:
            logger.info(f"Пропуск дубликата (DOI уже существует): {doi}")
            skipped_count += 1
            continue
            
        if arxiv_id != 'N/A' and arxiv_id in existing_arxiv_ids:
            logger.info(f"Пропуск дубликата (arXiv ID уже существует): {arxiv_id}")
            skipped_count += 1
            continue
            
        # Добавляем в базу существующих (на случай дубликатов в самом поисковом запросе)
        if doi != 'N/A':
            existing_dois.add(doi)
        if arxiv_id != 'N/A':
            existing_arxiv_ids.add(arxiv_id)
            
        # Настройка метаданных
        paper['sidebar_position'] = next_id
        # Генерируем теги автоматически на основе содержимого
        paper['tags'] = generate_tags_from_content(paper)
        paper['trl_level'] = 3
        paper['trl_description'] = 'Экспериментальное подтверждение концепции'
        
        source_prefix = paper['source'][:3].upper()
        filename = f"paper_{next_id:04d}_{source_prefix.lower()}.md"
        output_path = os.path.join(args.output_dir, filename)
        
        if generate_markdown_safe(paper, output_path):
            logger.info(f"✓ Добавлена статья: {paper['title'][:60]}...")
            logger.info(f"  Теги: {', '.join(paper['tags'])}")
            next_id += 1
            added_count += 1
    
    logger.info(f"\n✓ Найдено всего: {len(all_papers)} статей")
    logger.info(f"✓ Пропущено дубликатов: {skipped_count}")
    logger.info(f"✓ Успешно добавлено новых: {added_count}")
    logger.info(f"✓ Файлы сохранены в {args.output_dir}")

if __name__ == '__main__':
    main()
