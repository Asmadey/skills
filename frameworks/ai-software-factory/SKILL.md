---
name: ai-software-factory
description: Autonomous lights-out software engineering pipeline (Dark Factory). Takes an issue, checks against MISSION.md, plans, implements, verifies via isolated Judge and Holdout E2E tests, and merges without human review. Use when asked to set up a software factory, run autonomous issue-to-merge pipelines, or build verified software from specs.
---

# 🏭 AI Software Factory

## Назначение
Автономный конвейер разработки программного обеспечения («Dark Factory» / беспилотная фабрика софта).
Принимает задачу в виде GitHub Issue, верифицирует против `MISSION.md`, строит план, реализует код, тестирует через независимый `Judge` и скрытые тесты `Holdout E2E`, и вливает результат без ручной вычитки диффов.

## Архитектура конвейера (Pipeline)

```mermaid
flowchart TD
    Issue[GitHub Issue] --> Mission[Mission Gate / Scope Check]
    Mission --> Plan[factory-plan]
    Plan --> Implement[factory-implement]
    Implement --> Judge[factory-judge: Изолированный аудит]
    Judge --> Holdout[factory-holdout & factory-e2e]
    Holdout --> Merge[Auto-Merge & Closed Issue]
```

## Ключевые компоненты
1. **`MISSION.md`**: Что продукт делает и список вещей, чем он **никогда** не должен стать (Never-Build List для защиты от расползания скоупа).
2. **`harness/END-TO-END.md`**: Пользовательские сценарии (User Journeys) реального использования.
3. **`.factory/holdout/HOLDOUT.md`**: Скрытые инварианты и проверочные тесты, которые агент-строитель не может прочитать во время кодинга.
4. **Ролевая изоляция**: Судья (`factory-judge`) никогда не пишет код; Строитель (`factory-implement`) никогда сам себе не ставит оценку.

## Команды управления
- **Инициализация в проекте:**
  ```bash
  python skills/public/dev/ai-software-factory/bin/factory.py init
  ```
- **Проверка готовности (Pre-Flight Check):**
  ```bash
  python factory/doctor.py
  ```
- **Запуск цикла:**
  ```bash
  python skills/public/dev/ai-software-factory/bin/factory.py run
  ```

## Вложенные специализированные навыки (`template/.claude/skills/`)
- `factory-setup` — первичное интервью и подготовка 3 базовых файлов.
- `factory-prime` — загрузка контекста репозитория.
- `factory-plan` — декомпозиция задачи в план изменений.
- `factory-implement` — изолированное написание кода.
- `factory-judge` — беспристрастное ревью результата внешней моделью.
- `factory-review` — аудит качества и безопасности.
- `factory-fix` — точечное исправление замечаний судьи.
- `factory-holdout` & `factory-e2e` — запуск скрытых e2e проверок.
- `factory-triage` — маршрутизация входящих тикетов.
