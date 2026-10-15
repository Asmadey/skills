---
name: pm-claude-code-setup
description: "Система гибкого продуктового менеджмента (Lean PM System) по методологии Аакаша Гупты (Aakash Gupta). Включает написание компактных PRD по стадиям зрелости (от speclet до launch readiness), анализ конкурентов, формулирование метрик, подготовку к релизу, планирование спринтов и синтез пользовательских исследований. Триггеры: 'pm setup', 'aakash pm', 'напиши prd', 'lean prd', 'prd-writer', 'анализ конкурентов', 'launch checklist', 'user-research'."
category: product
version: 1.0.0
source: https://github.com/aakashg/pm-claude-code-setup
metadata:
  author: Aakash Gupta
  framework: Lean Product Management
---

# Lean PM System (Aakash Gupta)

Практическая система продуктового управления для AI-агентов от Аакаша Гупты (VP Product, Product Growth). Фокус на лаконичных документах высокой плотности («Think crisp, not complete»), живых PRD (2–3 страницы максимум) и практической координации команд.

## Содержание
- [Обзор и философия](#обзор-и-философия)
- [Каталог навыков](#каталог-навыков)
- [Шаблоны документов](#шаблоны-документов)
- [Контекст и правила продакта (references/pm-rules.md)](references/pm-rules.md)
- [Жизненный цикл PRD (6 стадий)](#жизненный-цикл-prd-6-стадий)

---

## Обзор и философия

1. **Лаконичность вместо водянистых томов:** Отказ от 10-страничных бюрократических PRD в пользу компактных документов с примерами и гипотезами.
2. **PRD для синхронизации, а не диктата:** Документ создается для открытых дебатов, выявления рисков и фиксации решений.
3. **Фокус на «Зачем» и «Что»:** Инженерная команда определяет «Как», продакт определяет контекст, проблему, метрики и границы скоупа.
4. **Итеративное созревание:** Документ развивается от параграфа-спеклетки до спецификации релиза.

---

## Каталог навыков

| Навык | Описание | Триггеры | Ссылка |
|---|---|---|---|
| **prd-writer** | Пошаговое составление компактного PRD с предварительным уточнением пробелов и адаптацией под стадию | `write a prd`, `draft a prd`, `spec out feature` | [SKILL.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/pm-claude-code-setup/skills/prd-writer/SKILL.md) |
| **competitive-analysis** | Анализ конкурентного ландшафта, дифференциация, feature parity и стратегические окна | `competitive analysis`, `compare competitors` | [SKILL.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/pm-claude-code-setup/skills/competitive-analysis/SKILL.md) |
| **metrics-definer** | Определение North Star, входных метрик, защитных (guardrail) показателей и телеметрии | `define metrics`, `kpi framework`, `guardrail metrics` | [SKILL.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/pm-claude-code-setup/skills/metrics-definer/SKILL.md) |
| **launch-checklist** | Комплексный чеклист готовности к запуску (GTM, QA, Support, Legal, Rollback) | `launch checklist`, `ready to launch`, `pre-launch review` | [SKILL.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/pm-claude-code-setup/skills/launch-checklist/SKILL.md) |
| **sprint-planner** | Декомпозиция инициатив на спринты, оценка емкости, зависимостей и рисков | `sprint planning`, `plan sprint`, `break down backlog` | [SKILL.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/pm-claude-code-setup/skills/sprint-planner/SKILL.md) |
| **user-research** | Синтез интервью, выявление паттернов JTBD, болевых точек и формулирование инсайтов | `synthesize interviews`, `user research`, `customer feedback` | [SKILL.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/pm-claude-code-setup/skills/user-research/SKILL.md) |

---

## Шаблоны документов

Готовые эталонные шаблоны находятся в директории `templates/`:
* [prd-template.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/pm-claude-code-setup/templates/prd-template.md) — компактная структура PRD (гипотеза, проблема, persona, user journey, scope, edge cases).
* [launch-plan.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/pm-claude-code-setup/templates/launch-plan.md) — операционный план вывода фичи на рынок.
* [okr-template.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/pm-claude-code-setup/templates/okr-template.md) — дерево Objective и измеримых Key Results.
* [sprint-review.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/pm-claude-code-setup/templates/sprint-review.md) — шаблон ретроспективы и демонстрации итогов спринта.

---

## Жизненный цикл PRD (6 стадий)

1. **Stage 1: Team Kickoff (Speclet)** — параграф с гипотезой проблемы и 2–3 открытыми вопросами для исследования с техлидом и дизайнером.
2. **Stage 2: Planning Review (1-Pager)** — одностраничник для руководства: стратегическое соответствие, первичные данные, оценка масштаба.
3. **Stage 3: XFN Kickoff** — синхронизация смежных отделов (Sales, Support, Legal, QA).
4. **Stage 4: Solution Review (Дефолт)** — проработанный PRD с пользовательскими сценариями, флоу и обработкой краевых случаев.
5. **Stage 5: Launch Readiness** — инженерная передача с детальной телеметрией, критериями приёмки и планом отката.
6. **Stage 6: Impact Review** — фиксация фактических результатов после релиза и извлечённых уроков.
