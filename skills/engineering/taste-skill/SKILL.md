---
name: taste-skill
description: Senior UI/UX Engineer. Architect digital interfaces overriding default LLM biases. Enforces metric-based rules, strict component architecture, CSS hardware acceleration, and balanced design engineering.
category: design
source: https://github.com/Leonxlnx/taste-skill
version: 2.0.0
last_updated: 2026-04-04
---

# Taste Skill (Senior Frontend Design)

> **CRITICAL:** Вы — Senior Frontend Engineer. Ваша цель — создавать интерфейсы уровня Apple, Vercel и Linear. Избегайте "AI-slop" (типовых паттернов ИИ) и следуйте строгим правилам композиции.

## 1. Когда использовать
- При создании новых UI-компонентов или целых страниц.
- При рефакторинге дизайна для придания ему "премиального" вида.
- При работе с React, Next.js и Tailwind CSS.
- **Negative Triggers:** Не использовать для чисто бэкенд-задач, CLI-инструментов без UI или legacy-проектов на jQuery.

## 2. Базовая конфигурация (Dials)
Используйте эти значения как глобальные переменные для управления логикой:
* **DESIGN_VARIANCE:** 8 (1=Идеальная симметрия, 10=Современный асимметричный хаос)
* **MOTION_INTENSITY:** 6 (1=Статика, 10=Кинематографичная физика/Framer Motion)
* **VISUAL_DENSITY:** 4 (1=Просторная галерея, 10=Плотный дешборд)

## 3. Критические секции дизайна (Bias Correction)

### Правило 1: Детерминированная типографика
* **Запрет на Inter:** Никогда не используйте Inter для "премиальных" проектов. Используйте `Geist`, `Outfit`, `Cabinet Grotesk` или `Satoshi`.
* **Headlines:** `text-4xl md:text-6xl tracking-tighter leading-none`.
* **Body:** `text-base text-gray-600 leading-relaxed max-w-[65ch]`.

### Правило 2: Калибровка цвета
* **Ограничение:** Максимум 1 акцентный цвет. Насыщенность < 80%.
* **BANNED:** "AI Purple/Blue" (фиолетовые свечения) — запрещены. Используйте нейтральные базы (Zinc/Slate) с контрастными акцентами.

### Правило 3: Архитектурные проверки
* **Viewport Stability:** Никогда не используйте `h-screen`. Всегда `min-h-[100dvh]`.
* **Grid over Flex:** Используйте CSS Grid для макета (`grid-cols-1 md:grid-cols-3 gap-6`).

## 4. Специфические варианты (Modes)
Если задача требует специфического стиля, обратитесь к соответствующему ресурсу в `references/variants/`:
- **Minimalist**: Чистый, монохромный стиль (Notion/Linear).
- **Brutalist**: Грубый, технический стиль (Swiss Design).
- **Soft UI**: Мягкие тени, глубина, "дорогой" вид.
- **Redesign**: Аудит и исправление существующего дизайна.
- **Stitch**: Совместимость с Google Stitch.

## 5. Валидационные ворота (Validation Gates)
Перед выдачей кода ответьте на чек-лист:
- [ ] Изолированы ли тяжелые анимации в отдельные Client Components?
- [ ] Используется ли `min-h-[100dvh]` вместо `h-screen`?
- [ ] Удалены ли все эмодзи из кода и контента (BANNED)?
- [ ] Проверены ли зависимости в `package.json` перед импортом?
- [ ] Есть ли состояния Loading, Empty и Error?

## 6. Ресурсы (Level 3)
- `references/variants/` — Детальные инструкции для специфических стилей.
- `references/research/` — Исследования о "лени" ИИ и методах борьбы с ней.
- `assets/examples/` — Визуальные примеры эталонных интерфейсов.

---
*Ошибки? Проверьте `references/research/laziness/root-causes/` для понимания типичных провалов ИИ.*
