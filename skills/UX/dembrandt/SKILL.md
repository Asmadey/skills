---
name: dembrandt
description: "Комплексный инженерный комплекс UX-аудита, реверс-инжиниринга дизайн-систем и экстракции токенов (Dembrandt Suite by VictorGjn). Объединяет 45 специализированных навыков (дизайн-системы, W3C Design Tokens DTCG, WCAG 2.2 accessibility, эвристики Нильсена, layout, тайпографика, цвета, микроинтеракции) и headless-движок Dembrandt с MCP-сервером для снятия токенов с живых сайтов (Playwright/Chromium). Триггеры: 'dembrandt', 'extract design', 'clone website', 'ux audit', 'design review', 'design tokens', 'nielsen heuristics', 'wcag accessibility', 'color palette', 'type scale'."
category: UX
version: 0.39.2
source: https://github.com/dembrandt/dembrandt
license: MIT
metadata:
  author: VictorGjn
  category: UX
  total_skills: 45
  engine: dembrandt
  mcp_server: dembrandt
---

# 🎨 Dembrandt Suite — Enterprise UX & Design System Engine

**Extract any website's design system in one command. Enforce UX excellence across your apps.**

Инженерный комплекс от **VictorGjn**, объединяющий:
1. **Движок экстракции Dembrandt (`engine/`)** — CLI и MCP-сервер на базе Playwright/Chromium, извлекающий W3C дизайн-токены (DTCG), цветовые палитры, масштабы шрифтов и отступов, тени, скругления и компоненты с любых сайтов.
2. **Библиотеку из 45 UX-навыков (`skills/`)** — экспертные правила продуктового дизайна, верстки, компонентной консистентности, эвристик Нильсена и доступности WCAG 2.2.

---

## 🧭 Стартовая точка и маршрутизация

| Задача | Рекомендуемый навык |
|---|---|
| Комплексный UX/UI аудит экрана или сценария | **[dembrandt](skills/dembrandt/SKILL.md)** (главный оркестратор) |
| Снятие дизайн-токенов с живого URL | **[extract-design](skills/extract-design/SKILL.md)** (через MCP/CLI) |
| Пиксель-в-пиксель воссоздание сайта (1:1) | **[clone-website](skills/clone-website/SKILL.md)** |
| Построение дизайн-системы из брендбука | **[generate-ui-from-brand](skills/generate-ui-from-brand/SKILL.md)** |
| Проверка доступности и контраста | **[wcag-accessibility](skills/wcag-accessibility/SKILL.md)** |
| Алгоритмическая генерация палитры | **[algorithmic-color-palette](skills/algorithmic-color-palette/SKILL.md)** |
| Модульная типографическая шкала | **[modular-scale-typography](skills/modular-scale-typography/SKILL.md)** |
| Аудит эвристик юзабилити Нильсена | **[nielsen-usability-heuristics](skills/nielsen-usability-heuristics/SKILL.md)** |

---

## ⚡ Движок экстракции и MCP-сервер (`engine/`)

### 1. Запуск через CLI
Движок запускается напрямую через npx или локальный скрипт:
```bash
# Извлечение дизайн-системы с выводом в консоль
npx -y dembrandt <url>

# Экспорт темы для shadcn/ui
npx -y dembrandt <url> --shadcn

# Экспорт токенов в формате W3C Design Tokens (DTCG)
npx -y dembrandt <url> --dtcg

# Аудит контрастности WCAG 2.1
npx -y dembrandt <url> --wcag

# Захват состояния сессии (cookies / auth)
npx -y dembrandt <url> --login --save-storage-state auth.json
```

### 2. MCP-сервер (`.mcp.json`)
В директории настроен запуск MCP-сервера:
```json
{
  "mcpServers": {
    "dembrandt": {
      "command": "npx",
      "args": ["-y", "dembrandt@0.39.2", "mcp"]
    }
  }
}
```

**Доступные MCP-инструменты:**
- `get_design_tokens` — полный W3C снимок дизайн-системы;
- `get_color_palette` — семантические роли цветов и палитра;
- `get_typography` — шрифтовые семьи, размеры, веса и URL файлов шрифтов;
- `get_spacing` — шкала внутренних и внешних отступов;
- `get_component_styles` — стили кнопок, инпутов, бейджей и ссылок;
- `export_shadcn` — генерация готовой темы `globals.css` для shadcn/ui;
- `export_tailwind` — блок `@theme` для Tailwind CSS v4;
- `compute_drift` — скоринг дрифта (0–100) между эталоном и текущей страницей;
- `check_contrast` — проверка контраста пар цветов по WCAG 2.1.

---

## 📦 Каталог 45 UX-навыков

### 1. Бренд и Визуальная идентичность
- **[brand-visual-language](skills/brand-visual-language/SKILL.md)** — геометрия форм, стиль иконок, тональность шрифтов.
- **[color-mode-and-theme](skills/color-mode-and-theme/SKILL.md)** — Light / Dark режимы, системная тема и переключатели.
- **[marketing-vs-product-system](skills/marketing-vs-product-system/SKILL.md)** — разделение лендинга и интерфейса сервиса без дрифта.
- **[authentic-product-representation](skills/authentic-product-representation/SKILL.md)** — честная демонстрация продукта без фейковых мокапов.

### 2. Дизайн-токены и Масштабы
- **[algorithmic-color-palette](skills/algorithmic-color-palette/SKILL.md)** — построение палитры и состояний из одного бренд-цвета.
- **[modular-scale-typography](skills/modular-scale-typography/SKILL.md)** — гармоничный модульный масштаб шрифтов.
- **[sizing-units](skills/sizing-units/SKILL.md)** — rem vs px vs %, адаптивные единицы измерения.
- **[status-colors-and-errors](skills/status-colors-and-errors/SKILL.md)** — семантика успеха, предупреждений и критических ошибок.

### 3. Структура, Макеты и Поверхности
- **[layout-paradigms-and-consistency](skills/layout-paradigms-and-consistency/SKILL.md)** — сетки, фреймворк продуктового нарратива.
- **[app-shell](skills/app-shell/SKILL.md)** — анатомия рабочего стола приложения (сайдбар, хедер, рабочая область).
- **[elevation-and-depth](skills/elevation-and-depth/SKILL.md)** — уровни теней, слои z-index и глубина интерфейса.
- **[surface-separation](skills/surface-separation/SKILL.md)** — контрастное разделение блоков без визуального шума.
- **[sticky-and-fixed-elements](skills/sticky-and-fixed-elements/SKILL.md)** — фиксированные панели, липкие заголовки и оверлеи.
- **[scroll-areas](skills/scroll-areas/SKILL.md)** — управление виртуальным скроллом и бесконечными списками.
- **[ui-density](skills/ui-density/SKILL.md)** — баланс плотности интерфейса (compact vs comfortable).

### 4. Навигация и Оверлеи
- **[tab-navigation](skills/tab-navigation/SKILL.md)** — вкладки, сохранение состояния и доступность с клавиатуры.
- **[modal-and-overlay-patterns](skills/modal-and-overlay-patterns/SKILL.md)** — выбор между Modal, Drawer, Sheet и Popover.
- **[global-toolbar-controls](skills/global-toolbar-controls/SKILL.md)** — глобальные панели управления и быстрые действия.
- **[user-flows-and-guided-paths](skills/user-flows-and-guided-paths/SKILL.md)** — многошаговые визарды, онбординг и воронки.
- **[information-architecture](skills/information-architecture/SKILL.md)** — ментальные модели и группировка разделов.

### 5. Компоненты и Формы
- **[button-states](skills/button-states/SKILL.md)** — полный цикл состояний кнопок (hover, active, focus-visible, disabled, loading).
- **[form-design](skills/form-design/SKILL.md)** — эргономика форм, валидация на лету, группировка fieldset.
- **[component-family-consistency](skills/component-family-consistency/SKILL.md)** — единство радиусов, бордеров и типографики контролов.
- **[data-display-and-selection](skills/data-display-and-selection/SKILL.md)** — таблицы, карточки, фильтры и множественный выбор.
- **[coordinated-data-views](skills/coordinated-data-views/SKILL.md)** — синхронизация списков и детальных карточек.
- **[repeated-component-alignment](skills/repeated-component-alignment/SKILL.md)** — идеальное выравнивание в повторяющихся списках.

### 6. Доступность, Скорость и Юзабилити
- **[wcag-accessibility](skills/wcag-accessibility/SKILL.md)** — строгое соответствие WCAG 2.2 AA (фокус, контраст, ARIA).
- **[nielsen-usability-heuristics](skills/nielsen-usability-heuristics/SKILL.md)** — проверка по 10 эвристикам Якоба Нильсена.
- **[loading-states-and-perceived-performance](skills/loading-states-and-perceived-performance/SKILL.md)** — скелетоны, оптимистичный UI и спиннеры.
- **[notifications-and-recovery](skills/notifications-and-recovery/SKILL.md)** — понятные ошибки с путями восстановления данных.
- **[performance-and-web-vitals](skills/performance-and-web-vitals/SKILL.md)** — Core Web Vitals и оптимизация отрисовки.
- **[semantic-html-and-seo](skills/semantic-html-and-seo/SKILL.md)** — корректные теги HTML5 для доступности и индексации.
- **[micro-interactions](skills/micro-interactions/SKILL.md)** — микроанимации и тактильный отклик интерфейса.
- **[gestalt-ui-organisation](skills/gestalt-ui-organisation/SKILL.md)** — гештальт-законы близости, сходства и непрерывности.
- **[visual-emphasis-and-hierarchy](skills/visual-emphasis-and-hierarchy/SKILL.md)** — управление вниманием пользователя на первом экране.
