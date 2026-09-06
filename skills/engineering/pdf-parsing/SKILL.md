---
name: PDF Parsing Skill
description: Извлекает текст из PDF файлов и сохраняет его в формате Markdown с помощью библиотеки PyPDF2.
category: automation
source: local
version: 1.0.0
last_updated: 2026-02-18
created: 2026-02-08
---

# PDF Parsing Skill

## 1. When to use
- При необходимости получить текстовое содержимое из PDF документа.
- При автоматизации процессов обработки документов для последующего анализа AI агентами.

## 2. Validation & Prerequisites
- [ ] Установлен Python 3.10+
- [ ] Установлена библиотека `PyPDF2`: `pip install PyPDF2`

## 3. Workflow (Checklist)
- [ ] Шаг 1: Подготовить путь к PDF файлу.
- [ ] Шаг 2: Запустить скрипт парсинга.
- [ ] Шаг 3: Проверить созданный .md файл в той же директории.

## 4. Instructions (Degrees of Freedom)
### Heuristics (High Freedom)
- Скрипт сохраняет результат в ту же папку, где лежит исходный файл.
- Текст извлекается постранично и объединяется.

### Templates (Low Freedom)
```bash
# Запуск парсинга
python skills/pdf-parsing/scripts/parse_pdf.py path/to/document.pdf
```

## 5. Resources
- `scripts/parse_pdf.py`: Основной скрипт парсинга.
