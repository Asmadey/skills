# Productivity Skills
High-agency planning, goal execution, de-slopping, text humanization, knowledge management, and research.

## User-invoked

- **[book-to-skill](./book-to-skill/SKILL.md)**: Converts books and documents (PDF, EPUB, DOCX, HTML, Markdown, plain text, RTF, MOBI/AZW with Calibre) into structured agent skills, extracting frameworks, mental models, principles, techniques, and anti-patterns. Use when the user wants to study a document through Amp or Claude Code, apply an author's frameworks while working, or build a reusable knowledge base from a file.
- **[find-skills](./find-skills/SKILL.md)**: Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.
- **[goal-buddy](./goal-buddy/SKILL.md)**: Автономный движок управления долгосрочными целями (Goal Management & Execution Engine). Формирует канбан-доску задач, обеспечивает декомпозицию намерений через Goal Oracle, ролевое распределение задач (Scout для разведки, Worker для реализации, Judge для проверки) и сохранение квитанций выполнения (durable receipts).
- **[second-brain](./second-brain/SKILL.md)**: Управляет динамической базой знаний (LLM Wiki) в Obsidian. Автоматизирует Ingest (синтез) новых источников, Query (извлечение) ответов из Wiki и Lint (поддержание здоровья графа).
- **[skill-creator](./skill-creator/SKILL.md)**: Специализированный агент для организации клонированных репозиториев в структурированную директорию skills/ с автоматической документацией.
- **[slop-monster](./slop-monster/SKILL.md)**: Очищает черновики и копирайтинг от признаков ИИ-генерации (AI slop), линтит клише и стилистические маркеры нейросетей, проводит многопроходный рерайт и очистку через альтернативную модель.

## Model-invoked

- **[brand-voice](./brand-voice/SKILL.md)**: Ensure all communication matches brand voice and tone guidelines. Use when creating marketing copy, customer communications, public-facing content, or when users mention brand voice, tone, or writing style.
- **[geo-seo-claude](./geo-seo-claude/SKILL.md)**: Инструмент для GEO (Generative Engine Optimization) и SEO аудита. Оптимизирует сайты для AI-поисковиков (ChatGPT, Claude, Perplexity, Gemini) и традиционного поиска.
- **[humanizer-en](./humanizer-en/SKILL.md)**: Removes signs of AI-generated writing to produce natural, human-sounding text. Based on Wikipedia's AI Cleanup guidelines.
- **[humanizer-ru](./humanizer-ru/SKILL.md)**: Скилл для очеловечивания русскоязычного текста. Убирает признаки AI-генерации, делает текст живым. Используй ВСЕГДА, когда пользователь просит: очеловечить текст, убрать следы нейросети, сделать текст живым/естественным, переписать как человек, humanize на русском, убрать канцелярит, убрать водянистость, сделать текст менее формальным. Также используй если пользователь вставляет русскоязычный текст и говорит что-то вроде 'перепиши', 'сделай лучше', 'звучит как робот', 'слишком искусственно'. Работает ТОЛЬКО с русским языком. Для английского используй оригинальный humanizer. НЕ используй для: перевод, написание с нуля, грамматика, код.
- **[prd-taskmaster](./prd-taskmaster/SKILL.md)**: Zero-config goal-to-tasks engine (the Atlas engine). Takes any goal (software, pentest,
- **[simple-english](./simple-english/SKILL.md)**: |
- **[slop-detector](./slop-detector/SKILL.md)**: Remove AI writing patterns from prose. Use when drafting, editing, or reviewing text to eliminate predictable AI tells.
- **[tavily-intelligence](./tavily-intelligence/SKILL.md)**: Инструментарий для глубокого поиска, извлечения контента и сканирования веб-сайтов с использованием API Tavily.
- **[watermarks-remover](./watermarks-remover/SKILL.md)**: Удаляет скрытые водяные знаки ИИ, цифровые маркеры прослеживаемости (provenance marks) и метаданные нейросетей из текста и файлов (изображения, документы, медиа). Очищает невидимый Unicode (Zero-Width Space, bidi-символы, гомоглифы), метаданные C2PA / Content Credentials, EXIF/XMP-маркеры генераторов (Midjourney, DALL-E, Stable Diffusion, Claude, ChatGPT, Gemini/SynthID).
- **[yandex-metrika](./yandex-metrika/SKILL.md)**: Аудит трафика через Яндекс.Метрику. Оценка истории, каналов, конверсий, органики. Кеширование для экономии контекстного окна (TSV/JSON).
- **[yandex-search-api](./yandex-search-api/SKILL.md)**: Выполняет веб-поиск через Yandex Search API v2 с поддержкой OAuth-авторизации и парсингом результатов в JSON.
- **[yandex-wordstat](./yandex-wordstat/SKILL.md)**: |
