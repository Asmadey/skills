---
name: watermarks-remover
description: >-
  Удаляет скрытые водяные знаки ИИ, цифровые маркеры прослеживаемости (provenance marks) и метаданные нейросетей из текста и файлов (изображения, документы, медиа). Очищает невидимый Unicode (Zero-Width Space, bidi-символы, гомоглифы), метаданные C2PA / Content Credentials, EXIF/XMP-маркеры генераторов (Midjourney, DALL-E, Stable Diffusion, Claude, ChatGPT, Gemini/SynthID).
  Триггеры: использовать при запросах на удаление водяных знаков ("watermark", "remove watermarks", "очисти водяные знаки", "удали водяной знак", "удали метаданные ИИ", "remove C2PA", "очисти невидимый Unicode", "очисти файл от следов ИИ", /remove-ai-marks, /watermarks-remover).
  Анти-триггеры: не использовать для обхода академической честности при сдаче экзаменационных работ, сокрытия нарушений авторских прав или работы с бинарными проприетарными базами данных.
category: tooling
source: https://github.com/guillaumemeyer/watermarks-remover
version: 0.7.0
---

# Watermarks Remover

Комплексный инструмент гигиены контента для удаления цифровых следов и водяных знаков ИИ (AI provenance marks) из **текста** (невидимый Unicode, стилометрические токены) и **файлов** (C2PA, EXIF, XMP, метаданные документов).

---

## 🎯 Три уровня очистки (Multi-Layer Protection)

| Уровень | Цель | Метод решения |
| :--- | :--- | :--- |
| **Layer A (Текст)** | Невидимый Unicode, скрытые пробелы нулевой ширины (ZWSP), bidi-изоляты, теги | Детерминированные Python-скрипты stdlib ([`clean_text.py`](./scripts/clean_text.py)) |
| **Layer B (Текст)** | Статистические маркеры (SynthID, Kirchenbauer, токенизация) | Стилометрический скоринг ([`score_stylometry.py`](./scripts/score_stylometry.py)) + рерайт |
| **Файлы & Медиа** | C2PA / Content Credentials, EXIF, XMP, свойства документов | Очистка контейнеров PNG, JPEG, WebP, PDF, DOCX, XLSX, PPTX ([`clean_file.py`](./scripts/clean_file.py)) |

---

## 🚀 Быстрый старт через CLI (Автономно, Python stdlib)

Все базовые скрипты работают на чистом Python 3.10+ без необходимости ставить внешние тяжелые библиотеки:

### 1. Инспекция и очистка текста (Layer A & B)

```bash
# Проверить текст на скрытый Unicode и стилометрию ИИ
python3 scripts/inspect_text.py draft.txt --stylometry

# Полный аудит подозрительных фрагментов без изменения файла
python3 scripts/inspect_text.py draft.txt --audit

# Очистить текст от невидимых символов и нормализовать пробелы
python3 scripts/clean_text.py draft.txt -o draft.cleaned.txt --stats
```

### 2. Очистка файлов и документов (Графика, PDF, Office)

```bash
# Проверить файл на наличие метаданных ИИ (C2PA, EXIF, генеративные теги)
python3 scripts/inspect_file.py image.png

# Очистить метаданные в файле (поддерживает PNG, JPEG, WebP, SVG, PDF, DOCX, XLSX, PPTX)
python3 scripts/clean_file.py document.pdf -o document.cleaned.pdf

# Очистить файл на месте (in-place)
python3 scripts/clean_file.py banner.png --in-place
```

---

## 🌐 Режим сервиса (Microservice HTTP API)

Для интеграции через API или работы как «тонкий клиент» доступен встроенный HTTP-сервер:

```bash
# Запуск локального сервера
python3 service/scripts/server.py --port 8765

# Проверка работоспособности
curl -sf http://127.0.0.1:8765/health

# Доступные возможности и бэкенды
curl -s http://127.0.0.1:8765/capabilities
```

### Эндпоинты API:
* `POST /inspect` — аудит файла (JSON с base64 содержимым).
* `POST /detect` — выявление меток водяных знаков.
* `POST /clean` — очистка файла и возврат чистого base64.

---

## 📚 Справочные материалы (References)

Подробная документация в каталоге [`references/`](./references/):
* [`references/mark-classes.md`](./references/mark-classes.md) — классификация меток: Unicode, C2PA, семплирование.
* [`references/vendor-notes.md`](./references/vendor-notes.md) — особенности меток Claude, OpenAI, Gemini/SynthID.
* [`references/removal-matrix.md`](./references/removal-matrix.md) — матрица очистки по типам файлов.
* [`references/detectors.md`](./references/detectors.md) — как работают ИИ-детекторы и их ограничения.
* [`references/ethics.md`](./references/ethics.md) — правила ответственного использования.
