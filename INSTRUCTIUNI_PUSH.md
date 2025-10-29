# 📤 Instrucțiuni: Push pe GitHub cu Script Python

## ⚠️ IMPORTANT: Configurează Token-ul și User-ul

### Opțiunea 1: Direct în Script (RAPID)

1. Deschide `push_to_github.py`
2. Găsește liniile de configurare la începutul fișierului:
   ```python
   USER_GITHUB = ""  # Adaugă aici: "ME-SUZY"
   TOKEN_GITHUB = ""  # Adaugă aici: "ghp_xxxxx"
   REPO_NAME = "Proiect-action-GitHub"  # Schimbă dacă vrei alt nume
   ```
3. Adaugă valorile tale
4. Salvează fișierul

### Opțiunea 2: Variabile de Mediu (RECOMANDAT - Mai Sigur)

**Windows PowerShell:**
```powershell
# Setează variabilele (doar pentru sesiunea curentă)
$env:GITHUB_USER = "ME-SUZY"
$env:GITHUB_TOKEN = "ghp_xxxxxxxxxxxxx"

# Apoi rulează scriptul
python push_to_github.py
```

**Windows CMD:**
```cmd
set GITHUB_USER=ME-SUZY
set GITHUB_TOKEN=ghp_xxxxxxxxxxxxx
python push_to_github.py
```

**Permanent (Windows):**
1. Settings → System → Advanced → Environment Variables
2. Adaugă `GITHUB_USER` și `GITHUB_TOKEN` în User variables
3. Restart terminal

### Opțiunea 3: Fișier Config Separat

1. Creează `config.py` (fără `.example`):
   ```python
   USER_GITHUB = "ME-SUZY"
   TOKEN_GITHUB = "ghp_xxxxxxxxxxxxx"
   REPO_NAME = "Proiect-action-GitHub"
   REPO_OWNER = "ME-SUZY"
   ```
2. Modifică `push_to_github.py` să importe din `config.py`
3. **IMPORTANT:** Adaugă `config.py` în `.gitignore`!

## 🚀 Rulare Script

```bash
# Navighează în folderul proiectului
cd "e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\2023\Proiect action GitHub"

# Rulează scriptul
python push_to_github.py
```

## 📋 Ce face scriptul:

1. ✅ Verifică dacă Git este instalat
2. ✅ Inițializează repository Git (dacă nu există)
3. ✅ Adaugă toate fișierele
4. ✅ Cere mesaj commit (sau folosește "Initial commit")
5. ✅ Creează commit
6. ✅ Configurează remote GitHub
7. ✅ Face push pe branch-ul `main`

## 🔍 Posibile Probleme

### "Repository nu există"
**Soluție:** Creează repository-ul manual:
1. Mergi pe: https://github.com/new
2. Nume: `Proiect-action-GitHub` (sau ce ai setat în `REPO_NAME`)
3. Public sau Private
4. **NU** bifa "Initialize with README"
5. Click "Create repository"
6. Rulează din nou scriptul

### "Authentication failed"
**Soluție:**
- Verifică că token-ul este valid
- Verifică că token-ul are permisiune `repo`
- Verifică că username-ul este corect

### "Git nu este instalat"
**Soluție:**
- Download Git: https://git-scm.com/download/win
- Instalează
- Restart terminal
- Rulează din nou scriptul

## 🔒 Securitate

✅ **BINE:**
- Folosește variabile de mediu
- Folosește `config.py` adăugat în `.gitignore`
- Token doar local, niciodată în chat/public

❌ **NU FĂ:**
- Nu comita `config.py` cu token-ul
- Nu posta token-uri în chat
- Nu partaja token-uri

## 📝 Exemplu Complet

```powershell
# 1. Setează variabilele
$env:GITHUB_USER = "ME-SUZY"
$env:GITHUB_TOKEN = "ghp_xxxxxxxxxxxxx"

# 2. Navighează în folder
cd "e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\2023\Proiect action GitHub"

# 3. Rulează scriptul
python push_to_github.py

# 4. Introduce mesaj commit (sau apasă Enter pentru default)
```

## ✅ Success!

După rulare, vei vedea:
```
✅ Push reușit!
🎉 Repository disponibil la:
   https://github.com/ME-SUZY/Proiect-action-GitHub
```

