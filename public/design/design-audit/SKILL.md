---
name: design-audit
description: "Комплексный фреймворк аудита дизайна, UX и Agentic Experience Design (AXD) от Owl-Listener. Включает 42 специализированных навыка по 6 направлениям: evaluation (эвристическая оценка Нильсена, аудит доступности WCAG, дизайн-критика, UX scorecard, бенчмаркинг), model-interaction-design (паттерны генеративного UI, адаптивное раскрытие, обнаружение фрустрации, циклы обратной связи), system-behavior-shaping (калибровка тональности, архитектура персоны, эмоциональный дизайн), alignment, orchestration и prompt-architecture. Используйте при проведении детального аудита интерфейсов, проектировании AI-взаимодействий и устранении эргономических дефектов."
---

# 🔍 Agentic Experience Design & Design Audit Suite

Комплексный академически выверенный фреймворк для аудита интерфейсов, эргономики и Agentic Experience Design (AXD) от Owl-Listener. Объединяет классические методики человеко-ориентированного дизайна (HCI) с новейшими практиками агентных и генеративных систем.

---

## 🧭 Структура библиотеки (6 направлений, 42 навыка)

### 1. 📊 Оценка и аудит (Evaluation & Quality Gate)
`skills/evaluation/`
- **`design-critique`**: Структурированный разбор композиции, иерархии, ритма и акцентов.
- **`heuristic-evaluation`**: Проверка по 10 классическим эвристикам Якоба Нильсена с адаптацией под современные веб-приложения.
- **`accessibility-audit`**: Проверка соответствия стандартам WCAG 2.1/2.2 AA (контрастность, экранные дикторы, фокус клавиатуры).
- **`ux-scorecard`**: Матрица оценки пользовательского опыта с числовыми метриками (Task Success, SUS, Cognitive Load).
- **`benchmarking`**: Сравнительный анализ интерфейса с лидерами рынка и прямыми аналогами.
- **`telemetry-design`** и **`user-testing`**: Проектирование воронки UX-метрик и сценариев тестирования.

### 2. 🤝 Проектирование взаимодействия с моделями (Model Interaction Design)
`skills/model-interaction-design/`
- **`generative-ui`**: Потоковая генерация адаптивных интерфейсов в реальном времени.
- **`progressive-disclosure`**: Постепенное раскрытие информации без перегрузки пользователя.
- **`frustration-detection`**: Распознавание признаков замешательства или недовольства пользователя и адаптация сценария.
- **`feedback-loops`**: Быстрые и ненавязчивые механизмы обратной связи.
- **`mixed-initiative-flow`**: Баланс автономности системы и пользовательского контроля.

### 3. 🎭 Формирование поведения и тональности (System Behavior Shaping)
`skills/system-behavior-shaping/`
- **`tone-calibration`**: Подстройка тона общения под контекст задачи и психологическое состояние пользователя.
- **`error-personality`**: Человечный, конструктивный и полезный UX сообщений об ошибках.
- **`behavioral-consistency`**: Предсказуемость и надежность ответов системы.
- **`cultural-adaptation`** и **`persona-architecture`**: Адаптация под культурный контекст и профиль роли.

### 4. 🧠 Выравнивание, Оркестрация и Архитектура промптов
- **`ai-alignment-reasoning`**: Оценка безопасности, этики и устойчивости к манипуляциям.
- **`design-agent-orchestration`**: Координация многоагентных дизайн-процессов (Scout, Critic, Builder).
- **`prompt-architecture`**: Структурирование системных и компонентных инструкций.

---

## 💡 Как запустить аудит

Для проведения комплексной проверки интерфейса обратитесь к модулям оценки:
```
skills/public/design/design-audit/skills/evaluation/heuristic-evaluation/SKILL.md
skills/public/design/design-audit/skills/evaluation/accessibility-audit/SKILL.md
skills/public/design/design-audit/skills/evaluation/design-critique/SKILL.md
```
