---
name: deck-craft
description: "Система создания автономных интерактивных веб-презентаций и слайд-деков в стиле Varick Agents (Single-File Zero-Dependency HTML5). Поддерживает фиксированный 16:9 стейдж, субслайды и пошаговую анимацию (#X.Y Stops & Beats), встроенную типографику Switzer/Chivo Mono, Bento-сетки, интерактивные диаграммы Венна и управление с клавиатуры/свайпов. Применять при запросах: создать веб-презентацию, слайды в стиле varick, интерактивный deck, презентация на HTML/CSS."
category: design
version: 1.0.0
metadata:
  framework: "Zero-Dependency Single-File HTML5 / Vanilla JS / CSS Grid"
  aspect_ratio: "16:9 (1920x1080 / auto-scaling)"
  addressing: "Hierarchical Hash Routing (#Slide.Beat)"
---

# 📽️ Deck-Craft: High-Agency Web Presentations (Varick Architecture)

Комплексный инженерный стандарт создания автономных интерактивных слайд-деков на чистом HTML5/CSS/JS без внешних рантайм-зависимостей (React, Reveal.js или Marp). 

Воспроизводит архитектуру вирусных презентаций **Varick Agents** (`dont-apply-ai`): глубокий контрастный темный интерфейс, техническая типографика, фиксированный 16:9 холст с автоматическим масштабированием под любой экран, пошаговое раскрытие смыслов (**Stops & Beats**) и прямая URL-адресация микрошагов (`#13.4`, `#14.6`, `#15.5`).

---

## 🏛️ Архитектурные принципы (Core Pillars)

1. **Zero-Dependency Single-File HTML:**
   - Вся презентация упаковывается в один `.html` файл. 
   - Никаких внешних npm-пакетов, сборщиков или CDN. Работает локально через `file://` и открывается мгновенно.
2. **Иерархическая адресация шагов (`#Slide.Beat`):**
   - Каждый экран — это `<section class="scr">` (номер `Slide`).
   - Внутри секции элементы размечаются атрибутом `data-b="N"` (номер `Beat`).
   - URL-хэш вида `#14.6` позволяет делиться ссылкой на конкретную фазу раскрытия мысли или слайда.
3. **Механика «Stops & Beats» (Progressive Disclosure):**
   - `data-stops="1,4,6"` задает точки останова.
   - Нажатие `→` (или `Space`) запускает автоматический каскадный проигрыш (stagger `420ms`) до следующего стопа, где колода ждет действия докладчика.
4. **Фиксированный 16:9 Stage с автоскейлом (`fitDeck`):**
   - Базовое разрешение сцены — `1920×1080` (или `1280×720`).
   - Скрипт пересчитывает масштаб по формуле:  
     `scale = Math.min(window.innerWidth / 1920, window.innerHeight / 1080)`
   - Идеальная геометрия без полос прокрутки и сдвигов макета на любом мониторе, проекторе или смартфоне.
5. **Типографическая пара и цветовая модель:**
   - **Заголовки:** Высокоплотный современный гротеск (Switzer, Plus Jakarta Sans или Geist).
   - **Метаданные, бейджи, счетчики:** Технический моноширинный шрифт (Chivo Mono или JetBrains Mono).
   - **Палитра:** Deep Off-Black (`#090a0f`), серая иерархия (`#7e8695`, `#f0f2f5`), строгие акцентные маркеры (Neon Blue, Emerald, Coral Red).

---

## 📐 Анатомия слайда (Slide Blueprint)

Каждый слайд строится по строгой семантической сетке:

```html
<section class="scr" id="s01" data-stops="2,4" data-stagger="420">
  <!-- Верхний бар метаданных -->
  <div class="head">
    <div class="meta">
      <span class="tag">01 / ARCHITECTURE</span>
      <span class="indicator">SYSTEMS FIRST</span>
    </div>
    <h1>The Real Process Is Never Written Down.</h1>
    <div class="sub">Interviews reveal the why. Agents on systems of record reveal the what.</div>
  </div>

  <!-- Рабочая область слайда (Bento, Buckets, Diagram, Table) -->
  <div class="area">
    <div class="grid-3">
      <div class="card" data-b="1">...</div>
      <div class="card" data-b="2">...</div>
      <div class="card" data-b="3">...</div>
    </div>
  </div>

  <!-- Нижняя смысловая сноска (Key takeaway / Source) -->
  <div class="foot">
    <div class="takeaway" data-b="4">A $12M firm and a $5B company. Same method, same four buckets.</div>
  </div>
</section>
```

---

## 🎨 4 Эталонных визуальных паттерна (Pattern Catalog)

1. **Process Buckets (Сортировочные корзины — `#13.4`):**
   - 4 колонки классификации шагов:
     - 🗑️ **Delete:** Шаги-паразиты (переспросы, дублирование, лишние согласования).
     - ⚙️ **Plain Code:** Детерминированные скрипты и вебхуки без AI.
     - 🤖 **Agents:** LLM-агенты для неструктурированных коммуникаций и исключений.
     - 👤 **Human:** Финальная подпись партнера и живое общение.
2. **Interactive Venn Diagram (Диаграмма Венна — `#14.6`):**
   - 3 пересекающихся SVG-круга (`Operator`, `Engineer`, `AI Engineer`).
   - Центральное пересечение активируется на финальном бите (`FDE / Forward Deployed Engineer`).
3. **Weekly Execution Grid (Календарный спринт — `#15.5`):**
   - 5-колоночная сетка дней (Mon–Fri) с пошаговым появлением задач.
4. **Bento Card Matrix:**
   - Сетка карточек с контрастными моно-бейджами `01`, `02`, `03` и микро-иконками в тонких линиях (`stroke-width: 1.5`).

---

## ⌨️ Горячие клавиши навигации (Engine Keybindings)

- `→` / `Space` / `PageDown` — следующий шаг (Beat) или слайд.
- `←` / `PageUp` — предыдущий шаг (Beat) или слайд.
- `Home` — перейти к титульному слайду (`#1.0`).
- `End` — перейти к финальному слайду.
- `F` — полноэкранный режим (Fullscreen toggle).
- `Touch Swipe` — свайп влево/вправо для планшетов и мобильных устройств.

---

## 🛠️ Быстрый старт и генерация

Эталонный шаблон и генератор находятся в:
- `template/deck-engine.html` — полный готовый каркас с движком.
- `scripts/generate-deck.py` — утилита компиляции Markdown в автономный HTML.

Для создания презентации скопируйте `template/deck-engine.html` или скомпилируйте через скрипт:
```bash
python3 skills/public/design/deck-craft/scripts/generate-deck.py my-presentation.md -o output.html
```
