---
name: technical-writer
description: "Комплексный инженерный комплекс технического писательства (Technical Writing Suite by riekelt). Включает 11 специализированных навыков: стандарты House Style и проверяемости фактов (Truth & Sourcing), подготовка RFC/Design Docs, ведение ADR (Architecture Decision Records), составление Runbooks, разбор аварий (Postmortems), документирование API-контрактов и легаси-систем. Триггеры: 'technical-writer', 'technical writing', 'rfc', 'design doc', 'adr', 'architecture decision', 'runbook', 'postmortem', 'api docs', 'документация архитектуры', 'напиши adr', 'составь rfc'."
category: dev
version: 1.8.4
source: https://github.com/riekelt/technical-writer
metadata:
  author: riekelt
  category: dev
  total_skills: 11
---

# Technical Writing Suite (riekelt)

Профессиональный инженерный фреймворк документирования кодовой базы и архитектурных процессов. 
Основан на принципе **верифицируемости и нулевых догадок**: документ описывает текущее, проверенное поведение («conclusion first»), каждое утверждение подтверждается ссылкой на источник (код, тест, коммит), а каждый факт имеет ровно один первоисточник («One fact, one home»).

## Содержание
- [Классификация документов](#классификация-документов)
- [Каталог 11 навыков](#каталог-11-навыков)
- [Базовые правила (Hard Rules)](#базовые-правила-hard-rules)
- [Субагенты и команды](#субагенты-и-команды)

---

## Классификация документов

Правило редактирования зависит от типа документа:

| Тип | Примеры | Правило редактирования |
|---|---|---|
| **Normative** | Архитектурные принципы, контракты, гайдлайны | Если код нарушает контракт, документ не размывают — фиксируют нарушение в кодовой базе. |
| **Descriptive** | Флоу, описания компонентов, стейт-машины | Обновляются строго в соответствии с реализацией в коде. |
| **Historical** | Чейнджлоги, решения (ADR), миграции | История неизменна. Ошибки не исправляются задним числом, создается новая датированная запись. |
| **Runbook** | Операции, траблшутинг, релизные чеклисты | Обновляются по фактической реальности; каждый шаг обязан быть реально выполнен. |
| **Reference** | API-документация, конфигурации, схемы | Исчерпывающий перечень: каждый ключ, каждый флаг с дефолтами и примерами. |

---

## Каталог 11 навыков

| Навык | Назначение | Триггеры | Ссылка |
|---|---|---|---|
| **technical-writing** | Базовый хаб: House Style, правила правдивости фактов (Truth & Sourcing) и запретные конструкции | `technical writing`, `техническая документация`, `house style` | [SKILL.md](skills/technical-writing/SKILL.md) |
| **writing-design-docs** | Создание RFC, Design Docs, архитектурных предложений и планов миграции | `design doc`, `rfc`, `write up approach`, `архитектурная спека` | [SKILL.md](skills/writing-design-docs/SKILL.md) |
| **recording-decisions** | Фиксация архитектурных решений в формате ADR и Decision Log | `adr`, `record decision`, `зафиксируй решение`, `архитектурное решение` | [SKILL.md](skills/recording-decisions/SKILL.md) |
| **writing-runbooks** | Эксплуатационная документация: Setup Guides, Runbooks, Troubleshooting и процедуры депрекации | `runbook`, `setup guide`, `инструкция эксплуатации`, `ранбук` | [SKILL.md](skills/writing-runbooks/SKILL.md) |
| **writing-postmortems** | Разбор инцидентов, аварий, root-cause analysis (безобвинительный формат, таймлайн фактов) | `postmortem`, `incident report`, `разбор инцидента`, `постмортем` | [SKILL.md](skills/writing-postmortems/SKILL.md) |
| **documenting-contracts** | Документирование API, DTO, очередей сообщений, форматов файлов и вебхуков | `api docs`, `document api`, `контракты api`, `документация эндпоинтов` | [SKILL.md](skills/documenting-contracts/SKILL.md) |
| **documenting-legacy-codebases** | Восстановление документации по унаследованному и легаси коду | `legacy docs`, `document legacy`, `восстанови документацию по коду` | [SKILL.md](skills/documenting-legacy-codebases/SKILL.md) |
| **diagramming-processes** | Проектирование процессов и стейт-машин в PlantUML / ArchiMate / Mermaid | `diagram process`, `state machine diagram`, `диаграмма процесса` | [SKILL.md](skills/diagramming-processes/SKILL.md) |
| **writing-changelogs** | Составление чейнджлогов и Release Notes по итогам выполненных работ | `changelog`, `release notes`, `что зарелизили`, `чейнджлог` | [SKILL.md](skills/writing-changelogs/SKILL.md) |
| **writing-issues** | Декомпозиция задач, Epics, Stories, баг-репорты с критериями приемки | `write issue`, `bug report`, `acceptance criteria`, `создай таску` | [SKILL.md](skills/writing-issues/SKILL.md) |
| **reviewing-technical-prose** | Финальный аудит и вычитка технического текста перед публикацией | `review prose`, `вычитай доку`, `проверь документацию` | [SKILL.md](skills/reviewing-technical-prose/SKILL.md) |

---

## Базовые правила (Hard Rules)

1. **Запрет выдумок (Evidence-based):** Никогда не утверждать как факт то, что нельзя подтвердить ссылкой на файл, строку кода, тест или коммит.
2. **Один факт — один источник (One fact, one home):** Документы не дублируют факты, а ссылаются на первоисточник.
3. **Неизменяемость принятых решений:** Принятые решения (ADR) и миграции не редактируются; исправления оформляются новой записью с отметкой `superseded`.
4. **Запрет нарративных статусов:** В теле технических документов не используются фразы о том, «в каком спринте это делалось» или «раньше было вот так». Документ описывает актуальное состояние.

---

## Субагенты и команды

В пакете доступны специализированные роли:
* **`doc-grounder`** ([agents/doc-grounder.md](agents/doc-grounder.md)) — субагент сверки документации с исходным кодом.
* **`prose-reviewer`** ([agents/prose-reviewer.md](agents/prose-reviewer.md)) — субагент стилистического и структурного аудита.
* Команды: `/ground-docs` ([commands/ground-docs.md](commands/ground-docs.md)) и `/prose-review` ([commands/prose-review.md](commands/prose-review.md)).
