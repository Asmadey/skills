---
name: "rtk-cli-optimize"
description: "Оптимизация и сжатие консольного вывода CLI (bash output) до 90% для AI-агентов через утилиту RTK (Rust Token Killer). Триггеры: rtk, rtk recall, сжатие вывода, оптимизация cli, rtk-cli-optimize. Use when configuring RTK proxy, inspecting compressed errors with rtk recall, reading stripped code signatures with rtk read, or analyzing token savings with rtk gain."
category: "skill-ops"
version: "1.0.0"
---

# RTK CLI Optimizer

Высокопроизводительный CLI-прокси на Rust (<10 ms overhead), перехватывающий вывод терминала и сжимающий его до 90% перед передачей в контекст LLM.

## Contents
- Quick Start
- Workflow: Error Recall Loop
- Команды ручной оптимизации
- Установка и интеграция агентов

## Quick Start
RTK автоматически перехватывает bash-команды после установки хуков.
- Проверка версии и статуса: `rtk --version && rtk gain`

## Workflow: Error Recall Loop
1. Выполнить команду в шелле.
2. При падении команды RTK выводит компактный отчет: `[full output: rtk recall <id>]`.
3. Ознакомиться со сжатой причиной сбоя.
4. Если контекста недостаточно для исправления, запросить полный вывод:
   ```bash
   rtk recall <id>
   ```

## Команды ручной оптимизации
- Чтение только сигнатур функций и интерфейсов (без тел): `rtk read <file> -l aggressive`
- Эвристическое резюме файла (2 строки): `rtk smart <file>`
- Компактный список файлов: `rtk ls .`
- Аналитика экономии токенов: `rtk gain --graph`
- Поиск неоптимизированных вызовов: `rtk discover`

## Установка и интеграция агентов
Полное руководство по установке (`brew`, `curl`, `winget`) и настройке хуков для Google Antigravity, Claude Code, Cursor и других агентов приведено в [install.md](install.md).
