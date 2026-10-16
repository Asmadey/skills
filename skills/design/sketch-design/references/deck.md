# Сборка колоды · Deck Recipes

Практическое руководство и типовые рецепты слайдов для создания убедительных рукописных презентаций.

---

## 🍳 Рецепт 1: Сравнение «Было / Стало» (Две колонки)

Подходит для демонстрации антипаттерна и эффективного решения.

```html
<sk-slide tone="green" number="3">
  <sk-title number="3">Разделяй контекст</sk-title>

  <!-- Колонка 1: Антипаттерн (слева, x=160) -->
  <sk-box x="160" y="240" w="560" h="480" label="Один огромный диалог" tone="red" rot="-1">
    <p class="sk-heading" style="color: #b42318; margin-bottom: 20px;">Контекст размывается</p>
    <p class="sk-body" style="color: var(--sk-muted); margin-bottom: 24px;">
      В длинной сессии модель теряет исходные инструкции и накапливает галлюцинации.
    </p>
    <div style="display: flex; align-items: center; gap: 16px;">
      <sk-chip>45 сообщений</sk-chip>
      <sk-mark kind="cross"></sk-mark>
    </div>
    <sk-note style="margin-top: 30px; display: block;">«память начинает шуметь»</sk-note>
  </sk-box>

  <!-- Колонка 2: Решение (справа, x=880, появляется на step="1") -->
  <sk-box x="880" y="240" w="560" h="480" label="Короткие итерации" tone="green" line="green" rot="1" step="1">
    <p class="sk-heading" style="color: #2b7a4b; margin-bottom: 20px;">Чистая цель на задачу</p>
    <p class="sk-body" style="color: var(--sk-muted); margin-bottom: 24px;">
      Одна подзадача &mdash; одна изолированная сессия с передачей только нужных артефактов.
    </p>
    <div style="display: flex; align-items: center; gap: 16px;">
      <sk-chip>1 задача &bull; 1 файл</sk-chip>
      <sk-mark kind="check"></sk-mark>
    </div>
    <sk-note style="margin-top: 30px; display: block; color: #2b7a4b;">быстро и воспроизводимо</sk-note>
  </sk-box>

  <sk-caption>Длинные чаты глупеют &mdash; перезапускай сессию после каждого этапа.</sk-caption>
</sk-slide>
```

---

## 🍳 Рецепт 2: Процесс из 3 шагов (Горизонтальный пайплайн)

Подходит для описания алгоритма или пошаговой инструкции.

```html
<sk-slide tone="teal" number="4">
  <sk-title number="4">Пайплайн создания артефакта</sk-title>

  <!-- Шаг 1 -->
  <sk-box x="120" y="280" w="380" h="400" label="1. Спецификация" tone="gray" rot="-0.8">
    <p class="sk-heading" style="margin-bottom: 16px;">Входные данные</p>
    <p class="sk-body" style="color: var(--sk-muted); margin-bottom: 20px;">Требования и ограничения задачи.</p>
    <sk-chip>spec.md</sk-chip>
  </sk-box>

  <sk-arrow x1="520" y1="480" x2="600" y2="480" tone="teal" step="1"></sk-arrow>

  <!-- Шаг 2 -->
  <sk-box x="610" y="280" w="380" h="400" label="2. Генерация" tone="purple" rot="0.5" step="1">
    <p class="sk-heading" style="color: #6941c6; margin-bottom: 16px;">Работа агента</p>
    <p class="sk-body" style="color: var(--sk-muted); margin-bottom: 20px;">Синтез решения по шаблону.</p>
    <sk-spark label="Claude Code"></sk-spark>
  </sk-box>

  <sk-arrow x1="1010" y1="480" x2="1090" y2="480" tone="teal" step="2"></sk-arrow>

  <!-- Шаг 3 -->
  <sk-box x="1100" y="280" w="380" h="400" label="3. Проверка" tone="green" line="green" rot="-0.5" step="2">
    <p class="sk-heading" style="color: #2b7a4b; margin-bottom: 16px;">Тестирование</p>
    <p class="sk-body" style="color: var(--sk-muted); margin-bottom: 20px;">Автономный прогон тестов.</p>
    <div style="display: flex; gap: 12px; align-items: center;">
      <sk-chip>pnpm test</sk-chip>
      <sk-mark kind="check"></sk-mark>
    </div>
  </sk-box>

  <sk-caption>Не доверяй первой генерации &mdash; замкни цикл через автоматический валидатор.</sk-caption>
</sk-slide>
```

---

## 🍳 Рецепт 3: Диалог Человек + ИИ (Интерактивная связка)

```html
<sk-slide tone="purple" number="5">
  <sk-title number="5">Делегируй, но верифицируй</sk-title>

  <!-- Человек слева -->
  <sk-figure x="180" y="380" label="Инженер"></sk-figure>
  <sk-bubble x="290" y="320" w="380" h="140" tail="bl" tone="blue">
    «Сделай рефакторинг модуля авторизации по спецификации»
  </sk-bubble>

  <sk-arrow x1="690" y1="390" x2="890" y2="390" tone="blue" label="делегирование" step="1"></sk-arrow>

  <!-- ИИ справа -->
  <sk-box x="920" y="280" w="520" h="380" label="Агент исполнения" tone="purple" line="purple" step="1">
    <p class="sk-heading" style="color: #6941c6; margin-bottom: 16px;">План из 3 шагов:</p>
    <div class="sk-body" style="line-height: 1.5;">
      1. Запуск регрессионных тестов<br>
      2. Применение точечного патча<br>
      3. Проверка покрытия
    </div>
    <div style="margin-top: 24px; display: flex; align-items: center; gap: 16px;">
      <sk-chip>patch.diff</sk-chip>
      <sk-mark kind="check" step="2"></sk-mark>
    </div>
  </sk-box>

  <sk-caption>Агент предлагает решения &mdash; человек контролирует границы и архитектуру.</sk-caption>
</sk-slide>
```
