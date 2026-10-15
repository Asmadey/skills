---
name: next-move-theory
description: "Канон и навыки методологии Next Move Theory и Advanced JTBD (Иван Замесин). Пошаговый алгоритм для принятия продуктовых решений: сегментация, поиск точек роста ценности, проведение и разбор кастдева, формулирование ценностного предложения, подготовка PRD и GTM. Включает 8 специализированных навыков во главе с /nmt-chat. Триггеры: \"nmt\", \"/nmt-chat\", \"zamesin\", \"next move theory\", \"ajtbd\", \"граф работ\", \"кастдев\", \"анализ интервью\", \"nmt-diagnose\"."
category: product
version: 1.0.0
source: https://github.com/zamesin/Next-Move-Theory-Canon-and-Skills
metadata:
  author: Ivan Zamesin
  frameworks: [Next Move Theory, Advanced JTBD, ABCDX Segmentation, RAT]
  total_skills: 8
---

# Next Move Theory & Advanced JTBD (Иван Замесин)

Методология и алгоритмическая система принятия продуктовых решений от Ивана Замесина. Интегрирует Advanced Jobs To Be Done (v3.4), Riskiest Assumption Test (RAT), ABCDX-сегментацию, теорию ограничений Голдратта и юнит-экономику в единую операционную систему.

## Contents
- Быстрый старт и точка входа (/nmt-chat)
- Пайплайн продуктовой работы
- Каталог навыков NMT
- Структура канона (база знаний)
- Принципы методологии и глоссарий

---

## Быстрый старт и точка входа

Главная точка входа во всю систему — диалоговый навык **`/nmt-chat`**.

В него можно передать любые сырые материалы:
* Обрывки мыслей и заметок о новом продукте
* Транскрипты или выжимки созвонов с клиентами
* Документацию существующего сервиса
* Ссылки и описания конкурентов

`/nmt-chat` автоматически извлекает контекст, отделяет проверенные факты от допущений, определяет самую рискованную гипотезу (RAT) и сам направляет вас в нужный шаг пайплайна.

---

## Пайплайн продуктовой работы

```
Новая идея         → /nmt-chat → /nmt-market-research
                               → /nmt-craft-value-proposition
                               → /nmt-product-requirements
                               → /nmt-craft-go-to-market

Работающий продукт → /nmt-diagnose (поиск утечек метрик и узких мест)
Транскрипты созвонов → /nmt-analyze-interviews (структурирование кастдева)
```

---

## Каталог навыков NMT

| Навык | Назначение | Триггер | Файл навыка |
|---|---|---|---|
| **nmt-chat** | Интерактивный продуктовый советник и маршрутизатор по методологии | `/nmt-chat`, `посоветуй по продукту`, `разбери идею` | [SKILL.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/skills/nmt-chat/SKILL.md) |
| **nmt-diagnose** | Диагностика живого продукта: выявление утечек конверсии, retention и поломок цепи ценности | `/nmt-diagnose`, `диагностика продукта`, `почему не растет` | [SKILL.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/skills/nmt-diagnose/SKILL.md) |
| **nmt-market-research** | Оценка объема рынка, каузальная сегментация и анализ барьеров переключения | `/nmt-market-research`, `исследование рынка`, `сегментация` | [SKILL.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/skills/nmt-market-research/SKILL.md) |
| **nmt-analyze-interviews** | Разбор транскриптов интервью, выделение 8 элементов работы и Consideration Set | `/nmt-analyze-interviews`, `разбери интервью`, `кастдев разбор` | [SKILL.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/skills/nmt-analyze-interviews/SKILL.md) |
| **nmt-craft-value-proposition** | Сборка ценностного предложения на базе формулы ценности и механик энергоэффективности | `/nmt-craft-value-proposition`, `ценностное предложение`, `value prop` | [SKILL.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/skills/nmt-craft-value-proposition/SKILL.md) |
| **nmt-product-requirements** | Подготовка PRD на основе критической цепи работ, Aha-момента и краевых случаев | `/nmt-product-requirements`, `prd по nmt`, `спецификация фичи` | [SKILL.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/skills/nmt-product-requirements/SKILL.md) |
| **nmt-craft-go-to-market** | Разработка GTM-стратегии, триггеров запуска и формул конвертящих сообщений | `/nmt-craft-go-to-market`, `gtm стратегия`, `позиционирование` | [SKILL.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/skills/nmt-craft-go-to-market/SKILL.md) |
| **nmt-update** | Проверка и обновление канона и навыков из официального репозитория | `/nmt-update`, `обнови nmt` | [SKILL.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/skills/nmt-update/SKILL.md) |

---

## Структура канона (база знаний)

Теоретический базис расположен в папке [Next-Move-Theory-Canon](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/Next-Move-Theory-Canon) (доступен также через корневой симлинк `Next-Move-Theory-Canon/`):

1. **[Advanced-Jobs-To-Be-Done](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done):**
   * [ajtbd-key-theses.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/ajtbd-key-theses.md) — 22 ключевых тезиса AJTBD.
   * [job-structure.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/job-structure.md) — 8 элементов Работы и уровни детализации (L1/L2/L3).
   * [job-graph.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/job-graph.md) — иерархия Графа Работ (Core, Big, Small, Micro).
   * [value-creation.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/value-creation.md) — нейробиологическая формула ценности (энергоэффективность мозга) и Aha-момент.
   * [value-creation-mechanics.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/value-creation-mechanics.md) — механики создания добавочной ценности.
   * [critical-chain.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/critical-chain.md) — критическая цепь работ и обрывы цепочки ценности.
   * [segmentation.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/segmentation.md) — каузальная сегментация против ложных критериев.
2. **[Next-Move-Theory](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/Next-Move-Theory-Canon/Next-Move-Theory):**
   * [nmt-key-theses.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/Next-Move-Theory-Canon/Next-Move-Theory/nmt-key-theses.md) — системные принципы NMT.
   * [local-vs-global-optimum.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/Next-Move-Theory-Canon/Next-Move-Theory/local-vs-global-optimum.md) — выбор между локальным и глобальным оптимумом.
   * [subtraction.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/Next-Move-Theory-Canon/Next-Move-Theory/subtraction.md) — вычитание (subtraction-first) как сильнейшая механика.
3. **[Riskiest-Assumption-Test](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/Next-Move-Theory-Canon/Riskiest-Assumption-Test):**
   * [rat-key-theses.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/Next-Move-Theory-Canon/Riskiest-Assumption-Test/rat-key-theses.md) — ранжирование допущений по смертоносности и стоимости фальсификации.
4. **[ABCDX-Segmentation](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/Next-Move-Theory-Canon/ABCDX-Segmentation):**
   * [abcdx-segmentation-key-theses.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/Next-Move-Theory-Canon/ABCDX-Segmentation/abcdx-segmentation-key-theses.md) — матрица классификации сегментов по готовности платить и масштабируемости.
5. **[Algorithms](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/Next-Move-Theory-Canon/Algorithms):**
   * [the-algorithm.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/public/product/next-move-theory/Next-Move-Theory-Canon/Algorithms/the-algorithm.md) — генеральный алгоритм принятия любого продуктового решения.

---

## Важные методологические инварианты

1. **Работа ≠ «прогресс»**: Работа — это спецификация желаемого перехода (Состояние А → Состояние Б) ради выполнения Работы более высокого уровня.
2. **Ценность = энергоэффективность для мозга**: Разница между предсказанием мозга и реальным опытом выполнения работы.
3. **Проблема ≠ первопричина**: Проблема возникает только тогда, когда нанятое Решение выполняет работу ниже критериев успеха.
4. **Ленивая загрузка**: Навыки считывают конкретные файлы канона по требованию во время диалога, обеспечивая максимальную методологическую точность без засорения контекста.
