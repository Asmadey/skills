# Static Banner Kit

AI-генератор рекламных баннеров для Meta, Instagram, TikTok.
Работает через Claude Code + Higgsfield API. Без дизайнера, без Figma, без Canva.

Ты говоришь Claude "сделай 10 баннеров для моего продукта" — он сам придумывает концепты, генерирует изображения и сохраняет готовые файлы.

---

## Что нужно перед началом

1. **Claude Code** — CLI от Anthropic. Если ещё нет: https://docs.anthropic.com/en/docs/claude-code
2. **Node.js 18+** — проверь: `node -v` в терминале. Если нет: https://nodejs.org
3. **Ключи Higgsfield Platform** — это API для генерации изображений:
   - Зайди на https://platform.higgsfield.ai
   - Зарегистрируйся
   - Перейди в раздел API Keys
   - Создай ключ — получишь `Key ID` и `Key Secret`

---

## Установка (5 минут)

### Шаг 1. Распакуй архив

Распакуй `static-banner-kit.zip` в любое место. Внутри:

```
static-banner-kit/
├── SKILL.md              # "Мозг" — инструкции для Claude
├── README.md             # Этот файл
├── .env.example          # Шаблон для API ключей
└── pipeline/
    ├── hf-api.mjs        # Код для общения с Higgsfield API
    └── generate-banners.mjs  # Шаблон скрипта генерации
```

### Шаг 2. Создай рабочую папку

Открой терминал и выполни:

```bash
# Создай папку проекта (имя любое)
mkdir my-banners
cd my-banners

# Скопируй файлы из kit
cp -r /путь/к/static-banner-kit/pipeline ./pipeline
cp /путь/к/static-banner-kit/.env.example ./.env
```

### Шаг 3. Впиши API ключи

Открой файл `.env` в любом текстовом редакторе и замени плейсхолдеры на свои ключи:

```
HF_KEY_ID=сюда_вставь_свой_key_id
HF_KEY_SECRET=сюда_вставь_свой_key_secret
```

### Шаг 4. Установи скилл для Claude Code

```bash
# Создай папку для скилла
mkdir -p .claude/skills/static-banner

# Скопируй скилл
cp /путь/к/static-banner-kit/SKILL.md .claude/skills/static-banner/SKILL.md
```

### Шаг 5. Готово! Запусти Claude Code

```bash
claude
```

---

## Как пользоваться

### Вариант A: Один баннер (интерактивно)

Открой Claude Code в папке проекта и напиши:

```
Создай баннер для моего продукта
```

Claude спросит:
- Что за продукт?
- Кто целевая аудитория?
- Какой стиль?
- Какой формат и CTA?

После ответов сгенерирует промпт и картинку.

### Вариант B: Пак баннеров (автоматически)

Напиши Claude:

```
Сделай пак из 10 баннеров для [описание продукта]. CTA: "Попробовать бесплатно". Формат: feed + stories.
```

Claude:
1. Придумает 10 концептов с разными scroll-stop механизмами
2. Покажет тебе на утверждение
3. Сгенерирует скрипт и запустит генерацию
4. Сохранит 20 картинок (10 баннеров x 2 формата) в папку `output/`

Каждый баннер ~30-60 секунд, весь пак ~10-15 минут.

### Вариант C: Ручной режим (без Claude)

Если хочешь сам контролировать промпты:

1. Открой `pipeline/generate-banners.mjs`
2. Замени `PACK_NAME` на имя своего пака
3. Заполни массив `BANNERS` своими промптами
4. Запусти: `node pipeline/generate-banners.mjs`
5. Результат в `output/имя-пака/`

---

## Примеры промптов, которые работают

Хороший промпт для баннера ВСЕГДА содержит:

```
[Описание визуала с ярким scroll-stop элементом].
Bold white text at top: "НАЗВАНИЕ БРЕНДА".
Large text: "Хук-фраза".
At the bottom: a bright teal rounded button with white bold text "CTA текст".
No watermarks, no AI labels.
```

Пример:

```
A hand holding a glowing golden ticket against a pure black background.
The ticket shimmers with metallic gold foil and emits warm radiant light.
The ticket reads: "YOUR PRODUCT — FREE ACCESS".
Golden sparkles float around the ticket.
Bold white text at top: "MY BRAND".
Large text: "Your golden ticket."
At the bottom: a bright teal rounded button with white bold text "Try for free".
High contrast gold on black. No watermarks, no AI labels.
```

---

## Какие баннеры работают, а какие нет

### Работает (яркие, контрастные, необычные):
- Неоновые объекты на чёрном фоне
- Лица с экстремальными эмоциями + вспышка камеры
- Горящие/рвущиеся предметы
- Сюрреальные сцены (человек под водой, космонавт)
- Яркие штампы/печати поверх портретов
- Разделённые пополам лица (до/после) с контрастным цветом
- Неоновые вывески в тёмных переулках

### НЕ работает (скучные, стоковые):
- Чистые студийные портреты с мягким светом
- Плоские раскладки предметов на столе
- Скриншоты переписок и постов
- Нейтральные тона без контраста
- Сложные UI дэшборды
- Стикеры и списки

---

## Модели для генерации

| Модель | Для чего | Текст на картинке |
|--------|----------|-------------------|
| `nano-banana-pro` | **Основная** — баннеры с текстом | Отличный |
| `nano-banana` | Быстрая генерация | Хороший |
| `flux-2` | Сложные сцены | Хороший |
| `reve` | UGC-стиль | Средний |
| `soul/standard` | Только портреты БЕЗ текста | Плохой |

**Правило:** если на баннере есть текст — всегда `nano-banana-pro`. Другие модели могут выдать нечитаемый текст.

---

## Форматы

| Формат | Соотношение | Где используется |
|--------|-------------|-----------------|
| Feed | 3:4 | Instagram/Facebook лента |
| Stories | 9:16 | Stories, Reels, TikTok |

Примечание: формат 4:5 не поддерживается API, используй 3:4 как замену.

---

## Структура проекта после установки

```
my-banners/
├── .claude/
│   └── skills/
│       └── static-banner/
│           └── SKILL.md          # Скилл (Claude читает его автоматически)
├── pipeline/
│   ├── hf-api.mjs                # API клиент (не трогай)
│   └── generate-banners.mjs      # Шаблон для батч-генерации
├── output/                       # Сюда сохраняются готовые баннеры
│   └── my-pack/
│       ├── 01-concept-feed.png
│       ├── 01-concept-stories.png
│       └── ...
├── .env                          # Твои API ключи (НЕ шарь этот файл!)
└── README.md
```

---

## FAQ

**Q: Сколько стоит генерация?**
A: Зависит от тарифа Higgsfield. Проверь на https://platform.higgsfield.ai/pricing

**Q: Можно без Higgsfield?**
A: Да. Скилл сгенерирует текстовые промпты, которые можно вставить в любой генератор: Midjourney, Nanobanana UI, Seedream, Krea, Flux.

**Q: Можно менять модель?**
A: Да. В скрипте замени `model: "nano-banana-pro"` на другую модель. Но для баннеров с текстом — только `nano-banana-pro`.

**Q: Баннер получился с кривым текстом — что делать?**
A: Перегенерируй (удали файл и запусти скрипт заново — он пропускает существующие). Или используй Nanobanana UI для ручной доработки текста.

**Q: Как отредактировать готовый баннер?**
A: Nanobanana2 — загрузи оригинал как reference, отметь что нужно изменить. Или Qwen Edit на wavespeed.ai.

---

## Требования

- Node.js 18+ (`node -v`)
- Claude Code CLI
- Ключи Higgsfield Platform API
- Никаких npm-зависимостей — всё работает из коробки
