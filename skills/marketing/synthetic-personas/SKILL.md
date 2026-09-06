---
name: Synthetic Personas Generation
description: Создание и использование синтетических персонажей для тестирования промптов и моделирования поведения пользователей. v1.0.
category: framework
source: /Users/asmadey/PersonalOS/syntethic.md
version: 1.0
last_updated: 2026-02-18
created: 2026-02-08
---

# Synthetic Personas Generation Standard

## 🎯 Обзор
Синтетические персонажи решают проблему "холодного старта" при отслеживании промптов, имитируя поведение реальных сегментов пользователей с точностью до 85%.

Скилл позволяет:
1. Создавать Carrot-карты персонажей на основе реальных данных (CRM, саппорт, отзывы).
2. Генерировать реалистичные промпты, которые эти пользователи вводили бы в AI.
3. Проводить Reality Check маркетинговых гипотез.

---

## 🔄 Workflow

*1.* Сбор данных (Data Ingestion)
Соберите данные из следующих источников:
- **Support Tickets & Community:** Язык проблем и фильтры по интентам.
- **CRM & Sales Transcripts:** Возражения, вопросы и условия закрытия сделок.
- **Reviews (G2, Trustpilot):** Разрыв между ожиданиями и реальностью.
- **Search Console:** Реальные вопросы пользователей (Google Query Data).

*2.* Заполнение Persona Card (5 полей)
Для каждого персонажа создайте карту:
1. **Job-to-be-done (JTBD):** Какую реальную задачу пытается решить? (Не "узнать про X", а "выбрать лучший инструмент для Y").
2. **Constraints (Ограничения):** Время, бюджет, риски, комплаенс, опыт.
3. **Success Metric:** Как персонаж поймет, что результат "достаточно хорош"?
4. **Decision Criteria:** Какого уровня детализации и доказательств требует персонаж?
5. **Vocabulary:** Какими словами он говорит? (Слэнг, технические термины или "человеческий" язык).

*3.* Спецификация и Метаданные (Provenance)
- **Provenance:** Источники данных.
- **Confidence Score:** Оценка уверенности по каждому из 5 полей (High/Med/Low).
- **Regeneration Triggers:** Когда нужно обновить персонажа (новый конкурент, смена трендов).

*4.* Генерация промптов
Используйте Persona Card для генерации 5-10 типичных промптов, которые этот персонаж отправил бы в AI-поисковик или чат-бот.

*5.* Сохранение (Preservation)
Все сгенерированные персонажи должны быть сохранены в папку:
`skills/synthetic-personas/personas/{persona_id}.md` (для чтения) и/или `.json` (для скриптов).

---

## ⚠️ Ограничения
- **Sycophancy Bias:** AI-персонажи склонны быть слишком позитивными.
- **Missing Friction:** Они могут не "чувствовать" новые боли, если их нет в данных.
- **Shallow Prioritization:** Склонность считать всё важным. Обязательно выставляйте веса.

---

## 📋 Формат карточки персонажа (Output Protocol)

**Путь сохранения:** `skills/synthetic-personas/personas/{name_kebab_case}.md`

```markdown
### 👤 Persona: [Name/Role]
#### 1. Core Profile
- **JTBD:** ...
- **Constraints:** ...
- **Success Metric:** ...
- **Decision Criteria:** ...
- **Vocabulary:** ...

#### 2. Specification (Metadata)
- **Provenance:** ...
- **Confidence:** ...
- **Coverage Notes:** ...
- **Validation Benchmarks:** ...
- **Regeneration Triggers:** ...

#### 3. Predicted Prompts
1. ...
2. ...
```

---

## 🛠 Скрипты и автоматизация

В папке `scripts/` находится инструмент для автоматической генерации промптов на основе ваших карт.

**Запуск генерации:**
```bash
python3 skills/synthetic-personas/scripts/generate_prompts.py --file skills/synthetic-personas/examples/aleksandr_persona.json
```

Этот скрипт превращает абстрактные характеристики персонажа в конкретные фразы, которые вы можете использовать для тестирования своих LLM-агентов или мониторинга поисковой выдачи.
