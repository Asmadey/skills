---
name: cinematic-landing
description: "Эталонный архитектурный шаблон иммерсивных лендингов PersonalOS (Cinematic Component Architecture — чемпион Arena Duel 2 a008). Синтезирует пространственную глубину и скролл-таймлайн (scroll-craft) с модульными UI-компонентами и Bento-сетками (magicui, shadcn, Tailwind). Применять при разработке премиальных посадочных страниц, продуктовых презентаций и витрин."
category: design
version: 1.0.0
metadata:
  champion_protocol: "Arena Duel 2 (a008 Systems Thinking & Edge Cases First)"
  framework: "Next.js / React / Tailwind CSS / Vanilla Scrollcraft Engine"
  total_templates: 4
---

# 🎬 Cinematic Component Architecture (PersonalOS Landing Suite)

Эталонная фронтенд-архитектура иммерсивных веб-интерфейсов, синтезирующая кинематографическую глубину **scroll-craft** с компонентной надежностью и доступностью **magicui** и **shadcn**.

Победитель турнира **Arena Duel 2** (решение `a008`), набравший 96/100 баллов за счет идеального решения краевых случаев мобильных браузеров, отсутствия скролл-джекинга и аппаратного ускорения 60 FPS.

---

## 🏛️ 3-уровневая архитектура

```
PersonalOS Landing Architecture
├── Layer 0: Scrubber Core (useScrollcraft / CSS transforms)
│   ├── Viewport Scrubber Timeline (t: 0 -> 1)
│   └── 4 Depth Planes (Backdrop, Subject, Foreground, Atmosphere)
├── Layer 1: Component Substrate (Tailwind CSS Tokens)
│   ├── Spacing floor, HSL color tokens, typography scales
│   └── High-contrast ratio > 7:1
└── Layer 2: Interactive Actors (magicui + shadcn)
    ├── Dimensional Hero Scene (Border Beam + Depth Anchor)
    ├── Feature Matrix: Dynamic Bento Grid
    ├── Proof Strip: Animated High-Agency Metrics
    └── Conversion Anchor: Interactive Command Center (CTA)
```

---

## 🛡️ Железные правила архитектуры (Hard Rules)

1. **Запрет скролл-джекинга (Zero Scroll-Jacking):**  
   Запрещен любой перехват нативного скролла (`preventDefault` на wheel / touchmove). Браузерный скролл — единственный источник таймлайна.
2. **Безопасная мобильная высота (`100dvh`):**  
   Используется только динамическая высота `100dvh`, исключающая рывки и перерисовку интерфейса при появлении адресной строки на iOS Safari и Android Chrome.
3. **Аппаратное ускорение (GPU-only):**  
   Анимации скролла анимируют только `transform: translate3d(x, y, 0)` и `opacity`. Никаких расчетов `top`, `margin`, `width` в цикле скролла.
4. **WAI-ARIA и Reduced Motion:**  
   При `@media (prefers-reduced-motion: reduce)` все параллакс-смещения отключаются мгновенно, выводя выверенную статичную композицию. Все интерактивные элементы полностью доступны с клавиатуры.

---

## 📦 Поставляемые шаблоны и компоненты

В каталоге `template/` доступны готовые компоненты:
1. `useScrollcraft.ts` — легковесный React-хук для связывания скролл-прогресса без внешних тяжелых библиотек.
2. `CinematicHero.tsx` — 4-слойный Hero-экран с Border Beam и пространственным параллаксом.
3. `BentoFeatures.tsx` — компонентная сетка возможностей в стиле MagicUI с интерактивными микро-анимациями.
4. `demo.html` — самодостаточный интерактивный прототип, открываемый в браузере в один клик.
