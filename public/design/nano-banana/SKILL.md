---
name: nano-banana
description: "Профессиональная генерация и мультимодальное редактирование гиперреалистичных изображений через Google Gemini 3 Pro (Nano Banana). Поддерживает Text-to-Image с физикой оптики (85mm, ISO 200, поры кожи, анти-пластик), Image-to-Image и композицию до 14 файлов, разрешения до 4K и параметризованный JSON-промптинг. Используйте при запросах 'сгенерируй картинку', 'создай фото', 'отредактируй изображение', 'сделай коллаж', 'фотореалистичный портрет'. Отличие: прямой доступ к Gemini 3 Pro, встроенный Visual Review Gate и 13 правил борьбы с AI-пластиком."
metadata:
  category: generation
  version: 3.0.0
  last_updated: 2026-09-06
---

# Nano Banana Image Generation Master

Флагманский навык для генерации и редактирования изображений институционального качества на базе **Google Gemini 3 Pro Image (`gemini-3-pro-image-preview`)**. Навык сочетает прямой доступ к флагманской мультимодальной модели с глубоким промпт-инжинирингом (13 правил фотореализма, физика оптики, борьба с «пластиковым» видом) и строгим циклом контроля качества (Visual Review Gate).

---

## 1. Когда использовать

- **Генерация фотореалистичных кадров:** Портреты людей, макросъемка, уличная фотография, кинематографичные сцены без искусственной бьютификации.
- **Редактирование и перенос стиля (Image-to-Image):** Модификация существующих изображений, замена деталей, объединение до 14 фотографий в единую композицию.
- **Коллажи и многопанельные сетки:** Генерация сеток 2x2 с сохранением консистентности персонажа или объекта.
- **Negative Triggers:**
  - Не использовать для работы с чистым текстом, генерации кода или верстки HTML/CSS.
  - Не использовать, если пользователь просит текстовую диаграмму (Mermaid) или SVG-иконку.

---

## 2. Предварительные проверки (Pre-flight)

Перед запуском генерации агент проверяет:
- [ ] Наличие API-ключа в `config/.env` (`GEMINI_API_KEY`, `AI_GATEWAY_API_KEY` или `KIE_API_KEY`).
- [ ] Наличие Python-зависимостей: `python3 -c "import PIL, requests"` (для прямого Gemini: `pip install google-genai pillow requests`).
- [ ] Существование целевых директорий: `mkdir -p images/miscellaneous prompts/miscellaneous`.

---

## 3. Рабочий процесс (Workflows)

### Режим 1: Фотореализм по тексту (Text-to-Image)

Для фотографий людей или объектов всегда применяйте физику оптики камеры и флаг `--realistic` (или JSON-промпт):

```bash
python3 skills/nano-banana/scripts/generate_image.py \
  --prompt "candid portrait of a 30-year-old barista pouring coffee, natural skin texture, visible pores, uneven lighting" \
  --filename "images/portraits/barista.png" \
  --resolution 2K \
  --realistic
```

### Режим 2: Редактирование и композиция (Image-to-Image, до 14 файлов)

Передайте одно или несколько исходных изображений через флаги `-i`:

```bash
python3 skills/nano-banana/scripts/generate_image.py \
  --prompt "seamlessly place the character from image 1 into the cyberpunk street environment from image 2, matching neon rim lighting" \
  --input-image "images/character.png" \
  --input-image "images/environment.png" \
  --filename "images/edits/cyberpunk_composite.png" \
  --resolution 2K
```

### Режим 3: Структурированный JSON-промптинг (Dense / Grid)

Для максимального контроля используйте схему из `resources/master_prompt_reference.md`:

```bash
python3 skills/nano-banana/scripts/generate_image.py \
  --json-prompt "skills/nano-banana/examples/portrait_dense.json" \
  --filename "images/portraits/gym_selfie.png"
```

---

## 4. Контроль качества (Visual Review Gate)

После каждой генерации агент **ОБЯЗАН** открыть и проанализировать полученное изображение перед показом пользователю:

1. **Текстура кожи и реализм:** Нет ли воскового «пластикового» сглаживания или эффекта бьюти-фильтра? Видны ли естественные поры и микродетали?
2. **Анатомическая корректность:** Правильно ли сформированы пальцы, кисти рук, глаза, зубы и уши?
3. **Освещение и оптика:** Соответствуют ли тени, глубина резкости (bokeh) и физика света заявленному объективу?

> ⚠️ **Протокол повторной генерации (Rectification Loop):**
> Если проверка **НЕ ПРОЙДЕНА** $\rightarrow$ удалите бракованный файл, сформируйте новый промпт с явной формулой исправления и запустите повторную генерацию:
> ```
> Rectification of failed artifact: Correcting [ТОЧНАЯ_ОШИБКА, например: removed artificial smooth plastic skin and replaced with authentic pores and uneven skin tone]...
> ```

---

## 5. Организация ассетов в проекте

Все сгенерированные файлы сохраняются парами для обеспечения воспроизводимости:
- Изображение: `images/<категория>/<название>.png`
- Использованный промпт / JSON: `prompts/<категория>/<название>.json` (или `.txt`)

Если категорию определить сложно, используйте папку по умолчанию: `images/miscellaneous/`.

---

## 6. Справочные материалы (Level 3)

- **[resources/master_prompt_reference.md](resources/master_prompt_reference.md):** Полная схема JSON-промптинга (Dense Narrative, 2x2 Deep Grid, Image-to-Image).
- **[resources/knowledge_packets/prompting_rules.md](resources/knowledge_packets/prompting_rules.md):** 13 правил фотореализма, физика оптики (фокусное расстояние, апертура, ISO), негативный стек.
- **[scripts/tools/crop_image.py](scripts/tools/crop_image.py):** Утилита для точного кадрирования под нестандартные форматы (`16:9`, `4:5`, `9:16`).
- **[examples/](examples/):** Готовые примеры промптов (`portrait_dense.json`, `product_macro.json`, `multi_image_edit.json`).

---

## 7. Обработка ошибок

| Ошибка | Причина | Решение |
| :--- | :--- | :--- |
| `No API key found` | Отсутствуют ключи | Добавьте `GEMINI_API_KEY` в `skills/nano-banana/config/.env`. |
| `Too many input images` | Передано более 14 файлов | Ограничьте число входных изображений до 14. |
| `Primary provider failed` | Таймаут или лимит запросов | Скрипт автоматически пробует резервные бэкенды (Kie.ai или AI Gateway). |
