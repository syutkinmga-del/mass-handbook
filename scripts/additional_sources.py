"""
Модули для работы с дополнительными источниками научных статей.
Поддерживаемые источники: IEEE Xplore, CORE, ResearchGate
"""

import requests
import logging
from typing import List, Optional, Dict
from dataclasses import dataclass
from datetime import datetime

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


class IEEEXploreFetcher:
    """Получение данных из IEEE Xplore API (требует API ключ)"""
    
    BASE_URL = "https://ieeexploreapi.ieee.org/api/v1/search/articles"
    
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("IEEE Xplore API key is required")
        self.api_key = api_key
        self.session = requests.Session()
    
    def search(self, query: str, max_results: int = 50) -> List[Paper]:
        """Поиск статей в IEEE Xplore"""
        params = {
            'apikey': self.api_key,
            'querytext': query,
            'max_records': min(max_results, 200),  # IEEE ограничивает до 200
            'sort_field': 'publication_year',
            'sort_order': 'desc'
        }
        
        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            papers = []
            for article in data.get('articles', []):
                paper = self._parse_article(article)
                if paper:
                    papers.append(paper)
            
            logger.info(f"IEEE Xplore: найдено {len(papers)} статей")
            return papers
        
        except requests.RequestException as e:
            logger.error(f"Ошибка IEEE Xplore: {e}")
            return []
    
    def _parse_article(self, article: Dict) -> Optional[Paper]:
        """Парсинг статьи из IEEE Xplore"""
        try:
            authors = [author.get('full_name', '') for author in article.get('authors', {}).get('authors', [])]
            
            return Paper(
                title=article.get('title', ''),
                authors=authors,
                abstract=article.get('abstract', ''),
                doi=article.get('doi'),
                publication_date=article.get('publication_date'),
                source='ieee',
                url=article.get('html_url'),
                keywords=article.get('keywords', [])
            )
        except Exception as e:
            logger.warning(f"Ошибка парсинга IEEE Xplore: {e}")
            return None


class COREFetcher:
    """Получение данных из CORE API (требует API ключ)"""
    
    BASE_URL = "https://api.core.ac.uk/v3/search/works"
    
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("CORE API key is required")
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}'
        })
    
    def search(self, query: str, max_results: int = 50) -> List[Paper]:
        """Поиск статей в CORE"""
        params = {
            'q': query,
            'limit': min(max_results, 100),  # CORE ограничивает до 100 за запрос
            'offset': 0
        }
        
        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            papers = []
            for work in data.get('results', []):
                paper = self._parse_work(work)
                if paper:
                    papers.append(paper)
            
            logger.info(f"CORE: найдено {len(papers)} статей")
            return papers
        
        except requests.RequestException as e:
            logger.error(f"Ошибка CORE: {e}")
            return []
    
    def _parse_work(self, work: Dict) -> Optional[Paper]:
        """Парсинг работы из CORE"""
        try:
            # Извлечение авторов
            authors = []
            if 'authors' in work and work['authors']:
                authors = [author.get('name', '') for author in work['authors']]
            
            # Извлечение даты публикации
            pub_date = None
            if 'publishedDate' in work:
                pub_date = work['publishedDate']
            elif 'yearPublished' in work:
                pub_date = str(work['yearPublished'])
            
            return Paper(
                title=work.get('title', ''),
                authors=authors,
                abstract=work.get('abstract', ''),
                doi=work.get('doi'),
                publication_date=pub_date,
                source='core',
                url=work.get('sourceUrl'),
                keywords=work.get('keywords', [])
            )
        except Exception as e:
            logger.warning(f"Ошибка парсинга CORE: {e}")
            return None


class ResearchGateFetcher:
    """Получение данных из ResearchGate (через неофициальный API)
    
    Примечание: ResearchGate не имеет официального публичного API.
    Этот класс предоставляет базовую реализацию для демонстрации.
    Для продакшена рекомендуется использовать официальные источники.
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search(self, query: str, max_results: int = 50) -> List[Paper]:
        """
        Поиск статей в ResearchGate.
        
        Важно: ResearchGate активно блокирует автоматизированные запросы.
        Используйте этот метод осторожно и соблюдайте их Terms of Service.
        """
        logger.warning("ResearchGate API не является официальным и может быть заблокирован. "
                      "Рекомендуется использовать официальные источники (CrossRef, arXiv).")
        return []


class PubMedFetcher:
    """Получение данных из PubMed Central (для биомедицинских статей)"""
    
    BASE_URL = "https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi"
    
    def search(self, query: str, max_results: int = 50) -> List[Paper]:
        """Поиск статей в PubMed Central"""
        # Примечание: PubMed Central больше ориентирован на биомедицину,
        # но может содержать статьи о морских технологиях
        logger.info("PubMed Central поиск может быть неэффективен для MASS тематики")
        return []


class GoogleScholarFetcher:
    """Получение данных из Google Scholar (через неофициальный API)
    
    Примечание: Google Scholar также не имеет официального API.
    Для продакшена рекомендуется использовать официальные источники.
    """
    
    def search(self, query: str, max_results: int = 50) -> List[Paper]:
        """
        Поиск статей в Google Scholar.
        
        Важно: Google Scholar активно блокирует автоматизированные запросы.
        Используйте этот метод осторожно и соблюдайте их Terms of Service.
        """
        logger.warning("Google Scholar не имеет официального API и блокирует автоматизированные запросы. "
                      "Рекомендуется использовать CrossRef или arXiv.")
        return []


# Рекомендуемые источники для MASS
RECOMMENDED_SOURCES = {
    'crossref': {
        'name': 'CrossRef',
        'description': 'Официальный API, лучший для опубликованных статей',
        'recommended': True,
        'requires_api_key': False
    },
    'arxiv': {
        'name': 'arXiv',
        'description': 'Препринты, быстрый доступ к новым работам',
        'recommended': True,
        'requires_api_key': False
    },
    'ieee': {
        'name': 'IEEE Xplore',
        'description': 'Статьи IEEE, требует API ключ',
        'recommended': True,
        'requires_api_key': True
    },
    'core': {
        'name': 'CORE',
        'description': 'Агрегатор открытых исследований, требует API ключ',
        'recommended': True,
        'requires_api_key': True
    },
    'pubmed': {
        'name': 'PubMed Central',
        'description': 'Биомедицинские статьи, может содержать морские технологии',
        'recommended': False,
        'requires_api_key': False
    }
}


def get_fetcher(source: str, api_key: Optional[str] = None):
    """Фабрика для создания объектов fetcher'ов"""
    if source == 'ieee':
        if not api_key:
            raise ValueError("IEEE Xplore requires an API key")
        return IEEEXploreFetcher(api_key)
    elif source == 'core':
        if not api_key:
            raise ValueError("CORE requires an API key")
        return COREFetcher(api_key)
    elif source == 'researchgate':
        logger.warning("ResearchGate is not recommended due to blocking of automated requests")
        return ResearchGateFetcher()
    elif source == 'pubmed':
        return PubMedFetcher()
    elif source == 'scholar':
        logger.warning("Google Scholar is not recommended due to blocking of automated requests")
        return GoogleScholarFetcher()
    else:
        raise ValueError(f"Unknown source: {source}")
