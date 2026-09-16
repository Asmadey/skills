---
name: public-skills-sync
description: >-
  Синхронизирует проверенные навыки строго из папки skills/public/ в публичный внешний репозиторий https://github.com/Asmadey/skills.
  Автоматически переносит структуру навыков, обновляет каталоги INDEX.md, README.md и журнал changelog.md, формирует Conventional Commits и отправляет изменения в Git.
  Триггеры: "синхронизируй скилы", "обнови репозиторий skills", "обнови Asmadey/skills", "запушь навыки в паблик", "sync skills", "sync public skills", /sync-skills.
  Анти-триггеры: не использовать для приватных файлов PersonalOS вне папки public/, не применять к не-скилловым директориям.
category: skill-ops
source: https://github.com/Asmadey/skills
version: 1.0.0
metadata:
  category: skill-ops
  version: 1.0.0
  source: https://github.com/Asmadey/skills
---

# Public Skills Sync (Asmadey/skills)

Мета-навык для изолированной и детерминированной синхронизации публичных навыков из рабочей среды `PersonalOS` (`skills/public/`) во внешний открытый репозиторий [Asmadey/skills](https://github.com/Asmadey/skills) (`/Users/asmadey/AntiGravity/skills`).

---

## 🔒 Принцип строгой изоляции (Security Invariant)

- **Только `skills/public/`**: Навык сканирует и обрабатывает исключительно поддиректории папки `public/` по 13 стандартным категориям.
- **Никаких утечек**: Приватные конфигурации, `.env` файлы, артефакты PersonalOS, внутренние workflows и правила агентов гарантированно изолированы и не попадают во внешний репозиторий.
- **Фильтрация артефактов**: При копировании автоматически игнорируются `.DS_Store`, `__pycache__`, `.git`, `.pytest_cache`.

---

## 🚀 Быстрый запуск синхронизации

Основной исполняемый скрипт находится по пути:
`skills/public/skill-ops/public-skills-sync/scripts/sync_public_skills.py`

### 1. Предварительный просмотр изменений (Dry Run)
Показывает, какие навыки новые или модифицированы, без реальной записи на диск:
```bash
python3 skills/public/skill-ops/public-skills-sync/scripts/sync_public_skills.py --dry-run
```

### 2. Полная синхронизация файлов и документации
Копирует файлы навыков и обновляет реестры `INDEX.md`, `README.md`, `changelog.md` в репозитории `Asmadey/skills`:
```bash
python3 skills/public/skill-ops/public-skills-sync/scripts/sync_public_skills.py
```

### 3. Синхронизация с созданием Git-коммита
```bash
python3 skills/public/skill-ops/public-skills-sync/scripts/sync_public_skills.py --commit
```

### 4. Полный цикл (Sync + Commit + Push в GitHub)
```bash
python3 skills/public/skill-ops/public-skills-sync/scripts/sync_public_skills.py --commit --push
```

### 5. Точечная синхронизация одного навыка
```bash
python3 skills/public/skill-ops/public-skills-sync/scripts/sync_public_skills.py --skill ai/Langfuse --commit
```

---

## 📋 Автоматически обновляемые реестры в Asmadey/skills

При обнаружении новых или обновленных навыков скрипт автоматически актуализирует:

1. **`INDEX.md`**:
   - Пересчитывает общее количество активных навыков в шапке.
   - Обновляет дату `last_updated`.
   - Вставляет строчку навыка в таблицу соответствующей категории со ссылкой вида `[SKILL.md](skills/<category>/<name>/SKILL.md)`.

2. **`README.md`**:
   - Обновляет счетчик специализированных навыков.
   - Добавляет строку в каталог навыков соответствующего домена.

3. **`changelog.md`**:
   - Формирует датированную секцию `## [YYYY-MM-DD] — Синхронизация навыков из PersonalOS (public)`.
   - Добавляет карточки добавленных и обновленных навыков.

---

## 🤖 Пошаговый протокол агента

Когда пользователь просит обновить/запушить новые навыки в `Asmadey/skills`:

1. **Проверка диффа:**
   Выполнить с флагом `--dry-run` для анализа расхождений:
   ```bash
   python3 skills/public/skill-ops/public-skills-sync/scripts/sync_public_skills.py --dry-run
   ```

2. **Выполнение синхронизации и коммита:**
   ```bash
   python3 skills/public/skill-ops/public-skills-sync/scripts/sync_public_skills.py --commit
   ```

3. **Отправка в remote (при подтверждении / необходимости):**
   ```bash
   git -C /Users/asmadey/AntiGravity/skills push origin main
   ```

4. **Отчет пользователю:**
   Вывести список перенесенных навыков, обновленные файлы реестров и хеш коммита.
