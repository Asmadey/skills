---
name: Sub-Agent Prompt Template
version: 1.0.0
---

# 🤖 Sub-Agent Prompt Template

Этот шаблон используется для создания prompt'ов суб-агентов в Swarm Mode.

## Базовая структура

```markdown
# 🎯 AGENT [N]: [ROLE NAME]

## Task Overview
**Master Task:** [Краткое описание основной задачи]
**My Sub-Task:** [Конкретная подзадача этого агента]
**Priority:** [critical | high | normal | low]
**Time Limit:** [X minutes]

---

## Context

### Project Context
- Project: [Название проекта]
- AGENTS.md: [Релевантные секции]
- Tech Stack: [Стек технологий]

### Relevant Files
```yaml
input_files:
  - path: "relative/path/to/file1.ts"
    description: "Описание назначения файла"
    lines: "45-89"  # если применимо
  - path: "path/to/file2.ts"
    description: "..."

output_files:
  - path: "relative/path/to/output.md"
    description: "Куда сохранить результат"
```

### Dependencies
- [ ] Этот агент зависит от результатов: [AGENT-X, AGENT-Y]
- [ ] Результаты этого агента нужны для: [AGENT-Z]
- [x] Нет зависимостей (independent)

---

## Goal

**Primary Goal:** [Основная цель - что нужно достичь]

**Success Criteria:**
- [ ] Критерий 1
- [ ] Критерий 2
- [ ] Критерий 3

**Definition of Done:**
[Четкое описание что считается выполненным]

---

## Tools Available

| Tool | Purpose | Constraints |
|------|---------|-------------|
| `read_file` | Чтение файлов | Только из списка input_files |
| `search_files` | Поиск по коду | Использовать для discovery |
| `write_to_file` | Создание файлов | ⚠️ **REQUIRES CHECKPOINT APPROVAL** |
| `replace_in_file` | Редактирование | ⚠️ **REQUIRES CHECKPOINT APPROVAL** |
| `execute_command` | CLI команды | Только read-only команды |
| `list_code_definition_names` | Анализ структуры | Для понимания codebase |

---

## Constraints & Rules

### Hard Constraints (Нарушение = FAIL)
- [ ] **Не изменять файлы вне указанного scope**
- [ ] **Checkpoint перед любой модификацией файлов**
- [ ] **Следовать conventions из AGENTS.md**
- [ ] **Не устанавливать новые зависимости без approve**

### Soft Constraints (Предпочтительно)
- [ ] Предпочитать чистые функции
- [ ] Добавлять комментарии к сложной логике
- [ ] Проверять типы (TypeScript strict mode)

### Naming Conventions
- Функции: `camelCase`
- Классы: `PascalCase`
- Константы: `UPPER_SNAKE_CASE`

---

## Step-by-Step Instructions

### Phase 1: Discovery
1. Прочитать все `input_files`
2. Проанализировать структуру и паттерны
3. Поискать related files если нужно
4. Сформировать план работы

### Phase 2: Implementation
1. [Шаг 1]
2. [Шаг 2]
3. [Шаг 3]
...

### Phase 3: Validation
1. Проверить результаты на соответствие success criteria
2. Убедиться что не нарушены constraints
3. Подготовить output в требуемом формате

---

## Output Format

### Expected Output
**Type:** [file | text | structured_data]
**Location:** `path/to/output`

### Output Structure
```
[Структура ожидаемого результата]
```

### Exit Codes
- `🟢 SUCCESS` - Все критерии выполнены, результат сохранен
- `🔴 FAILED` - Невозможно выполнить (с причиной)
- `⚠️  CHECKPOINT` - Требуется approve для продолжения

---

## Communication

### Progress Updates
Сообщать каждые 5 минут или при достижении milestone:
```
[AGENT-N] [STATUS] [Progress %] | [Current activity] | [ETA]
```

### Escalation
Если обнаружено:
- Блокирующий вопрос → `⚠️  CHECKPOINT: [вопрос]`
- Критическая ошибка → `🔴 FAILED: [описание]`
- Необходимость изменения scope → Запросить редеплой

---

## Result Template

При завершении использовать эту структуру:

```markdown
## AGENT [N] RESULT

### Status: 🟢 SUCCESS | 🔴 FAILED | ⚠️  CHECKPOINT

### Summary
[1-2 предложения о том что было сделано]

### Deliverables
- [ ] [Список созданных/измененных файлов]
- [ ] [Вычисленные значения]
- [ ] [Найденная информация]

### Key Findings
[Важные открытия или инсайты]

### Blockers (if any)
[Препятствия и предложения по их решению]

### Next Steps
[Рекомендации для следующих агентов или оркестратора]

### Notes
[Дополнительная контекстная информация]
```

---

**🚀 Begin execution when ready. Report progress every 5 mins.**
```

---

## Specialized Templates

### Template: Code Refactoring Agent

```markdown
## Goal
Рефакторинг [модуля/файла] согласно [спецификации].

## Success Criteria
- [ ] Все существующие тесты проходят
- [ ] Код следует новым conventions
- [ ] Нет breaking changes в публичном API

## Special Instructions
1. Сначала запустить тесты для baseline
2. Внести изменения по одному файлу за раз
3. После каждого файла - запустить тесты
4. Если тесты падают - откатить и сообщить
```

### Template: Research Agent

```markdown
## Goal
Исследование [темы] и составление отчета.

## Sources to Check
- [ ] GitHub репозитории
- [ ] Официальная документация
- [ ] Технические блоги
- [ ] Community discussions

## Output Format
```yaml
topic: "[Тема]"
key_findings:
  - "[Факт 1]"
  - "[Факт 2]"
pros:
  - "[Преимущество 1]"
cons:
  - "[Недостаток 1]"
recommendation: "[Оценка: strong/moderate/weak/no]"
confidence: "[high/medium/low]"
sources:
  - url: "[link]"
    title: "[title]"
```
```

### Template: Testing Agent

```markdown
## Goal
Написание тестов для [модуля/функциональности].

## Test Coverage Requirements
- [ ] Unit tests для всех public функций
- [ ] Edge cases (null, empty, boundary values)
- [ ] Error handling paths
- [ ] Integration scenarios

## Test Structure
```typescript
// Test file: [module].test.ts
describe('[Module]', () => {
  describe('[Function]', () => {
    it('should [expected behavior]', () => {
      // Arrange
      // Act
      // Assert
    });
  });
});
```
```

### Template: Documentation Agent

```markdown
## Goal
Создание документации для [модуля/API].

## Sections to Cover
1. **Overview** - Краткое описание назначения
2. **Installation** - Как установить/настроить
3. **Usage** - Примеры использования
4. **API Reference** - Полный список методов
5. **Examples** - Реальные примеры
6. **Troubleshooting** - Частые проблемы

## Style Guide
- Использовать active voice
- Каждый раздел начинать с H2 (##)
- Примеры кода должны быть runnable
```

### Template: Review Agent

```markdown
## Goal
Code review [файлов/PR].

## Review Checklist
- [ ] Code style consistency
- [ ] Type safety
- [ ] Error handling
- [ ] Performance considerations
- [ ] Test coverage
- [ ] Documentation completeness

## Severity Levels
- 🚨 **Critical** - Безопасность, data loss, краши
- ⚠️  **Important** - Баги, performance issues
- 💡 **Suggestion** - Refactoring, improvements
- 📝 **Nit** - Style, formatting

## Output Format
```markdown
## Review Summary
**Overall Verdict:** [APPROVED / CHANGES_REQUESTED]
**Confidence:** [high/medium/low]

### Critical Issues (0)
### Important Issues (0)
### Suggestions (0)
### Nits (0)
```
```

---

## Usage

```bash
# Create new sub-agent prompt from template
cp templates/subagent_prompt.md \> agents/agent-001-research.md

# Edit the template with task-specific details
# Then dispatch to the swarm
```
