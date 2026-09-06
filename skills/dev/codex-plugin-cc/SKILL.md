---
name: codex-plugin-cc
description: Official OpenAI Codex CLI integration suite for agent environments. Orchestrates Codex runs, manages headless execution sessions, parses diffs and structured results, and enforces GPT-5.4 reasoning and prompt patterns. Use when asked to run tasks via Codex CLI, delegate coding subtasks to Codex, or structure prompts for advanced reasoning models.
---

# 🤖 OpenAI Codex CLI Suite (codex-plugin-cc)

## Назначение
Официальный интеграционный пакет OpenAI Codex CLI для агентных сред (Claude Code, Antigravity, Cursor).
Позволяет делегировать автономные задачи разработки в Codex CLI, изолированно управлять средой исполнения, парсить диффы и применять паттерны промптинга для флагманских моделей reasoning.

## Компоненты пакета

### 1. `codex-cli-runtime` (`skills/codex-cli-runtime/`)
- Управление фоновыми сессиями Codex CLI (`codex run`).
- Контроль таймаутов, потоков ввода-вывода и изоляции окружения.

### 2. `codex-result-handling` (`skills/codex-result-handling/`)
- Парсинг артефактов выполнения Codex.
- Валидация git-диффов и сгенерированного кода перед применением.

### 3. `gpt-5-4-prompting` (`skills/gpt-5-4-prompting/`)
- Официальные рецепты и блоки промптов для моделей с расширенным reasoning (`o-series`, `gpt-5.4`).
- Чек-листы защиты от анти-паттернов в агентных промптах.

## Быстрый запуск
Делегирование задачи в Codex CLI:
```bash
node skills/public/dev/codex-plugin-cc/scripts/run-codex.mjs --prompt "<task description>"
```
