---
name: claude-obsidian
description: Official claude-obsidian knowledge system for Obsidian vaults. Turns sources into linked, source-grounded notes, answers from existing vault evidence, visualizes via Obsidian Canvas, and provides 15 specialized skills for vault research, retrieval, linting, and maintenance. Use when working with Obsidian vaults, creating connected knowledge bases, querying vault notes, or organizing personal knowledge.
---

# 🔮 Claude-Obsidian Knowledge Suite

## Назначение
Полнофункциональная локальная система управления знаниями для Obsidian.
Превращает сырые источники в структурированную сеть связанных заметок, проверяет факты по локальным утверждениям (claims ledger), создает визуальные карты знаний Obsidian Canvas и поддерживает здоровье хранилища.

## Доступные навыки (`skills/`)

| Навык | Назначение |
| :--- | :--- |
| [obsidian-markdown](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/personal/claude-obsidian/skills/obsidian-markdown/SKILL.md) | Стандарты разметки Obsidian: вики-ссылки `[[Note]]`, эмбеды `![[Note]]`, теги и коллауты |
| [canvas](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/personal/claude-obsidian/skills/canvas/SKILL.md) | Создание и редактирование интерактивных визуальных карт в формате Obsidian Canvas (`.canvas`) |
| [obsidian-bases](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/personal/claude-obsidian/skills/obsidian-bases/SKILL.md) | Управление метаданными, свойствами (properties) и YAML frontmatter заметок |
| [wiki](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/personal/claude-obsidian/skills/wiki/SKILL.md) | Построение архитектуры личной вики, карт содержания (MOC) и индексных хабов |
| [wiki-ingest](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/personal/claude-obsidian/skills/wiki-ingest/SKILL.md) | Конвейер захвата и нормализации внешних источников с сохранением первоисточника |
| [wiki-retrieve](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/personal/claude-obsidian/skills/wiki-retrieve/SKILL.md) | Поиск релевантных фактов и доказательств в хранилище с точным цитированием |
| [wiki-query](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/personal/claude-obsidian/skills/wiki-query/SKILL.md) | Структурированные запросы к локальному графу знаний и реестрам утверждений |
| [wiki-lint](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/personal/claude-obsidian/skills/wiki-lint/SKILL.md) | Линтинг хранилища: поиск битых ссылок, неразрешенных алиасов и изолированных страниц |
| [wiki-fold](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/personal/claude-obsidian/skills/wiki-fold/SKILL.md) | Синтез и сжатие разросшихся тем в плотные сводные заметки |
| [wiki-mode](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/personal/claude-obsidian/skills/wiki-mode/SKILL.md) | Интерактивная навигация и сессии исследования по материалам хранилища |
| [autoresearch](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/personal/claude-obsidian/skills/autoresearch/SKILL.md) | Автономное итеративное исследование предметной области по источникам в хранилище |
| [think](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/personal/claude-obsidian/skills/think/SKILL.md) | Аналитическое рассуждение с верификацией по claims ledger |
| [defuddle](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/personal/claude-obsidian/skills/defuddle/SKILL.md) | Очистка и структурирование сложных неструктурированных заметок и веб-статей |
| [save](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/personal/claude-obsidian/skills/save/SKILL.md) | Надежное сохранение артефактов в защищенный входящий накопитель (inbox) |
| [wiki-cli](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/personal/claude-obsidian/skills/wiki-cli/SKILL.md) | CLI-интерфейс для автоматизации рутинных операций над vault |

## Ключевые принципы
1. **Файлы остаются файлами:** Все артефакты сохраняются как стандартный Markdown и JSON, vault доступен без облачных блокировок.
2. **Опора на первоисточник (Evidence-Grounded):** Любое ключевое утверждение привязывается к первоисточнику в реестре свидетельств.
3. **Визуализация Canvas:** Сложные взаимосвязи отображаются не только текстовыми ссылками, но и готовыми холстами `.canvas`.
