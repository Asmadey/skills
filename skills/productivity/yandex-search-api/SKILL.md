---
name: Yandex Search API
description: Выполняет веб-поиск через Yandex Search API v2 с поддержкой OAuth-авторизации и парсингом результатов в JSON.
category: integration
source: https://github.com/artwist-polyakov/polyakov-claude-skills
version: 1.0.0
last_updated: 2026-02-23
---

# Yandex Search API

## 1. Когда использовать
- Когда нужно найти актуальную информацию в интернете (рунете).
- Когда требуется получить структурированные результаты поиска (заголовки, ссылки, сниппеты).
- Как альтернатива или дополнение к другим поисковым системам.

## 2. Валидация и требования
- [ ] Наличие файла `skills/yandex-search-api/config/config.json`.
- [ ] Валидный `yandex_passport_oauth_token` в конфиге.
- [ ] Установленный `python3` (стандартная библиотека).
- [ ] Установленный `curl`.

## 3. Рабочий процесс (Workflow)
- [ ] **Шаг 1**: Использовать `web_search_sync.sh` для выполнения поиска.
- [ ] **Шаг 2**: Обработать полученный JSON-результат в `cache/results/[hash].json`.

## 4. Инструкции
### Синхронный поиск (Sync Search)
```bash
# Выполнить поиск по запросу
bash scripts/web_search_sync.sh --query "Ваш поисковый запрос"

# Выполнить поиск с параметрами
bash scripts/web_search_sync.sh --query "Python" --results 5 --region-id 225
```

### Параметры
- `--query, -q`: Текст поискового запроса.
- `--results, -n`: Количество результатов (1-100, по умолчанию 10).
- `--region-id, -r`: ID региона (225 — Россия, 213 — Москва).
- `--page, -p`: Номер страницы результатов (начиная с 0).

## 5. Ресурсы
- `scripts/`: Скрипты для работы с API и парсинга XML.
- `cache/`: Временные файлы и кэшированные IAM-токены.
- `config/`: Файлы конфигурации.
