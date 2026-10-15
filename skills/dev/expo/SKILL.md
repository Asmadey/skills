---
name: expo
description: "Официальный инженерный комплекс навыков Expo и React Native для агентов (Expo Skills Suite). Охватывает 25 специализированных навыков: общая маршрутизация (expo-overview), структура проектов (expo-project-structure), навигация (expo-router), анимации и жесты (expo-animation), нативный UI и компоненты (@expo/ui, expo-native-ui), дизайн-системы (expo-design-system), работа с данными (expo-data-fetching), DOM-компоненты (expo-dom), миграция с веба (expo-web-to-native), нативные модули и Swift/Kotlin (expo-module, expo-migrate-module), brownfield-интеграции (expo-brownfield), dev-клиенты (expo-dev-client), App Clips (expo-app-clip), обновления SDK (expo-upgrade), и сервисы EAS (eas-app-stores, eas-hosting, eas-workflows, eas-observe, eas-update, eas-update-insights, eas-simulator). Триггеры: 'expo', 'react native', 'expo router', 'eas', 'eas build', 'eas update', 'mobile app', 'ios android expo'."
category: dev
version: 1.0.0
source: https://github.com/expo/skills
metadata:
  author: Expo Team
  category: dev
  total_skills: 25
---

# Expo Skills Suite (Official Expo AI Agent Skills)

Официальный набор AI-агентных навыков от команды Expo для проектирования, разработки, нативного тюнинга, деплоя и отладки приложений на Expo и React Native.

## 🧭 Стартовая точка

При общих, комплексных или неоднозначных запросах по разработке на Expo сначала используйте:
- **[expo-overview](skills/expo-overview/SKILL.md)** — маршрутизация запросов, архитектурные правила, совместимость SDK и навигация по стеку.

---

## 📦 Каталог 25 навыков Expo

### 1. Framework & Core (Open Source)

| Навык | Назначение | Документация |
|---|---|---|
| **expo-overview** | Архитектурные правила, определение контекста и роутинг по инструментам Expo | [SKILL.md](skills/expo-overview/SKILL.md) |
| **expo-project-structure** | Эталонная структура каталогов: `src/`, routes-only `app/`, изоляция платформ | [SKILL.md](skills/expo-project-structure/SKILL.md) |
| **expo-router** | Файловая маршрутизация, нативные стеки, табы, модалки, sheets и deeplinks | [SKILL.md](skills/expo-router/SKILL.md) |
| **expo-animation** | Премиальные анимации и жесты: Reanimated 3+, Gesture Handler, Haptics | [SKILL.md](skills/expo-animation/SKILL.md) |
| **expo-native-ui** | Нативные интерфейсы, семантические цвета, размытия, медиа, WebGPU/Three.js | [SKILL.md](skills/expo-native-ui/SKILL.md) |
| **expo-design-system** | Токены темы, адаптивные отступы, типографика, аудит дрифта дизайн-системы | [SKILL.md](skills/expo-design-system/SKILL.md) |
| **expo-ui** | Нативные компоненты `@expo/ui`: кроссплатформенный UI, SwiftUI, Jetpack Compose | [SKILL.md](skills/expo-ui/SKILL.md) |
| **expo-data-fetching** | Запросы к API, TanStack React Query, SWR, кэширование, оффлайн, loaders | [SKILL.md](skills/expo-data-fetching/SKILL.md) |
| **expo-dom** | Использование веб-компонентов внутри нативного приложения через Expo DOM | [SKILL.md](skills/expo-dom/SKILL.md) |
| **expo-web-to-native** | Миграция веб-приложений (Next.js, Vite, CRA) в нативные iOS/Android приложения | [SKILL.md](skills/expo-web-to-native/SKILL.md) |
| **expo-module** | Разработка нативных модулей на Swift и Kotlin, autolinking, config plugins | [SKILL.md](skills/expo-module/SKILL.md) |
| **expo-migrate-module** | Миграция легаси React Native модулей на современный Expo Module API | [SKILL.md](skills/expo-migrate-module/SKILL.md) |
| **expo-brownfield** | Встраивание Expo / React Native экранов в существующие нативные iOS/Android аппы | [SKILL.md](skills/expo-brownfield/SKILL.md) |
| **expo-dev-client** | Конфигурация и запуск собственных Development Builds вместо Expo Go | [SKILL.md](skills/expo-dev-client/SKILL.md) |
| **expo-examples** | Готовые паттерны и интеграции из репозитория `expo/examples` (`with-*`) | [SKILL.md](skills/expo-examples/SKILL.md) |
| **expo-app-clip** | Разработка легких iOS App Clips, AASA файлы, ассоциированные домены | [SKILL.md](skills/expo-app-clip/SKILL.md) |
| **expo-upgrade** | Безопасное обновление версий Expo SDK, разрешение конфликтов зависимостей | [SKILL.md](skills/expo-upgrade/SKILL.md) |
| **expo-skill-feedback** | Обратная связь, телеметрия и отчетность по использованию навыков Expo | [skills/expo-skill-feedback/SKILL.md](skills/expo-skill-feedback/SKILL.md) |

### 2. Сервисы EAS (Expo Application Services)

| Навык | Назначение | Документация |
|---|---|---|
| **eas-app-stores** | Сборка и публикация в App Store / Google Play, TestFlight, профили и сертификаты | [SKILL.md](skills/eas-app-stores/SKILL.md) |
| **eas-hosting** | Хостинг веб-версий Expo и серверных API routes: Cloudflare Workers, домены | [SKILL.md](skills/eas-hosting/SKILL.md) |
| **eas-workflows** | Настройка CI/CD пайплайнов автоматизации в EAS Workflows | [SKILL.md](skills/eas-workflows/SKILL.md) |
| **eas-observe** | Мониторинг производительности, аналитика маршрутов, метрики запусков и крашей | [SKILL.md](skills/eas-observe/SKILL.md) |
| **eas-update** | Настройка OTA (Over-The-Air) обновлений без перепубликации в магазины | [SKILL.md](skills/eas-update/SKILL.md) |
| **eas-update-insights** | Диагностика стабильности OTA релизов, откат сбойных обновлений | [SKILL.md](skills/eas-update-insights/SKILL.md) |
| **eas-simulator** | Удаленный запуск iOS/Android симуляторов в облаке EAS с интерактивным превью | [SKILL.md](skills/eas-simulator/SKILL.md) |

---

## 🛠️ Интеграция с кодовой базой

- Всегда используйте `pnpm` или `npx expo` в соответствии с конфигурацией проекта.
- Перед внесением глубоких изменений в нативные зависимости проверяйте совместимость с текущей версией SDK через `npx expo install --check`.
