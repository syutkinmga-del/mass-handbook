import os
import json
import logging
from typing import Dict, Optional
from openai import OpenAI
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ProcessedPaper:
    translated_abstract: str
    key_findings: list[str]
    trl_assessment: str
    trl_level: int
    tags: list[str]

class OpenAIPaperProcessor:
    """Модуль для обработки научных статей с помощью OpenAI API"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set. Please provide it or set the environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        
        # Системный промпт для задания роли и формата вывода
        self.system_prompt = """
        Вы - эксперт-аналитик в области морских автономных надводных судов (MASS) и морской навигации.
        Ваша задача - проанализировать аннотацию (abstract) научной статьи и предоставить структурированный ответ в формате JSON.
        
        Ожидаемый формат JSON:
        {
            "translated_abstract": "Перевод аннотации на профессиональный русский язык",
            "key_findings": [
                "Ключевой вывод 1 (на русском)",
                "Ключевой вывод 2 (на русском)",
                "Ключевой вывод 3 (на русском)"
            ],
            "trl_assessment": "Краткое обоснование оценки уровня готовности технологии (TRL) на основе текста аннотации",
            "trl_level": 3, // Целое число от 1 до 9 (где 1 - базовая идея, 3 - симуляция/доказательство концепции, 9 - готовое решение)
            "tags": ["Тег 1", "Тег 2", "Тег 3"] // 3-5 ключевых тегов на английском (например, Collision Avoidance, DWA, DRL)
        }
        """

    def process_paper(self, title: str, abstract: str) -> Optional[ProcessedPaper]:
        """Анализирует статью и возвращает структурированные данные"""
        if not abstract or len(abstract) < 50:
            logger.warning(f"Аннотация слишком короткая для анализа: {title}")
            return None
            
        prompt = f"Проанализируйте следующую научную статью.\n\nНазвание: {title}\n\nАннотация: {abstract}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3, # Низкая температура для более детерминированных результатов
                max_tokens=1500
            )
            
            content = response.choices[0].message.content
            if not content:
                return None
                
            data = json.loads(content)
            
            return ProcessedPaper(
                translated_abstract=data.get("translated_abstract", ""),
                key_findings=data.get("key_findings", []),
                trl_assessment=data.get("trl_assessment", ""),
                trl_level=data.get("trl_level", 1),
                tags=data.get("tags", [])
            )
            
        except Exception as e:
            logger.error(f"Ошибка при обработке статьи '{title}' через OpenAI: {e}")
            return None
