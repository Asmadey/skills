---
name: GEO-SEO Claude (Antigravity Edition)
description: Инструмент для GEO (Generative Engine Optimization) и SEO аудита. Оптимизирует сайты для AI-поисковиков (ChatGPT, Claude, Perplexity, Gemini) и традиционного поиска.
category: automation
source: https://github.com/zubair-trabzada/geo-seo-claude
version: 1.0.0
last_updated: 2026-04-10
---

# GEO-SEO & AI Visibility Skill

Этот навык превращает Антигравити в мощного GEO-специалиста, способного проводить глубокий аудит видимости сайта в эру ИИ-поиска.

## 1. Когда использовать
- Когда пользователь просит "сделать SEO аудит" или "проверить видимость в ИИ".
- При упоминании терминов: `geo`, `seo`, `citability`, `llms.txt`, `ai search`, `perplexity optimization`.
- Когда нужно подготовить отчет для клиента по оптимизации под поисковые LLM.
- При анализе URL для поиска точек роста в цитируемости (citability).

## 2. Проверка и требования
- [ ] Python 3.8+ (проверить: `python3 --version`)
- [ ] Зависимости: `pip install -r requirements.txt`
- [ ] Playwright (для скриншотов): `python3 -m playwright install chromium`

## 3. Основные команды (Триггеры)

Вы можете выполнять эти действия, имитируя команды оригинального инструмента:

| Команда | Действие |
|---------|----------|
| **Аудит GEO + SEO** | Запустить полный цикл анализа (AI Visibility, Platform Analysis, Technical, Content, Schema). |
| **Citability Score** | Оценить готовность контента к цитированию нейросетями (блоки 134-167 слов, факты, E-E-A-T). |
| **Crawler Access** | Проверить `robots.txt` на наличие разрешений для GPTBot, ClaudeBot, PerplexityBot и др. |
| **llms.txt** | Проверить наличие или сгенерировать файл `llms.txt`. |
| **Brand Mentions** | Найти упоминания бренда на Reddit, YouTube, Wikipedia, LinkedIn (сигнал для Entity Recognition). |
| **PDF Report** | Сгенерировать профессиональный PDF-отчет с графиками. |

## 4. Рабочий процесс (Workflow)

*1.* Сбор данных
Используйте `read_url_content` или `firecrawl_scrape`, чтобы получить содержимое главной страницы и ключевых разделов.

*2.* Параллельный анализ (Мульти-агентность)
Разделите задачу на подзадачи, используя инструкции из `agents/`:
1. **AI Visibility**: Цитируемость, роботы, llms.txt, бренды.
2. **Platform Specific**: Готовность под ChatGPT vs Perplexity vs Google AIO.
3. **Technical SEO**: Скорость, мобильность, SSR.
4. **Content & E-E-A-T**: Экспертность, уникальность, доверие.
5. **Schema Markup**: Проверка JSON-LD.

*3.* Синтез и Скоринг
Используйте формулу GEO Score:
`GEO_Score = (Citability * 0.25) + (Brands * 0.20) + (Content * 0.20) + (Technical * 0.15) + (Schema * 0.10) + (Platforms * 0.10)`

*4.* Генерация отчета
- Создайте `GEO-AUDIT-REPORT.md` с приоритетными действиями (Quick Wins).
- Для PDF используйте скрипт: `python3 scripts/generate_pdf_report.py`.

## 5. Ресурсы
- `scripts/`: Python-утилиты для парсинга и скоринга.
- `agents/`: Глубокие инструкции для каждого аспекта аудита.
- `schema/`: Шаблоны JSON-LD (Organization, LocalBusiness, SaaS).
- `examples/`: Примеры отчетов.

## Эвристики (Принципы GEO)
- **Цитируемость > Ссылки**: Для ИИ важнее прямое упоминание сущности (Entity) и фактов в тексте, чем обратные ссылки.
- **Оптимальный объем**: Фрагменты для цитирования должны быть 134-167 слов.
- **llms.txt — это новый sitemap**: Помогите ботам понять структуру вашего сайта для обучения и RAG.
- **Wikipedia — Король**: Упоминание в Википедии дает +30 баллов к авторитету бренда для LLM.
