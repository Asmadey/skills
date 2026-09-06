# Настройка аутентификации для Obsidian Git

Плагин использует нативный Git (на десктопе) или isomorphic-git (на мобильных устройствах). Для бесперебойной автоматической синхронизации без запроса паролей при каждом коммите требуется настроить системный Credential Helper или SSH-ключи.

---

## 1. macOS

### HTTPS (macOS Keychain) — Рекомендуется
Сохраняет учетные данные GitHub/GitLab в защищенной системной связке ключей macOS:

```bash
git config --global credential.helper osxkeychain
```

После выполнения команды сделайте один тестовый `git push` или `git pull` в терминале и введите логин и Personal Access Token (PAT). В дальнейшем Obsidian Git будет авторизовываться автоматически.

### SSH
1. Убедитесь, что SSH-ключ добавлен в `ssh-agent`:
   ```bash
   ssh-add --apple-use-keychain ~/.ssh/id_ed25519
   ```
2. Проверьте подключение к GitHub:
   ```bash
   ssh -T git@github.com
   # Ожидаемый ответ: Hi <username>! You've successfully authenticated...
   ```

---

## 2. Windows

### HTTPS (Git Credential Manager)
Проверьте активный хелпер:
```bash
git config credential.helper
# Должно вернуть: manager или manager-core
```
Если возвращает пустоту, включите менеджер:
```bash
git config --global credential.helper manager
```

---

## 3. Linux

### HTTPS (libsecret)
Для сред GNOME (Keyring) или KDE (KWallet):
```bash
# Ubuntu / Debian
sudo apt install libsecret-1-0 libsecret-1-dev make gcc
cd /usr/share/doc/git/contrib/credential/libsecret
sudo make
git config --global credential.helper /usr/share/doc/git/contrib/credential/libsecret/git-credential-libsecret
```

---

## 4. Personal Access Token (PAT) для GitHub

При авторизации по HTTPS GitHub больше не принимает пароль аккаунта. Требуется Fine-grained или Classic Token:
1. Перейдите в **GitHub Settings** $\rightarrow$ **Developer settings** $\rightarrow$ **Personal access tokens** $\rightarrow$ **Tokens (classic)**.
2. Сгенерируйте токен со следующими скоупами:
   - `repo` (полный доступ к репозиториям заметок).
   - `workflow` (опционально, если используются GitHub Actions для публикаций).
3. Используйте ваш логин GitHub и скопированный токен (`ghp_...`) в качестве пароля.
