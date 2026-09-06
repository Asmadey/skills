---
description: Официальный реестр навыков библиотеки PersonalOS (skills). Каталог сгруппирован по 13 категориям.
created: 2026-08-30
last_updated: 2026-09-06
---

# 🧠 Каталог навыков PersonalOS (skills)

Центральный реестр всех активных навыков (79 навыков) проекта PersonalOS. Библиотека организована по трехуровневой архитектуре L1-L3 и разделена на 13 категорий.

> 💡 Полная хронология добавлений, удалений и обновлений версий задокументирована в [changelog.md](changelog.md).

---

## 📌 Быстрая навигация по категориям

- [🛠 Разработка, Качество кода и MCP (Development & Engineering)](#dev)
- [🤖 Автоматизация, Воркфлоу и Браузер (Automation & Agents)](#automation)
- [📦 Продуктовый менеджмент и PRD (Product Management)](#product)
- [✍️ Тексты, Редактура и Humanizing (Writing & Anti-Slop)](#writing)
- [🎨 UI/UX и Дизайн-системы (Design & UI/UX)](#ux)
- [✨ Анимации, Графика и Стили (Motion & Visuals)](#design)
- [⚙️ Операционные задачи и Делегация (Operations & Tasks)](#ops)
- [💼 Бизнес, Стратегия и Продажи (Business & Strategy)](#business)
- [📈 Маркетинг, SEO и Аналитика (Marketing & SEO)](#marketing)
- [🔬 Исследования, Анализ и SOTA (Research & Intelligence)](#research)
- [👤 Личная продуктивность и База знаний (Personal & PKM)](#personal)
- [🧠 ИИ-оптимизация и Безопасность (AI Core & Context)](#ai)
- [🏗 Мета-навыки и Аудит (Skill Engineering & Operations)](#skill-ops)

---

## <a id="dev"></a>🛠 Разработка, Качество кода и MCP (Development & Engineering)

| Навык | Назначение | Триггеры вызова | Стек | Документация |
| :--- | :--- | :--- | :--- | :--- |
| **adhd** | **Parallel Divergent Ideation**.<br>Параллельное исследование инженерных решений под 5 когнитивными фреймами (Biology, Speedrunner, Regulator, 10yo, $0 budget), отсеивание ловушек и углубление архитектурных гипотез | `/adhd, «ADHD mode», дивергентное мышление, брейншторм архитектуры, поиск неочевидных решений` | Node/CLI | [SKILL.md](skills/dev/adhd/SKILL.md) |
| **ai-software-factory** | **Autonomous Dark Factory**.<br>Беспилотный конвейер разработки: Issue → Mission → Plan → Build → Judge → Holdout E2E → Auto-Merge | `«software factory», «dark factory», автоматический конвейер разработки` | Python / CLI | [SKILL.md](frameworks/ai-software-factory/SKILL.md) |
| **code-reviewer** | **Total Review Engine**.<br>Двухпроходный аудит кода (Архитектура/Логика + Безопасность/NFR) с фильтрацией оверсинкинга и консенсусом | `/total-review, ревью кода, проверка PR, code review` | Prompt | [SKILL.md](skills/dev/code-reviewer/SKILL.md) |
| **codex-plugin-cc** | **OpenAI Codex CLI Suite**.<br>Оркестрация Codex CLI, headless сессии выполнения, валидация диффов и паттерны reasoning для GPT-5.4 | `делегирование в Codex, запуск codex cli, gpt-5.4 reasoning` | Node/CLI | [SKILL.md](skills/dev/codex-plugin-cc/SKILL.md) |
| **diy-mcp-connector** | **MCP Generator**.<br>Автоматическое создание локальных MCP-серверов под любые веб-сайты через анализ HAR/CDP | `создание кастомного MCP-сервера, интеграция сервисов без API` | Python / Node/CLI | [SKILL.md](skills/dev/diy-mcp-connector/SKILL.md) |
| **git-worktree** | **Git Worktree Manager**.<br>Управление изолированными параллельными рабочими ветками без переключения git stash | `параллельная разработка нескольких фич, работа в worktree` | Prompt | [SKILL.md](skills/dev/git-worktree/SKILL.md) |
| **gnhf** | **Autonomous Agent Orchestrator**.<br>Оркестратор длительных ночных прогонов агентов до естественного stop condition (Hands-Off и Companion режимы) | `«gnhf», «я спать / ушел, доделай ветку», супервизия автономного прогона` | Node/CLI | [SKILL.md](skills/dev/gnhf/SKILL.md) |
| **magicui** | **Animated UI Library**.<br>Коллекция интерактивных компонентов и эффектов на React/Next.js (marquee, globe, particles) | `анимированные лендинги, интерактивные React-компоненты` | Node/CLI | [SKILL.md](skills/dev/magicui/SKILL.md) |
| **mobile** | **Mobile Design Master Hub**.<br>Хаб проектирования мобильных приложений: UX-потоки Airbnb/Revolut + Google Material 3 | `мобильный UI/UX, iOS/Android экраны, Material You` | Node/CLI | [SKILL.md](skills/dev/mobile/SKILL.md) |
| **no-mistakes** | **Pre-Commit Gate & Code Quality**.<br>Локальный гейт-прокси, линтинг, статический анализ и валидация кода без ошибок перед сдачей | `проверка кода перед коммитом, валидация правок, no-mistakes` | Prompt | [SKILL.md](skills/dev/no-mistakes/SKILL.md) |
| **open-graph** | **Technical SEO & OG Meta**.<br>Генерация динамических Open Graph тегов, изображений и метаданных для поисковиков | `настройка соцсетей, превью ссылок, Open Graph, meta-теги` | Prompt | [SKILL.md](skills/dev/open-graph/SKILL.md) |
| **react-native-skills** | **React Native / Expo Standards**.<br>Лучшие практики и паттерны оптимизации производительности мобильных приложений React Native/Expo | `разработка мобильных приложений, Expo, React Native` | Node/CLI | [SKILL.md](skills/dev/react-native-skills/SKILL.md) |
| **sgr-core** | **SGR Agent Core**.<br>Фреймворк построения интеллектуальных исследовательских и reasoning-агентов | `сложная агентная логика, многоагентные системы, SGR` | Prompt | [SKILL.md](skills/dev/sgr-core/SKILL.md) |
| **shadcn** | **shadcn/ui Manager**.<br>Официальный менеджер компонентов shadcn/ui, пресеты, формы и токены Tailwind CSS | `добавление компонентов shadcn, components.json, стилизация` | Node/CLI | [SKILL.md](skills/dev/shadcn/SKILL.md) |
| **unlazy** | **Completion Discipline & Acceptance Gates**.<br>Устранение недоделок и лени ИИ: построение дерева задач Depth Tree, генерация acceptance gates (GATES.md) до исполнения, изоляция файлов и строгая повторная верификация доказательств | `/unlazy, $unlazy, «не останавливайся пока не готово», «tree N», «gates», защита от лени ИИ` | Node/CLI | [SKILL.md](skills/dev/unlazy/SKILL.md) |
| **supabase** | **Supabase & Postgres Suite**.<br>Официальный пакет навыков Supabase: база данных, Auth, RLS-политики, Edge Functions, Storage, лучшие практики PostgreSQL | `Supabase, настройка RLS, оптимизация PostgreSQL, миграции, Auth` | Node/CLI | [SKILL.md](skills/dev/supabase/SKILL.md) |
| **vercel-automation** | **Vercel Automation MCP**.<br>Управление деплоями, доменами, проектами и окружениями на Vercel через MCP | `деплой на Vercel, управление проектами, DNS-записи` | Prompt | [SKILL.md](skills/dev/vercel-automation/SKILL.md) |

---

## <a id="automation"></a>🤖 Автоматизация, Воркфлоу и Браузер (Automation & Agents)

| Навык | Назначение | Триггеры вызова | Стек | Документация |
| :--- | :--- | :--- | :--- | :--- |
| **Browser-automation** | **Headless Browser CLI & Proxy**.<br>Высокоскоростное управление браузером по CDP (скриншоты, клики, доступность, парсинг) | `автоматизация браузера, тестирование, скрейпинг страниц` | Node/CLI | [SKILL.md](skills/automation/Browser-automation/SKILL.md) |
| **googlesheets-automation** | **Google Sheets Manager**.<br>Чтение, запись, форматирование и фильтрация таблиц Google Sheets через API | `автоматизация Google Таблиц, выгрузка отчетов, синхронизация данных` | Prompt | [SKILL.md](skills/automation/googlesheets-automation/SKILL.md) |
| **linear-automation** | **Linear Automation MCP**.<br>Управление задачами, проектами, спринтами и циклами Linear через MCP | `создание задач в Linear, трекинг тикетов, управление бэклогом` | Prompt | [SKILL.md](skills/automation/linear-automation/SKILL.md) |
| **modal-cloud** | **Modal Cloud Compute**.<br>Платформа бессерверных облачных вычислений на Python (GPU, контейнеры, ML-воркеры) | `запуск тяжелых вычислений, ML инференс, фоновые воркеры` | Python | [SKILL.md](skills/automation/modal-cloud/SKILL.md) |
| **n8n-architect** | **n8n Workflow Architect**.<br>Проектирование, валидация, траблшутинг и деплой сценариев автоматизации n8n | `создание/редактирование n8n воркфлоу, n8n automation` | Prompt | [SKILL.md](skills/automation/n8n-architect/SKILL.md) |
| **n8n-as-code** | **n8n-as-Code Engine**.<br>Разработка и синхронизация n8n сценариев в формате JSON-кода из репозитория | `экспорт/импорт сценариев n8n, версионирование автоматизаций` | Node/CLI | [SKILL.md](skills/automation/n8n-as-code/SKILL.md) |
| **n8n-official** | **Official n8n Knowledge Suite**.<br>Полная база знаний по всем 14 аспектам n8n (узлы, циклы, код, агенты, обработка ошибок) | `любые вопросы по узлам n8n, выражениям, Code Node, Subworkflows` | Node/CLI | [SKILL.md](skills/automation/n8n-official/SKILL.md) |
| **second-brain** | **Second Brain / LLM Wiki**.<br>Управление персональной динамической базой знаний в Obsidian, синтез заметок | `синтез заметок, ведение wiki, связывание знаний` | Prompt | [SKILL.md](skills/automation/second-brain/SKILL.md) |
| **self-improving-workflow** | **Self-Improving Loop**.<br>Система непрерывного обучения и обратной связи для автоматизаций и процессов | `анализ сбоев, самообучение пайплайнов, улучшение процессов` | Python | [SKILL.md](skills/automation/self-improving-workflow/SKILL.md) |
| **xlsx** | **Spreadsheet Engine**.<br>Работа с таблицами Excel/XLSX: чтение, модификация данных, формулы, форматирование | `обработка excel-файлов, xlsx отчеты, парсинг таблиц` | Python | [SKILL.md](skills/automation/xlsx/SKILL.md) |

---

## <a id="product"></a>📦 Продуктовый менеджмент и PRD (Product Management)

| Навык | Назначение | Триггеры вызова | Стек | Документация |
| :--- | :--- | :--- | :--- | :--- |
| **AJTBD** | **Applied JTBD Framework**.<br>Глубокий анализ задач пользователей по методологии Jobs-To-Be-Done, микро-шаги и барьеры | `исследование JTBD, формулировка job stories, анализ барьеров` | Prompt | [SKILL.md](skills/product/AJTBD/SKILL.md) |
| **advise-project-approach** | **Tech Strategy & Stack Advisor**.<br>Анализ аналогов (comparables), выбор оптимального стека, архитектуры и оценка операционных затрат | `выбор стека, архитектурный подход, similar projects, stack selection, advise-project-approach` | Python | [SKILL.md](skills/product/advise-project-approach/SKILL.md) |
| **prd-taskmaster** | **Atlas Goal-to-Tasks Engine (v5.3.0)**.<br>Генерация полного валидированного PRD, декомпозиция в граф задач и оркестрация выполнения | `«PRD», «product requirements», «хочу создать проект», /atlas` | Python / Node/CLI | [SKILL.md](skills/product/prd-taskmaster/SKILL.md) |

---

## <a id="writing"></a>✍️ Тексты, Редактура и Humanizing (Writing & Anti-Slop)

| Навык | Назначение | Триггеры вызова | Стек | Документация |
| :--- | :--- | :--- | :--- | :--- |
| **humanizer-en** | **English Humanizer**.<br>Устранение маркеров ИИ-генерации для английских текстов на базе гайдлайнов Wikipedia | `очеловечить английский текст, humanize en, убрать AI-признаки` | Prompt | [SKILL.md](skills/writing/humanizer-en/SKILL.md) |
| **humanizer-ru** | **Russian Humanizer**.<br>Очеловечивание русскоязычных текстов, удаление канцелярита, штампов и водянистости ИИ | `«очеловечь текст», «убери следы нейросети», живой русский язык` | Python / Node/CLI | [SKILL.md](skills/writing/humanizer-ru/SKILL.md) |
| **simple-english** | **Simplified Technical English**.<br>Стандарт ASD-STE100: ясный, лаконичный английский без двусмысленности для документации | `написание README, API docs, документация для не-носителей языка` | Python / Node/CLI | [SKILL.md](skills/writing/simple-english/SKILL.md) |
| **slop-monster** | **De-Slop Multi-Pass Engine**.<br>4-шаговый пайплайн очистки от ИИ-клише: Lint (deslop.py) → Rewrite → Cleanse → Re-Lint | `/slopmonster, «де-слоп», чистка маркетинговых черновиков` | Python | [SKILL.md](skills/writing/slop-monster/SKILL.md) |

---

## <a id="ux"></a>🎨 UI/UX и Дизайн-системы (Design & UI/UX)

| Навык | Назначение | Триггеры вызова | Стек | Документация |
| :--- | :--- | :--- | :--- | :--- |
| **hallmark** | **Anti-AI-Slop Design Engine**.<br>Генерация нетривиальных UI/лендингов, аудит визуального стиля, устранение шаблонного ИИ-дизайна | `создание новых UI, редизайн, аудит интерфейса на AI-slop` | Node/CLI | [SKILL.md](skills/UX/hallmark/SKILL.md) |
| **ui-ux-pro-max** | **UI/UX Design Master Suite**.<br>Комплексное проектирование дизайн-систем, баннеров, слайдов и UI-компонентов | `дизайн сайтов, дизайн-системы, баннеры, презентации` | Python / Node/CLI | [SKILL.md](skills/UX/ui-ux-pro-max/SKILL.md) |

---

## <a id="design"></a>✨ Анимации, Графика и Стили (Motion & Visuals)

| Навык | Назначение | Триггеры вызова | Стек | Документация |
| :--- | :--- | :--- | :--- | :--- |
| **GSAP** | **Motion & Animation Suite**.<br>Профессиональная библиотека анимаций: ScrollTrigger, Flip, MorphSVG, 60fps оптимизация | `сложные анимации, скролл-эффекты, интерактивный фронтенд` | Node/CLI | [SKILL.md](skills/design/GSAP/SKILL.md) |
| **awesome-design-skills** | **Каталог 67 Дизайн-систем**.<br>Готовые токены, палитры и стили (Bento, Brutalism, Glassmorphism, Retro, Futuristic и др.) | `выбор визуального стиля фронтенда, стилизация под конкретный тренд` | Node/CLI | [SKILL.md](skills/design/awesome-design-skills/SKILL.md) |
| **better-interface** | **Interface Inspector & Reviewer**.<br>Комплексный аудит и исправление дефектов UI от Jakub Krehel: доступность, верстка, типографика, цвета, стресс-тест состояний (`break`), генерация вариантов (`variant`) | `проверка интерфейса, ревью UI, аудит типографики и цветов, better-interface` | Prompt | [SKILL.md](skills/design/better-interface/SKILL.md) |
| **design-audit** | **AXD & Design Audit Suite**.<br>Академически выверенный фреймворк аудита дизайна и Agentic Experience Design (AXD) от Owl-Listener: 42 навыка (эвристики Нильсена, WCAG 2.2, UX scorecard, генеративный UI, калибровка тональности) | `аудит дизайна, UX-аудит, эвристическая оценка, WCAG доступность, AXD` | Prompt | [SKILL.md](skills/design/design-audit/SKILL.md) |
| **design-top100** | **Design Top-100 & Creative Suite**.<br>Коллекция 130+ дизайн-навыков от MengTo (Design+Code / Aura Build): Awwwards-стили, Three.js 3D/шейдеры, Bento, анти-AI-slop фильтры, видео-в-суперпромпт, интерактивные частицы | `awwwards сайт, Three.js 3D, Bento grid, анти-AI дизайн, superprompt по видео` | Node/CLI | [SKILL.md](skills/design/design-top100/SKILL.md) |
| **garden-skills** | **Garden Skills Suite**.<br>Кураторский пакет визуального инжиниринга от ConardLi: верстка веб-интерфейсов (`web-design-engineer`), интерактивные 16:9 клик-презентации (`web-video-presentation`), автономные статьи reacticle (`beautiful-article`), GPT Image 2 и KB-поиск | `создание веб-презентации 16:9, красивая веб-статья, прототипирование UI, garden-skills` | Python / Node/CLI | [SKILL.md](skills/design/garden-skills/SKILL.md) |
| **landing-page-design** | **High-Converting Landing Page System**.<br>Система проектирования конверсионных лендингов от elayadesign: опросник intake, структура страницы, офферы, копирайтинг и строгая визуальная система (шрифты, отступы, радиусы, цвета) | `создать лендинг, посадочная страница, landing page, конверсионный дизайн` | Prompt | [SKILL.md](skills/design/landing-page-design/SKILL.md) |
| **nano-banana** | **Visual Asset Generator**.<br>Генерация изображений и промо-графики через модели генерации | `генерация иллюстраций, промо-графика, вижуалы` | Python / Node/CLI | [SKILL.md](skills/design/nano-banana/SKILL.md) |
| **scroll-craft** | **Scroll-Driven Website Engine**.<br>Специализированный движок создания кинематографичных сайтов с плавной прокруткой от nateherkai: многослойные 3D-сцены, глубина Hero, физика скролла, адаптация под мобильные устройства | `скролл-анимации, scroll-driven сайт, интерактивный скролл, кинематографичный лендинг` | Node/CLI | [SKILL.md](skills/design/scroll-craft/SKILL.md) |
| **static-banner** | **Static Banner Designer**.<br>Создание статических рекламных и контентных баннеров по строгой сетке | `создание баннеров, промо-креативы, постеры` | Prompt | [SKILL.md](skills/design/static-banner/SKILL.md) |
| **tastemaker** | **Anti-AI Design & Taste Engine**.<br>Движок авторского вкуса от Rohith: устранение шаблонного AI-дизайна, генерация гармоничных палитр под проект, локальные CLI-скрипты проверки контраста WCAG (`check_contrast.py`), стиль-локи `.tastemaker/style-lock.md` | `красивый UI без AI-шаблонов, подбор цветов, расчет контраста, дизайн со вкусом` | Python / CLI | [SKILL.md](skills/design/tastemaker/SKILL.md) |

---

## <a id="ops"></a>⚙️ Операционные задачи и Делегация (Operations & Tasks)

| Навык | Назначение | Триггеры вызова | Стек | Документация |
| :--- | :--- | :--- | :--- | :--- |
| **goal-buddy** | **Autonomous Goal Engine**.<br>Автономное управление целями: компилятор намерений, Goal Oracle, канбан-доска, роли Scout/Judge/Worker | `/goalbuddy, /goal-prep, запуск долгосрочных автономных задач` | Node/CLI | [SKILL.md](skills/ops/goal-buddy/SKILL.md) |
| **todoist-automation** | **Todoist Automation MCP**.<br>Управление проектами, задачами, дедлайнами и фильтрами Todoist через MCP | `создание задач Todoist, синхронизация списков дел` | Prompt | [SKILL.md](skills/ops/todoist-automation/SKILL.md) |
| **whatsup** | **WhatsApp MCP Server**.<br>Двунаправленный WhatsApp-мост (протокол Baileys, linked-device) для чтения и отправки сообщений | `отправка/чтение сообщений WhatsApp, сопряжение через QR` | Node/CLI | [SKILL.md](skills/ops/whatsup/SKILL.md) |

---

## <a id="business"></a>💼 Бизнес, Стратегия и Продажи (Business & Strategy)

| Навык | Назначение | Триггеры вызова | Стек | Документация |
| :--- | :--- | :--- | :--- | :--- |
| **biznes-plan-architect** | **Business Plan Architect**.<br>Разработка инвестиционных и операционных бизнес-планов, юнит-экономика и финмодели | `составление бизнес-плана, расчет финмодели, питч-дек` | Python | [SKILL.md](skills/business/biznes-plan-architect/SKILL.md) |
| **growth-expert** | **Growth Marketing Framework**.<br>Стратегии масштабирования, воронки привлечения, виральные петли и когортный анализ | `стратегия роста, масштабирование продукта, CAC/LTV оптимизация` | Python | [SKILL.md](skills/business/growth-expert/SKILL.md) |
| **pptx-generator** | **PPTX Deck Generator**.<br>Генерация профессиональных презентаций PowerPoint из markdown и структурированных данных | `создать презентацию, сделать слайды, PPTX отчет` | Python / Node/CLI | [SKILL.md](skills/business/pptx-generator/SKILL.md) |
| **pricing-strategy** | **Pricing Strategy Engine**.<br>Проектирование тарифных сеток, монетизации SaaS, эластичности спроса и прайсинга | `выбор тарифов, расчет цен, изменение модели монетизации` | Prompt | [SKILL.md](skills/business/pricing-strategy/SKILL.md) |
| **revops** | **Revenue Operations Framework**.<br>Оптимизация сквозных процессов продаж, маркетинга и клиентского успеха (RevOps) | `настройка воронки продаж, аудит CRM процессов, RevOps` | Node/CLI | [SKILL.md](skills/business/revops/SKILL.md) |
| **sales-enablement** | **Sales Enablement Suite**.<br>Создание скриптов продаж, battle cards против конкурентов, онбординга сейлзов | `материалы для продаж, скрипты переговоров, сравнение с конкурентами` | Node/CLI | [SKILL.md](skills/business/sales-enablement/SKILL.md) |
| **site-architecture** | **Information Architecture Suite**.<br>Проектирование структуры сайтов, карты навигации, перелинковки и пользовательских путей | `структура сайта, sitemap, навигация веб-приложения` | Node/CLI | [SKILL.md](skills/business/site-architecture/SKILL.md) |

---

## <a id="marketing"></a>📈 Маркетинг, SEO и Аналитика (Marketing & SEO)

| Навык | Назначение | Триггеры вызова | Стек | Документация |
| :--- | :--- | :--- | :--- | :--- |
| **aeo-geo-skill-ru** | **Answer & Generative Engine Optimization (AEO/GEO)**.<br>Полный плейбук AEO/GEO на русском: 4 канала выдачи, 289-значные H1 под labrador, обход кэша OpenAI, 117-словные пассажи, защита от Ghost Citations, Python stdlib CLI | `AEO, GEO, оптимизация под нейросети, ChatGPT labrador, Perplexity, цитируемость, llms.txt, Ghost Citations` | Python / CLI | [SKILL.md](skills/marketing/aeo-geo-skill-ru/SKILL.md) |
| **agent-reach** | **Multi-Platform Intelligence & Retrieval Router**.<br>Маршрутизатор сбора контента по 15 платформам (Twitter/X, Reddit, LinkedIn, Xiaohongshu, Bilibili, YouTube, RSS, Facebook, Instagram) с авто-роутингом бэкендов | `сбор постов, анализ трендов соцсетей, поиск в Twitter/Reddit/XHS, agent-reach` | Python / CLI | [SKILL.md](skills/marketing/agent-reach/SKILL.md) |
| **seo-audit** | **Comprehensive SEO Audit**.<br>Технический и контентный аудит веб-сайтов, анализ индексации, Core Web Vitals | `SEO аудит, проверка ошибок индексации, аудит сайта` | Node/CLI | [SKILL.md](skills/marketing/seo-audit/SKILL.md) |
| **synthetic-exploration** | **Synthetic Hypothesis Testing**.<br>Масштабное тестирование продуктовых гипотез на виртуальных выборках синтетических пользователей | `тестирование гипотез, симуляция фокус-групп, синтетические респонденты` | Prompt | [SKILL.md](skills/marketing/synthetic-exploration/SKILL.md) |
| **synthetic-personas** | **Synthetic Personas Generator**.<br>Генерация детальных синтетических профилей ЦА с реалистичными психологическими установками | `создание портретов ЦА, синтетические персоны` | Python / Node/CLI | [SKILL.md](skills/marketing/synthetic-personas/SKILL.md) |
| **video-use** | **Conversational Video Editing & Production**.<br>Интеллектуальный монтаж видео через разговорный интерфейс: распознавание пауз и слов (ASR), склейка без перекодирования (`-c copy`), Manim-анимации, цветокоррекция и субтитры | `монтаж видео, нарезка ролика, добавление субтитров, Manim видео, video-use` | Python / CLI | [SKILL.md](skills/marketing/video-use/SKILL.md) |
| **yandex-metrika** | **Yandex Metrika Analytics**.<br>Анализ трафика, конверсий, источников и поведения пользователей через API Яндекс.Метрики | `аналитика Метрики, отчет по трафику, конверсии сайта` | Node/CLI | [SKILL.md](skills/marketing/yandex-metrika/SKILL.md) |
| **yandex-search-api** | **Yandex Search API Suite**.<br>Веб-поиск и парсинг поисковой выдачи Яндекса для сбора данных и анализа SERP | `поиск через Яндекс API, мониторинг позиций в Яндексе` | Node/CLI | [SKILL.md](skills/marketing/yandex-search-api/SKILL.md) |
| **yandex-wordstat** | **Yandex Wordstat Explorer**.<br>Анализ частотности поисковых запросов и сезонности спроса через API Wordstat | `сбор семантического ядра, частотность запросов, Wordstat` | Python | [SKILL.md](skills/marketing/yandex-wordstat/SKILL.md) |
| **youtube-automation** | **YouTube Automation MCP**.<br>Управление видео, загрузка роликов, метаданные и аналитика YouTube через MCP | `автоматизация YouTube, выгрузка видео, обновление метаданных` | Prompt | [SKILL.md](skills/marketing/youtube-automation/SKILL.md) |
| **youtube-downloader** | **YouTube Media Downloader**.<br>Загрузка видео и аудио с YouTube в настраиваемом качестве и формате | `скачать видео с YouTube, извлечь аудиодорожку` | Python | [SKILL.md](skills/marketing/youtube-downloader/SKILL.md) |

---

## <a id="research"></a>🔬 Исследования, Анализ и SOTA (Research & Intelligence)

| Навык | Назначение | Триггеры вызова | Стек | Документация |
| :--- | :--- | :--- | :--- | :--- |
| **HeroesGPT** | **Strategic Research Standard (v7.0)**.<br>Полный цикл стратегического исследования: JTBD, Journey Map, генерация офферов и матрица внедрения | `стратегический анализ продукта, исследование рынка v7.0` | Python | [SKILL.md](skills/research/HeroesGPT/SKILL.md) |
| **consulting** | **Consulting Analysis Engine**.<br>Подготовка аналитических отчетов и структурированных фреймворков уровня McKinsey/BCG | `консалтинговый отчет, глубокий анализ рынка, стратегический репорт` | Prompt | [SKILL.md](skills/research/consulting/SKILL.md) |
| **hypothesis-designer** | **Hypothesis Designer**.<br>Проектирование гипотез проблем и решений на базе данных сегментов, расчет выборки | `проектирование продуктовых гипотез, дизайн экспериментов` | Prompt | [SKILL.md](skills/research/hypothesis-designer/SKILL.md) |
| **neuroarxiv** | **ArXiv Prior-Art Research**.<br>Исследование научной литературы на arXiv, поиск готовых архитектур и алгоритмов перед кодингом | `/neuroarxiv, поиск научных статей, SOTA решения, проверка новизны` | Prompt | [SKILL.md](skills/research/neuroarxiv/SKILL.md) |
| **tavily-intelligence** | **Tavily Intelligence Suite**.<br>Глубокий исследовательский поиск, сканирование веб-страниц и извлечение фактов через API Tavily | `комплексный веб-поиск, сбор информации о технологиях/компаниях` | Python | [SKILL.md](skills/research/tavily-intelligence/SKILL.md) |

---

## <a id="personal"></a>👤 Личная продуктивность и База знаний (Personal & PKM)

| Навык | Назначение | Триггеры вызова | Стек | Документация |
| :--- | :--- | :--- | :--- | :--- |
| **book-to-skill** | **Book-to-Skill Transformer**.<br>Трансформация книг и методических материалов в практические исполняемые навыки для агентов | `превратить книгу в навык, оцифровка методологии` | Python | [SKILL.md](skills/personal/book-to-skill/SKILL.md) |
| **claude-obsidian** | **Compounding Knowledge System**.<br>Полноценный комплекс из 15 навыков для Obsidian: захват первоисточников, связывание знаний, верификация claims, Canvas-карты | `база знаний Obsidian, создание заметок, claims ledger, Obsidian Canvas, claude-obsidian` | Python / Node/CLI | [SKILL.md](skills/personal/claude-obsidian/SKILL.md) |
| **obsidian-git** | **Obsidian Git Sync**.<br>Автоматическое резервное копирование, версионирование и синхронизация базы Obsidian через Git | `бэкап заметок, синхронизация базы знаний через Git, obsidian-git` | Python / Node/CLI | [SKILL.md](skills/personal/obsidian-git/SKILL.md) |

---

## <a id="ai"></a>🧠 ИИ-оптимизация и Безопасность (AI Core & Context)

| Навык | Назначение | Триггеры вызова | Стек | Документация |
| :--- | :--- | :--- | :--- | :--- |
| **low-toten** | **Token Efficiency & Context Optimization**.<br>Протокол экономии токенов, сжатие промптов и высокоплотная передача данных | `оптимизация контекста, протокол Low-Token, чистка оверхеда` | Python / Node/CLI | [SKILL.md](skills/ai/low-toten/SKILL.md) |
| **watermarks-remover** | **AI Watermark & Metadata Stripper**.<br>3-уровневая очистка: невидимый Unicode, стилометрия ИИ и метаданные C2PA/EXIF/XMP | `/remove-ai-marks, удаление водяных знаков ИИ, очистка C2PA` | Python / Node/CLI | [SKILL.md](skills/ai/watermarks-remover/SKILL.md) |

---

## <a id="skill-ops"></a>🏗 Мета-навыки и Аудит (Skill Engineering & Operations)

| Навык | Назначение | Триггеры вызова | Стек | Документация |
| :--- | :--- | :--- | :--- | :--- |
| **skill-creator** | **Skill Engineering Engine**.<br>Создание навыков с нуля, адаптация git-репозиториев, валидация L1-L3 и упаковка навыков PersonalOS | `«создай навык», «новый скилл», «git clone», /skill-creator` | Python / CLI | [SKILL.md](skills/skill-ops/skill-creator/SKILL.md) |
| **skillspector** | **NVIDIA SkillSpector Gate**.<br>Шлюз безопасности: статический и семантический аудит навыков перед установкой (YARA, AST, Prompt Injection, Data Exfiltration) | `аудит навыка, проверка безопасности, skillspector, skill-inspector, verify skill` | Python / CLI | [SKILL.md](skills/skill-ops/skillspector/SKILL.md) |

---
