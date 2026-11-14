---
description: Хронологический журнал изменений библиотеки навыков PersonalOS (skills). Фиксирует добавления, обновления, удаления и реструктуризацию навыков.
created: 2026-08-30
last_updated: 2026-11-14
---
# 📜 Журнал изменений (Changelog) — Библиотека навыков PersonalOS


## [2026-11-14] — Новый навык marketing/aeo-geo-claim-pipeline

### 📦 Добавленные навыки
- **`marketing/aeo-geo-claim-pipeline`** ([`skills/marketing/aeo-geo-claim-pipeline/SKILL.md`](skills/marketing/aeo-geo-claim-pipeline/SKILL.md)):
  - Конвейер «статья → атом-claim → вердикт против доктрины → гейт → патч скилла». Оформлен по образцу `claude-seo`: Primary Source со статусом проверки, When to Use, таблицы вердиктов и гейтов, Error Handling, Security, `references/`.
  - `scripts/aeo_claims_blocks.py` — доктрина в блоки с тирами и источниками (158 блоков, у 75 источника нет).
  - `scripts/aeo_claims_extract.py` — атомы без LLM: topic scope, гигиена предложений, двуязычные числовые сигнатуры (`200 символов` ≡ `200 characters`).
  - `scripts/aeo_claims_adjudicate.py` — LLM-адjudication (Ollama Cloud, batch 6) с шортлистом блоков-кандидатов.
  - `scripts/aeo_numbers.py` — нормализация «число + единица» для сравнения русской доктрины с англоязычными статьями.
  - Замер 2026-11-14: 291 атом → REFINES 110 / NEW 123 / DUPLICATE 54 / CONTRADICTS 4; 0 кредитов Firecrawl.

---

## [2026-11-12] — Новый навык dev/prefab-ui

### 📦 Добавленные навыки
- **`dev/prefab-ui`** ([`skills/dev/prefab-ui/SKILL.md`](skills/dev/prefab-ui/SKILL.md)):
  - Создание интерфейса для Python-проектов на Prefab (prefab-ui от Prefect): локальное превью, статический HTML, FastAPI + Fetch, MCP-приложения FastMCP, generative UI.
  - Справочники по компонентам, действиям, выражениям, стилям и темам собраны из документации prefab.prefect.io; шаблоны (standalone, FastAPI, MCP) проверены запуском на prefab-ui 0.21.1.

---

## [2026-11-11] — Синхронизация навыков из PersonalOS (public)

### 📦 Добавленные навыки
- **`design/stageshow`** ([`skills/design/stageshow/SKILL.md`](skills/design/stageshow/SKILL.md)):
  - Build faux product UI that looks like a real product, as a still illustration or an animated demo with a cursor.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).

---

## [2026-11-04] — Синхронизация навыков из PersonalOS (public)

### 📦 Добавленные навыки
## [2026-11-04] — Синхронизация навыков из PersonalOS (public)

### 📦 Добавленные навыки
- **`automation/agent-desktop`** ([`skills/automation/agent-desktop/SKILL.md`](skills/automation/agent-desktop/SKILL.md)):
  - Operate desktop applications on macOS, Windows and Linux through native accessibility trees.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`design/kie-image-generation`** ([`skills/design/kie-image-generation/SKILL.md`](skills/design/kie-image-generation/SKILL.md)):
  - Асинхронный конвейер генерации картинок через kie.ai API (nano banana, Flux-2, GPT Image 2.5, Seedream): `createTask` → `recordInfo` → `download-url`.
  - `scripts/kie_image.py` — создание задачи, ожидание, скачивание, cover-кроп в webp под размеры сайта (`--background transparent`, `--resolution 1K|2K|4K`).
  - `scripts/check_image.py` — приёмка: размер, альфа/отклонение фона по рамке, контактный лист.

---

## [2026-11-03] — Синхронизация навыков из PersonalOS (public)

### 📦 Добавленные навыки
- **`dev/bama`** ([`skills/dev/bama/SKILL.md`](skills/dev/bama/SKILL.md)):
  - Build Any Mac App (BAMA).
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).

---

## [2026-11-01] — Синхронизация навыков из PersonalOS (public)

### 📦 Добавленные навыки
- **`automation/b24phpsdk-maintainer`** ([`skills/automation/b24phpsdk-maintainer/SKILL.md`](skills/automation/b24phpsdk-maintainer/SKILL.md)):
  - Maintainer tools and workflows for bitrix24/b24phpsdk (OpenAPI schema refresh, code generators, issue lifecycle, TDD implementation, quality gates, and release PRs).
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`marketing/reverse-engineer-marketing`** ([`skills/marketing/reverse-engineer-marketing/SKILL.md`](skills/marketing/reverse-engineer-marketing/SKILL.md)):
  - When the user wants to reverse engineer how another company grew and copy what worked.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
### 🔄 Обновленные навыки
- **`UX/ui-ux-pro-max`** ([`skills/UX/ui-ux-pro-max/SKILL.md`](skills/UX/ui-ux-pro-max/SKILL.md)): синхронизированы обновления и ресурсы.
- **`dev/improve-codebase-architecture`** ([`skills/dev/improve-codebase-architecture/SKILL.md`](skills/dev/improve-codebase-architecture/SKILL.md)): синхронизированы обновления и ресурсы.
- **`dev/no-mistakes`** ([`skills/dev/no-mistakes/SKILL.md`](skills/dev/no-mistakes/SKILL.md)): синхронизированы обновления и ресурсы.
- **`dev/reverse-engineer-anything`** ([`skills/dev/reverse-engineer-anything/SKILL.md`](skills/dev/reverse-engineer-anything/SKILL.md)): синхронизированы обновления и ресурсы.
- **`marketing/ad-creative`** ([`skills/marketing/ad-creative/SKILL.md`](skills/marketing/ad-creative/SKILL.md)): синхронизированы обновления и ресурсы.
- **`marketing/ai-seo`** ([`skills/marketing/ai-seo/SKILL.md`](skills/marketing/ai-seo/SKILL.md)): синхронизированы обновления и ресурсы.
- **`marketing/offers`** ([`skills/marketing/offers/SKILL.md`](skills/marketing/offers/SKILL.md)): синхронизированы обновления и ресурсы.
- **`marketing/ppt-master`** ([`skills/marketing/ppt-master/SKILL.md`](skills/marketing/ppt-master/SKILL.md)): синхронизированы обновления и ресурсы.
- **`research/last30days`** ([`skills/research/last30days/SKILL.md`](skills/research/last30days/SKILL.md)): синхронизированы обновления и ресурсы.
- **`video/brag`** ([`skills/video/brag/SKILL.md`](skills/video/brag/SKILL.md)): синхронизированы обновления и ресурсы.
- **`writing/humanizer`** ([`skills/writing/humanizer-en/SKILL.md`](skills/writing/humanizer-en/SKILL.md)): синхронизированы обновления и ресурсы.
- **`writing/humanizer-ru`** ([`skills/writing/humanizer-ru/SKILL.md`](skills/writing/humanizer-ru/SKILL.md)): синхронизированы обновления и ресурсы.

---

## [2026-10-31] — Синхронизация навыков из PersonalOS (public)

### 📦 Добавленные навыки
- **`UX/dembrandt`** ([`skills/UX/dembrandt/SKILL.md`](skills/UX/dembrandt/SKILL.md)):
  - Комплексный инженерный комплекс UX-аудита, реверс-инжиниринга дизайн-систем и экстракции токенов (Dembrandt Suite by VictorGjn).
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`ai/evals-from-sessions`** ([`skills/ai/evals-from-sessions/SKILL.md`](skills/ai/evals-from-sessions/SKILL.md)):
  - Turn your own coding-agent sessions (Claude Code, Codex, Pi, Gemini CLI, or other JSONL session exports) into verified Harbor eval tasks.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`design/design-to-motion`** ([`skills/design/design-to-motion/SKILL.md`](skills/design/design-to-motion/SKILL.md)):
  - Turns a static design (a Figma frame, dashboard, card set, app screen, or a UI on a photo background) into a pixel exact HTML replica that loads in from an empty state, then has every visual act out what it does (a chart being read, a list receiving items, a prompt being typed) in a seamless loop, and exports an MP4 for X, a website GIF, and an 800×500 GIF.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`design/ux-designer`** ([`skills/design/ux-designer/SKILL.md`](skills/design/ux-designer/SKILL.md)):
  - UX principles for planning or auditing an interface: accessibility (WCAG, EAA), information architecture, microcopy, i18n/RTL, and AI or voice UX.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`dev/reverse-engineer-anything`** ([`skills/dev/reverse-engineer-anything/SKILL.md`](skills/dev/reverse-engineer-anything/SKILL.md)):
  - Reverse engineer native, managed, Electron/JavaScript, packaged, firmware, and browser targets with REA.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`marketing/app-store-screenshots`** ([`skills/marketing/app-store-screenshots/SKILL.md`](skills/marketing/app-store-screenshots/SKILL.md)):
  - Use when building App Store or Google Play screenshot pages, generating exportable marketing screenshots for iOS, macOS, and/or Android apps, or scaffolding a screenshot editor with Next.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`marketing/claude-seo`** ([`skills/marketing/claude-seo/SKILL.md`](skills/marketing/claude-seo/SKILL.md)):
  - Комплексный инженерный комплекс SEO-навыков, технического аудита и GEO/AEO-оптимизации (Claude SEO Suite by AgriciDaniel).
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`marketing/clone-website`** ([`skills/marketing/clone-website/SKILL.md`](skills/marketing/clone-website/SKILL.md)):
  - Реконструкция существующих веб-страниц в рабочий локальный код с реальным контентом, ассетами, адаптивной версткой и интеракциями.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`marketing/landing-page-design`** ([`skills/marketing/landing-page-design/SKILL.md`](skills/marketing/landing-page-design/SKILL.md)):
  - Complete system for building high converting landing pages: intake questions, page structure, layout selection, conversion copywriting, SEO, plus strict visual rules for typography, spacing, corner radius, backgrounds, hero layout, icons, and motion.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`video/brag`** ([`skills/video/brag/SKILL.md`](skills/video/brag/SKILL.md)):
  - Генерация динамичных промо- и лаунч-видеороликов (Launch Videos) для проектов, продуктов и сайтов.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
### 🔄 Обновленные навыки
- **`UX/hallmark`** ([`skills/UX/hallmark/SKILL.md`](skills/UX/hallmark/SKILL.md)): синхронизированы обновления и ресурсы.
- **`design/impeccable`** ([`skills/design/impeccable/SKILL.md`](skills/design/impeccable/SKILL.md)): синхронизированы обновления и ресурсы.
- **`design/design-taste-frontend`** ([`skills/design/taste-skill/SKILL.md`](skills/design/taste-skill/SKILL.md)): синхронизированы обновления и ресурсы.

---

## [2026-10-16] — Синхронизация навыков из PersonalOS (public)

### 📦 Добавленные навыки
- **`business/ai-business-evaluator`** ([`skills/business/ai-business-evaluator/SKILL.md`](skills/business/ai-business-evaluator/SKILL.md)):
  - Экспертный аудит применимости ИИ в бизнесе, декомпозиция бизнес-процессов по методологии Varick Agents, Michael Hammer и Yakov & Partners (4 корзины: Eliminate, Deterministic, Agentic, HITL), выявление разрыва Touch Time vs.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`design/deck-craft`** ([`skills/design/deck-craft/SKILL.md`](skills/design/deck-craft/SKILL.md)):
  - Система создания автономных интерактивных веб-презентаций и слайд-деков в стиле Varick Agents (Single-File Zero-Dependency HTML5).
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`design/diagram-design`** ([`skills/design/diagram-design/SKILL.md`](skills/design/diagram-design/SKILL.md)):
  - Create branded architecture, architecture delta, IT current-state, flowchart, sequence, state machine, ER/data model, timeline, swimlane, quadrant, radar/spider, polar chart (polar/radial lollipop), loop/flywheel, nested, tree, org chart, layer stack, exploded axonometric, axonometric plan, Venn, pyramid/funnel, treemap and marimekko, heatmap, bar and dumbbell, waterfall, line (slopegraph, ridgeline, streamgraph, bump), Gantt and scatter charts (bubble, beeswarm), high-level, process, medallion, data flow, DP integration, DP security matrix, Sankey, fishbone, Wardley map, kanban, user journey, service blueprint, deployment, dependency graph, UML class, story map, or database schema diagrams as HTML/SVG/PNG, with.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`design/sketch-design`** ([`skills/design/sketch-design/SKILL.md`](skills/design/sketch-design/SKILL.md)):
  - Создание рисованных интерактивных презентаций и архитектурных схем в духе доски Excalidraw (черный контур от руки, пастельные заливки, акцентный тон, пошаговая сборка, Pangolin + JetBrains Mono, Zero-Dependency HTML5 Custom Elements).
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`ops/evals-from-sessions`** ([`skills/ops/evals-from-sessions/SKILL.md`](skills/ops/evals-from-sessions/SKILL.md)):
  - Turn your own coding-agent sessions (Claude Code, Codex, Pi, Gemini CLI, or other JSONL session exports) into verified Harbor eval tasks.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).

---

## [2026-10-15] — Синхронизация навыков из PersonalOS (public)

### 📦 Добавленные навыки
- **`design/cinematic-landing`** ([`skills/design/cinematic-landing/SKILL.md`](skills/design/cinematic-landing/SKILL.md)):
  - Эталонный архитектурный шаблон иммерсивных лендингов PersonalOS (Cinematic Component Architecture — чемпион Arena Duel 2 a008).
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`dev/cinematic-landing`** ([`skills/dev/cinematic-landing/SKILL.md`](skills/dev/cinematic-landing/SKILL.md)):
  - Эталонный архитектурный шаблон иммерсивных лендингов PersonalOS (Cinematic Component Architecture — чемпион Arena Duel 2 a008).
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`dev/expo`** ([`skills/dev/expo/SKILL.md`](skills/dev/expo/SKILL.md)):
  - Официальный инженерный комплекс навыков Expo и React Native для агентов (Expo Skills Suite).
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`dev/handoff`** ([`skills/dev/handoff/SKILL.md`](skills/dev/handoff/SKILL.md)):
  - Фиксация и передача контекста текущей сессии (Session Handoff) в компактный чекпоинт-документ (HANDOFF.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`dev/improve-codebase-architecture`** ([`skills/dev/improve-codebase-architecture/SKILL.md`](skills/dev/improve-codebase-architecture/SKILL.md)):
  - Аудит архитектуры кодовой базы и поиск возможностей углубления модулей (Deep Modules по Джону Оустерхауту).
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`dev/scroll-craft`** ([`skills/dev/scroll-craft/SKILL.md`](skills/dev/scroll-craft/SKILL.md)):
  - Build premium scroll-driven landing pages for service, product, food, and.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`dev/tdd`** ([`skills/dev/tdd/SKILL.md`](skills/dev/tdd/SKILL.md)):
  - Разработка через тестирование (Test-Driven Development) по циклу Red-Green-Refactor.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`dev/technical-writer`** ([`skills/dev/technical-writer/SKILL.md`](skills/dev/technical-writer/SKILL.md)):
  - Комплексный инженерный комплекс технического писательства (Technical Writing Suite by riekelt).
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`marketing/ad-creative`** ([`skills/marketing/ad-creative/SKILL.md`](skills/marketing/ad-creative/SKILL.md)):
  - Генерация, масштабирование и A/B тестирование рекламных креативов и текстов для платного трафика (Meta, Google RSA, TikTok, LinkedIn).
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`marketing/ai-seo`** ([`skills/marketing/ai-seo/SKILL.md`](skills/marketing/ai-seo/SKILL.md)):
  - Оптимизация контента под поисковые ИИ-системы и ассистенты (AEO, GEO, LLMO, Google AI Overviews, Perplexity, ChatGPT, Claude, Gemini).
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`marketing/offers`** ([`skills/marketing/offers/SKILL.md`](skills/marketing/offers/SKILL.md)):
  - Проектирование и упаковка высококонверсионных офферов (Grand Slam Offers): Value Equation, стэкинг бонусов, устранение риска (гарантии), дефицит и срочность, ценовая архитектура и форматирование.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`marketing/ppt-master`** ([`skills/marketing/ppt-master/SKILL.md`](skills/marketing/ppt-master/SKILL.md)):
  - AI-driven presentation workflow for generating editable PPTX decks and slides,.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`marketing/video`** ([`skills/marketing/video/SKILL.md`](skills/marketing/video/SKILL.md)):
  - Пайплайн создания и генерации видеоконтента с помощью AI-моделей (Sora, Kling, Runway, Veo, Hailuo, Pika) и кодовых фреймворков (Remotion, Hyperframes).
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`product/next-move-theory`** ([`skills/product/next-move-theory/SKILL.md`](skills/product/next-move-theory/SKILL.md)):
  - Канон и навыки методологии Next Move Theory и Advanced JTBD (Иван Замесин).
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`product/pm-claude-code-setup`** ([`skills/product/pm-claude-code-setup/SKILL.md`](skills/product/pm-claude-code-setup/SKILL.md)):
  - Система гибкого продуктового менеджмента (Lean PM System) по методологии Аакаша Гупты (Aakash Gupta).
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`product/pm-skills`** ([`skills/product/pm-skills/SKILL.md`](skills/product/pm-skills/SKILL.md)):
  - Комплексная библиотека из 68 модульных навыков продуктового менеджмента (Product on Purpose) по фазам Triple Diamond, Lean Startup и Design Thinking.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`skill-ops/ablate-ai-layer`** ([`skills/skill-ops/ablate-ai-layer/SKILL.md`](skills/skill-ops/ablate-ai-layer/SKILL.md)):
  - Эмпирическое тестирование и сокращение инструкций ИИ (CLAUDE.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`skill-ops/arena`** ([`skills/skill-ops/arena/SKILL.md`](skills/skill-ops/arena/SKILL.md)):
  - Make 100 versions of Claude fight to the death over one task.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
### 🔄 Обновленные навыки
- **`dev/shadcn`** ([`skills/dev/shadcn/SKILL.md`](skills/dev/shadcn/SKILL.md)): синхронизированы обновления и ресурсы.

---

## [2026-10-06] — Синхронизация навыков из PersonalOS (public)

### 📦 Добавленные навыки
- **`design/design-taste-frontend`** ([`skills/design/taste-skill/SKILL.md`](skills/design/taste-skill/SKILL.md)):
  - Anti-slop frontend skill for landing pages, portfolios, and redesigns.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`marketing/google-maps-scraper`** ([`skills/marketing/google-maps-scraper-kit/SKILL.md`](skills/marketing/google-maps-scraper-kit/SKILL.md)):
  - Scrape Google Maps business listings (name, address, phone, website, rating, reviews, lat/lng, emails) via local REST API.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`skill-ops/authoring-skills`** ([`skills/skill-ops/anthropic/SKILL.md`](skills/skill-ops/anthropic/SKILL.md)):
  - Creates new Agent Skills and audits existing ones against Anthropic best practices (ToC in long files, degrees of freedom, one-level references, checklists, feedback loops, dependencies, model testing).
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`skill-ops/bain-skill-refactor`** ([`skills/skill-ops/bain-skill-refactor/SKILL.md`](skills/skill-ops/bain-skill-refactor/SKILL.md)):
  - Рефакторинг и актуализация навыков, системных промптов и инструкций по методологии Wulfie Bain (каркас Background / Behaviour / Output, MECE, устранение prompt debt).
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`skill-ops/optimize`** ([`skills/skill-ops/optimize/SKILL.md`](skills/skill-ops/optimize/SKILL.md)):
  - Модуль возможностей ИИ-агента.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`skill-ops/rtk-cli-optimize`** ([`skills/skill-ops/rtk-CLI-optimize/SKILL.md`](skills/skill-ops/rtk-CLI-optimize/SKILL.md)):
  - Оптимизация и сжатие консольного вывода CLI (bash output) до 90% для AI-агентов через утилиту RTK (Rust Token Killer).
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
### 🔄 Обновленные навыки
- **`skill-ops/public-skills-sync`** ([`skills/skill-ops/public-skills-sync/SKILL.md`](skills/skill-ops/public-skills-sync/SKILL.md)): синхронизированы обновления и ресурсы.

---

## [2026-09-16] — Синхронизация навыков из PersonalOS (public)

### 📦 Добавленные навыки
- **`ai/langfuse`** ([`skills/ai/Langfuse/SKILL.md`](skills/ai/Langfuse/SKILL.md)):
  - Interact with Langfuse and access its documentation: tracing, monitoring, creating datasets, running experiments, and evaluating AI applications.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`design/design-loop`** ([`skills/design/design-loop/SKILL.md`](skills/design/design-loop/SKILL.md)):
  - Takes a goal and a real-world reference, extracts what actually makes the reference good, then runs builder and three fresh-context critics on every piece until all three agree ours wins.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`dev/graft`** ([`skills/dev/graft/SKILL.md`](skills/dev/graft/SKILL.md)):
  - Локальный контекстный граф кодовой базы (Graft / NanoNets).
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`research/quality-check`** ([`skills/research/quality-check/SKILL.md`](skills/research/quality-check/SKILL.md)):
  - Structured quality review for AI-generated artifacts before they are trusted.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).
- **`skill-ops/public-skills-sync`** ([`skills/skill-ops/public-skills-sync/SKILL.md`](skills/skill-ops/public-skills-sync/SKILL.md)):
  - Синхронизирует проверенные навыки строго из папки skills/public/ в публичный внешний репозиторий https://github.
  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).

---
## [2026-09-06] — Интеграция навыка last30days (mvanhorn/last30days-skill)

### 📦 Добавленные навыки

- **`research/last30days`** ([`skills/research/last30days/SKILL.md`](skills/research/last30days/SKILL.md)):
  - Кросс-платформенное исследование мнений и трендов за последние 30 дней.
  - Сбор постов, вовлеченности и реакций с Reddit, X (Twitter), YouTube, TikTok, Hacker News, Polymarket, GitHub и веб-источников.
  - Встроенный Doctor Health Check для диагностики работоспособности и доступности внешних источников.
  - Прошел аудит NVIDIA SkillSpector (APPROVE, 0 критических уязвимостей).

---

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
