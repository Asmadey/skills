---
name: Modal Cloud
description: Платформа для облачных вычислений на Python (GPU, серверные функции).
category: tooling
source: https://modal.com
version: 1.0.0
last_updated: 2026-02-18
created: 2026-02-08
---

# Modal Cloud

## 1. Когда использовать
- Когда нужно запустить тяжелые Python функции в облаке (GPU, большие объемы памяти).
- Когда требуется быстрое развертывание API или веб-скрейперов без настройки инфраструктуры.

## 2. Валидация
- [ ] Modal установлен: `python3.12 -m modal --version`
- [ ] Авторизация выполнена: `python3.12 -m modal setup`

## 3. Команды (Instructions)
### Запуск скрипта локально (с выполнением функции в облаке)
```bash
python3.12 -m modal run examples/get_started.py
```

### Деплой приложения
```bash
python3.12 -m modal deploy examples/app.py
```

## 4. Ресурсы
- `examples/get_started.py`: Базовый пример (квадрат числа 42).
