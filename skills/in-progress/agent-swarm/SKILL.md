---
name: Agent Swarm
description: Orchestrate parallel agent execution for complex tasks using multi-agent decomposition. Supports both API-based Swarm (Kimi K2.5) and IDE-based Swarm Mode. Decomposes tasks into parallel subtasks, dispatches sub-agents (up to 100+), aggregates results. For complex research, code generation, multi-file refactoring, and data processing pipelines.
category: superpowers
type: workflow
version: 2.0.0
last_updated: 2026-02-18
requirements:
  - Python 3.10+ for API-based Swarm
  - IDE with agent support for IDE Swarm
  - Project with AGENTS.md structure
  - OpenAI/OpenRouter API key (for API Swarm)
degrees_of_freedom:
  high:
    - "Выбор режима: API Swarm vs IDE Swarm"
    - "Количество агентов (2-100+)"
    - "Стратегия агрегации: synthesize|merge|compare|vote"
    - "Набор инструментов для каждого агента"
  low:
    - "Структура sub-agent prompt"
    - "Формат финального отчета"
    - "Checkpoint перед destructive operations"
created: 2026-02-08
---

# 🐝 Agent Swarm

**Оркестрация параллельного выполнения задач через рой специализированных агентов.**

Этот skill объединяет два подхода:
1. **API Swarm** — Python-скрипты для автономной работы с Kimi K2.5/OpenRouter
2. **IDE Swarm Mode** — Интерактивное управление агентами в среде разработки

---

## 1. Quick Start

### Для пользователя IDE (Cline, Cursor, etc.)

```markdown
🐝 Запусти Swarm Mode: [описание задачи]
```

### Для API-использования (Python)

```python
from skills.agent_swarm.scripts.swarm_orchestrator import SwarmOrchestrator, ToolRegistry
from skills.agent_swarm.scripts.tools import register_all

async def main():
    registry = ToolRegistry()
    register_all(registry)  # Регистрируем инструменты
    
    orchestrator = SwarmOrchestrator(
        registry=registry,
        max_agents=10
    )
    
    result = await orchestrator.run(
        "Проведи анализ фреймворков для продакшена"
    )
    print(result["final_output"])

asyncio.run(main())
```

---

## 2. When to Use

✅ **Используй Agent Swarm когда:**
- Задача требует декомпозиции на 5+ независимых подзадач
- Нужен параллельный анализ (research, code review, testing)
- Работа с множеством файлов (refactoring, documentation)
- Сложные data pipelines
- Коллективная оценка или review

❌ **Не используй когда:**
- Линейная последовательность шагов
- Сильные зависимости между задачами
- Работа с чувствительными данными
- Маленькие задачи (< 15 минут)

---

## 3. Two Modes

### 3.1 Mode A: API Swarm (Autonomous)

**Use case:** Автономное выполнение без взаимодействия с пользователем

**Architecture:**
```
User Query
    ↓
[Orchestrator] → Decomposes into N sub-tasks
    ↓
[Sub-Agent 1] ──┐
[Sub-Agent 2] ──┼→ Parallel execution via API
[Sub-Agent N] ──┘
    ↓
[Synthesizer] → Aggregates results
    ↓
Final Output
```

**Requirements:**
- Python 3.10+
- `pip install openai aiohttp`
- API ключ в переменной окружения

### 3.2 Mode B: IDE Swarm Mode (Interactive)

**Use case:** Работа с IDE tools (read_file, replace_in_file, execute_command)

**Architecture:**
```
User Request
    ↓
[Orchestrator] → Analyzes & Plans
    ↓
Dispatches parallel agent sessions
    ↓
Agent 1: Research ──┐
Agent 2: Code ──────┼→ Each uses IDE tools
Agent 3: Tests ─────┘
    ↓
Real-time monitoring & aggregation
    ↓
Checkpoint approvals → Writes
    ↓
Final report
```

**Requirements:**
- IDE с поддержкой агентов (Cline, Cursor)
- AGENTS.md в проекте
- Файловый доступ

---

## 4. Three-Phase Workflow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   PLAN      │────→│  EXECUTE    │────→│  SYNTHESIZE │
│  (Orchestrate)    │  (Swarm)          │  (Aggregate)      │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Phase 1: Plan

**Декомпозиция задачи:**

```python
# API Swarm
agents = await orchestrator.decompose_task(
    user_query="Рефакторинг auth модуля",
    context={"tech_stack": "FastAPI"}
)
# → Returns: [SubAgent(role="models"), SubAgent(role="controllers"), ...]
```

**Структура sub-agent:**

```yaml
agent_id: "agent-001"
role: "Model Refactorer"
objective: "Переписать auth models на Pydantic v2"
tools: ["read_file", "replace_in_file", "search_files"]
context:
  files: ["auth/models.py", "auth/schemas.py"]
  conventions: "Use strict types"
priority: 8  # 1-10
timeout: 300  # seconds
```

### Phase 2: Execute

**API Swarm:**
```python
results = await asyncio.gather(*[
    orchestrator.execute_sub_agent(agent, shared_context)
    for agent in agents
])
```

**IDE Swarm:**
```
🐝 SWARM MODE ACTIVATED
═══════════════════════════════════════════════════════════
📋 Master Task: Рефакторинг auth модуля
⚡ Parallel Agents: 5
⏱️  Estimated Time: 15 minutes

───────────────────────────────────────────────────────────
🤖 AGENT [1/5]: Model Refactorer
   Scope: Переписать auth/models.py
   Status: 🟡 STARTING → 🔵 RUNNING → 🟢 COMPLETED
───────────────────────────────────────────────────────────
🤖 AGENT [2/5]: Controller Refactorer  
   Scope: Обновить auth/controllers.py
   Status: 🟡 STARTING → 🔵 RUNNING
...
```

**Status Indicators:**
- 🟡 STARTING — Инициализация
- 🔵 RUNNING — Выполнение
- 🟢 COMPLETED — Успех
- 🔴 FAILED — Ошибка
- ⚠️  CHECKPOINT — Точка синхронизации (требуется approve)

### Phase 3: Synthesize

**Стратегии агрегации:**

| Strategy | Use When | Output |
|----------|----------|--------|
| **SYNTHESIZE** | Нужен связный документ | Объединённый текст |
| **MERGE** | Списки данных | Объединённый список |
| **COMPARE** | Сравнение опций | Таблица сравнения |
| **VOTE** | Коллективная оценка | Средняя оценка + консенсус |

---

## 5. Tools & Capabilities

### API Swarm Tools

```python
# Регистрация инструментов
registry = ToolRegistry()

registry.register(
    name="web_search",
    description="Поиск в интернете",
    parameters={"query": "string", "max_results": "integer"},
    func=web_search
)

registry.register(
    name="execute_code",
    description="Выполнение кода",
    parameters={"code": "string", "language": "string"},
    func=execute_code
)

registry.register(
    name="read_file",
    description="Чтение файла",
    parameters={"file_path": "string"},
    func=read_file
)

registry.register(
    name="write_file",
    description="Запись файла",
    parameters={"file_path": "string", "content": "string"},
    func=write_file
)
```

### IDE Swarm Tools

| Tool | Purpose | Checkpoint |
|------|---------|------------|
| `read_file` | Чтение | Нет |
| `search_files` | Поиск | Нет |
| `list_files` | Листинг | Нет |
| `write_to_file` | Создание | ✅ Да |
| `replace_in_file` | Редактирование | ✅ Да |
| `execute_command` | CLI | Только read-only |

---

## 6. Configuration

### API Swarm Config

```yaml
# skills/agent-swarm/config.yaml
swarm:
  max_agents: 100
  max_parallel_tools: 1500
  default_timeout: 120
  aggregation_strategy: "synthesize"

models:
  default: "moonshotai/kimi-k2.5"
  fallback: "anthropic/claude-3.5-sonnet"
  
rate_limits:
  requests_per_minute: 60
  tokens_per_minute: 100000
  
tools:
  enabled:
    - web_search
    - execute_code
    - read_file
    - write_file
    
  config:
    web_search:
      provider: "serper"
      max_results: 10
      
    execute_code:
      sandbox: "e2b"
      timeout: 30
```

### Environment Variables

```bash
# API Swarm
export OPENROUTER_API_KEY="sk-or-v1-..."
export SERPER_API_KEY="..."

# IDE Swarm (optional)
export SWARM_MAX_AGENTS="50"
export SWARM_CHECKPOINT_MODE="interactive"  # or "auto"
```

---

## 7. Usage Examples

### Example 1: Code Refactoring

```python
from skills.agent_swarm.scripts.swarm_orchestrator import SwarmOrchestrator

async def refactor_auth_module():
    orchestrator = SwarmOrchestrator(max_agents=5)
    
    result = await orchestrator.run(
        user_query="""
        Рефакторинг auth модуля:
        1. Переписать models на Pydantic v2
        2. Обновить controllers для новых моделей  
        3. Адаптировать тесты
        4. Обновить документацию
        """
    )
    
    # Results
    for agent_result in result["agent_results"]:
        print(f"{agent_result['agent_id']}: {agent_result['status']}")
    
    print("\nFinal Output:")
    print(result["final_output"])
```

### Example 2: Technology Research

```python
async def research_llm_frameworks():
    orchestrator = SwarmOrchestrator(max_agents=8)
    
    result = await orchestrator.run(
        user_query="""
        Исследование LLM фреймворков для продакшена:
        - vLLM vs llama.cpp vs TGI
        - Производительность
        - Масштабируемость
        - Интеграция с FastAPI
        """
    )
    
    return result["final_output"]
```

### Example 3: IDE Swarm — Documentation Generation

```markdown
🐝 SWARM: Generate Documentation

AGENT-1 (API Reference):
└── Scope: docs/api/auth.md
└── Input: src/auth/*.py
└── Task: Сгенерировать API reference

AGENT-2 (Guide):
└── Scope: docs/guides/authentication.md
└── Input: examples/auth/, README.md
└── Task: How-to guide

AGENT-3 (Architecture):
└── Scope: docs/architecture/auth-flow.md
└── Input: src/auth/, docs/adr/
└── Task: Описание архитектуры

AGENT-4 (Troubleshooting):
└── Scope: docs/troubleshooting/auth.md
└── Input: src/auth/exceptions.py, issues/
└── Task: FAQ и troubleshooting

→ SYNTHESIZE: Полная документация
```

---

## 8. Sub-Agent Prompt Template

### Базовая структура

```markdown
# 🎯 AGENT [N]: [ROLE NAME]

## Task Overview
**Master Task:** [Описание основной задачи]
**My Sub-Task:** [Конкретная подзадача]
**Priority:** [critical | high | normal | low]
**Time Limit:** [X minutes]

---

## Context

### Project Context
- Project: [Название]
- AGENTS.md: [Релевантные секции]
- Tech Stack: [Стек]

### Relevant Files
```yaml
input_files:
  - path: "auth/models.py"
    description: "Модели аутентификации"
    lines: "1-150"

output_files:
  - path: "docs/api/auth.md"
    description: "Куда сохранить результат"
```

---

## Goal

**Primary Goal:** [Что нужно достичь]

**Success Criteria:**
- [ ] Критерий 1
- [ ] Критерий 2

**Definition of Done:**
[Четкое описание завершённости]

---

## Tools Available

| Tool | Purpose | Constraints |
|------|---------|-------------|
| `read_file` | Чтение | Только из input_files |
| `search_files` | Поиск | Для discovery |
| `replace_in_file` | Редактирование | ⚠️ Требует checkpoint |
| `execute_command` | CLI | Read-only |

---

## Constraints

### Hard Constraints
- [ ] Не изменять файлы вне scope
- [ ] Checkpoint перед writes
- [ ] Следовать AGENTS.md conventions

### Naming Conventions
- Функции: `camelCase`
- Классы: `PascalCase`
- Константы: `UPPER_SNAKE_CASE`

---

## Result Template

### Status: 🟢 SUCCESS | 🔴 FAILED | ⚠️ CHECKPOINT

### Summary
[1-2 предложения]

### Deliverables
- [ ] [Список созданного]

### Key Findings
[Важные открытия]

### Next Steps
[Рекомендации]
```

---

## 9. Best Practices

### High Freedom (Оркестратор решает)
- **Количество агентов:** 3-100, масштабируйте под задачу
- **Размер подзадачи:** 10-15 минут работы
- **Стратегия агрегации:** Автовыбор по типу задачи
- **Checkpoint:** Каждые 3-5 агентов

### Strict Rules
- **Prompt format:** Использовать структуру из раздела 8
- **Tool safety:** Никаких destructive операций без checkpoint
- **Idempotency:** Команды должны быть безопасны для повторного запуска
- **Error handling:** Graceful degradation

### Anti-Patterns
❌ Слишком много агентов (>100) — накладные расходы  
❌ Слишком крупные подзадачи — теряется параллелизм  
❌ Shared mutable state — race conditions  
❌ Нет checkpoint'ов — риск нежелательных изменений  
❌ Linear tasks in Swarm — используйте обычный режим

---

## 10. File Structure

```
skills/agent-swarm/
├── SKILL.md                 # This file
├── config.yaml              # Конфигурация Swarm
├── scripts/
│   ├── __init__.py
│   ├── swarm_orchestrator.py    # Ядро оркестратора
│   ├── tools.py                 # Реестр инструментов
│   └── async_utils.py           # Async helpers
├── templates/
│   └── subagent_prompt.md       # Шаблоны для агентов
└── examples/
    ├── refactoring_example.py
    ├── research_example.py
    └── documentation_example.py
```

---

## 11. Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Agents timeout | Увеличить `timeout` или разбить задачу |
| Rate limiting | Добавить delays, уменьшить `max_agents` |
| Conflicting changes | Использовать checkpoint approvals |
| Poor aggregation | Уточнить sub-task objectives |
| Too many agents | Оптимальное количество: 5-20 для большинства задач |

### Debug Mode

```python
# Включить verbose logging
orchestrator = SwarmOrchestrator(
    registry=registry,
    max_agents=10,
    debug=True  # Подробные логи
)
```

---

**🎯 Success Criteria:**
- [ ] Swarm завершился за предсказуемое время
- [ ] Все агенты вернули результаты
- [ ] Результаты агрегированы без потерь
- [ ] Конфликты разрешены
- [ ] Финальный отчёт предоставлен

---

## 12. Commands Reference

### API Swarm

```bash
# Установка зависимостей
pip install openai aiohttp pyyaml

# Запуск примера
python -m skills.agent_swarm.examples.research_example

# С кастомной конфигурацией
SWARM_CONFIG=custom.yaml python -m skills.agent_swarm.scripts.swarm_orchestrator
```

### IDE Swarm

```markdown
# Быстрый запуск
🐝 Запусти Swarm Mode: [задача]

# С параметрами
🐝 Swarm Mode:
- Task: Рефакторинг auth
- Agents: 5
- Strategy: synthesize
- Checkpoint: on_write
```
