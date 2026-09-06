---
name: Open Graph Implementation
description: Senior Frontend Developer skill for Technical SEO. Use when implementing or validating Open Graph meta tags for web pages to ensure perfect link previews in social networks (Facebook, LinkedIn, X/Twitter) and messengers (Telegram, Slack, Discord). Covers OG image requirements (1200×630), HTML implementation, and validation checklist.
created: 2026-02-08
last_updated: 2026-02-18
---

# Open Graph Implementation

Expert implementation of Open Graph meta tags for perfect link previews across all platforms.

**Role:** Senior Frontend Developer с экспертизой в Technical SEO.

---

## Quick Reference

| Platform | Image Size | Aspect Ratio | Max Size |
|----------|-----------|--------------|----------|
| **Standard** (FB, LinkedIn, X, Slack, Discord) | 1200 × 630 px | 1.91:1 | 300 KB |
| **Telegram** (link preview) | 1200 × 630 px | 1.91:1 | 300 KB |
| **Telegram** (channel image) | 1280 px (long side) | - | - |

---

## 1. OG Image Requirements

### Стандартные размеры
```
┌─────────────────────────────────────────┐
│              1200 × 630 px              │
│  ┌─────────────────────────────────┐    │
│  │      Safe Zone: 1080 × 566      │    │
│  │   (60px отступ от краев)        │    │
│  │                                 │    │
│  │   [LOGO]                        │    │
│  │   [ЗАГОЛОВОК]                   │    │
│  │   [ПОДЗАГОЛОВОК]                │    │
│  │                                 │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

### Технические требования

| Параметр | Требование |
|----------|------------|
| **Разрешение** | 1200 × 630 px |
| **Соотношение** | 1.91:1 |
| **Safe Zone** | 1080 × 566 px (центр) |
| **Отступы** | Минимум 60 px от краев |
| **Формат** | JPG или PNG (без прозрачности!) |
| **Вес файла** | < 300 KB (идеально 100-200 KB) |
| **URL** | Абсолютный HTTPS путь |

### Чего избегать

- ❌ Прозрачный фон (PNG с alpha)
- ❌ Относительные пути (`/images/og.jpg`)
- ❌ Файлы > 300 KB
- ❌ Текст у самого края (обрезка)
- ❌ GIF и SVG форматы

---

## 2. HTML Implementation

### Полный шаблон

```html
<!DOCTYPE html>
<html lang="ru" prefix="og: https://ogp.me/ns#">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <!-- Основные Open Graph теги -->
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="[Название Проекта]" />
  <meta property="og:url" content="https://mysite.com/current-page-url" />
  <meta property="og:title" content="[Заголовок | До 60-95 символов]" />
  <meta property="og:description" content="[Описание | 2-4 предложения, до 200 символов]" />
  <meta property="og:locale" content="ru_RU" />

  <!-- OG Image -->
  <meta property="og:image" content="https://mysite.com/images/og/page-preview.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:type" content="image/jpeg" />
  <meta property="og:image:alt" content="[Описание изображения]" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="[Тот же заголовок]" />
  <meta name="twitter:description" content="[То же описание]" />
  <meta name="twitter:image" content="https://mysite.com/images/og/page-preview.jpg" />
  
  <title>[Заголовок страницы]</title>
</head>
```

### Минимальный набор тегов

```html
<meta property="og:title" content="Заголовок" />
<meta property="og:description" content="Описание" />
<meta property="og:image" content="https://example.com/image.jpg" />
<meta property="og:url" content="https://example.com/page" />
<meta name="twitter:card" content="summary_large_image" />
```

---

## 3. Типы контента (og:type)

| Тип | Когда использовать |
|-----|-------------------|
| `website` | Главная, лендинги, обычные страницы |
| `article` | Блог-посты, новости, статьи |
| `product` | Страницы товаров |
| `video.other` | Страницы с видео |
| `profile` | Профили пользователей |

### Для статей (article)

```html
<meta property="og:type" content="article" />
<meta property="article:published_time" content="2026-02-09T12:00:00+03:00" />
<meta property="article:modified_time" content="2026-02-09T14:30:00+03:00" />
<meta property="article:author" content="https://example.com/authors/john" />
<meta property="article:section" content="Technology" />
<meta property="article:tag" content="AI" />
<meta property="article:tag" content="Development" />
```

---

## 4. Framework Examples

### React / Next.js

```tsx
// components/SEO.tsx
import Head from 'next/head';

interface SEOProps {
  title: string;
  description: string;
  image: string;
  url: string;
}

export function SEO({ title, description, image, url }: SEOProps) {
  const siteName = "My Site";
  const fullImage = image.startsWith('http') ? image : `https://mysite.com${image}`;
  
  return (
    <Head>
      <title>{title}</title>
      <meta property="og:type" content="website" />
      <meta property="og:site_name" content={siteName} />
      <meta property="og:url" content={url} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={fullImage} />
      <meta property="og:image:width" content="1200" />
      <meta property="og:image:height" content="630" />
      
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={fullImage} />
    </Head>
  );
}
```

### Vue / Nuxt

```vue
<script setup lang="ts">
useHead({
  title: 'Page Title',
  meta: [
    { property: 'og:type', content: 'website' },
    { property: 'og:title', content: 'Page Title' },
    { property: 'og:description', content: 'Description' },
    { property: 'og:image', content: 'https://mysite.com/og-image.jpg' },
    { property: 'og:url', content: 'https://mysite.com/page' },
    { name: 'twitter:card', content: 'summary_large_image' },
  ],
});
</script>
```

### Astro

```astro
---
// components/SEO.astro
interface Props {
  title: string;
  description: string;
  image?: string;
}

const { title, description, image = '/images/og-default.jpg' } = Astro.props;
const canonicalURL = new URL(Astro.url.pathname, Astro.site);
const ogImage = new URL(image, Astro.site);
---

<meta property="og:type" content="website" />
<meta property="og:url" content={canonicalURL} />
<meta property="og:title" content={title} />
<meta property="og:description" content={description} />
<meta property="og:image" content={ogImage} />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />

<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content={title} />
<meta name="twitter:description" content={description} />
<meta name="twitter:image" content={ogImage} />
```

---

## 5. Validation Checklist

### Перед деплоем проверь:

- [ ] **HTTPS URLs**: Все `og:image` и `og:url` начинаются с `https://`
- [ ] **Абсолютные пути**: Никаких относительных путей (`/img/...`)
- [ ] **Уникальность**: Каждая страница имеет свои title, description, image
- [ ] **Доступность**: Изображение открывается в incognito (без редиректов)
- [ ] **HTML prefix**: `<html prefix="og: https://ogp.me/ns#">`
- [ ] **Размер изображения**: 1200 × 630 px, < 300 KB
- [ ] **Формат**: JPG или PNG без прозрачности
- [ ] **Кодировка**: UTF-8 для кириллицы

### Инструменты валидации

| Платформа | URL |
|-----------|-----|
| **Facebook** | https://developers.facebook.com/tools/debug/ |
| **Twitter** | https://cards-dev.twitter.com/validator |
| **LinkedIn** | https://www.linkedin.com/post-inspector/ |
| **General** | https://www.opengraph.xyz/ |
| **Telegram** | Отправить ссылку боту @webpagebot |

---

## 6. File Structure

```
public/
├── images/
│   └── og/
│       ├── default.jpg          # Дефолтное OG изображение
│       ├── home.jpg             # Главная страница
│       ├── about.jpg            # О нас
│       ├── blog/
│       │   ├── article-1.jpg    # Статья 1
│       │   └── article-2.jpg    # Статья 2
│       └── products/
│           ├── product-a.jpg
│           └── product-b.jpg
```

### Именование файлов

```
{page-slug}-og.jpg
{page-slug}-og.png
```

---

## 7. Common Mistakes

| ❌ Ошибка | ✅ Решение |
|----------|-----------|
| Относительный путь `/img/og.jpg` | Абсолютный `https://site.com/img/og.jpg` |
| Прозрачный PNG | JPG или PNG с фоном |
| Файл > 5 MB | Оптимизировать до < 300 KB |
| Один og:image на весь сайт | Уникальные изображения для каждой страницы |
| Текст у края изображения | Текст в Safe Zone (60px от края) |
| Забыли twitter:card | Добавить `summary_large_image` |
| HTTP вместо HTTPS | Всегда HTTPS |

---

## 8. Dynamic OG Images

Для генерации динамических OG-изображений:

### Vercel OG (Next.js)

```tsx
// app/api/og/route.tsx
import { ImageResponse } from 'next/og';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const title = searchParams.get('title') ?? 'Default Title';

  return new ImageResponse(
    (
      <div style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#1a1a2e',
        color: 'white',
      }}>
        <h1 style={{ fontSize: 60 }}>{title}</h1>
      </div>
    ),
    { width: 1200, height: 630 }
  );
}
```

Использование:
```html
<meta property="og:image" content="https://mysite.com/api/og?title=My%20Page" />
```

---

## Templates

See `templates/` folder for:
- `og-tags.html` — Copy-paste template
- `react-seo.tsx` — React component
- `vue-seo.vue` — Vue composable
