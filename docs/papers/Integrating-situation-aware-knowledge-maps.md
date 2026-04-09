---
sidebar_position: 1
tags: [Navigation, Situational Awareness, Collision Avoidance, DWA, Knowledge Maps]
---

# Integrating situation-aware knowledge maps and dynamic window approach for collision avoidance

**Авторы:** Liguo Zhang, Zhibo Zhang, Jiarong Cai, Tianxu Yan
**Год:** 2024
**Источник:** Ocean Engineering
**DOI:** 10.1016/j.oceaneng.2024.118882

## Аннотация (оригинал)

With the continuous development of Maritime Autonomous Surface Ships (MASS), intelligent decision-making in autonomous navigation has emerged as a key technology for ensuring the safety of maritime transportation. However, due to the unpredictability and uncertainty of dynamic environments, as well as the complexity of multi-ship encounter scenarios, relying solely on algorithmic optimization or mathematical models often fails to guarantee robust decision-making. In this study, we propose a situation-aware knowledge map tailored for collision avoidance in MASS, aiming to comprehensively model the dynamic environmental information of multi-ship encounters and explicitly represent decision-making rules based on COLREGs. Building upon this, we introduce an intelligent decision-making algorithm that integrates the situation-aware knowledge map with the dynamic window approach. Through the retrieval and reasoning capabilities of the knowledge map, we establish the fundamental logic for collision avoidance decision-making. Additionally, the algorithm incorporates dynamic risk factors into the evaluation function, enabling safe and COLREGs-compliant path planning. The proposed method is validated through simulation experiments across various typical multi-ship encounter scenarios, demonstrating its significant advantages in improving safety, enhancing reasoning interpretability, and ensuring COLREGs compliance in autonomous collision avoidance.

## Аннотация (русский перевод)

С непрерывным развитием морских автономных надводных судов (MASS) интеллектуальное принятие решений в автономной навигации стало ключевой технологией для обеспечения безопасности морских перевозок. Однако из-за непредсказуемости и неопределенности динамической среды, а также сложности сценариев расхождения нескольких судов, использование только алгоритмической оптимизации или математических моделей часто не гарантирует надежного принятия решений. В данном исследовании предлагается ситуационно-осведомленная карта знаний, адаптированная для предотвращения столкновений MASS, с целью комплексного моделирования динамической информации об окружающей среде при расхождении нескольких судов и явного представления правил принятия решений на основе МППСС (COLREGs). На основе этого представлен алгоритм интеллектуального принятия решений, который интегрирует ситуационно-осведомленную карту знаний с подходом динамического окна (DWA). Благодаря возможностям поиска и рассуждения карты знаний устанавливается базовая логика для принятия решений по предотвращению столкновений. Кроме того, алгоритм включает динамические факторы риска в функцию оценки, обеспечивая безопасное планирование пути в соответствии с COLREGs. Предложенный метод проверен с помощью имитационных экспериментов в различных типичных сценариях расхождения нескольких судов, демонстрируя свои значительные преимущества в повышении безопасности, улучшении интерпретируемости рассуждений и обеспечении соответствия COLREGs при автономном предотвращении столкновений.

## Ключевые выводы для разработчиков

- **Интеграция онтологий и DWA**: Предложен новый подход, объединяющий символические рассуждения (карты знаний) с локальным планированием пути (DWA).
- **Соответствие COLREGs**: Карты знаний позволяют явно кодировать правила МППСС (COLREGs), обеспечивая их соблюдение при принятии решений.
- **Динамическая оценка риска**: Алгоритм DWA модифицирован включением динамических факторов риска в целевую функцию.
- **Интерпретируемость**: Использование карт знаний делает процесс принятия решений прозрачным и понятным, в отличие от подходов на базе "черного ящика" (например, DRL).

## Оценка применимости (TRL)

**TRL 4** - Технология подтверждена в лабораторных условиях (имитационное моделирование).

## Связанные ресурсы

- [Гайд по интеграции DWA](/docs/guides/dwa-integration)
- [Глоссарий: COLREGs](/docs/glossary#colregs)

## Ссылки

- [Полный текст на CrossRef](https://doi.org/10.1016/j.oceaneng.2024.118882)
