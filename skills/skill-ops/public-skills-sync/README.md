# Public Skills Sync (`public-skills-sync`)

Инструмент автоматической и изолированной синхронизации публичных навыков между персональной рабочей средой `PersonalOS` (`skills/public/`) и открытым репозиторием [Asmadey/skills](https://github.com/Asmadey/skills).

## Возможности

- **Строгая изоляция `skills/public/`**: обрабатывает только публично доступные навыки, защищая приватные модули и конфиги PersonalOS от случайной публикации.
- **Детекция изменений**: автоматически определяет новые и модифицированные навыки.
- **Автоматизация реестров**: синхронно актуализирует `INDEX.md`, `README.md` и `changelog.md` в целевом репозитории со ссылками на документацию.
- **Git автоматизация**: создает конвенциональные коммиты (`feat(<category>): ...`) и отправляет изменения в `origin main`.

## Использование

```bash
# Предпросмотр изменений без записи
python3 scripts/sync_public_skills.py --dry-run

# Синхронизация файлов и реестров
python3 scripts/sync_public_skills.py

# Синхронизация с созданием коммита в Asmadey/skills
python3 scripts/sync_public_skills.py --commit

# Полный цикл с отправкой в GitHub
python3 scripts/sync_public_skills.py --commit --push
```
