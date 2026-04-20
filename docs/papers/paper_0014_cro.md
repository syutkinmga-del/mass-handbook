---
title: "Effectiveness of Attention Mechanisms in YOLOv8 for Maritime Vessel Detection"
authors: "Changui Lee, Seojeong Lee"
year: "2026"
doi: "10.3390/jmse14050433"
source: "crossref"
url: "https://doi.org/10.3390/jmse14050433"
arxiv_id: "N/A"
sidebar_position: "14"
tags: ["Fault Tolerance", "Knowledge Representation", "Optimization Algorithm", "Perception", "Testing", "User Interface"]
trl_level: "3"
trl_description: "Экспериментальное подтверждение концепции"
abstract_en: "Maritime vessel detection in nearshore waters is a fundamental capability for artificial intelligence (AI)-enabled maritime transportation systems, including coastal monitoring, traffic management, and digital maritime services. Although attention mechanisms are widely incorporated into YOLO-based detectors, their relative effectiveness in marine environments under strictly controlled experimental conditions remains insufficiently clarified. This study presents a systematic comparison of Coordinate Attention (CA), Convolutional Block Attention Module (CBAM), and CLIP-based semantic fusion within a unified YOLOv8n framework for binary discrimination between ships and fishing boats in cluttered coastal imagery. All model variants were trained under identical data partitions and optimization settings to isolate architectural effects. The experimental results show that CA achieves the highest localization robustness (mAP@0.5:0.95 = 0.6127) and substantially improves precision (+7.13% over baseline), while CBAM provides the most balanced performance with the highest F1-score. In contrast, CLIP-based semantic fusion consistently degrades detection reliability, indicating limitations of global vision–language representations in small-scale maritime datasets. Precision–Recall and F1 analyses further reveal architecture-specific confidence calibration behaviors relevant to deployment-sensitive maritime applications. The findings provide practical guidance for selecting attention mechanisms in AI-driven maritime perception systems and support reliable AI integration in marine science and engineering applications."
abstract_ru: "Обнаружение морских судов в прибрежных водах является фундаментальной функцией для систем морского транспорта с искусственным интеллектом (ИИ), включая прибрежный мониторинг, управление движением и цифровые морские сервисы. Несмотря на широкое внедрение механизмов внимания в детекторы на базе YOLO, их относительная эффективность в морской среде при строго контролируемых экспериментальных условиях остается недостаточно изученной. В данном исследовании представлен систематический сравнительный анализ механизмов Coordinate Attention (CA), Convolutional Block Attention Module (CBAM) и семантического слияния на основе CLIP в единой архитектуре YOLOv8n для бинарной классификации между кораблями и рыболовными судами на сложных прибрежных изображениях. Все варианты моделей обучались на идентичных разбиениях данных и с одинаковыми настройками оптимизации для изоляции архитектурных эффектов. Экспериментальные результаты показывают, что CA достигает наивысшей устойчивости локализации (mAP@0.5:0.95 = 0.6127) и существенно повышает точность (+7,13% по сравнению с базовой моделью), в то время как CBAM обеспечивает наиболее сбалансированную производительность с максимальным значением F1-меры. Напротив, семантическое слияние на основе CLIP последовательно ухудшает надежность обнаружения, что указывает на ограничения глобальных визуально-языковых представлений в маломасштабных морских датасетах. Анализ Precision–Recall и F1 дополнительно выявляет архитектурно-специфические особенности калибровки уверенности, важные для приложений с чувствительностью к развертыванию в морской сфере. Полученные результаты предоставляют практические рекомендации по выбору механизмов внимания в системах восприятия морской среды на базе ИИ и способствуют надежной интеграции ИИ в морскую науку и инженерные приложения."
key_findings: "- Coordinate Attention (CA) integrated into YOLOv8n achieved the highest localization robustness with mAP@0.5:0.95 = 0.6127 and improved precision by 7.13% over the baseline.  
- Convolutional Block Attention Module (CBAM) delivered the most balanced performance, attaining the highest F1-score among tested attention mechanisms.  
- CLIP-based semantic fusion consistently reduced detection reliability, highlighting limitations of global vision–language models on small-scale maritime datasets.  
- Precision–Recall and F1 analyses revealed distinct confidence calibration behaviors depending on the attention architecture, important for deployment in maritime applications.  
- The study offers practical recommendations for selecting attention mechanisms in AI-driven maritime vessel detection systems under controlled experimental conditions."
---

# Effectiveness of Attention Mechanisms in YOLOv8 for Maritime Vessel Detection

**Авторы:** Changui Lee, Seojeong Lee
**Год:** 2026
**Источник:** crossref
**DOI:** 10.3390/jmse14050433
**arXiv ID:** N/A

## Аннотация (оригинал)

Maritime vessel detection in nearshore waters is a fundamental capability for artificial intelligence (AI)-enabled maritime transportation systems, including coastal monitoring, traffic management, and digital maritime services. Although attention mechanisms are widely incorporated into YOLO-based detectors, their relative effectiveness in marine environments under strictly controlled experimental conditions remains insufficiently clarified. This study presents a systematic comparison of Coordinate Attention (CA), Convolutional Block Attention Module (CBAM), and CLIP-based semantic fusion within a unified YOLOv8n framework for binary discrimination between ships and fishing boats in cluttered coastal imagery. All model variants were trained under identical data partitions and optimization settings to isolate architectural effects. The experimental results show that CA achieves the highest localization robustness (mAP@0.5:0.95 = 0.6127) and substantially improves precision (+7.13% over baseline), while CBAM provides the most balanced performance with the highest F1-score. In contrast, CLIP-based semantic fusion consistently degrades detection reliability, indicating limitations of global vision–language representations in small-scale maritime datasets. Precision–Recall and F1 analyses further reveal architecture-specific confidence calibration behaviors relevant to deployment-sensitive maritime applications. The findings provide practical guidance for selecting attention mechanisms in AI-driven maritime perception systems and support reliable AI integration in marine science and engineering applications.

## Аннотация (русский перевод)

Обнаружение морских судов в прибрежных водах является фундаментальной функцией для систем морского транспорта с искусственным интеллектом (ИИ), включая прибрежный мониторинг, управление движением и цифровые морские сервисы. Несмотря на широкое внедрение механизмов внимания в детекторы на базе YOLO, их относительная эффективность в морской среде при строго контролируемых экспериментальных условиях остается недостаточно изученной. В данном исследовании представлен систематический сравнительный анализ механизмов Coordinate Attention (CA), Convolutional Block Attention Module (CBAM) и семантического слияния на основе CLIP в единой архитектуре YOLOv8n для бинарной классификации между кораблями и рыболовными судами на сложных прибрежных изображениях. Все варианты моделей обучались на идентичных разбиениях данных и с одинаковыми настройками оптимизации для изоляции архитектурных эффектов. Экспериментальные результаты показывают, что CA достигает наивысшей устойчивости локализации (mAP@0.5:0.95 = 0.6127) и существенно повышает точность (+7,13% по сравнению с базовой моделью), в то время как CBAM обеспечивает наиболее сбалансированную производительность с максимальным значением F1-меры. Напротив, семантическое слияние на основе CLIP последовательно ухудшает надежность обнаружения, что указывает на ограничения глобальных визуально-языковых представлений в маломасштабных морских датасетах. Анализ Precision–Recall и F1 дополнительно выявляет архитектурно-специфические особенности калибровки уверенности, важные для приложений с чувствительностью к развертыванию в морской сфере. Полученные результаты предоставляют практические рекомендации по выбору механизмов внимания в системах восприятия морской среды на базе ИИ и способствуют надежной интеграции ИИ в морскую науку и инженерные приложения.

## Ключевые выводы

- Coordinate Attention (CA) integrated into YOLOv8n achieved the highest localization robustness with mAP@0.5:0.95 = 0.6127 and improved precision by 7.13% over the baseline.  
- Convolutional Block Attention Module (CBAM) delivered the most balanced performance, attaining the highest F1-score among tested attention mechanisms.  
- CLIP-based semantic fusion consistently reduced detection reliability, highlighting limitations of global vision–language models on small-scale maritime datasets.  
- Precision–Recall and F1 analyses revealed distinct confidence calibration behaviors depending on the attention architecture, important for deployment in maritime applications.  
- The study offers practical recommendations for selecting attention mechanisms in AI-driven maritime vessel detection systems under controlled experimental conditions.

## Оценка применимости (TRL)

**TRL 3** - Экспериментальное подтверждение концепции

## Ссылки

- [Полный текст на CrossRef](https://doi.org/10.3390/jmse14050433 )
- [Источник](https://doi.org/10.3390/jmse14050433)