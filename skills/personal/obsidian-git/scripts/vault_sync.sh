#!/usr/bin/env bash
# ==============================================================================
# Obsidian Vault Git Sync Utility
# Безопасная синхронизация хранилища заметок без открытого интерфейса Obsidian
# ==============================================================================

set -euo pipefail

VAULT_DIR="${1:-.}"
cd "$VAULT_DIR"

if [ ! -d ".git" ]; then
    echo "❌ Ошибка: В директории $VAULT_DIR не обнаружен репозиторий Git (.git отсутствует)."
    exit 1
fi

echo "🔄 [1/4] Проверка удаленного репозитория и Pull..."
# Защита от зависаний: проверяем связь
git fetch origin || {
    echo "⚠️ Не удалось получить данные из remote. Проверьте интернет или настройки аутентификации."
    exit 1
}

# Если есть незакоммиченные изменения, стэшим или авто-коммитим перед pull
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "📝 [2/4] Фиксация локальных изменений перед слиянием..."
    git add -A
    HOSTNAME_STR=$(hostname -s 2>/dev/null || echo "device")
    DATE_STR=$(date "+%Y-%m-%d %H:%M:%S")
    git commit -m "vault backup ($HOSTNAME_STR): $DATE_STR" || true
fi

echo "📥 [3/4] Слияние изменений с remote (pull rebase)..."
git pull --rebase origin "$(git branch --show-current)" || {
    echo "⚠️ Конфликт при rebase! Запустите 'python3 scripts/scan_conflicts.py' для анализа."
    exit 1
}

echo "📤 [4/4] Отправка изменений в remote (push)..."
git push origin "$(git branch --show-current)"

echo "✅ Синхронизация хранилища завершена успешно!"
