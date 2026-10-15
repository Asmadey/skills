---
name: impeccable
description: "Система профессионального дизайн-руководства, анти-шаблонного аудита и полировки интерфейсов от Пола Бакауса (Paul Bakaus). 24 команды дизайн-инженерии: UX/UI аудит (/critique, /audit), устранение AI-slop паттернов (запрет дефолтного Inter, фиолетовых градиентов, бессмысленных вложенных карточек), калибровка характера интерфейса (/bolder, /quieter, /distill, /delight, /overdrive), предрелизный лоск (/polish, /harden), генерация стандартов PRODUCT.md и DESIGN.md (OKLCH токены). Синергия со scroll-craft, magicui, shadcn и cinematic-landing. Триггеры: 'impeccable', '/impeccable', 'дизайн аудит', 'улучши дизайн', 'убери ai slop', 'дизайн системы', 'polish ui', 'critique ui', 'bolder design', 'сделай красивый дизайн'."
category: design
author: Paul Bakaus (адаптировано для PersonalOS)
version: 4.5.2
---

# 🎨 Impeccable: Design Engineering & Anti-Slop System

Комплекс инженерного проектирования и аудита интерфейсов от **Пола Бакауса** (Paul Bakaus — создатель jQuery UI, ex-Google Web Stories). Переводит генерацию UI из режима «безопасного шаблонного ИИ-дизайна» в режим **Out-of-Distribution Craft** (авторский уровень арт-директора).

---

## 🚫 Главные антипаттерны AI-дизайна (AI-Slop Tells)

Impeccable искореняет 5 маркеров шаблонного ИИ-дизайна:
1. **Шрифт Inter повсюду:** заменяется осмысленными шрифтовыми парами под задачу продукта.
2. **Фиолетово-синие градиенты (Purple-to-Blue):** заменяются палитрами в пространстве **OKLCH** с физически точной яркостью.
3. **Бессмысленные карточки в карточках (Card-in-Card Nesting):** заменяются пространственным ритмом, отступами и линиями-разделителями.
4. **Серый неконтрастный текст (#666):** заменяется калиброванными ступенями контрастности (WCAG AAA).
5. **Одинаковые иконки в скругленных плашках:** заменяются акцентной типографикой и функциональными визуальными доминантами.

---

## 🏛️ Двухуровневый стандарт правды (Сценарий 2)

Перед созданием или масштабным рефакторингом интерфейса фиксируются два файла:

### 1. `PRODUCT.md` (Долговечная продуктовая правда)
Фиксирует бизнес-контекст, независимый от визуальных стилей:
- Целевая аудитория и ее реальный контекст использования.
- Проблема и ценностное предложение.
- Тон голоса (Voice & Tone) и продуктовые ограничения.
- Шаблон: [`reference/PRODUCT.template.md`](reference/PRODUCT.template.md).

### 2. `DESIGN.md` (Живая дизайн-система проекта)
Фиксирует визуальный фундамент интерфейса:
- Цветовые токены в пространстве **OKLCH** (Light/Dark темы, акценты, подложки).
- Типографическая шкала (Display, Heading, Body, Mono).
- Сетка, отступы и правила радиусов.
- Шаблон: [`reference/DESIGN.template.md`](reference/DESIGN.template.md).

---

## 🕹️ 24 Дизайн-команды Impeccable

Вызываются через ментальную модель `/impeccable <command> [target]`:

| Команда | Категория | Описание | Руководство |
| :--- | :--- | :--- | :--- |
| **`init`** | Build | Первичный сбор продуктовой правды и генерация `PRODUCT.md` | [reference/init.md](reference/init.md) |
| **`shape`** | Build | Проектирование информационной архитектуры и UX до кода | [reference/shape.md](reference/shape.md) |
| **`document`**| Build | Извлечение дизайн-системы из существующего кода в `DESIGN.md` | [reference/document.md](reference/document.md) |
| **`extract`** | Build | Выделение переиспользуемых токенов и компонентов | [reference/extract.md](reference/extract.md) |
| **`critique`**| Evaluate | Экспертный UX-аудит (иерархия, сканируемость, когнитивная нагрузка) | [reference/critique.md](reference/critique.md) |
| **`audit`** | Evaluate | Технический аудит качества (a11y контраст, производительность, адаптив) | [reference/audit.md](reference/audit.md) |
| **`polish`** | Refine | Финальный лоск, микровыравнивание отступов и готовность к релизу | [reference/polish.md](reference/polish.md) |
| **`bolder`** | Refine | Усиление смелости: выразительный контраст, масштабные заголовки | [reference/bolder.md](reference/bolder.md) |
| **`quieter`**| Refine | Снижение визуального шума и агрессивных акцентов | [reference/quieter.md](reference/quieter.md) |
| **`distill`**| Refine | Очистка до голой сути: удаление декоративного мусора | [reference/distill.md](reference/distill.md) |
| **`harden`** | Refine | Стресс-тест верстки: длинный текст, ошибки, переполнение, i18n | [reference/harden.md](reference/harden.md) |
| **`onboard`**| Refine | Проектирование первого экрана, пустых состояний (empty states) | [reference/onboard.md](reference/onboard.md) |
| **`animate`**| Enhance | Добавление осмысленного движения, микро-анимаций и переходов | [reference/animate.md](reference/animate.md) |
| **`colorize`**| Enhance | Внедрение стратегической палитры вместо монохромной скуки | [reference/colorize.md](reference/colorize.md) |
| **`typeset`** | Enhance | Настройка типографической иерархии, кернинга и подбора гарнитур | [reference/typeset.md](reference/typeset.md) |
| **`layout`** | Enhance | Исправление ритма сетки, выравнивания и дыхания блоков | [reference/layout.md](reference/layout.md) |
| **`delight`** | Enhance | Добавление запоминающихся микродеталей и приятных микровзаимодействий | [reference/delight.md](reference/delight.md) |
| **`overdrive`**| Enhance | Прорывные технологические эффекты (шейдеры, кинематика) | [reference/overdrive.md](reference/overdrive.md) |
| **`clarify`**| Fix | Редактура интерфейсного текста, подсказок и сообщений об ошибках | [reference/clarify.md](reference/clarify.md) |
| **`adapt`** | Fix | Глубокая адаптация под мобильные устройства и разные экраны | [reference/adapt.md](reference/adapt.md) |
| **`optimize`**| Fix | Диагностика и устранение тормозов рендеринга и тяжелых стилей | [reference/optimize.md](reference/optimize.md) |
| **`live`** | Iterate | Интерактивный подбор вариантов компонентов в браузере | [reference/live.md](reference/live.md) |

---

## ⚡ Синергия с экосистемой PersonalOS (Сценарий 3)

В PersonalOS навык `impeccable` выполняет роль **Верховного Дизайн-Арбитра**, дополняя компоненты и анимации:

1. **`cinematic-landing` + `scroll-craft`:**
   - `scroll-craft` обеспечивает физику скролла и пространственную глубину (3D/Canvas).
   - `impeccable /critique` и `/polish` верифицируют, чтобы анимации не заслоняли контент и не снижали конверсию.
2. **`shadcn` + `magicui`:**
   - Компоненты shadcn стилизуются через токены `DESIGN.md` (OKLCH).
   - `impeccable /harden` проверяет все состояния (`disabled`, `loading`, `empty`, `error`).
3. **`high-agency-design`:**
   - Использование шкал Variance, Intensity, Density согласуется с командами `/bolder` и `/quieter`.

---

## 📋 Пошаговый протокол работы агента

1. **Инициализация:** Запроси продуктовый скоуп и зафиксируй базовые токены (`PRODUCT.md` и `DESIGN.md`).
2. **Планирование (`/shape`):** Определи визуальный мир и сетку до написания кода.
3. **Исполнение:** Напиши интерфейс с опорой на токены.
4. **Аудит качества (`/critique` + `/audit`):**
   - Обязательно прочитай [reference/craft-floor.md](reference/craft-floor.md) перед правками.
   - Проверь контраст, адаптив и отсутствие шаблонных карточек в карточках.
5. **Финальный лоск (`/polish`):** Проверь микро-выравнивание, плавность скруглений и типографику.
