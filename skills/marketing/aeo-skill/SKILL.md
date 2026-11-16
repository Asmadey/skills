---
name: aeo-skill
description: "Набор навыков SEO / AEO / GEO для вывода сайта в топ поиска и в ответы LLM (ChatGPT, Google AI Overviews и AI Mode, Gemini, Claude, Perplexity, Copilot): оркестратор /aeo, 11 под-навыков, 4 агента, скрипты проверки. Используй при запросах: аудит SEO/AEO/GEO, AI-видимость, «нас нет в ChatGPT», оптимизация под нейросети, цитирование в LLM, /aeo. Не используй для платной рекламы и для задач, не связанных с поисковой видимостью."
category: marketing
version: 1.0.0
license: MIT
metadata:
  author: Asmadey
  category: marketing
  total_skills: 12
  total_agents: 4
---

# AEO Skill: SEO / AEO / GEO

Набор устроен по образцу `claude-seo`: один оркестратор, под-навыки по направлениям, агенты для параллельного аудита, скрипты на стандартной библиотеке Python. База знаний — 920 материалов Search Engine Land за май–ноябрь 2026; в навык включён только пересказ выводов со ссылками на оригиналы ([реестр источников](skills/aeo/references/sources.md)).

## Стартовая точка

Для любой задачи открой оркестратор **[aeo](skills/aeo/SKILL.md)**: в нём таблица маршрутизации, порядок работы и формат результата.

| Команда | Что делает | Под-навык |
|---|---|---|
| `/aeo audit <url>` | Полный аудит: 7 блоков, оценка 0–100, план на 90 дней | [aeo-audit](skills/aeo-audit/SKILL.md) |
| `/aeo technical <url>` | Доступность для AI-ботов: robots.txt, CDN, JavaScript, сырой HTML, Bing, Brave | [aeo-technical](skills/aeo-technical/SKILL.md) |
| `/aeo content <url>` | Перестройка страницы под извлечение пассажей и цитирование | [aeo-content](skills/aeo-content/SKILL.md) |
| `/aeo entity <бренд>` | Распознавание бренда моделями, консистентность данных, schema | [aeo-entity](skills/aeo-entity/SKILL.md) |
| `/aeo offpage <бренд>` | Карта источников, digital PR, Reddit, YouTube, возражения | [aeo-offpage](skills/aeo-offpage/SKILL.md) |
| `/aeo visibility <бренд>` | Замер упоминаний, цитат и рекомендаций по набору промптов | [aeo-visibility](skills/aeo-visibility/SKILL.md) |
| `/aeo measure` | GA4, Search Console, Bing, логи, отчётность | [aeo-measure](skills/aeo-measure/SKILL.md) |
| `/aeo local <бизнес>` | Локальный бизнес и сети | [aeo-local](skills/aeo-local/SKILL.md) |
| `/aeo ecommerce <url>` | Фиды, карточки, категории, фильтры | [aeo-ecommerce](skills/aeo-ecommerce/SKILL.md) |
| `/aeo refresh <url>` | Диагноз падения трафика, обновление, чистка | [aeo-refresh](skills/aeo-refresh/SKILL.md) |
| `/aeo plan <бренд>` | Стратегия, кластеры, план на 90 дней | [aeo-plan](skills/aeo-plan/SKILL.md) |

## Справочники и скрипты

- [evidence-base](skills/aeo/references/evidence-base.md) — цифры исследований с ключами источников.
- [engines](skills/aeo/references/engines.md) — как устроены ChatGPT, Google AI, Gemini, Claude, Perplexity, Copilot.
- [myths](skills/aeo/references/myths.md) — что не работает и где данные расходятся.
- [scoring](skills/aeo/references/scoring.md) — методика оценки 0–100.
- [prompt-set](skills/aeo/references/prompt-set.md) — наборы промптов для замеров.

```bash
python3 skills/aeo/scripts/check_access.py https://example.com
python3 skills/aeo/scripts/page_audit.py https://example.com/page
python3 skills/aeo/scripts/log_bots.py access.log
python3 skills/aeo/scripts/visibility_tracker.py report
```

## Установка под-навыков как отдельных команд

```bash
bash install.sh      # копирует под-навыки в ~/.claude/skills и агентов в ~/.claude/agents
bash uninstall.sh    # переносит их в отдельную папку, ничего не стирая
```

## Проверка перед выдачей результата

- Каждая находка имеет доказательство и ключ источника `Sxxx`.
- Непроверенное помечено `НЕ ПРОВЕРЕНО`.
- Рекомендации сверены с `myths.md`.
