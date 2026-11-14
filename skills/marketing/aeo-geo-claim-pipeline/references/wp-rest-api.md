# WP REST API: SearchEngineLand

Сайт за Cloudflare managed challenge. Прямой `curl` → 403 «Just a moment», `curl_cffi` с импersonate chrome/safari → 403, headless-браузер висит на challenge. **Работает только Firecrawl-канал**: Hermes `web_extract` или локальный ротатор `127.0.0.1:9123`.

## Эндпоинты

| Что | URL |
|---|---|
| Корень API | `https://searchengineland.com/wp-json/` |
| Посты | `/wp-json/wp/v2/posts?per_page=15&page=N&_fields=id,slug,date,link,title,content,categories` |
| Страницы `/guide/…` | `/wp-json/wp/v2/pages?per_page=15&page=N` |
| Категории | `/wp-json/wp/v2/categories?per_page=100` (всего 101) |

`content.rendered` — полное HTML-тело статьи, не выжимка и не кеш. Проверено сверкой фрагментов с живой страницей.

## Категории для AEO/GEO

| id | Категория | Постов |
|---|---|---|
| 9521 | Generative Engine Optimization (GEO) | 852 |
| 9106 | Search features | 900 |
| 9520 | ChatGPT | 141 |
| 9519 | OpenAI | 95 |
| 9534 | AI SEO Guides | 69 |
| 4758 | SEO (зонтик) | 17 686 |

Тематическая выборка = `posts?categories=9521,9106,9520,9519,9534` (~1 900 постов ≈ 130 кредитов с полным текстом). **Правильный способ сузить тему — категории на входе**, а не постфактум по ключевым словам: категория назначена редакцией, словарь — твоей догадкой.

## Объём и стоимость

| Режим | Документов | Кредитов |
|---|---|---|
| Полный архив с контентом | 30 146 постов (301×100 + 46) | ~2 010 |
| Только метаданные | те же | ~314 |
| AEO/GEO-срез с контентом | ~1 900 | ~130 |
| Инкремент (сутки) | ~5 постов | 1 |

1 URL `web_extract` = 1 кредит независимо от веса ответа. С полным контентом держать `per_page ≤ 15`: при 30 ответ обрезается на ~375–500 KB и JSON ломается.

`X-WP-Total` через `web_extract` не виден (нет заголовков) — количество выводить из формы страниц: пустая страница = конец.

## Ловушки

| Ловушка | Симптом | Правильно |
|---|---|---|
| Slug с числовым суффиксом | `?slug=chatgpt-ads-…-dominate` → `[]` | Permalink = `%postname%-%post_id%`, поле `slug` без суффикса. Брать slug из ответа API |
| `?search=` | В выдачу лезут нерелевантные посты | Ищет по полному тексту, не по заголовку. Для темы использовать `categories` |
| `per_page=30` + `content` | Битый JSON | `per_page ≤ 15` |
| `/latest-posts` как discovery | Обрывается на page 720 (~18k статей) | Архив НЕ покрывает; только для свежего инкремента |
| Sitemap | `web_extract` склеивает URL с датой | Парсить `(https://searchengineland\.com/[^\s]+?)(?=\d{4}-\d{2}-\d{2}T)` |

## Проверка перед большим обходом

```bash
# остаток кредитов Firecrawl — до планирования, не после
curl -s https://api.firecrawl.dev/v1/team/credit-usage -H "Authorization: Bearer $FIRECRAWL_API_KEY"
```

Правило: сначала посчитать объём и стоимость, показать срез, потом запускать. Прогон «на весь архив» без проверки бюджета уже приводил к остановке на середине.

## Инкремент (для крона)

```bash
# 1 запрос ≈ 1 кредит/сутки
/wp-json/wp/v2/posts?categories=9521,9106,9520,9519,9534&after=<ISO-дата>&per_page=15\&_fields=id,slug,date,link,title,content,categories
```

Дату брать из последнего обработанного атома (`max(date)` в `claims.jsonl`), не из «сегодня минус 7 дней» — иначе окно дрейфует и появляются дубли.
