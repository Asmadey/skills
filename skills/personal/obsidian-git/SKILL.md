---
name: obsidian-git
description: >-
  Синхронизация, версионирование и автоматический бэкап заметок Obsidian через Git.
  Позволяет инициализировать Git в хранилище (vault), настраивать плагин obsidian-git,
  конфигурировать защитный .gitignore, разрешать конфликты слияния в markdown-файлах,
  автоматизировать коммиты и пуши по расписанию, а также настраивать кросс-платформенную
  аутентификацию (macOS Keychain, SSH, GitHub PAT) и мобильную синхронизацию.
  Триггеры: использовать при запросах "obsidian git", "синхронизация obsidian", "бэкап obsidian в github",
  "конфликт git в obsidian", "настройка obsidian-git", /obsidian-git.
category: personal
source: https://github.com/Vinzent03/obsidian-git
version: 2.31.0
last_updated: 2026-09-06
---

# Obsidian Git (Автоматизация и синхронизация хранилища)

Комплексный навык для автоматического версионирования, резервного копирования и синхронизации заметок Obsidian через Git на Desktop (macOS/Linux/Windows) и Mobile (iOS/Android).

---

## 🚀 Быстрый старт (Инициализация нового хранилища)

Если у пользователя локальное хранилище Obsidian еще не подключено к Git:

1. **Создайте `.gitignore` в корне хранилища:**
   Скопируйте эталонный шаблон из `examples/vault.gitignore`. Он предотвращает засорение истории позициями вкладок (`workspace.json`) и кэшем графа.
   ```bash
   cp "${SKILL_DIR}/examples/vault.gitignore" /path/to/vault/.gitignore
   ```

2. **Инициализируйте репозиторий и сделайте первый коммит:**
   ```bash
   cd /path/to/vault
   git init -b main
   git add .
   git commit -m "feat: initial obsidian vault setup"
   ```

3. **Свяжите с удаленным репозиторием (GitHub/GitLab):**
   ```bash
   git remote add origin git@github.com:<username>/<my-notes-vault>.git
   git push -u origin main
   ```

---

## ⚙️ Рекомендуемая конфигурация плагина

Файл настроек плагина хранится по пути `.obsidian/plugins/obsidian-git/data.json`.
Готовый шаблон находится в `examples/plugin-config.json`:

* **Интервал автосохранения (`autoSaveInterval`):** `10` минут (коммит изменений).
* **Интервал автопуша (`autoPushInterval`):** `10` минут (отправка в remote).
* **Подтягивание при старте (`autoPullOnBoot`):** `true` (гарантирует получение правок с других устройств до начала работы).
* **Шаблон сообщения коммита:** `"vault backup: {{date}}"` с форматом даты `"YYYY-MM-DD HH:mm:ss"`.

---

## 🛠️ Рабочие процессы (Workflows)

### 1. Автономная синхронизация из терминала (без GUI Obsidian)
Используйте скрипт `scripts/vault_sync.sh` для быстрого фонового сохранения и пуша:
```bash
bash "${SKILL_DIR}/scripts/vault_sync.sh" /path/to/vault
```
*Скрипт проверяет статус, автоматически фиксирует локальные изменения с именем устройства и временем, делает `git pull --rebase` и пушит на сервер.*

---

### 2. Поиск и разрешение конфликтов Git в заметках
При одновременном редактировании на разных устройствах в тексте заметок могут появиться маркеры конфликтов (`<<<<<<< HEAD`, `=======`, `>>>>>>>`).

1. **Запустите сканер конфликтов:**
   ```bash
   python3 "${SKILL_DIR}/scripts/scan_conflicts.py" /path/to/vault
   ```
2. **Разрешите конфликт:**
   - Откройте указанные файлы.
   - Оставьте актуальный фрагмент мысли/заметки, объединив текст.
   - Удалите маркеры `<<<<<<<`, `=======`, `>>>>>>>`.
3. **Зафиксируйте слияние:**
   ```bash
   git add -A
   git commit -m "fix: resolve sync conflict in notes"
   git push origin main
   ```
Подробное руководство по конфликтам: `references/troubleshooting.md`.

---

### 3. Настройка беспарольного доступа (Credential Helper)
Если Obsidian зависает при pull/push, значит Git в фоне запрашивает пароль.
- **macOS:**
  ```bash
  git config --global credential.helper osxkeychain
  ```
- **Windows:**
  ```bash
  git config --global credential.helper manager
  ```
- **Linux:**
  ```bash
  git config --global credential.helper libsecret
  ```
Полная инструкция по ключам SSH и GitHub PAT доступна в `references/authentication.md`.

---

### 4. Особенности мобильных устройств (iOS & Android)
На смартфонах отсутствует нативный бинарник `git`, плагин работает через `isomorphic-git` в JavaScript.
- **Ограничения:** нет поддержки SSH (только HTTPS с токеном), возможны сбои при объеме хранилища > 300 МБ.
- **Надежная альтернатива на iOS:** использование приложения **Working Copy** для клонирования репозитория с последующим открытием хранилища в Obsidian через системный файловый менеджер.
Подробнее: `references/mobile-guide.md`.

---

## 📂 Структура вспомогательных ресурсов (L3)

- [`examples/vault.gitignore`](examples/vault.gitignore) — надежный фильтр временных файлов и кэша Obsidian.
- [`examples/plugin-config.json`](examples/plugin-config.json) — сбалансированный конфиг `data.json`.
- [`references/authentication.md`](references/authentication.md) — настройка Keychain, SSH и GitHub Personal Access Tokens.
- [`references/troubleshooting.md`](references/troubleshooting.md) — исправление ошибок `index.lock`, `xcrun`, вечных pull/push.
- [`references/mobile-guide.md`](references/mobile-guide.md) — особенности работы на iOS и Android.
- [`scripts/vault_sync.sh`](scripts/vault_sync.sh) — CLI-синхронизатор хранилища.
- [`scripts/scan_conflicts.py`](scripts/scan_conflicts.py) — сканер маркеров конфликтов в markdown-файлах.
