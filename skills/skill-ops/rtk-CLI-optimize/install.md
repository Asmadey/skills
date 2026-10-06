# RTK (Rust Token Killer) — Руководство по установке и использованию

Высокопроизводительный CLI-прокси на Rust (<10 ms overhead), сокращающий до 90% консольного вывода (bash output), считываемого AI-агентами.

## Contents
- Обзор
- Установка
  - macOS (Homebrew)
  - Linux / macOS (Быстрая установка)
  - Windows (winget)
  - Сборка из исходников (Cargo)
  - Pre-built Binaries
- Проверка установки
- Интеграция с AI-агентами
  - Google Antigravity
  - Claude Code
  - Cursor
  - Другие агенты
- Ключевые рабочие процессы
  - 1. Прозрачный перехват (Auto-Rewrite Hook)
  - 2. Восстановление полного вывода при ошибках (Recall Loop)
  - 3. Ручные команды глубокой оптимизации
  - 4. Аналитика экономии токенов
- Конфигурация
- Удаление

---

## Обзор

RTK перехватывает вызовы команд оболочки и сжимает их вывод перед передачей в контекстное окно модели.

| Тип команд | Действие RTK |
|---|---|
| `ls` / `tree` | Компактное дерево с подсчётом файлов вместо полного листинга |
| `git status` / `git diff` | Сжатый статус по состояниям, урезание заголовков diff |
| `git add` / `commit` / `push` | Схлопывание прогресс-баров в краткий статус (`ok main`) |
| `npm test` / `pytest` / `cargo test` | Исключение успешных тестов, показ только сбоев (failures only) |
| `tsc` / `eslint` / `ruff` | Группировка диагностик по файлам и правилам |
| `docker ps` / `docker logs` | Фильтрация второстепенных полей, дедупликация строк логов |

---

## Установка

### macOS (Homebrew — рекомендуется)
```bash
brew install rtk
```

### Linux / macOS (Быстрая установка)
```bash
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
```
> Устанавливается в `~/.local/bin`. При необходимости добавьте путь в `~/.zshrc` или `~/.bashrc`:
> ```bash
> echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
> ```

### Windows (winget)
```powershell
winget install rtk-ai.rtk
```

### Сборка из исходников (Cargo)
```bash
cargo install --git https://github.com/rtk-ai/rtk
```
> Примечание: не используйте `cargo install rtk` без флага `--git`, так как на crates.io под этим именем зарегистрирован другой пакет.

### Pre-built Binaries
Прямые архивы доступны в [GitHub Releases](https://github.com/rtk-ai/rtk/releases):
* **macOS (Apple Silicon):** `rtk-aarch64-apple-darwin.tar.gz`
* **macOS (Intel):** `rtk-x86_64-apple-darwin.tar.gz`
* **Linux (x86_64):** `rtk-x86_64-unknown-linux-musl.tar.gz`
* **Windows (x86_64):** `rtk-x86_64-pc-windows-msvc.zip`

---

## Проверка установки

```bash
rtk --version   # Ожидаемый вывод: rtk 0.x.x
rtk gain        # Открывает дашборд статистики экономии токенов
```

---

## Интеграция с AI-агентами

RTK активируется через встроенные хуки без изменения привычного рабочего процесса.

### Google Antigravity
Создаёт правила в `.agents/rules/antigravity-rtk-rules.md` текущего проекта:
```bash
rtk init --agent antigravity
```

### Claude Code
Устанавливает глобальный бинарный PreToolUse хук:
```bash
rtk init -g
```

### Cursor
Настраивает глобальный `hooks.json`:
```bash
rtk init -g --agent cursor
```

### Другие агенты
```bash
rtk init -g --gemini          # Gemini CLI
rtk init -g --codex           # OpenAI Codex
rtk init -g --agent windsurf  # Windsurf
rtk init --agent cline        # Cline / Roo Code
rtk init --agent hermes       # Hermes
```

После инициализации перезапустите соответствующую среду разработки или CLI.

---

## Ключевые рабочие процессы

### 1. Прозрачный перехват (Auto-Rewrite Hook)
После инициализации хук перехватывает стандартные вызовы Bash и неявно выполняет эквивалент RTK:
* Команда `git status` прозрачно выполняется как `rtk git status`.
* Команда `cargo test` выполняется как `rtk cargo test`.
Агент получает сжатый ответ без ручного набора префикса `rtk`.

### 2. Восстановление полного вывода при ошибках (Recall Loop)
Если команда завершается с ошибкой, RTK сохраняет полный нефильтрованный вывод в локальное хранилище и выводит идентификатор:
```text
FAILED: 2/15 tests
[full output: rtk recall 3f9c2a81d4e7]
```

**Workflow агента:**
1. Ознакомиться со сжатым отчётом об ошибке.
2. Если контекста недостаточно для диагностики, запросить полный вывод:
   ```bash
   rtk recall 3f9c2a81d4e7
   ```

### 3. Ручные команды глубокой оптимизации
Команды, полезные для точечного анализа кода с минимальным расходом контекста:

```bash
# Чтение файла только с сигнатурами типов и функций (без тел функций)
rtk read path/to/file.ts -l aggressive

# Быстрое 2-строчное эвристическое резюме структуры файла
rtk smart path/to/file.rs

# Компактное представление файловой структуры
rtk ls .

# Сгруппированный поиск без лишнего шума
rtk grep "functionName" .

# Сжатый diff между файлами
rtk diff file1.py file2.py
```

### 4. Аналитика экономии токенов

```bash
rtk gain                        # Сводка сэкономленных токенов
rtk gain --graph                # ASCII-график за последние 30 дней
rtk gain --history              # История последних оптимизированных команд
rtk discover                    # Поиск пропущенных возможностей оптимизации
```

---

## Конфигурация

Файл конфигурации:
* **macOS:** `~/Library/Application Support/rtk/config.toml`
* **Linux:** `~/.config/rtk/config.toml`

Пример настройки:
```toml
[hooks]
# Исключение команд из автоматической перезаписи
exclude_commands = ["curl", "playwright"]

[retriever]
# Режим сохранения полных логов: "sqlite" (по умолчанию), "tee" или "disabled"
mode = "sqlite"

[telemetry]
# Телеметрия отключена по умолчанию
enabled = false
```

---

## Удаление

```bash
# 1. Удаление хуков и правил интеграций
rtk init -g --uninstall

# 2. Удаление бинарника
brew uninstall rtk       # если устанавливался через Homebrew
cargo uninstall rtk      # если устанавливался через Cargo
rm ~/.local/bin/rtk      # если устанавливался через curl-скрипт
```
