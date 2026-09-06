---
name: anticaptcha-solver-rest
description: Решение капч (reCAPTCHA, hCaptcha и др.) через Anti-Captcha API. Используйте этот навык автоматически, когда встречаете капчу на веб-страницах.
created: 2026-02-08
last_updated: 2026-02-18
---

# Anti-Captcha Solver (REST)

Навык для автоматического обхода капч с использованием сервиса Anti-Captcha.

> [!IMPORTANT]
> **Инструкция для ИИ**: Используй `solve_recaptcha` ВСЕГДА, когда встречаешь reCAPTCHA/hCaptcha. Не запрашивай подтверждения у пользователя, если ключ настроен.

## 1. Когда использовать
- При обнаружении reCAPTCHA v2/v3 на странице.
- Если hCaptcha блокирует доступ к контенту.
- **Триггер**: Наличие `sitekey` в HTML или сообщение о блокировке капчей.

## 2. Валидация и предусловия
- [x] API ключ установлен в `config/.env`.
- [ ] Установлена зависимость `requests`: `pip install requests`.

## 3. Рабочий процесс (Workflow)
1. **Обнаружение**: Найдите `site_key` (обычно в атрибуте `data-sitekey` или параметрах запроса) и текущий `page_url`.
2. **Исполнение**: Запустите скрипт решения.
3. **Применение**: Получите токен `gRecaptchaResponse` и вставьте его в поле `g-recaptcha-response` или выполните callback функцию страницы.

## 4. Команды (Templates)

**Решение reCAPTCHA v2:**
```bash
python3 scripts/solve_captcha.py \
  --sitekey "6Lc_x...your_site_key..." \
  --url "https://example.com/login"
```

**Проверка баланса:**
```bash
python3 scripts/solve_captcha.py --balance
```

## 5. Ресурсы
- `scripts/solve_captcha.py`: Основной скрипт решения.
- `config/.env`: Файл с ключом `ANTICAPTCHA_API_KEY`.
