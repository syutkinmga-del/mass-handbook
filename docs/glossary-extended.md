---
sidebar_position: 4
---
# Расширенный глоссарий MASS

Подробное описание ключевых терминов, концепций и технологий, используемых в разработке морских автономных надводных судов.
Каждый термин включает определение, контекст применения, связанные концепции и примеры использования.

> Глоссарий содержит **27 терминов**. Последнее обновление: 21.04.2026.

---

### Collision Avoidance

**Определение:** Избежание столкновений — это процесс обнаружения и предотвращения столкновений судна с другими объектами или судами в морской среде с помощью автоматизированных систем и алгоритмов.

**Definition (EN):** Collision avoidance is the process of detecting and preventing collisions between a vessel and other objects or ships in the maritime environment using automated systems and algorithms.

**Контекст применения в MASS:**

В области морских автономных надводных судов (MASS) системы избежания столкновений играют ключевую роль в обеспечении безопасности навигации. Они интегрируют данные с датчиков, картографические знания и алгоритмы планирования маршрута для принятия решений в реальном времени. Такие системы позволяют автономным судам эффективно реагировать на динамические изменения обстановки и минимизировать риск аварий.

**Связанные термины:**

- Автономная навигация
- Планирование маршрута
- Датчики и сенсоры
- Ситуационная осведомленность
- Динамическое окно
- Обнаружение препятствий

**Примеры использования:**

- Использование алгоритма динамического окна для локального планирования маршрута с целью избежания столкновений.
- Интеграция ситуационно-осведомленных карт знаний для повышения точности систем избежания столкновений в MASS.

**Статьи по теме:**

- [Integrating-situation-aware-knowledge-maps.md](./papers/Integrating-situation-aware-knowledge-maps)
- [Local Route Planning for Collision Avoidance of Maritime Autonomous Surface Ships in Compliance with COLREGs Rules](./papers/paper_0001_cro)
- [Improved dynamic window approach for autonomous collision avoidance decision-making algorithm](./papers/paper_0002_cro)
- [Collision avoidance on maritime autonomous surface ships](./papers/paper_0003_cro)
- [Deep reinforcement learning with dynamic window approach based collision avoidance path planning for maritime autonomous surface ships](./papers/paper_0004_cro)
- [SWOT ANALYSIS OF LEADING SAFETY INDICATORS FOR COLLISION AVOIDANCE OF MARITIME AUTONOMOUS SURFACE SHIPS](./papers/paper_0005_cro)
- [A Dynamic Programming Approach to Collision Avoidance of Autonomous Ships](./papers/paper_0006_cro)
- [Dynamic Tabu Search for Collision Avoidance in Autonomous Maritime Ships](./papers/paper_0007_cro)
- [Collaborative collision avoidance for Maritime Autonomous Surface Ships: A review](./papers/paper_0009_cro)
- [A Dynamic Programming Approach to the Collision Avoidance of Autonomous Ships](./papers/paper_0011_cro)
- [Improved DDPG algorithm-based path planning for unmanned surface vehicles](./papers/paper_0013_cro)
- [Maritime Autonomous Surface Ships: Architecture for Autonomous Navigation Systems](./papers/paper_0016_cro)

---

### COLREGs

**Определение:** COLREGs (Международные правила предотвращения столкновений судов) — свод правил, регулирующих поведение судов на море для предотвращения столкновений. Они устанавливают нормы движения, приоритеты и сигналы между судами.

**Definition (EN):** COLREGs (International Regulations for Preventing Collisions at Sea) are a set of rules governing vessel behavior to avoid collisions. They define navigation norms, priorities, and signaling between ships.

**Контекст применения в MASS:**

В области морских автономных надводных судов (MASS) COLREGs используются для разработки алгоритмов планирования маршрутов и принятия решений, обеспечивающих безопасное взаимодействие автономных судов с другими морскими объектами. Соблюдение COLREGs является ключевым фактором для предотвращения аварий и обеспечения интеграции MASS в существующее морское пространство.

**Связанные термины:**

- автономное судно
- планирование маршрута
- избежание столкновений
- навигационные правила
- системы обнаружения и предупреждения

**Примеры использования:**

- Использование COLREGs для локального планирования маршрута автономного судна.
- Моделирование поведения MASS в соответствии с COLREGs для предотвращения столкновений.

**Статьи по теме:**

- [Local Route Planning for Collision Avoidance of Maritime Autonomous Surface Ships in Compliance with COLREGs Rules](./papers/paper_0001_cro)

---

### Compliance

**Определение:** Compliance — это соблюдение нормативных требований, стандартов и правил, обеспечивающих безопасность и законность эксплуатации морских автономных надводных судов.

**Definition (EN):** Compliance refers to adherence to regulatory requirements, standards, and rules that ensure the safe and lawful operation of Maritime Autonomous Surface Ships.

**Контекст применения в MASS:**

В области MASS compliance играет ключевую роль в обеспечении безопасности навигации и предотвращении столкновений, так как автономные системы должны соответствовать международным и национальным морским нормам. Это включает в себя соблюдение правил Коллизии (COLREGs), стандартов безопасности и требований к программному обеспечению автономных судов.

**Связанные термины:**

- [COLREGs](#colregs)
- [Collision Avoidance](#collision-avoidance)
- Safety Standards
- Regulatory Compliance
- Autonomous Navigation

**Примеры использования:**

- Соблюдение COLREGs для предотвращения столкновений в локальном маршруте автономного судна.
- Анализ соответствия систем автономного судна международным стандартам безопасности.

**Статьи по теме:**

- [Local Route Planning for Collision Avoidance of Maritime Autonomous Surface Ships in Compliance with COLREGs Rules](./papers/paper_0001_cro)
- [SWOT ANALYSIS OF LEADING SAFETY INDICATORS FOR COLLISION AVOIDANCE OF MARITIME AUTONOMOUS SURFACE SHIPS](./papers/paper_0005_cro)
- [Deploying Efficient LLM Agents on Maritime Autonomous Surface Ships: Fine-Tuning, RAG, and Function Calling in a Mid-Size Model](./papers/paper_0015_cro)

---

### Decision Making

**Определение:** Принятие решений — процесс выбора оптимального действия или маршрута на основе анализа текущей ситуации и доступной информации для обеспечения безопасности и эффективности движения автономного надводного судна.

**Definition (EN):** Decision making is the process of selecting the optimal action or route based on the analysis of the current situation and available information to ensure the safety and efficiency of an autonomous surface ship's navigation.

**Контекст применения в MASS:**

В области морских автономных надводных судов (MASS) принятие решений играет ключевую роль в задачах предотвращения столкновений и планирования маршрута. Используются методы глубокого обучения, динамического программирования и локального планирования для адаптивного выбора безопасных и эффективных траекторий движения.

**Связанные термины:**

- [Collision Avoidance](#collision-avoidance)
- Route Planning
- Autonomous Navigation
- Dynamic Programming
- [Reinforcement Learning](#reinforcement-learning)

**Примеры использования:**

- Использование глубокого обучения для принятия решений при маневрировании в условиях плотного трафика.
- Применение динамического программирования для выбора оптимального маршрута с учетом возможных столкновений.

**Статьи по теме:**

- [Local Route Planning for Collision Avoidance of Maritime Autonomous Surface Ships in Compliance with COLREGs Rules](./papers/paper_0001_cro)
- [Deep reinforcement learning with dynamic window approach based collision avoidance path planning for maritime autonomous surface ships](./papers/paper_0004_cro)
- [A Dynamic Programming Approach to Collision Avoidance of Autonomous Ships](./papers/paper_0006_cro)
- [Integrating situation-aware knowledge maps and dynamic window approach for safe path planning by maritime autonomous surface ships](./papers/paper_0010_cro)
- [A Dynamic Programming Approach to the Collision Avoidance of Autonomous Ships](./papers/paper_0011_cro)
- [Improved DDPG algorithm-based path planning for unmanned surface vehicles](./papers/paper_0013_cro)
- [Deploying Efficient LLM Agents on Maritime Autonomous Surface Ships: Fine-Tuning, RAG, and Function Calling in a Mid-Size Model](./papers/paper_0015_cro)

---

### Deep Reinforcement Learning

**Определение:** Глубокое подкрепляющее обучение — метод машинного обучения, объединяющий глубокие нейронные сети и алгоритмы обучения с подкреплением для принятия решений в сложных средах. Оно позволяет агенту учиться оптимальной стратегии поведения на основе взаимодействия с окружающей средой и получаемых наград.

**Definition (EN):** Deep Reinforcement Learning is a machine learning approach combining deep neural networks with reinforcement learning algorithms to make decisions in complex environments. It enables an agent to learn optimal policies through interaction with the environment and reward feedback.

**Контекст применения в MASS:**

В области морских автономных надводных судов (MASS) глубокое подкрепляющее обучение применяется для решения задач планирования маршрутов и предотвращения столкновений. Использование таких методов позволяет автономным судам адаптивно реагировать на динамические изменения в морской обстановке и обеспечивать безопасное и эффективное движение.

**Связанные термины:**

- обучение с подкреплением
- глубокие нейронные сети
- планирование маршрута
- избегание столкновений
- автономные надводные суда

**Примеры использования:**

- Deep reinforcement learning with dynamic window approach based collision avoidance
- Improved DDPG algorithm-based path planning for unmanned surface vehicles

**Статьи по теме:**

- [Deep reinforcement learning with dynamic window approach based collision avoidance path planning for maritime autonomous surface ships](./papers/paper_0004_cro)
- [Improved DDPG algorithm-based path planning for unmanned surface vehicles](./papers/paper_0013_cro)

---

### Digital Twin

**Определение:** Цифровой двойник — это виртуальная модель физического объекта или системы, которая отражает их состояние и поведение в реальном времени с помощью данных и симуляций.

**Definition (EN):** A digital twin is a virtual model of a physical object or system that reflects its state and behavior in real time through data and simulations.

**Контекст применения в MASS:**

В области морских автономных надводных судов (MASS) цифровой двойник используется для моделирования и оптимизации работы автономных систем, включая планирование маршрутов и управление движением. Это позволяет повысить эффективность и безопасность эксплуатации судов за счет прогнозирования и анализа различных сценариев в виртуальной среде.

**Связанные термины:**

- автономное судно
- планирование маршрута
- искусственный интеллект
- моделирование
- система управления
- обучение с подкреплением

**Примеры использования:**

- Использование цифрового двойника для тестирования алгоритмов планирования пути на основе улучшенного DDPG.
- Моделирование поведения автономного судна в различных погодных условиях с помощью цифрового двойника.

**Статьи по теме:**

- [Improved DDPG algorithm-based path planning for unmanned surface vehicles](./papers/paper_0013_cro)

---

### DWA

**Определение:** DWA (Dynamic Window Approach) — это алгоритм локального планирования траектории, который учитывает динамические ограничения судна для безопасного и эффективного маневрирования в реальном времени.

**Definition (EN):** DWA (Dynamic Window Approach) is a local trajectory planning algorithm that considers the dynamic constraints of a vessel to enable safe and efficient real-time maneuvering.

**Контекст применения в MASS:**

В области морских автономных надводных судов DWA применяется для обеспечения адаптивного и ситуационно-зависимого управления движением, позволяя судну избегать препятствий и оптимизировать маршрут с учётом текущих условий и ограничений.

**Связанные термины:**

- локальное планирование траектории
- динамические ограничения
- автономное управление
- избегание препятствий
- [MASS](#mass)

**Примеры использования:**

- Использование DWA для обхода неподвижных и движущихся препятствий в реальном времени.
- Интеграция DWA с ситуационно-зависимыми картами знаний для улучшения навигации MASS.

**Статьи по теме:**

- [Integrating-situation-aware-knowledge-maps.md](./papers/Integrating-situation-aware-knowledge-maps)

---

### Dynamic Window Approach

**Определение:** Dynamic Window Approach (DWA) — это метод локального планирования траектории для автономных транспортных средств, основанный на оценке допустимых скоростей и ускорений с целью безопасного и эффективного обхода препятствий в реальном времени.

**Definition (EN):** Dynamic Window Approach (DWA) is a local trajectory planning method for autonomous vehicles that evaluates feasible velocities and accelerations to safely and efficiently avoid obstacles in real-time.

**Контекст применения в MASS:**

В области морских автономных надводных судов (MASS) DWA используется для локального планирования маршрута с целью предотвращения столкновений с другими судами и препятствиями. Метод позволяет учитывать динамические ограничения судна и изменяющиеся условия окружающей среды, обеспечивая адаптивное и безопасное маневрирование в сложных морских ситуациях.

**Связанные термины:**

- локальное планирование маршрута
- избежание столкновений
- автономное управление
- динамические ограничения
- маршрутизация
- обход препятствий

**Примеры использования:**

- Использование DWA для локального планирования маршрута при обходе неподвижных и движущихся препятствий на море.
- Интеграция DWA с алгоритмами глубокого обучения для улучшения решений по предотвращению столкновений в MASS.

**Статьи по теме:**

- [Local Route Planning for Collision Avoidance of Maritime Autonomous Surface Ships in Compliance with COLREGs Rules](./papers/paper_0001_cro)
- [Improved dynamic window approach for autonomous collision avoidance decision-making algorithm](./papers/paper_0002_cro)
- [Deep reinforcement learning with dynamic window approach based collision avoidance path planning for maritime autonomous surface ships](./papers/paper_0004_cro)
- [Integrating situation-aware knowledge maps and dynamic window approach for safe path planning by maritime autonomous surface ships](./papers/paper_0010_cro)
- [Deploying Efficient LLM Agents on Maritime Autonomous Surface Ships: Fine-Tuning, RAG, and Function Calling in a Mid-Size Model](./papers/paper_0015_cro)

---

### Fault Tolerance

**Определение:** Отказоустойчивость — способность системы продолжать корректно функционировать при возникновении сбоев или ошибок в её компонентах. Это обеспечивает надежность и безопасность работы автономных систем.

**Definition (EN):** Fault tolerance is the ability of a system to continue operating correctly in the event of failures or errors in its components. It ensures the reliability and safety of autonomous systems.

**Контекст применения в MASS:**

В области морских автономных надводных судов отказоустойчивость критична для обеспечения бесперебойной работы систем обнаружения, навигации и управления. Например, в системах распознавания объектов, таких как YOLOv8, отказоустойчивость помогает сохранять точность и стабильность работы при возможных сбоях сенсоров или вычислительных модулей.

**Связанные термины:**

- Надежность
- Резервирование
- Обработка ошибок
- Автономность
- Системы обнаружения

**Примеры использования:**

- Использование резервных сенсоров для поддержания работы системы при отказе основного датчика.
- Применение алгоритмов обработки ошибок в модели YOLOv8 для устойчивости к шуму и потерям данных.

**Статьи по теме:**

- [Effectiveness of Attention Mechanisms in YOLOv8 for Maritime Vessel Detection](./papers/paper_0014_cro)

---

### Fuzzy Logic

**Определение:** Нечеткая логика — это метод обработки информации, основанный на многозначных логических значениях, позволяющий моделировать неопределенность и нечёткость в принятии решений.

**Definition (EN):** Fuzzy logic is an information processing method based on multi-valued logic, enabling the modeling of uncertainty and imprecision in decision-making.

**Контекст применения в MASS:**

В области морских автономных надводных судов (MASS) нечеткая логика применяется для локального планирования маршрутов и предотвращения столкновений, позволяя учитывать неопределённые и изменяющиеся условия окружающей среды и поведения других судов.

**Связанные термины:**

- автономное судно
- планирование маршрута
- принятие решений
- искусственный интеллект
- обработка неопределённости

**Примеры использования:**

- Использование нечеткой логики для оценки риска столкновения при изменении курса судна.
- Применение нечетких правил для адаптивного управления скоростью и направлением автономного судна в сложных морских условиях.

**Статьи по теме:**

- [Local Route Planning for Collision Avoidance of Maritime Autonomous Surface Ships in Compliance with COLREGs Rules](./papers/paper_0001_cro)

---

### Genetic Algorithm

**Определение:** Генетический алгоритм — это метод оптимизации и поиска решений, основанный на принципах естественного отбора и генетики, имитирующий процесс эволюции популяции возможных решений.

**Definition (EN):** A genetic algorithm is an optimization and search method inspired by natural selection and genetics, simulating the evolutionary process of a population of candidate solutions.

**Контекст применения в MASS:**

В области морских автономных надводных судов (MASS) генетические алгоритмы применяются для решения задач планирования маршрутов и предотвращения столкновений, обеспечивая эффективный поиск оптимальных путей движения в динамической и неопределённой среде.

**Связанные термины:**

- оптимизация
- эвристические методы
- планирование маршрута
- избежание столкновений
- динамическое программирование

**Примеры использования:**

- Использование генетического алгоритма для локального планирования маршрута с учётом препятствий и движущихся объектов.
- Применение генетического алгоритма для оптимизации параметров системы предотвращения столкновений в автономных судах.

**Статьи по теме:**

- [Local Route Planning for Collision Avoidance of Maritime Autonomous Surface Ships in Compliance with COLREGs Rules](./papers/paper_0001_cro)
- [SWOT ANALYSIS OF LEADING SAFETY INDICATORS FOR COLLISION AVOIDANCE OF MARITIME AUTONOMOUS SURFACE SHIPS](./papers/paper_0005_cro)
- [A Dynamic Programming Approach to Collision Avoidance of Autonomous Ships](./papers/paper_0006_cro)
- [A Dynamic Programming Approach to the Collision Avoidance of Autonomous Ships](./papers/paper_0011_cro)
- [Scenario-Based Sensor Selection for Autonomous Maritime Systems: A Multi-Criteria Analysis of Sensor Configurations for Situational Awareness](./papers/paper_0012_cro)
- [Improved DDPG algorithm-based path planning for unmanned surface vehicles](./papers/paper_0013_cro)
- [Deploying Efficient LLM Agents on Maritime Autonomous Surface Ships: Fine-Tuning, RAG, and Function Calling in a Mid-Size Model](./papers/paper_0015_cro)
- [Maritime Autonomous Surface Ships: Architecture for Autonomous Navigation Systems](./papers/paper_0016_cro)

---

### Knowledge Maps

**Определение:** Knowledge Maps — это структурированные визуальные представления знаний, которые отображают взаимосвязи между различными элементами информации в определённой области. Они помогают систематизировать и упорядочивать данные для облегчения понимания и принятия решений.

**Definition (EN):** Knowledge Maps are structured visual representations of knowledge that illustrate relationships between different information elements within a specific domain. They aid in organizing and systematizing data to facilitate understanding and decision-making.

**Контекст применения в MASS:**

В области морских автономных надводных судов (MASS) Knowledge Maps используются для интеграции и анализа ситуационно-зависимых данных, что позволяет улучшить осведомлённость о текущей обстановке и повысить эффективность автономного управления. Они помогают объединять разнородную информацию о морской среде, навигации и техническом состоянии судна для принятия обоснованных решений в реальном времени.

**Связанные термины:**

- Ситуационная осведомлённость
- Автономное управление
- Интеллектуальные системы
- Морская навигация
- Обработка данных

**Примеры использования:**

- Использование Knowledge Maps для визуализации угроз и рисков в зоне плавания MASS
- Применение Knowledge Maps для интеграции данных с различных сенсоров и систем судна в режиме реального времени

**Статьи по теме:**

- [Integrating-situation-aware-knowledge-maps.md](./papers/Integrating-situation-aware-knowledge-maps)

---

### Knowledge Representation

**Определение:** Представление знаний — это способ структурирования и организации информации для моделирования и понимания сложных ситуаций, обеспечивающий эффективный доступ и обработку данных. В контексте автономных систем это позволяет формализовать знания о морской обстановке и поведении судов.

**Definition (EN):** Knowledge representation is the method of structuring and organizing information to model and understand complex situations, enabling efficient data access and processing. In autonomous systems, it formalizes knowledge about the maritime environment and vessel behavior.

**Контекст применения в MASS:**

В морских автономных надводных судах (MASS) представление знаний используется для создания карт знаний, которые повышают ситуационную осведомленность и безопасность навигации. Это позволяет интегрировать данные с различных сенсоров и алгоритмов, таких как методы обнаружения судов и планирования траекторий, для принятия обоснованных решений в реальном времени.

**Связанные термины:**

- Ситуационная осведомленность
- Карта знаний
- Обнаружение объектов
- Планирование траектории
- Машинное обучение

**Примеры использования:**

- Использование карт знаний для оценки морской обстановки в реальном времени
- Интеграция представления знаний с алгоритмами обнаружения судов на основе YOLOv8

**Статьи по теме:**

- [Constructing Knowledge Maps for Situation Awareness of Maritime Autonomous Surface Ships](./papers/paper_0008_cro)
- [Integrating situation-aware knowledge maps and dynamic window approach for safe path planning by maritime autonomous surface ships](./papers/paper_0010_cro)
- [Effectiveness of Attention Mechanisms in YOLOv8 for Maritime Vessel Detection](./papers/paper_0014_cro)
- [Deploying Efficient LLM Agents on Maritime Autonomous Surface Ships: Fine-Tuning, RAG, and Function Calling in a Mid-Size Model](./papers/paper_0015_cro)

---

### MASS

**Определение:** MASS (морские автономные надводные суда) — это суда, способные выполнять навигацию и операции без постоянного участия человека на борту, используя автоматизированные системы управления и сенсоры.

**Definition (EN):** MASS (Maritime Autonomous Surface Ships) are vessels capable of navigating and operating without continuous human intervention on board, utilizing automated control systems and sensors.

**Контекст применения в MASS:**

В области MASS основное внимание уделяется разработке алгоритмов автономного управления, включая планирование маршрутов и предотвращение столкновений. Такие суда применяются для повышения безопасности, эффективности и снижения затрат в морской навигации. В научных исследованиях часто рассматриваются методы машинного обучения и алгоритмы динамического окна для обеспечения безопасного движения MASS.

**Связанные термины:**

- автономное управление
- система предотвращения столкновений
- планирование маршрута
- глубокое обучение
- динамическое окно
- сенсорные системы

**Примеры использования:**

- Local Route Planning for Collision Avoidance of Maritime Autonomous Surface Ship
- Collision avoidance on maritime autonomous surface ships
- Deep reinforcement learning with dynamic window approach based collision avoidance

**Статьи по теме:**

- [Local Route Planning for Collision Avoidance of Maritime Autonomous Surface Ships in Compliance with COLREGs Rules](./papers/paper_0001_cro)
- [Collision avoidance on maritime autonomous surface ships](./papers/paper_0003_cro)
- [Deep reinforcement learning with dynamic window approach based collision avoidance path planning for maritime autonomous surface ships](./papers/paper_0004_cro)
- [SWOT ANALYSIS OF LEADING SAFETY INDICATORS FOR COLLISION AVOIDANCE OF MARITIME AUTONOMOUS SURFACE SHIPS](./papers/paper_0005_cro)
- [Constructing Knowledge Maps for Situation Awareness of Maritime Autonomous Surface Ships](./papers/paper_0008_cro)
- [Collaborative collision avoidance for Maritime Autonomous Surface Ships: A review](./papers/paper_0009_cro)
- [Integrating situation-aware knowledge maps and dynamic window approach for safe path planning by maritime autonomous surface ships](./papers/paper_0010_cro)
- [Deploying Efficient LLM Agents on Maritime Autonomous Surface Ships: Fine-Tuning, RAG, and Function Calling in a Mid-Size Model](./papers/paper_0015_cro)
- [Maritime Autonomous Surface Ships: Architecture for Autonomous Navigation Systems](./papers/paper_0016_cro)

---

### Navigation

**Определение:** Навигация — это процесс определения и поддержания курса судна для безопасного и эффективного перемещения по водной поверхности. Она включает сбор, обработку и использование информации о положении, маршруте и окружающей обстановке.

**Definition (EN):** Navigation is the process of determining and maintaining a vessel's course for safe and efficient movement over water. It involves collecting, processing, and utilizing information about position, route, and the surrounding environment.

**Контекст применения в MASS:**

В контексте морских автономных надводных судов (MASS) навигация играет ключевую роль в обеспечении автономного управления и принятия решений. Используются интегрированные системы, учитывающие ситуацию и знания для адаптивного планирования маршрута и предотвращения столкновений.

**Связанные термины:**

- автономное управление
- ситуационная осведомленность
- маршрутизация
- сенсоры
- обработка данных

**Примеры использования:**

- Автономное судно корректирует курс на основе данных навигационной системы.
- Система навигации интегрируется с картами знаний для повышения безопасности движения.

**Статьи по теме:**

- [Integrating-situation-aware-knowledge-maps.md](./papers/Integrating-situation-aware-knowledge-maps)

---

### Obstacle Avoidance

**Определение:** Обход препятствий — это процесс обнаружения и маневрирования вокруг объектов или опасностей на пути автономного надводного судна для предотвращения столкновений. Он включает в себя планирование маршрута и принятие решений в реальном времени с учетом динамической обстановки.

**Definition (EN):** Obstacle avoidance is the process of detecting and maneuvering around objects or hazards in the path of an autonomous surface vessel to prevent collisions. It involves route planning and real-time decision-making considering dynamic environments.

**Контекст применения в MASS:**

В области морских автономных надводных судов (MASS) обход препятствий является ключевой задачей для обеспечения безопасности навигации. Алгоритмы обхода препятствий интегрируются с системами планирования маршрута и управления движением, позволяя автономным судам адаптироваться к изменяющимся условиям и избегать столкновений с другими судами, буями и природными объектами.

**Связанные термины:**

- [Collision Avoidance](#collision-avoidance)
- [Path Planning](#path-planning)
- Dynamic Programming
- Autonomous Navigation
- [Sensor Fusion](#sensor-fusion)

**Примеры использования:**

- Использование алгоритма динамического программирования для обхода препятствий на автономном судне
- Применение улучшенного DDPG-алгоритма для планирования пути с учетом обхода препятствий у беспилотных надводных судов

**Статьи по теме:**

- [A Dynamic Programming Approach to Collision Avoidance of Autonomous Ships](./papers/paper_0006_cro)
- [A Dynamic Programming Approach to the Collision Avoidance of Autonomous Ships](./papers/paper_0011_cro)
- [Improved DDPG algorithm-based path planning for unmanned surface vehicles](./papers/paper_0013_cro)

---

### Optimization Algorithm

**Определение:** Оптимизационный алгоритм — это метод или набор правил, используемых для поиска наилучшего решения задачи среди множества возможных вариантов с целью максимизации или минимизации заданной функции.

**Definition (EN):** An optimization algorithm is a method or set of rules used to find the best solution to a problem among many possible options, aiming to maximize or minimize a given function.

**Контекст применения в MASS:**

В области морских автономных надводных судов (MASS) оптимизационные алгоритмы применяются для улучшения работы систем обнаружения и классификации объектов, таких как алгоритмы внимания в YOLOv8, что повышает точность и эффективность распознавания морских судов в сложных условиях.

**Связанные термины:**

- машинное обучение
- нейронные сети
- алгоритмы внимания
- обнаружение объектов
- автономные системы

**Примеры использования:**

- Оптимизация параметров модели YOLOv8 для повышения точности обнаружения судов
- Использование алгоритмов оптимизации для настройки систем автономного управления MASS

**Статьи по теме:**

- [Effectiveness of Attention Mechanisms in YOLOv8 for Maritime Vessel Detection](./papers/paper_0014_cro)

---

### Path Planning

**Определение:** Планирование пути (Path Planning) — процесс определения оптимального маршрута движения автономного надводного судна с учётом ограничений и препятствий для обеспечения безопасного и эффективного плавания.

**Definition (EN):** Path Planning is the process of determining an optimal navigation route for an autonomous surface vessel, considering constraints and obstacles to ensure safe and efficient travel.

**Контекст применения в MASS:**

В области морских автономных надводных судов планирование пути используется для локального и глобального построения маршрутов, позволяя избегать столкновений с другими судами и препятствиями. Методы планирования пути часто интегрируются с системами обнаружения и оценки ситуации, а также с алгоритмами управления движением, такими как динамическое окно и методы глубокого обучения.

**Связанные термины:**

- [Collision Avoidance](#collision-avoidance)
- [Dynamic Window Approach](#dynamic-window-approach)
- Autonomous Navigation
- Obstacle Detection
- [Reinforcement Learning](#reinforcement-learning)

**Примеры использования:**

- Локальное планирование маршрута для предотвращения столкновений с другими судами.
- Использование глубокого обучения совместно с динамическим окном для адаптивного изменения пути в реальном времени.

**Статьи по теме:**

- [Local Route Planning for Collision Avoidance of Maritime Autonomous Surface Ships in Compliance with COLREGs Rules](./papers/paper_0001_cro)
- [Deep reinforcement learning with dynamic window approach based collision avoidance path planning for maritime autonomous surface ships](./papers/paper_0004_cro)
- [Integrating situation-aware knowledge maps and dynamic window approach for safe path planning by maritime autonomous surface ships](./papers/paper_0010_cro)
- [Improved DDPG algorithm-based path planning for unmanned surface vehicles](./papers/paper_0013_cro)

---

### Perception

**Определение:** Восприятие — это процесс сбора и обработки данных с сенсоров для формирования представления об окружающей морской обстановке автономным надводным судном.

**Definition (EN):** Perception is the process of collecting and processing sensor data to create an understanding of the surrounding maritime environment for an autonomous surface vessel.

**Контекст применения в MASS:**

В MASS восприятие играет ключевую роль в обеспечении безопасной навигации и принятия решений, позволяя системе обнаруживать, классифицировать и отслеживать объекты на воде. Используются различные сенсоры и алгоритмы, включая методы компьютерного зрения и машинного обучения, для повышения точности и надежности восприятия в сложных морских условиях.

**Связанные термины:**

- сенсоры
- обнаружение объектов
- классификация
- обработка данных
- автономная навигация
- машинное обучение
- компьютерное зрение

**Примеры использования:**

- Использование YOLOv8 для обнаружения морских судов в режиме реального времени
- Выбор сенсоров на основе сценариев для оптимизации восприятия в различных условиях

**Статьи по теме:**

- [Scenario-Based Sensor Selection for Autonomous Maritime Systems: A Multi-Criteria Analysis of Sensor Configurations for Situational Awareness](./papers/paper_0012_cro)
- [Effectiveness of Attention Mechanisms in YOLOv8 for Maritime Vessel Detection](./papers/paper_0014_cro)
- [Maritime Autonomous Surface Ships: Architecture for Autonomous Navigation Systems](./papers/paper_0016_cro)

---

### Reinforcement Learning

**Определение:** Обучение с подкреплением — это метод машинного обучения, при котором агент учится принимать решения, максимизируя суммарное вознаграждение через взаимодействие с окружающей средой.

**Definition (EN):** Reinforcement learning is a machine learning approach where an agent learns to make decisions by maximizing cumulative rewards through interaction with the environment.

**Контекст применения в MASS:**

В области морских автономных надводных судов (MASS) обучение с подкреплением применяется для разработки алгоритмов автономного управления, таких как планирование маршрутов и избегание столкновений. Использование методов глубокого обучения с подкреплением позволяет улучшить адаптивность и эффективность навигационных систем в динамичных морских условиях.

**Связанные термины:**

- глубокое обучение
- DDPG
- планирование маршрута
- избегание столкновений
- агент
- вознаграждение

**Примеры использования:**

- Deep reinforcement learning with dynamic window approach based collision avoidance для предотвращения столкновений судов.
- Improved DDPG algorithm-based path planning для оптимизации маршрутов автономных надводных судов.

**Статьи по теме:**

- [Deep reinforcement learning with dynamic window approach based collision avoidance path planning for maritime autonomous surface ships](./papers/paper_0004_cro)
- [Improved DDPG algorithm-based path planning for unmanned surface vehicles](./papers/paper_0013_cro)

---

### Safety

**Определение:** Safety — состояние защищённости судна, экипажа и окружающей среды от аварий, повреждений и опасных ситуаций во время эксплуатации морских автономных надводных судов.

**Definition (EN):** Safety is the condition of being protected from accidents, damage, and hazardous situations during the operation of maritime autonomous surface ships.

**Контекст применения в MASS:**

В области MASS безопасность включает предотвращение столкновений, обеспечение надежного функционирования систем автономного управления и минимизацию рисков для судна и окружающей среды. Это ключевой аспект при разработке алгоритмов локального планирования маршрутов и оценки показателей безопасности для предотвращения аварийных ситуаций.

**Связанные термины:**

- [Collision Avoidance](#collision-avoidance)
- Risk Assessment
- Autonomous Navigation
- Safety Indicators
- Route Planning

**Примеры использования:**

- Использование локального планирования маршрутов для повышения безопасности при автономном движении судна.
- Анализ ведущих показателей безопасности для предотвращения столкновений в системах MASS.

**Статьи по теме:**

- [Local Route Planning for Collision Avoidance of Maritime Autonomous Surface Ships in Compliance with COLREGs Rules](./papers/paper_0001_cro)
- [SWOT ANALYSIS OF LEADING SAFETY INDICATORS FOR COLLISION AVOIDANCE OF MARITIME AUTONOMOUS SURFACE SHIPS](./papers/paper_0005_cro)

---

### Sensor Fusion

**Определение:** Sensor Fusion — это процесс объединения данных с нескольких сенсоров для получения более точной и надежной информации о внешней среде. Он позволяет компенсировать ограничения отдельных датчиков и улучшать качество восприятия.

**Definition (EN):** Sensor Fusion is the process of combining data from multiple sensors to obtain more accurate and reliable information about the environment. It helps to compensate for individual sensor limitations and enhances perception quality.

**Контекст применения в MASS:**

В системах автономных морских надводных судов Sensor Fusion используется для интеграции данных с радаров, лидаров, камер и других сенсоров, обеспечивая надежное обнаружение и классификацию объектов, а также повышение безопасности навигации. Это критически важно для принятия решений в реальном времени в сложных морских условиях.

**Связанные термины:**

- радар
- лидар
- автономная навигация
- обработка данных
- мультисенсорная интеграция

**Примеры использования:**

- Объединение данных радаров и лидаров для точного определения положения других судов
- Использование Sensor Fusion для улучшения обнаружения препятствий в условиях плохой видимости

**Статьи по теме:**

- [Maritime Autonomous Surface Ships: Architecture for Autonomous Navigation Systems](./papers/paper_0016_cro)

---

### Simulation

**Определение:** Симуляция — это процесс создания и использования компьютерных моделей для имитации поведения морских автономных надводных судов в различных условиях и сценариях. Она позволяет тестировать алгоритмы управления и навигации без необходимости физического запуска судна.

**Definition (EN):** Simulation is the process of creating and using computer models to imitate the behavior of maritime autonomous surface ships under various conditions and scenarios. It enables testing of control and navigation algorithms without the need for physical deployment.

**Контекст применения в MASS:**

В области морских автономных надводных судов симуляция применяется для разработки и проверки алгоритмов планирования маршрута, таких как улучшенный алгоритм DDPG, позволяющий оптимизировать движение беспилотных судов. Это снижает риски и затраты, связанные с экспериментами в реальных условиях.

**Связанные термины:**

- DDPG алгоритм
- планирование маршрута
- автономное управление
- моделирование
- тестирование алгоритмов

**Примеры использования:**

- Использование симуляции для проверки алгоритма планирования пути беспилотного судна.
- Моделирование взаимодействия нескольких автономных надводных судов в сложных морских условиях.

**Статьи по теме:**

- [Improved DDPG algorithm-based path planning for unmanned surface vehicles](./papers/paper_0013_cro)

---

### Situational Awareness

**Определение:** Situational Awareness — это осознание текущей обстановки и динамики окружающей среды, включая состояние судна, другие объекты и потенциальные риски, необходимое для принятия эффективных решений в управлении автономным судном.

**Definition (EN):** Situational Awareness is the perception and understanding of the current environment and its dynamics, including the status of the vessel, other objects, and potential hazards, essential for effective decision-making in autonomous vessel operations.

**Контекст применения в MASS:**

В области морских автономных надводных судов (MASS) situational awareness играет ключевую роль в обеспечении безопасности и эффективности навигации. Она достигается посредством интеграции данных с различных сенсоров и построения знаний о морской обстановке, что позволяет автономным системам адаптироваться к изменяющимся условиям и предотвращать аварийные ситуации.

**Связанные термины:**

- Автономная навигация
- Сенсорные системы
- Обработка данных
- Принятие решений
- Карта знаний

**Примеры использования:**

- Использование knowledge maps для улучшения situational awareness в автономных судах.
- Выбор сенсоров на основе сценариев для повышения situational awareness в морских автономных системах.

**Статьи по теме:**

- [Integrating-situation-aware-knowledge-maps.md](./papers/Integrating-situation-aware-knowledge-maps)
- [Constructing Knowledge Maps for Situation Awareness of Maritime Autonomous Surface Ships](./papers/paper_0008_cro)
- [Scenario-Based Sensor Selection for Autonomous Maritime Systems: A Multi-Criteria Analysis of Sensor Configurations for Situational Awareness](./papers/paper_0012_cro)
- [Maritime Autonomous Surface Ships: Architecture for Autonomous Navigation Systems](./papers/paper_0016_cro)

---

### Testing

**Определение:** Тестирование — процесс проверки и оценки работы систем и компонентов автономных надводных судов для обеспечения их надежности и безопасности. Включает в себя проверку алгоритмов, сенсоров и программного обеспечения в различных условиях.

**Definition (EN):** Testing is the process of verifying and evaluating the performance of systems and components of autonomous surface vessels to ensure their reliability and safety. It includes checking algorithms, sensors, and software under various conditions.

**Контекст применения в MASS:**

В области MASS тестирование применяется для оценки эффективности алгоритмов обнаружения объектов, таких как системы компьютерного зрения на базе YOLOv8, а также для проверки взаимодействия различных подсистем судна в реальных и симулированных морских условиях. Это позволяет выявлять и устранять ошибки до внедрения в эксплуатацию.

**Связанные термины:**

- автономность
- детекция объектов
- алгоритмы машинного обучения
- сенсоры
- верификация
- валидация

**Примеры использования:**

- Тестирование модели YOLOv8 для обнаружения морских судов в условиях различной освещенности.
- Полевое тестирование автономного судна для проверки работы навигационных систем.

**Статьи по теме:**

- [Effectiveness of Attention Mechanisms in YOLOv8 for Maritime Vessel Detection](./papers/paper_0014_cro)

---

### Trajectory Planning

**Определение:** Планирование траектории — процесс определения оптимального пути движения автономного надводного судна с учётом динамических ограничений и препятствий. Оно обеспечивает безопасное и эффективное перемещение судна в заданной среде.

**Definition (EN):** Trajectory planning is the process of determining an optimal path for an autonomous surface vessel considering dynamic constraints and obstacles. It ensures safe and efficient navigation within the operational environment.

**Контекст применения в MASS:**

В области морских автономных надводных судов (MASS) планирование траектории используется для обеспечения безопасного обхода препятствий и адаптации к изменяющимся условиям окружающей среды. Современные методы, такие как глубокое обучение с подкреплением и алгоритмы динамического окна, применяются для улучшения качества и надёжности траекторий.

**Связанные термины:**

- [Collision Avoidance](#collision-avoidance)
- [Dynamic Window Approach](#dynamic-window-approach)
- [Path Planning](#path-planning)
- [Deep Reinforcement Learning](#deep-reinforcement-learning)
- Unmanned Surface Vehicles

**Примеры использования:**

- Использование алгоритма DDPG для улучшенного планирования траектории беспилотного судна
- Применение динамического окна для предотвращения столкновений при построении траектории

**Статьи по теме:**

- [Deep reinforcement learning with dynamic window approach based collision avoidance path planning for maritime autonomous surface ships](./papers/paper_0004_cro)
- [Integrating situation-aware knowledge maps and dynamic window approach for safe path planning by maritime autonomous surface ships](./papers/paper_0010_cro)
- [Improved DDPG algorithm-based path planning for unmanned surface vehicles](./papers/paper_0013_cro)

---

### User Interface

**Определение:** Пользовательский интерфейс (User Interface) — это совокупность средств и методов взаимодействия человека с системой управления автономным надводным судном, обеспечивающая ввод команд и получение информации о состоянии судна и окружающей среды.

**Definition (EN):** User Interface is the set of tools and methods enabling human interaction with the autonomous surface vessel's control system, allowing command input and feedback on the vessel's status and environment.

**Контекст применения в MASS:**

В области морских автономных надводных судов пользовательский интерфейс играет ключевую роль в обеспечении безопасного и эффективного управления, особенно при реализации систем предотвращения столкновений. Он позволяет оператору контролировать и корректировать действия судна, а также получать важные данные о навигационной обстановке и предупреждениях безопасности.

**Связанные термины:**

- автономное судно
- система предотвращения столкновений
- человеко-машинный интерфейс
- система управления
- навигационные данные

**Примеры использования:**

- Интерфейс оператора для мониторинга и управления маневрами судна при обходе препятствий
- Визуализация предупреждений о рисках столкновения на экране пользователя

**Статьи по теме:**

- [SWOT ANALYSIS OF LEADING SAFETY INDICATORS FOR COLLISION AVOIDANCE OF MARITIME AUTONOMOUS SURFACE SHIPS](./papers/paper_0005_cro)
- [A Dynamic Programming Approach to Collision Avoidance of Autonomous Ships](./papers/paper_0006_cro)
- [A Dynamic Programming Approach to the Collision Avoidance of Autonomous Ships](./papers/paper_0011_cro)
- [Scenario-Based Sensor Selection for Autonomous Maritime Systems: A Multi-Criteria Analysis of Sensor Configurations for Situational Awareness](./papers/paper_0012_cro)
- [Effectiveness of Attention Mechanisms in YOLOv8 for Maritime Vessel Detection](./papers/paper_0014_cro)
- [Deploying Efficient LLM Agents on Maritime Autonomous Surface Ships: Fine-Tuning, RAG, and Function Calling in a Mid-Size Model](./papers/paper_0015_cro)
