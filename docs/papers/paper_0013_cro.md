---
title: "Improved DDPG algorithm-based path planning for unmanned surface vehicles"
authors: "Menglong Hua, Weixiang Zhou, Hongying Cheng"
year: "2024"
doi: "10.20517/ir.2024.22"
source: "crossref"
url: "https://doi.org/10.20517/ir.2024.22"
arxiv_id: "N/A"
sidebar_position: "13"
tags: ["Collision Avoidance", "Decision Making", "Deep Reinforcement Learning", "Digital Twin", "Genetic Algorithm", "Obstacle Avoidance", "Path Planning", "Reinforcement Learning", "Simulation", "Trajectory Planning"]
trl_level: "3"
trl_description: "Экспериментальное подтверждение концепции"
abstract_en: "As a promising mode of water transportation, unmanned surface vehicles (USVs) are used in various fields owing to their small size, high flexibility, favorable price, and other advantages. Traditional navigation algorithms are affected by various path planning issues. To address the limitations of the traditional deep deterministic policy gradient (DDPG) algorithm, namely slow convergence speed and sparse reward and punishment functions, we proposed an improved DDPG algorithm for USV path planning. First, the principle and workflow of the DDPG deep reinforcement learning (DRL) algorithm are described. Second, the improved method (based on the USVs kinematic model) is proposed, and a continuous state and action space is designed. The reward and punishment function are improved, and the principle of collision avoidance at sea is introduced. Dynamic region restriction is added, distant obstacles in the state space are ignored, and the nearby obstacles are observed to reduce the number of algorithm iterations and save computational resources. The introduction of a multi-intelligence approach combined with a prioritized experience replay mechanism accelerates algorithm convergence, thereby increasing the efficiency and robustness of training. Finally, through a combination of theory and simulation, the DDPG DRL is explored for USV obstacle avoidance and optimal path planning."
abstract_ru: "В качестве перспективного способа водного транспорта беспилотные надводные аппараты (БНА) применяются в различных областях благодаря своим компактным размерам, высокой маневренности, доступной стоимости и другим преимуществам. Традиционные алгоритмы навигации сталкиваются с различными проблемами планирования маршрута. Для преодоления ограничений традиционного алгоритма глубокого детерминированного градиентного метода политики (DDPG), таких как медленная скорость сходимости и разреженные функции вознаграждения и наказания, нами предложен усовершенствованный алгоритм DDPG для планирования маршрутов БНА. Во-первых, описываются принципы и рабочий процесс алгоритма глубокого обучения с подкреплением (DRL) DDPG. Во-вторых, предложен улучшенный метод, основанный на кинематической модели БНА, и разработано непрерывное пространство состояний и действий. Улучшены функции вознаграждения и наказания, введён принцип предотвращения столкновений в морской среде. Добавлено динамическое ограничение области, при котором дальние препятствия в пространстве состояний игнорируются, а ближайшие препятствия учитываются, что позволяет сократить количество итераций алгоритма и сэкономить вычислительные ресурсы. Внедрение мультиинтеллектуального подхода в сочетании с механизмом приоритетного повторного воспроизведения опыта ускоряет сходимость алгоритма, повышая тем самым эффективность и устойчивость обучения. Наконец, посредством сочетания теории и моделирования исследуется применение DDPG DRL для предотвращения столкновений и оптимального планирования маршрута БНА."
key_findings: "- Proposed an improved DDPG algorithm for USV path planning to overcome slow convergence and sparse reward issues in traditional DDPG.  
- Designed a continuous state and action space based on the USV kinematic model, with enhanced reward and punishment functions incorporating collision avoidance principles.  
- Introduced dynamic region restriction to ignore distant obstacles and focus on nearby ones, reducing iterations and computational load.  
- Combined a multi-intelligence approach with prioritized experience replay to accelerate convergence and improve training efficiency and robustness.  
- Validated the improved DDPG algorithm through theoretical analysis and simulation for effective USV obstacle avoidance and optimal path planning."
---

# Improved DDPG algorithm-based path planning for unmanned surface vehicles

**Авторы:** Menglong Hua, Weixiang Zhou, Hongying Cheng
**Год:** 2024
**Источник:** crossref
**DOI:** 10.20517/ir.2024.22
**arXiv ID:** N/A

## Аннотация (оригинал)

As a promising mode of water transportation, unmanned surface vehicles (USVs) are used in various fields owing to their small size, high flexibility, favorable price, and other advantages. Traditional navigation algorithms are affected by various path planning issues. To address the limitations of the traditional deep deterministic policy gradient (DDPG) algorithm, namely slow convergence speed and sparse reward and punishment functions, we proposed an improved DDPG algorithm for USV path planning. First, the principle and workflow of the DDPG deep reinforcement learning (DRL) algorithm are described. Second, the improved method (based on the USVs kinematic model) is proposed, and a continuous state and action space is designed. The reward and punishment function are improved, and the principle of collision avoidance at sea is introduced. Dynamic region restriction is added, distant obstacles in the state space are ignored, and the nearby obstacles are observed to reduce the number of algorithm iterations and save computational resources. The introduction of a multi-intelligence approach combined with a prioritized experience replay mechanism accelerates algorithm convergence, thereby increasing the efficiency and robustness of training. Finally, through a combination of theory and simulation, the DDPG DRL is explored for USV obstacle avoidance and optimal path planning.

## Аннотация (русский перевод)

В качестве перспективного способа водного транспорта беспилотные надводные аппараты (БНА) применяются в различных областях благодаря своим компактным размерам, высокой маневренности, доступной стоимости и другим преимуществам. Традиционные алгоритмы навигации сталкиваются с различными проблемами планирования маршрута. Для преодоления ограничений традиционного алгоритма глубокого детерминированного градиентного метода политики (DDPG), таких как медленная скорость сходимости и разреженные функции вознаграждения и наказания, нами предложен усовершенствованный алгоритм DDPG для планирования маршрутов БНА. Во-первых, описываются принципы и рабочий процесс алгоритма глубокого обучения с подкреплением (DRL) DDPG. Во-вторых, предложен улучшенный метод, основанный на кинематической модели БНА, и разработано непрерывное пространство состояний и действий. Улучшены функции вознаграждения и наказания, введён принцип предотвращения столкновений в морской среде. Добавлено динамическое ограничение области, при котором дальние препятствия в пространстве состояний игнорируются, а ближайшие препятствия учитываются, что позволяет сократить количество итераций алгоритма и сэкономить вычислительные ресурсы. Внедрение мультиинтеллектуального подхода в сочетании с механизмом приоритетного повторного воспроизведения опыта ускоряет сходимость алгоритма, повышая тем самым эффективность и устойчивость обучения. Наконец, посредством сочетания теории и моделирования исследуется применение DDPG DRL для предотвращения столкновений и оптимального планирования маршрута БНА.

## Ключевые выводы

- Proposed an improved DDPG algorithm for USV path planning to overcome slow convergence and sparse reward issues in traditional DDPG.  
- Designed a continuous state and action space based on the USV kinematic model, with enhanced reward and punishment functions incorporating collision avoidance principles.  
- Introduced dynamic region restriction to ignore distant obstacles and focus on nearby ones, reducing iterations and computational load.  
- Combined a multi-intelligence approach with prioritized experience replay to accelerate convergence and improve training efficiency and robustness.  
- Validated the improved DDPG algorithm through theoretical analysis and simulation for effective USV obstacle avoidance and optimal path planning.

## Оценка применимости (TRL)

**TRL 3** - Экспериментальное подтверждение концепции

## Ссылки

- [Полный текст на CrossRef](https://doi.org/10.20517/ir.2024.22 )
- [Источник](https://doi.org/10.20517/ir.2024.22)