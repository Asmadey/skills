---
description: Хронологический журнал изменений библиотеки навыков PersonalOS (skills). Фиксирует добавления, обновления, удаления и реструктуризацию навыков.
created: 2026-08-30
last_updated: 2026-09-06
---

# 📜 Журнал изменений (Changelog) — Библиотека навыков PersonalOS

## [2026-09-06] — Интеграция навыка unlazy (Leonxlnx/unlazy)

### 📦 Добавленные навыки
- **`dev/unlazy`** ([`skills/dev/unlazy/SKILL.md`](skills/dev/unlazy/SKILL.md)):
  - Фреймворк дисциплины исполнения и устранения лени автономных ИИ-агентов.
  - Формирование фальсифицируемых acceptance gates (`GATES.md`) до начала работы.
  - Построение дерева декомпозиции Depth Tree, параллельный запуск независимых ветвей и обязательная повторная верификация доказательств (`--reverify`).
  - Прошел аудит NVIDIA SkillSpector (APPROVE, 0 критических уязвимостей).

---

Все значимые изменения библиотеки навыков `skills/` документируются в этом файле.
Формат основан на стандартах [Keep a Changelog](https://keepachangelog.com/ru/1.0.0/).

---

## [2026-09-06] — Комплексный аудит, реструктуризация и мажорные обновления

### 🧹 Удалено (Removed)
- **`skills NEW/skills/ai-slop-detector`**: Устаревшая текстовая памятка, дублировала функционал специализированных де-слопперов.
- **`skills NEW/skills/writing/slop-detector`**: Короткая выжимка правил, полностью покрываемая расширенным пайплайном `slop-monster`.
- **`skills NEW/skills/writing/Anti-AI Writing Style Skill`**: Директория с нестандартным именем, дублировала правила `humanizer-en` и `humanizer-ru`.
- **`skills/autoresearch`**: Устаревший прототип, удален в пользу исследовательских модулей `neuroarxiv` и `sgr-core`.
- **`skills NEW/goal-loop`**: Устаревший цикл планирования, полностью заменен ролевым движком `goal-buddy`.
- **`skills NEW/awesome-design-md`**: Избыточный каталог, дублировавший дизайн-системы `awesome-design-skills`.
- **`~/.gemini/config/skills/no-ai-slop`**: Удален избыточный глобальный навык, дублирующий встроенные системные правила.
- **`skills/skills/marketing/ai-seo`**: Устаревший декларативный гайд, полностью вытеснен и поглощен инженерным фреймворком `aeo-geo-skill-ru`.
- **`onpage-seo` / `article-seo`**: Исключены устаревшие концепты классического SEO, противоречащие алгоритмам генеративной видимости в пользу атомарных пассажей и `aeo-geo-skill-ru`.

### 📁 Реорганизация и нормализация (Changed)
- **Слияние и финализация структуры**: Временная директория `skills NEW/` окончательно синхронизирована и перенесена в каноническую корневую папку `skills/` (13 категорий в `skills/skills/`, 78 активных навыков).
- **Устранение структурных нарушений и аудит**:
  - `skills/skills/business/pricing-strategy/SKILL.md`: создан мастер-манифест навыка (архетипы монетизации SaaS/B2B/B2C, сетки тарифов, Grandfathering, протоколы экспериментов).
  - `skills/skills/automation/n8n-official/SKILL.md`: создан корневой манифест со спецификацией всех 14 под-навыков; удалена вложенная директория `.git`.
  - `skills/skills/dev/git-worktree/SKILL.md`: нормализован YAML frontmatter (устранена пустая строка перед сигнатурой).
  - 100% активных навыков на диске приведены к стандарту Agent Skills с валидными `name` и `description`.
- **Переименование `brw`**: Папка `skills/skills/automation/brw` переименована в каноничный `skills/skills/automation/Browser-automation` для соответствия стандартам наименования инструментов.
- **Релокация `prd-taskmaster`**: Перенесен из корня `skills/` в структурированную категорию `skills/skills/product/prd-taskmaster`.
- **Синхронизация документации**: Полностью переписаны и актуализированы [INDEX.md](INDEX.md), [README.md](README.md) и [changelog.md](changelog.md).

### ⚡ Добавлено (Added)
- **`adhd`** ([skills/dev/adhd/SKILL.md](skills/dev/adhd/SKILL.md)): Движок параллельного дивергентного мышления для кодинг-агентов от Udit Akhouri: одновременное исследование проблемы под 5 когнитивными фреймами (Biology, Speedrunner, Regulator, 10yo, $0 budget), скоринг гипотез, отсеивание ловушек и углубление архитектурных решений. Прошел аудит SkillSpector (`APPROVE`).
- **`agent-reach`** ([skills/marketing/agent-reach/SKILL.md](skills/marketing/agent-reach/SKILL.md)): Маршрутизатор сбора контента по 15 платформам (Twitter/X, Reddit, LinkedIn, Xiaohongshu, Bilibili, YouTube, RSS, Facebook, Instagram) с авто-роутингом бэкендов (CLI/API/Browser). Прошел аудит SkillSpector (`APPROVE`).
- **`video-use`** ([skills/marketing/video-use/SKILL.md](skills/marketing/video-use/SKILL.md)): Интеллектуальный монтаж видео через диалоговый интерфейс от Browser-Use: распознавание слов/пауз (ASR), склейка без перекодирования (`-c copy`), Manim-анимации оверлеев, цветокоррекция и субтитры. Прошел аудит SkillSpector (`APPROVE`).
- **`garden-skills`** ([skills/design/garden-skills/SKILL.md](skills/design/garden-skills/SKILL.md)): Кураторский пакет визуального инжиниринга от ConardLi из 5 специализированных навыков: `web-design-engineer` (верстка интерфейсов и дашбордов), `web-video-presentation` (интерактивные 16:9 клик-презентации), `beautiful-article` (автономные веб-статьи reacticle), `gpt-image-2` (80+ шаблонов промптинга) и `kb-retriever` (поиск по базам знаний). Прошел аудит SkillSpector (`APPROVE`).
- **`landing-page-design`** ([skills/design/landing-page-design/SKILL.md](skills/design/landing-page-design/SKILL.md)): Фреймворк проектирования конверсионных посадочных страниц от elayadesign: анкетирование intake, структура оффера, конверсионный копирайтинг и строгая система дизайн-токенов (типографика, сетка, радиусы, цвета). Прошел аудит SkillSpector (`APPROVE`).
- **`design-top100`** ([skills/design/design-top100/SKILL.md](skills/design/design-top100/SKILL.md)): Флагманская библиотека из 130+ навыков веб-дизайна от MengTo (Design+Code / Aura Build): Three.js 3D/шейдеры, Awwwards-стили, Bento-сетки, детекторы AI-slop, генерация суперпромптов по видеозаписям и интерактивные эффекты. Прошел аудит SkillSpector (`APPROVE`).
- **`better-interface`** ([skills/design/better-interface/SKILL.md](skills/design/better-interface/SKILL.md)): Пакет из 11 навыков инспекции интерфейсов от Jakub Krehel (Interfaces.dev): системный аудит верстки (`better-layout`), доступности (`better-accessibility`), типографики (`better-typography`), палитр (`better-colors`), стресс-тестирование всех состояний (`break`) и генерация вариантов (`variant`). Прошел аудит SkillSpector (`APPROVE`).
- **`tastemaker`** ([skills/design/tastemaker/SKILL.md](skills/design/tastemaker/SKILL.md)): Anti-AI-slop движок авторского вкуса от Rohith: устранение однотипных градиентов, алгоритмическая генерация гармоничных палитр под проект, локальные CLI-утилиты проверки контраста WCAG (`check_contrast.py`), дизайн-память в `.tastemaker/style-lock.md`. Прошел аудит SkillSpector (`APPROVE`).
- **`design-audit`** ([skills/design/design-audit/SKILL.md](skills/design/design-audit/SKILL.md)): Комплексный фреймворк аудита интерфейсов и Agentic Experience Design (AXD) от Owl-Listener из 42 навыков по 6 направлениям: `evaluation` (эвристики Нильсена, WCAG, UX scorecard), `model-interaction` (генеративный UI, адаптивное раскрытие), `behavior` (калибровка тональности, персоны), alignment, orchestration и prompt-architecture. Прошел аудит SkillSpector (`APPROVE`).
- **`scroll-craft`** ([skills/design/scroll-craft/SKILL.md](skills/design/scroll-craft/SKILL.md)): Специализированный движок создания кинематографичных сайтов с плавной скролл-анимацией от nateherkai: многослойная 3D-глубина, физика перемещения, покадровая анимация и мобильная адаптивность. Прошел аудит SkillSpector (`APPROVE`).
- **`gnhf`** ([skills/dev/gnhf/SKILL.md](skills/dev/gnhf/SKILL.md)): Автономный оркестратор длительных ночных прогонов кодинг-агентов (Good Night, Have Fun) до естественного stop condition в режимах Hands-Off и Companion.
- **`ai-software-factory`** ([frameworks/ai-software-factory/SKILL.md](frameworks/ai-software-factory/SKILL.md)): Беспилотная фабрика софта («Dark Factory»): полный конвейер Issue → Mission Gate → Plan → Implement → Изолированный Judge → Holdout E2E → Auto-Merge.
- **`codex-plugin-cc`** ([skills/dev/codex-plugin-cc/SKILL.md](skills/dev/codex-plugin-cc/SKILL.md)): Официальный интеграционный пакет OpenAI Codex CLI для агентных сред (запуск Codex CLI, обработка диффов, рецепты промптинга для GPT-5.4).
- **`skillspector`** ([skills/skill-ops/skillspector/SKILL.md](skills/skill-ops/skillspector/SKILL.md)): Официальный шлюз безопасности NVIDIA SkillSpector. Проводит статический YARA/AST скан и семантический аудит внешних навыков перед установкой.
- **`advise-project-approach`** ([skills/product/advise-project-approach/SKILL.md](skills/product/advise-project-approach/SKILL.md)): Интеллектуальный советник по архитектуре и выбору технологического стека на базе анализа реальных аналогов (comparables), оценки компромиссов и операционных расходов.
- **`obsidian-git`** ([skills/personal/obsidian-git/SKILL.md](skills/personal/obsidian-git/SKILL.md)): Навык интеграции и автоматизации Git для локальных хранилищ Obsidian (периодический коммит, пуш/пулл, бэкап заметок).
- **`no-mistakes`** ([skills/dev/no-mistakes/SKILL.md](skills/dev/no-mistakes/SKILL.md)): Локальный гейт-прокси и pre-commit пайплайн валидации правок кода (синтаксис, статический анализ, отсутствие регрессий).
- **`claude-obsidian`** ([skills/personal/claude-obsidian/SKILL.md](skills/personal/claude-obsidian/SKILL.md)): Полнофункциональная локальная система знаний для Obsidian из 15 специализированных навыков: захват источников, claim-first grounding, Canvas-карты, autoresearch и валидация хранилища. Проверен через NVIDIA SkillSpector (`APPROVE`).
- **`supabase`** ([skills/dev/supabase/SKILL.md](skills/dev/supabase/SKILL.md)): Официальный агентный пакет навыков Supabase: работа с продуктами платформы (Auth, DB, Storage, Realtime, Edge Functions), RLS-политики, SSR-интеграции и оптимизация PostgreSQL (`supabase-postgres-best-practices`). Проверен через NVIDIA SkillSpector (`APPROVE`).
- **`aeo-geo-skill-ru`** ([skills/marketing/aeo-geo-skill-ru/SKILL.md](skills/marketing/aeo-geo-skill-ru/SKILL.md)): Фундаментальный Playbook V2 оптимизации под поисковые AI-системы (AEO/GEO на русском языке): 4 канала выдачи, 289-символьные H1 под labrador, обход кэша OpenAI, 117-словные пассажи, защита от Ghost Citations, 5 CLI-утилит на Python stdlib. Проверен через NVIDIA SkillSpector (`APPROVE`).
- **`frameworks/gsd-core`** ([frameworks/gsd-core/](frameworks/gsd-core/)): Полнофункциональный оркестратор разработки **Git. Ship. Done - Core** (ветка `next`, коммит `c95b73414`). 72 специализированных навыка, 37 автономных ролевых агентов, архитектура Spec-Driven Development (SDD) и изоляция контекста через свежие 200k контекстные окна субагентов. Прошел обязательный аудит безопасности NVIDIA SkillSpector (`APPROVE`).

### 🚀 Обновлено (Updated)
- **`prd-taskmaster`** ([skills/product/prd-taskmaster/SKILL.md](skills/product/prd-taskmaster/SKILL.md)):
  - Мажорный апгрейд до **Atlas Engine v5.3.0**.
  - Установлен полный бэкенд-пакет `prd_taskmaster/` (33 модуля Python).
  - Заменен устаревший `script.py` на официальный CLI-шим `taskmaster`.
  - Добавлена фазовая логика `phases/` (`DISCOVER.md`, `GENERATE.md`, `HANDOFF.md`).
  - Добавлен проверочный чеклист сдачи проекта `skel/ship-check.py`.
- **`code-reviewer`** ([skills/dev/code-reviewer/SKILL.md](skills/dev/code-reviewer/SKILL.md)):
  - Мажорный апгрейд до **Total Review Multi-Agent Suite v2.1.0** на базе архитектуры `davidondrej/total-review`.
  - Внедрен параллельный запуск двух независимых моделей: **Claude** (хост/субагент) + **OpenAI Codex CLI** (через `codex-plugin-cc`).
  - Закреплен **Unbiased Prompt Protocol** (строго нейтральный шаблон без наводящих вопросов для исключения галлюцинаций).
  - Введена **Overthinking Rejection Rubric** (формализованная матрица дисквалификации придирок к стилю, форматированию и теоретических edge-cases).
  - Добавлен интерактивный Approval Gate (`all`, `1, 3`, `none`) и сквозная верификация внесенных правок через **`no-mistakes`** перед коммитом.
- **`frameworks/superpowers`** ([frameworks/superpowers/](frameworks/superpowers/)):
  - Мажорный апгрейд с **v5.0.6 до v6.3.0** из апстрим-репозитория `obra/superpowers`.
  - Внедрена поддержка Devin CLI, Hermes Agent, Kimi и Grok Build CLI.
  - Реструктуризация SDD: plan-scoped рабочая область `.superpowers/sdd/<plan>/`, resume-based цикл правок, 5-раундовый circuit breaker, батчинг микрозадач.
  - Масштабируемый роутер в `brainstorming` (spike, bounded, architectural).
  - Полное сжатие текстов навыков и замена `testing-anti-patterns.md` на `writing-good-tests.md` с дисциплиной фальсифицируемости.

### 🏛 Конституция проекта (AGENTS.md)
- **Очистка и оптимизация**: Файл [AGENTS.md](AGENTS.md) сокращен со 118 до 44 строк.
- **Удаление оверхеда**: Исключен 62-строчный специализированный блок n8n (делегирован в `skills/skills/automation/n8n-*`).
- **Low-Token Mode**: Интегрирован стандарт высокой плотности информации на базе `low-toten` (Zero Fluff, прямой запуск инструментов, формат передачи фактов).
- **Раздел 6 (Skill Pre-Install Gate)**: Закреплен обязательный шлюз безопасности: аудит любого нового навыка из GitHub через `skillspector` в изолированном `/tmp/` ДО установки. Запрет вердикта `REJECT`, подтверждение при `CAUTION`.

---

## [2026-09-05] — Системы контроля качества контента и автономных целей

### ⚡ Добавлено (Added)
- **`goal-buddy`** ([skills/ops/goal-buddy/SKILL.md](skills/ops/goal-buddy/SKILL.md)): Автономный движок управления долгосрочными целями (Goal Oracle, локальная канбан-доска `.goalbuddy-board/`, роли Scout/Judge/Worker, квитанции о выполнении).
- **`watermarks-remover`** ([skills/ai/watermarks-remover/SKILL.md](skills/ai/watermarks-remover/SKILL.md)): 3-уровневая очистка: невидимый Unicode (Layer A), стилометрия ИИ (Layer B) и метаданные контейнеров C2PA/EXIF/XMP.
- **`slop-monster`** ([skills/writing/slop-monster/SKILL.md](skills/writing/slop-monster/SKILL.md)): 4-шаговый пайплайн де-слопинга текстов (Lint через `deslop.py` $\rightarrow$ Rewrite $\rightarrow$ Cleanse с альтернативной LLM $\rightarrow$ Re-Lint).

---

## [2026-08-30] — Интеграция дизайн-систем, анимаций и MCP-коннекторов

### ⚡ Добавлено (Added)
- **`hallmark`**: Anti-AI-Slop дизайн-движок для создания характерного авторского интерфейса.
- **`awesome-design-skills`**: Каталог 67 дизайн-систем и трендов (Bento, Brutalism, Glassmorphism и др.).
- **`shadcn`**: Официальный менеджер компонентов `shadcn/ui` и Tailwind CSS.
- **`magicui`**: Коллекция анимированных React/Next.js компонентов.
- **`GSAP`**: Библиотека скриптовой веб-анимации (ScrollTrigger, Flip, MorphSVG).
- **`mobile`**: Мастер-хаб проектирования мобильных приложений (`mobile-app-ui-design` + Google MD3).
- **`diy-mcp-connector`**: Генератор автономных MCP-серверов через HAR/CDP анализ.
- **`whatsup`**: Двунаправленный WhatsApp MCP-сервер на базе Baileys.

---

## [2026-08-29] — Первичная структуризация библиотеки навыков

### ⚡ Добавлено (Added)
- Интеграция базовых навыков: `simple-english`, `git-worktree`, `low-toten`, `consulting`.
- Создан первичный реестр и трехуровневая модель контекста (L1: AGENTS.md $\rightarrow$ L2: SKILL.md $\rightarrow$ L3: код/скрипты).\n