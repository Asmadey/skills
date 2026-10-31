---
name: claude-seo
description: "Комплексный инженерный комплекс SEO-навыков, технического аудита и GEO/AEO-оптимизации (Claude SEO Suite by AgriciDaniel). Охватывает 26 специализированных навыков: глубокий аудит сайтов (/seo audit), постраничный анализ (/seo page), технический SEO (Core Web Vitals, краулинг, индексация), Schema.org микроразметка, E-E-A-T анализ качества контента, генерация контент-планов и брифов, AI Overviews/GEO оптимизация (Perplexity, ChatGPT, Claude, Gemini), аудит доступности для AI-агентов (/seo agentic), анализ обратных ссылок, локальное и Maps SEO, семантическая кластеризация SERP, многоязычный hreflang и отслеживание дрифта выдачи. Триггеры: 'claude-seo', 'seo audit', 'technical seo', 'core web vitals', 'schema markup', 'eeat', 'geo', 'ai search optimization', 'sitemap audit', 'hreflang', 'keyword cluster', 'backlink analysis'."
category: marketing
version: 2.5.0
source: https://github.com/AgriciDaniel/claude-seo
license: MIT
metadata:
  author: AgriciDaniel
  category: marketing
  total_skills: 26
  total_agents: 19
---

# 🚀 Claude SEO Suite (by AgriciDaniel)

Комплексный открытый набор из 26 AI-навыков и 19 специализированных агентов для технического SEO, оптимизации под классический поиск Google и генеративный AI-поиск (GEO/AEO: Google AI Overviews, Perplexity, ChatGPT, Claude, Gemini).

---

## 🧭 Стартовая точка и быстрый запуск

При общих, комплексных или сквозных SEO-задачах используйте основной хаб:
- **[seo](skills/seo/SKILL.md)** — универсальный диспетчер аудита, распределяющий задачи по специализированным агентам и утилитам.

### Командный интерфейс (`/seo`)

| Команда | Описание | Основной навык |
|---|---|---|
| `/seo audit <url>` | Полный комплексный аудит сайта с параллельным запуском субагентов | [seo-audit](skills/seo-audit/SKILL.md) |
| `/seo page <url>` | Глубокий аудит одиночной страницы (on-page, technical, schema) | [seo-page](skills/seo-page/SKILL.md) |
| `/seo technical <url>` | Технический аудит (краулинг, индексация, Core Web Vitals, безопасность) | [seo-technical](skills/seo-technical/SKILL.md) |
| `/seo schema <url>` | Проверка, валидация и генерация Schema.org JSON-LD | [seo-schema](skills/seo-schema/SKILL.md) |
| `/seo geo <url>` | Оптимизация цитируемости под AI-движки (AI Overviews, Perplexity, ChatGPT) | [seo-geo](skills/seo-geo/SKILL.md) |
| `/seo agentic <url>` | Аудит готовности сайта к AI-агентам (Lighthouse Agentic Browsing, llms.txt) | [seo-agentic](skills/seo-agentic/SKILL.md) |
| `/seo content <url>` | Анализ контента, E-E-A-T, читаемости и тонких страниц | [seo-content](skills/seo-content/SKILL.md) |
| `/seo content-brief <topic>` | Построение детализированного SEO-брифа с ключевыми словами и структурой | [seo-content-brief](skills/seo-content-brief/SKILL.md) |
| `/seo cluster <keyword>` | Семантическая кластеризация SERP и архитектура хаб-статей | [seo-cluster](skills/seo-cluster/SKILL.md) |
| `/seo sitemap <url>` | Анализ структуры XML Sitemap или генерация карты сайта | [seo-sitemap](skills/seo-sitemap/SKILL.md) |
| `/seo images <url>` | Аудит изображений, alt-тегов, сжатия, WebP/AVIF и SERP | [seo-images](skills/seo-images/SKILL.md) |
| `/seo image-gen` | AI-генерация оптимизированных SEO/OG изображений (Gemini Image API) | [seo-image-gen](skills/seo-image-gen/SKILL.md) |
| `/seo backlinks <url>` | Профиль обратных ссылок, анкоры, токсичные домены (Moz, Bing, CC) | [seo-backlinks](skills/seo-backlinks/SKILL.md) |
| `/seo local <url>` | Локальное SEO (Google Business Profile, NAP-консистентность, отзывы) | [seo-local](skills/seo-local/SKILL.md) |
| `/seo maps <args>` | Гео-сетка позиций Google Maps, аудит карточки компании | [seo-maps](skills/seo-maps/SKILL.md) |
| `/seo hreflang <url>` | Аудит мультиязычности, тегов hreflang и валидация локалей | [seo-hreflang](skills/seo-hreflang/SKILL.md) |
| `/seo ecommerce <url>` | E-commerce SEO: Product schema, Google Shopping, маркетплейсы | [seo-ecommerce](skills/seo-ecommerce/SKILL.md) |
| `/seo programmatic` | Проектирование и аудит страниц программного SEO масштаба 1000+ | [seo-programmatic](skills/seo-programmatic/SKILL.md) |
| `/seo competitor-pages` | Генерация страниц сравнения с конкурентами (X vs Y, Alternatives) | [seo-competitor-pages](skills/seo-competitor-pages/SKILL.md) |
| `/seo sxo <url>` | Search Experience Optimization: согласование интента с UX/UI | [seo-sxo](skills/seo-sxo/SKILL.md) |
| `/seo flow` | FLOW-фреймворк: итерационный цикл Find → Leverage → Optimize → Win | [seo-flow](skills/seo-flow/SKILL.md) |
| `/seo drift baseline <url>` | Захват эталонного снимка SEO-состояния сайта | [seo-drift](skills/seo-drift/SKILL.md) |
| `/seo drift compare <url>` | Сравнение текущего состояния с эталоном и выявление регрессий | [seo-drift](skills/seo-drift/SKILL.md) |
| `/seo google <cmd>` | Интеграция с Google Search Console, CrUX, PageSpeed Insights API | [seo-google](skills/seo-google/SKILL.md) |
| `/seo dataforseo <cmd>` | Живые данные SERP и ключевых слов через DataForSEO API/MCP | [seo-dataforseo](skills/seo-dataforseo/SKILL.md) |
| `/seo plan <business>` | Долгосрочный стратегический план развития поисковой видимости | [seo-plan](skills/seo-plan/SKILL.md) |

---

## 📦 Каталог 26 навыков Claude SEO

### 1. Фундаментальный аудит и архитектура
- **[seo](skills/seo/SKILL.md)** — Единая точка входа и оркестрации всех проверок.
- **[seo-audit](skills/seo-audit/SKILL.md)** — Сквозной аудит домена со скорингом и приоритизированным планом.
- **[seo-page](skills/seo-page/SKILL.md)** — Глубокий срез конкретного URL по всем факторам ранжирования.
- **[seo-technical](skills/seo-technical/SKILL.md)** — Краулинг, коды ответов, редиректы, Core Web Vitals (LCP, CLS, INP).
- **[seo-schema](skills/seo-schema/SKILL.md)** — Генерация и валидация микроразметки Schema.org (JSON-LD).
- **[seo-sitemap](skills/seo-sitemap/SKILL.md)** — Проверка и генерация валидных XML-карт сайта.
- **[seo-hreflang](skills/seo-hreflang/SKILL.md)** — Международная индексация, языковые теги и региональные версии.

### 2. AI Search & Новая поисковая эра (GEO / LLMO)
- **[seo-geo](skills/seo-geo/SKILL.md)** — Подготовка контента к цитированию в Google AI Overviews, Perplexity, ChatGPT.
- **[seo-agentic](skills/seo-agentic/SKILL.md)** — Оптимизация под AI-агентов: дерево доступности, Markdown, `llms.txt`, WebMCP.

### 3. Контент, E-E-A-T и семантика
- **[seo-content](skills/seo-content/SKILL.md)** — Оценка полноты информации, экспертности E-E-A-T и читаемости.
- **[seo-content-brief](skills/seo-content-brief/SKILL.md)** — Составление ТЗ копирайтерам с расчетом объема и ключевых слов.
- **[seo-cluster](skills/seo-cluster/SKILL.md)** — Кластеризация запросов на основе пересечений SERP и внутренняя перелинковка.
- **[seo-competitor-pages](skills/seo-competitor-pages/SKILL.md)** — Шаблоны страниц сравнения («X vs Y», «Альтернативы Z»).
- **[seo-programmatic](skills/seo-programmatic/SKILL.md)** — Проектирование шаблонных посадочных страниц из баз данных.
- **[seo-sxo](skills/seo-sxo/SKILL.md)** — Устранение разрыва между поисковым интентом и конверсионным UX.

### 4. Мультимедиа и графика
- **[seo-images](skills/seo-images/SKILL.md)** — Оптимизация существующих изображений для Google Images и быстрой загрузки.
- **[seo-image-gen](skills/seo-image-gen/SKILL.md)** — Автоматическая генерация OpenGraph и баннеров для статей через Gemini.

### 5. Внешние факторы, локальное SEO и мониторинг
- **[seo-backlinks](skills/seo-backlinks/SKILL.md)** — Анализ ссылочной массы, токсичных доменов и анкор-листов.
- **[seo-local](skills/seo-local/SKILL.md)** — Оптимизация под локальную выдачу и карточки Google Business.
- **[seo-maps](skills/seo-maps/SKILL.md)** — Ранжирование в Google Maps и гео-сетки видимости.
- **[seo-ecommerce](skills/seo-ecommerce/SKILL.md)** — SEO для интернет-магазинов, товарных карточек и категорий.
- **[seo-drift](skills/seo-drift/SKILL.md)** — Автоматический мониторинг изменений и предотвращение деградации позиций.
- **[seo-plan](skills/seo-plan/SKILL.md)** — Разработка индивидуальной SEO-стратегии по типу бизнеса (SaaS, E-com, Local, B2B).
- **[seo-flow](skills/seo-flow/SKILL.md)** — Управление SEO-экспериментами по методологии FLOW.

### 6. API-интеграции (опциональные)
- **[seo-google](skills/seo-google/SKILL.md)** — Прямое подключение к Google Search Console и PageSpeed API.
- **[seo-dataforseo](skills/seo-dataforseo/SKILL.md)** — Интеграция с базой DataForSEO для парсинга поисковой выдачи.

---

## 🛠️ Внутренние инструменты и утилиты

Встроенные скрипты запускаются через лаунчер:
```bash
bash skills/public/marketing/claude-seo/scripts/claude-seo run <script.py> [args]
```

Включает специализированные анализаторы:
- `scripts/pagespeed_check.py` — проверка PageSpeed & CrUX;
- `scripts/url_safety.py` — безопасный сбор контента страниц с защитой от SSRF и DNS-rebinding;
- `scripts/metadata_template.py` — генерация шаблонов разметки;
- `scripts/drift_compare.py` — выявление дрифта выдачи;
- `scripts/content_quality.py` — проверка глубины контента и E-E-A-T.
