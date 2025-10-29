# 📚 Explicații: GitHub Actions & Security

## 🔄 GitHub Actions

**GitHub Actions** este un sistem de CI/CD (Continuous Integration / Continuous Deployment) integrat în GitHub.

### Ce face Actions?

1. **Automatizare Workflows**
   - Rulează cod Python/JavaScript/etc. automat
   - La fiecare commit, pull request, sau pe schedule
   - Pe sisteme virtuale (Ubuntu, Windows, macOS)

2. **Testing Automat**
   - Rulează teste la fiecare modificare
   - Verifică că codul funcționează pe multiple versiuni Python
   - Detectează bug-uri înainte de merge

3. **Deployment Automat**
   - Publică aplicații automat
   - Build executabile
   - Upload artefacte

4. **Rapoarte și Notificări**
   - Generează rapoarte de test
   - Trimite email-uri la eșecuri
   - Comentează pe PR-uri

### Exemple Workflows

#### 1. Monitor Website (în acest proiect)
```yaml
on:
  schedule:
    - cron: '0 */6 * * *'  # La fiecare 6 ore
```

**Ce face:** Rulează `website_monitor.py` automat și generează rapoarte.

#### 2. Test la fiecare commit
```yaml
on:
  push:
    branches: [ main ]
```

**Ce face:** Rulează teste când cineva face push pe branch-ul main.

### Fișiere Workflow

- Location: `.github/workflows/`
- Format: YAML (`.yml`)
- Trigger: Events (push, PR, schedule, manual)

### Beneficii

✅ **Calitate:** Teste automate → mai puține bug-uri
✅ **Eficiență:** Nu trebuie să rulezi manual teste
✅ **Transparență:** Toată lumea vede rezultatele
✅ **Confidență:** Merge doar cod testat

---

## 🛡️ GitHub Security

**GitHub Security** oferă instrumente pentru protecția codului.

### Funcționalități

1. **Dependabot Alerts**
   - Detectează vulnerabilități în dependențe (`pip`, `npm`, etc.)
   - Sugerează update-uri pentru librării vulnerabile
   - Exemple: `requests` versiune veche cu bug-uri

2. **Secret Scanning**
   - Detectează token-uri, parole, API keys expuse în cod
   - Blochează commit-uri cu secrete
   - Notificări imediate

3. **Code Scanning**
   - Analiză cod pentru pattern-uri nesigure
   - Detectează SQL injection, XSS, etc.
   - Suportă CodeQL și alte tool-uri

4. **Dependency Review**
   - Verifică dependențele noi în PR-uri
   - Alertă dacă se adaugă librării vulnerabile

### Tab Security în Repository

Când deschizi tab-ul **Security**, vezi:

- 🔴 **Dependabot alerts:** Lista vulnerabilităților
- ⚠️ **Secret scanning:** Secrete găsite (dacă există)
- 📊 **Code scanning:** Probleme de securitate găsite
- 🔒 **Security policies:** Reguli și contact

### Exemple Alerte

**Dependabot Alert:**
```
Package: requests
Version: 2.25.1
Vulnerability: CVE-2023-32681
Severity: HIGH
Fix: Upgrade to 2.31.0
```

**Secret Scanning:**
```
Found: GitHub Personal Access Token
Location: config.py:45
Action: Revoked automatically
```

### Beneficii

✅ **Protecție:** Detectare automată a problemelor
✅ **Compliance:** Respectă standardele de securitate
✅ **Încredere:** Utilizatorii știu că proiectul este securizat
✅ **Prevenire:** Blochează probleme înainte să se ajungă în producție

---

## 🔗 Cum lucrează împreună

**Actions** + **Security** = Development Pipeline Securizat

1. **Developer face commit**
2. **Security** verifică secrete și vulnerabilități
3. **Actions** rulează teste
4. Dacă totul e OK → merge; altfel → blocat

### Exemplu Real

```yaml
# .github/workflows/security.yml
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run security scan
        run: |
          # Scanează pentru vulnerabilități
          pip-audit
          # Verifică cod pentru probleme
          bandit -r ./
```

---

## 📝 În Acest Proiect

### Actions Workflows

1. **`.github/workflows/monitor.yml`**
   - Monitorizează site-uri automat
   - Generează rapoarte
   - Upload artefacte

2. **`.github/workflows/test.yml`**
   - Rulează teste pe multiple versiuni Python
   - Generează coverage reports

### Security Features

- ✅ `.gitignore` exclude fișiere cu secrete
- ✅ Nu există token-uri hardcodate
- ✅ Dependențe minime (`requests`)
- ✅ `requirements.txt` pentru tracking versiuni

---

## 🎓 Resurse de Învățare

- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **Security Docs:** https://docs.github.com/en/code-security
- **YAML Syntax:** https://yaml.org/

---

## ❓ FAQ

**Q: Actions costă bani?**
A: Pentru repository-uri publice e GRATIS. Pentru private, ai 2000 minute/lună gratis.

**Q: Security alerts sunt automate?**
A: Da, Dependabot scanează automat la fiecare scan sau commit.

**Q: Pot dezactiva Actions?**
A: Da, în Settings → Actions → General → poți dezactiva.

**Q: Cum văd rezultatele Actions?**
A: Tab-ul "Actions" → vezi istoricul rulărilor → click pe un run pentru detalii.

---

**Sper că acum înțelegi diferența! Actions = automatizare, Security = protecție.** 🚀

