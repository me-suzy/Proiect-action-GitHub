# 🔒 Configurare Git cu Token GitHub (SIGUR)

## ⚠️ IMPORTANT: Nu mai posta token-uri în chat!

## Configurare Token Local

### Opțiunea 1: Credential Helper (RECOMANDAT)

**Windows:**

1. Instalează Git Credential Manager (dacă nu e instalat):
   - Download: https://github.com/git-ecosystem/git-credential-manager/releases

2. Configurează credential helper:
   ```bash
   git config --global credential.helper wincred
   ```

3. La primul push, Git va cere token-ul:
   ```bash
   git push origin main
   # Username: ME-SUZY (sau username-ul tău GitHub)
   # Password: [paste token-ul NOU aici]
   ```

### Opțiunea 2: Environment Variable (temporar)

```powershell
# Setează token-ul ca variabilă de mediu (doar pentru sesiunea curentă)
$env:GITHUB_TOKEN = "ghp_your_new_token_here"

# Folosește în URL când adaugi remote:
git remote set-url origin https://$env:GITHUB_TOKEN@github.com/ME-SUZY/GITHUB_32BIT.git
```

### Opțiunea 3: SSH Keys (Cea mai sigură metodă)

1. Generează SSH key:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. Copiază public key:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

3. Adaugă pe GitHub:
   - Settings → SSH and GPG keys → New SSH key
   - Paste public key

4. Folosește SSH URL:
   ```bash
   git remote set-url origin git@github.com:ME-SUZY/GITHUB_32BIT.git
   ```

## 🔐 Best Practices

✅ **FĂ:**
- Folosește token local (nu în chat/email)
- Token cu permisiuni minime necesare
- Revocă token-urile vechi
- Folosește SSH keys pentru proiecte long-term

❌ **NU FĂ:**
- Nu posta token-uri în chat/email
- Nu comita token-uri în cod
- Nu partaja token-uri public
- Nu folosi token-uri în screenshot-uri

## 📝 Exemplu Push (după configurare)

```bash
cd "e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\2023\Proiect action GitHub"

git init
git add .
git commit -m "Initial commit: Website Monitor"

git remote add origin https://github.com/ME-SUZY/your-repo-name.git
git branch -M main
git push -u origin main
```

**La prima dată va cere token-ul - folosește cel NOU!**

