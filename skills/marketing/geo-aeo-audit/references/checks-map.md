# Карта проверок: что смотреть, как чинить, какая техника плейбука

Один ряд = одна проверка в `geo_audit.py`. `id` совпадает с ключом в `ACTIONS` и в JSON-снимке.

| id | severity | как проверяется | как чинить | §плейбука |
|---|---|---|---|---|
| `robots_ai` | critical | `Disallow: /` для GPTBot, ClaudeBot, PerplexityBot, OAI-SearchBot, ChatGPT-User, Google-Extended, Applebot, CCBot | открыть доступ; закрытый бот = нулевая видимость в AI | 1.6 |
| `raw_text` | critical | меньше 150 слов в HTML без исполнения JS | SSR/static export, контент в первом ответе сервера | 1.1, 1.12 |
| `size` | critical | HTML больше 4 МБ | резать инлайн-данные, выносить медиа | 1.5 |
| `noindex` | critical | `<meta name="robots" content="noindex">` | убрать; noindex ставить только когда страница не нужна в поиске | 1.13 |
| `http` | critical | статус не 200 | починить роут или убрать URL из sitemap | — |
| `sitemap` | critical | sitemap отсутствует или пуст | собрать sitemap, добавить в robots.txt | 1.10 |
| `orphans` | high | URL из sitemap не достижим за 2 клика по raw-ссылкам | HTML-ссылки с хабов и соседних страниц | 1.2 |
| `h1` | high | h1 не один | один h1 = тема страницы | 13.2 |
| `internal_links` | high | меньше 3 внутренних ссылок в HTML | блок «читайте также», хлебные крошки | 2.7 |
| `answer_first` | high | первые символы после h1 — дата/оглавление/крошки | ответ в первом абзаце, служебное ниже | 1.3, 2.4 |
| `canonical` | high | canonical ведёт на другой URL | self-canonical | 1.11 |
| `schema` | high | нет JSON-LD | добавить WebPage/Article + Organization | 5.1 |
| `question_h2` | medium | ≥4 h2 и ни один не вопрос | переформулировать часть h2 вопросами | 2.1, 2.10 |
| `schema_type` | medium | JSON-LD без типа страницы | добавить WebPage/Article/FAQPage | 5.1 |
| `sameas` | medium | Organization без `sameAs` | ссылки на Wikidata, LinkedIn, GitHub, Crunchbase | 4.2 |
| `date_modified` | medium | у статьи нет `dateModified` | отдавать дату обновления в JSON-LD | 4.6 |
| `meta_description` | medium | нет description | заполнить человеческой фразой | 1.4 |
| `cluster_links` | medium | статья блога без ссылок на другие статьи | двусторонняя перелинковка кластера | 2.7 |
| `table` | medium | сравнительный заголовок без `<table>` | HTML-таблица сравнения | 2.6 |
| `img_alt` | medium | у `<img>` нет атрибута alt | проставить | 14.2 |
| `img_alt_empty` | low | alt пустой у половины картинок | заполнить содержательным текстом у смысловых | 14.2 |
| `img_format` | low | не webp/avif/svg | перекодировать | 1.9 |
| `lang` | low | нет `lang` у `<html>` | указать | 13.2 |
| `title` | high | нет title | самодостаточная фраза | 1.4 |
| `title_len` | low | title длиннее 120 символов | сократить, смысл в начало | 1.4 |
| `robots_sitemap` | low | в robots.txt нет `Sitemap:` | добавить | 1.10 |

## Приоритеты плейбука, которые закрываются не скриптом, а работой

| Приоритет | Что делать |
|---|---|
| 3. Контентная стратегия | topic clusters, pillar + 3-5 кластерных страниц, query fan-out в подзаголовки |
| 3.5 / 7.3 | проприетарные данные и названные исследования — единственный moat |
| 4. E-E-A-T | named-авторы с проверяемыми регалиями, expert quotes, консистентность бренда |
| 6. Off-page | brand mentions важнее ссылок (0.664 против 0.218); отзывы на G2/Trustpilot/отзовиках |
| 4.11 | UGC-площадки дают 17.1% цитирований против 4% у издателей — Reddit, YouTube, Quora, LinkedIn |
| 7. Ghost citations | называть бренд внутри предложения с фактом, а не «наше исследование показало» |
| 10. Мониторинг | GSC AI performance reports, money-query set, `#:~:text=` в GA4 |

## Порог «пора не аудит, а контент»

Если скрипт даёт ≥90 и нет `critical`, дальнейший рост даёт не техника, а:
новая страница под кластер спроса, проприетарный датасет, внешние упоминания.
Технический аудит в этот момент перестаёт быть рычагом.
