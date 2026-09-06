# Быстрый старт с no-mistakes

## 1. Установка бинарного файла

```bash
# Автоматическая установка через скрипт
bash skills/no-mistakes/scripts/install.sh

# Либо через curl напрямую
curl -fsSL https://raw.githubusercontent.com/kunchenguid/no-mistakes/main/docs/install.sh | sh
```

---

## 2. Инициализация репозитория

В корне любого Git-репозитория запустите:
```bash
no-mistakes init
```
Команда настраивает локальный Git-remote `no-mistakes`, который перехватывает пуши и запускает верификацию в изолированном worktree.

---

## 3. Использование

### Вариант А: Через Git (вручную)
```bash
git checkout -b feature/my-new-feature
# ... пишем код и коммитим ...
git commit -m "feat: add user authentication"

# Отправляем через локальный гейт вместо origin:
git push no-mistakes
```

### Вариант Б: Через агента (/no-mistakes)
Агент может выполнять задачу и автоматически прогонять ее через гейт:
```bash
no-mistakes axi run --intent "Добавить поддержку фильтрации по тегам в API"
```

---

## 4. Конфигурация (.no-mistakes.yaml)

Создайте `.no-mistakes.yaml` в корне проекта:
```yaml
commands:
  lint: "pnpm lint"
  format: "pnpm format"
  test: "pnpm test"

auto_fix:
  review: 0   # требовать подтверждения человека для ревью
```
