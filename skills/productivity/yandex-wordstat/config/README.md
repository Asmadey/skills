# Настройка Yandex Wordstat API

Актуальный способ — **Yandex Cloud Search API v2** (`searchapi.api.cloud.yandex.net/v2/wordstat`).  
Старый OAuth endpoint `api.wordstat.yandex.net/v1` больше не подключает новых пользователей и работает ненадёжно.

## Быстрый старт (Cloud API key)

1. Зайдите в [Yandex Cloud Console](https://console.cloud.yandex.ru/) и создайте API-ключ для сервиса **Search API**.
2. Скопируйте ключ.
3. В файле `config/.env` укажите:
   ```
   YANDEX_WORDSTAT_API_KEY=AQV...ваш_ключ
   ```
4. Проверьте подключение:
   ```bash
   bash scripts/quota.sh
   ```

## Legacy OAuth (DEPRECATED)

Используйте только если у вас уже есть одобренное приложение в Yandex OAuth.

1. Получите OAuth токен через `scripts/get_token.sh`.
2. Укажите `YANDEX_WORDSTAT_TOKEN` в `config/.env`.

## Лимиты

- **10 запросов в секунду**
- **1000 запросов в день**

## Регионы

ID регионов не изменились. Москва — `213`, Россия — `225`.
Список: `bash scripts/regions_tree.sh`.

## Примеры

```bash
# Топ запросов по Москве
bash scripts/top_requests.sh --phrase "внедрение ИИ в бизнес" --regions 213 --limit 100

# Динамика
bash scripts/dynamics.sh --phrase "внедрение ИИ в бизнес" --from-date 2025-01-01

# Региональная статистика
bash scripts/regions_stats.sh --phrase "внедрение ИИ в бизнес"
```

## Примечания по cloud API

- Даты динамики передаются в формате RFC3339.
- При `PERIOD_MONTHLY` конечная дата автоматически приводится к последнему дню месяца.
- Поле `count` возвращается строкой, но скрипты нормализуют его в число.
- Фильтр устройств: `DEVICE_DESKTOP`, `DEVICE_PHONE`, `DEVICE_TABLET`.
