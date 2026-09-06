---
name: Yandex Metrika
description: Аудит трафика через Яндекс.Метрику. Оценка истории, каналов, конверсий, органики. Кеширование для экономии контекстного окна (TSV/JSON).
category: integration
source: https://github.com/artwist-polyakov/polyakov-claude-skills/tree/main/plugins/yandex-metrika/skills/yandex-metrika
version: 1.0.0
last_updated: 2026-03-06
---

# Yandex Metrika

## 1. When to use
- Оценка статистики Яндекс.Метрики («что работает, что нет»).
- Сбор данных по источникам трафика, целям, конверсиям, UTM-меткам, органике из поиска.
- Быстрый аудит рекламных каналов и поведения пользователей на сайте.
- Анализ эффективности прямого трафика в сравнении с рекламным.

## 2. Validation & Prerequisites
- [ ] Обязательно наличие `YANDEX_METRIKA_TOKEN` в файле `config/.env`. (Токен OAuth Яндекса с правом `metrika:read`).
- [ ] Проверьте статус API вызовом списка счётчиков: `bash scripts/counters.sh`. 

## 3. Workflow (Checklist)
- [ ] Шаг 1: Получить список доступных счётчиков (`bash scripts/counters.sh`).
- [ ] Шаг 2: Уточнить у пользователя ID или название нужного счётчика, если он не очевиден (`bash scripts/counters.sh --search <name>`).
- [ ] Шаг 3: Получить метаданные и цели выбранного счётчика (`bash scripts/counter_info.sh --counter <ID>` и `bash scripts/goals.sh --counter <ID>`).
- [ ] Шаг 4: Уточнить у пользователя, какие цели являются конверсионными (для бизнеса).
- [ ] Шаг 5: Сохранить конфигурацию в `cache/counter_<id>/config.json`.
- [ ] Шаг 6: Сгенерировать отчёты (трафик, конверсии, UTM и поисковые системы) по задаче пользователя.
- [ ] Шаг 7: Проанализировать полученные выжимки (результаты ограничены 30 строками в stdout, полные данные уходят в CSV).

## 4. Instructions (Degrees of Freedom)
### Heuristics (High Freedom)
- Используйте **cache-first** подход. Скрипты автоматически кэшируют ответы. Повторный запрос за тот же период не тратит квоту.
- Читайте только заголовки (первые 30 строк ответа). Полные данные доступны в CSV и через grep/rg для поиска без загрузки в контекст.
- Для атрибуции конверсий уточняйте у пользователя (по умолчанию `lastsign` — последний значимый источник).
- Фильтр ботов включен по умолчанию (`isRobot='No'`). Без сэмплирования (`accuracy=1`).

### Templates (Low Freedom)
```bash
# 1. Получение списка счетчиков
bash scripts/counters.sh
bash scripts/counters.sh --search "site_name"

# 2. Информация по счетчику
bash scripts/counter_info.sh --counter 12345
bash scripts/goals.sh --counter 12345

# 3. Сводка по трафику с группировкой по месяцам
bash scripts/traffic_summary.sh \
  --counter 12345 \
  --date1 2025-01-01 \
  --date2 2025-12-31 \
  --group month

# 4. Конверсии по целям (по умолчанию берутся конверсионные из конфига)
bash scripts/conversions.sh \
  --counter 12345 \
  --date1 2025-01-01

# 5. Разбивка по UTM-меткам
bash scripts/utm_report.sh \
  --counter 12345 \
  --date1 2025-01-01 \
  --group month

# 6. Трафик из поисковых систем (органика)
bash scripts/search_engines.sh \
  --counter 12345 \
  --date1 2025-01-01
```

## 5. Resources
- `scripts/`: Скрипты (counters, goals, traffic, conversions, utm, search_engines)
- `config/`: Файлы конфигурации (инструкция `README.md`, шаблон `.env.example`)
- `cache/`: Локальный кэш (TSV/JSON файлы) для экономии токенов
- `references/`: Дополнительные инструкции по сложным отчетам, лимитам и сравнениям
