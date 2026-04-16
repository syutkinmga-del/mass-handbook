#!/usr/bin/env python3
"""
Скрипт для переиндексирования существующих статей с новыми тегами.
Использует функцию generate_tags_from_content из collect_papers_extended.py
"""
import os
import re
import glob
import logging
from typing import List, Dict

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Словарь ключевых слов для автоматического тегирования (скопирован из collect_papers_extended.py)
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

def parse_paper_file(filepath: str) -> Dict:
    """
    Парсит markdown файл статьи и извлекает метаданные и контент.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Извлекаем frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if not frontmatter_match:
            logger.warning(f"Не удалось найти frontmatter в {filepath}")
            return None
        
        frontmatter_text = frontmatter_match.group(1)
        body = content[frontmatter_match.end():]
        
        # Парсим frontmatter
        paper_data = {}
        for line in frontmatter_text.split('\n'):
            if ':' not in line:
                continue
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # Убираем кавычки
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            
            # Парсим списки
            if value.startswith('[') and value.endswith(']'):
                value = [v.strip().strip('"') for v in value[1:-1].split(',')]
            
            paper_data[key] = value
        
        # Извлекаем аннотацию из тела
        abstract_match = re.search(r'## Аннотация \(оригинал\)\n\n(.*?)\n\n##', body, re.DOTALL)
        if abstract_match:
            paper_data['abstract_en'] = abstract_match.group(1).strip()
        
        return paper_data
        
    except Exception as e:
        logger.error(f"Ошибка при парсинге {filepath}: {e}")
        return None

def update_paper_file(filepath: str, paper_data: Dict, new_tags: List[str]) -> bool:
    """
    Обновляет файл статьи с новыми тегами.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Заменяем старые теги на новые
        old_tags_pattern = r'tags:\s*\[.*?\]'
        tags_list = ', '.join(f'"{tag}"' for tag in new_tags)
        new_tags_str = f'tags: [{tags_list}]'       
        new_content = re.sub(old_tags_pattern, new_tags_str, content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при обновлении {filepath}: {e}")
        return False

def main():
    """
    Главная функция для переиндексирования всех статей.
    """
    papers_dir = 'docs/papers'
    
    if not os.path.exists(papers_dir):
        logger.error(f"Директория {papers_dir} не найдена")
        return
    
    # Находим все файлы статей
    paper_files = sorted(glob.glob(os.path.join(papers_dir, 'paper_*.md')))
    
    logger.info(f"Найдено {len(paper_files)} файлов статей для переиндексирования")
    
    updated_count = 0
    
    for filepath in paper_files:
        filename = os.path.basename(filepath)
        
        # Парсим файл
        paper_data = parse_paper_file(filepath)
        if not paper_data:
            continue
        
        # Генерируем новые теги
        new_tags = generate_tags_from_content(paper_data)
        old_tags = paper_data.get('tags', [])
        
        # Если теги изменились, обновляем файл
        if set(new_tags) != set(old_tags if isinstance(old_tags, list) else [old_tags]):
            if update_paper_file(filepath, paper_data, new_tags):
                logger.info(f"✓ Обновлена статья: {filename}")
                logger.info(f"  Старые теги: {old_tags}")
                logger.info(f"  Новые теги: {new_tags}")
                updated_count += 1
        else:
            logger.info(f"- Статья {filename} уже имеет корректные теги")
    
    logger.info(f"\n✓ Успешно обновлено {updated_count} статей")

if __name__ == '__main__':
    main()
