---
name: Ars Contexta — Knowledge Graph Engine
description: Генерирует полную когнитивную архитектуру для агентов: vault из markdown-файлов, processing pipeline (6 Rs), automation hooks, MOC-навигация. Использовать когда нужно: создать personal knowledge system, запустить /setup для нового vault, обработать новые источники через /reduce → /reflect → /reweave, выполнить диагностику vault через /health.
category: knowledge
source: https://github.com/cognitivecomputations/arscontexta
version: 0.8.0
last_updated: 2026-02-21
---

# Ars Contexta — «Второй мозг» для агента

## 1. Когда использовать

- Создание нового personal knowledge system (vault) → запустить setup
- Обработка новых источников (статьи, видео, заметки) → pipeline
- Поиск связей между старыми заметками → `/reflect`
- Диагностика/починка vault → `/health`
- Переопрос архитектуры с нуля → `/reseed`

## 2. Структура этого skill

```
skills/arscontexta/
├── SKILL.md              ← этот файл
├── README.md             ← полная документация
├── skills/               ← 10 команд плагина
│   ├── setup/SKILL.md    ← ГЛАВНЫЙ: 76KB движок деривации
│   ├── health/           ← диагностика
│   ├── ask/              ← запрос к 249 research claims
│   ├── recommend/        ← советы по архитектуре
│   └── ...
├── skill-sources/        ← 16 шаблонов генерируемых команд
│   ├── reduce/           ← Extract insights
│   ├── reflect/          ← Find connections
│   ├── reweave/          ← Backward pass
│   └── ...
├── methodology/          ← 249 research claims (backing all decisions)
├── reference/
│   ├── kernel.yaml       ← 15 kernel primitives
│   ├── use-case-presets.md
│   └── three-spaces.md
└── generators/           ← Feature blocks для генерации CLAUDE.md
```

## 3. Как запустить Setup

Setup-движок живёт в `skills/arscontexta/skills/setup/SKILL.md`. Для запуска:

*1.* Прочитай setup SKILL.md целиком
```
Файл: skills/arscontexta/skills/setup/SKILL.md
```

*2.* Прочитай все reference files (указаны в начале SKILL.md)
- `reference/kernel.yaml`
- `reference/interaction-constraints.md`
- `reference/failure-modes.md`
- `reference/vocabulary-transforms.md`
- `reference/personality-layer.md`
- `reference/three-spaces.md`
- `reference/use-case-presets.md`
- `reference/conversation-patterns.md`

*3.* Определи платформу
Для PersonalOS: `.claude/` не существует → **platform = "minimal"**
Это означает: context file = `README.md` вместо `CLAUDE.md`, skills в `knowledge/.claude/skills/` опционально.

*4.* Пройди все 6 фаз setup
Phase 1 (Detection) → Phase 1.5 (Onboarding screens) → Phase 2 (2-4 вопроса) → Phase 3 (Derivation, internal) → Phase 4 (Proposal) → Phase 5 (Generation) → Phase 6 (Validation)

**Целевая директория vault:** `/Users/asmadey/PersonalOS/knowledge/`

## 4. Processing Pipeline (6 Rs)

После setup доступны команды (шаблоны в `skill-sources/`):

| Команда | Фаза | Описание |
|---------|------|----------|
| capture в inbox/ | Record | Zero-friction захват |
| `/reduce` | Reduce | Извлечение insights из источника |
| `/reflect` | Reflect | Поиск связей, обновление MOCs |
| `/reweave` | Reweave | Обновление старых заметок новым контекстом |
| `/verify` | Verify | Проверка качества (description + schema + health) |
| `/rethink` | Rethink | Ревизия архитектурных предположений |

**Принцип свежего контекста:** каждая фаза запускается как subagent (`/ralph N` для N задач).

## 5. Three-Space Architecture

Каждый vault разделён на три пространства (имена адаптируются к домену):

| Space | Назначение | Рост |
|-------|-----------|------|
| `self/` | Идентичность агента, методология | Медленный |
| `notes/` | Knowledge graph | Постоянный (10-50/неделю) |
| `ops/` | Задачи, очереди, сессии | Переменный |

## 6. Kernel Primitives

Все 15 primitives обязательны в каждом vault (см. `reference/kernel.yaml`):
prose-as-title, wiki-links, inbox, inbox-routing, three-spaces, moc-hierarchy, description-field, schema-blocks, maintenance-conditions, self-space, discovery-first, operational-learning-loop, archive-structure, methodology-folder, pipeline-compliance

## 7. Heuristics

- Всегда читай `self/` в начале сессии
- НИКОГДА не пиши напрямую в `notes/` — только через `inbox/`
- При >200 заметках нужен semantic search (`qmd`)
- Vocab: используй слова пользователя, не preset-термины
