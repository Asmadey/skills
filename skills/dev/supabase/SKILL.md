---
name: supabase
description: Official Supabase Agent Skills suite. Complete toolkit for working with Supabase products (Database, Auth, Edge Functions, Realtime, Storage, Vector, Queues), Postgres performance optimization, migrations, RLS policies, and SSR integrations with Next.js/React. Use when designing schemas, debugging RLS/Auth, writing database migrations, or optimizing Postgres queries.
---

# ⚡ Supabase Agent Skills Suite

## Назначение
Официальный пакет агентных навыков от команды Supabase. Охватывает полный стек разработки, администрирования баз данных Postgres, настройки Row Level Security (RLS) и серверных интеграций.

## Доступные навыки

| Навык | Описание | Путь |
| :--- | :--- | :--- |
| **`supabase`** | Полный спектр работы с продуктами Supabase: База данных, Auth, Edge Functions, Realtime, Storage, Vectors, Cron, Queues, SSR-интеграции (Next.js/React), миграции и траблшутинг. | [skills/supabase/SKILL.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/supabase/skills/supabase/SKILL.md) |
| **`supabase-postgres-best-practices`** | Руководство по оптимизации производительности PostgreSQL: проектирование индексов, эффективные запросы, RLS без деградации скорости, пулинг соединений, чистка bloat. | [skills/supabase-postgres-best-practices/SKILL.md](file:///Users/asmadey/AntiGravity/PersonalOS/skills/supabase/skills/supabase-postgres-best-practices/SKILL.md) |

## Золотые правила безопасности Supabase
1. **Никогда не используйте `user_metadata` для авторизации в RLS:** Поле редактируется пользователем на клиенте. Используйте `app_metadata` (`raw_app_meta_data`).
2. **Представления (Views) обходят RLS по умолчанию:** В Postgres 15+ всегда указывайте `CREATE VIEW ... WITH (security_invoker = true)`.
3. **Для UPDATE требуется SELECT policy:** Без политики SELECT операции UPDATE тихо возвращают 0 обновленных строк.
4. **`auth.role()` устарел:** Задавайте целевую роль непосредственно через клаузу `TO authenticated` или `TO anon`.
5. **Всегда включайте RLS на открытых схемах (`public`):** Таблицы без RLS доступны через Data API всем, у кого есть права роли `anon`.
