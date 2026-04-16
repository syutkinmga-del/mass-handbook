---
title: "Deploying Efficient LLM Agents on Maritime Autonomous Surface Ships: Fine-Tuning, RAG, and Function Calling in a Mid-Size Model"
authors: "Yiling Ren, Mozi Chen, Junjie Weng"
year: "2026"
doi: "10.3390/info17030284"
source: "crossref"
url: "https://doi.org/10.3390/info17030284"
arxiv_id: "N/A"
sidebar_position: "15"
tags: ["Compliance", "Decision Making", "Dynamic Window Approach", "Genetic Algorithm", "Knowledge Representation", "MASS", "User Interface"]
trl_level: "3"
trl_description: "Экспериментальное подтверждение концепции"
---

# Deploying Efficient LLM Agents on Maritime Autonomous Surface Ships: Fine-Tuning, RAG, and Function Calling in a Mid-Size Model

**Авторы:** Yiling Ren, Mozi Chen, Junjie Weng
**Год:** 2026
**Источник:** crossref
**DOI:** 10.3390/info17030284
**arXiv ID:** N/A

## Аннотация (оригинал)

<jats:p>Deploying Large Language Models (LLMs) on Maritime Autonomous Surface Ships (MASS) entails a critical trade-off between reasoning depth, inference latency, and hardware constraints. To fill the existing gap, we introduce MARTIAN (Maritime Agent for Real-time Tactical Inference And Navigation), a 14B-parameter decision support agent engineered for edge deployment on standard vessel hardware (e.g., the NVIDIA Jetson AGX Orin). Central to our approach is the Cognitive Core architecture, which utilizes a verified dataset of 21,800 Chain-of-Thought (CoT) instruction–response pairs to align general linguistic capabilities with maritime procedural logic. Empirical evaluations demonstrate that MARTIAN achieves an overall accuracy of 73.23% (SFT only) and 81.16% (SFT + RAG) on the Bilingual Maritime Multiple-Choice Questionnaire (BM-MCQ), a standardized assessment dataset constructed based on Officer of the Watch (OOW) competencies. Notably, the SFT-only configuration attains 78.53% on pure-logic-intensive COLREG tasks—surpassing the 72B-parameter Qwen-2.5 foundation model in this domain—while maintaining a real-time inference latency of 22.4 ms/token. Crucially, our ablation studies support a nuanced Interference Hypothesis: while RAG significantly enhances factual recall in knowledge-intensive domains (boosting total accuracy from 73.23% to 81.16%), it concurrently introduces semantic noise that degrades performance in pure logic reasoning tasks (e.g., COLREG maneuvering accuracy decreases from 78.53% to 77.36%). On the basis of this finding, we identify and empirically motivate a decoupled cognitive design principle that separates procedural reflexes (via SFT) from declarative knowledge (via RAG). While the full implementation of an adaptive routing mechanism is deferred to future work, the ablation results presented herein offer a validated, cost-effective reference architecture for deploying transparent and regulation-compliant AI on resource-constrained merchant vessels.</jats:p>

## Аннотация (русский перевод)

_Перевод недоступен_

## Ключевые выводы

- Статья добавлена автоматически

## Оценка применимости (TRL)

**TRL 3** - Экспериментальное подтверждение концепции

## Ссылки

- [Полный текст на CrossRef](https://doi.org/10.3390/info17030284 )
- [Источник](https://doi.org/10.3390/info17030284)