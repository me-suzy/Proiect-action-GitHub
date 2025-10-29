# 📘 Ghid Complet: Cum Folosești GitHub Actions

## 🎯 Ce sunt GitHub Actions?

**GitHub Actions** = Automatizare care rulează pe GitHub când faci push sau conform unui program.

### Exemple:
- ✅ Testează codul automat la fiecare push
- ✅ Monitorizează site-uri web la ore programate
- ✅ Generează rapoarte și le păstrează ca artefacte
- ✅ Notifică când ceva nu merge bine

---

## 🚀 Cum Funcționează În Acest Proiect

Proiectul are **2 workflow-uri**:

### 1. **Run Tests** (`test.yml`)
- **Când rulează:** La fiecare push/PR pe `main`
- **Ce face:** Rulează teste pe:
  - Ubuntu și Windows
  - Python 3.9, 3.10, 3.11
  - Generează rapoarte de coverage

### 2. **Website Health Monitor** (`monitor.yml`)
- **Când rulează:**
  - La fiecare push (doar când modifici `sites.json` sau `website_monitor.py`)
  - La fiecare 6 ore (automat)
  - Manual (prin butonul "Run workflow")
- **Ce face:**
  - Verifică toate site-urile din `sites.json`
  - Generează rapoarte JSON și Markdown
  - Upload artefacte (rapoarte păstrate 30 zile)

---

## 📊 Cum Vizualizezi Rezultatele

### Pas 1: Deschide Tab-ul Actions

1. Mergi pe repository: https://github.com/me-suzy/Proiect-action-GitHub
2. Click pe tab-ul **"Actions"** (lângă "Code", "Issues", etc.)

### Pas 2: Vezi Lista de Rulări

Vei vedea:
- ✅ **Verde (checkmark)** = Succes
- ❌ **Roșu (X)** = Eșuat
- 🟡 **Galben (cercuri)** = În curs

**Click pe orice rulare** pentru detalii.

### Pas 3: Detalii Rulare

**Link direct către Actions:** https://github.com/me-suzy/Proiect-action-GitHub/actions

**Pentru o rulare specifică:**
1. Click pe orice rulare din listă
2. Sau accesează direct: `https://github.com/me-suzy/Proiect-action-GitHub/actions/runs/<RUN_ID>`
   - `<RUN_ID>` = numărul rulării (vezi în URL când ești pe pagina de detalii)

După ce click-ezi pe o rulare, vezi:

#### **Left Sidebar:**
- **Jobs** - Toate task-urile rulate
- Click pe un job pentru detalii

#### **Right Panel:**
- **Workflow Trigger** - Ce a declanșat rularea (push, schedule, manual)
- **Status** - Success/Failed
- **Duration** - Cât a durat
- **Artifacts** - Rapoarte generate (dacă există)

### Pas 4: Download Artefacte (Rapoarte)

Dacă workflow-ul a generat rapoarte:

1. Scroll jos în pagina de detalii
2. Secțiunea **"Artifacts"**
3. Download `monitor-report-json` sau `monitor-report-md`
4. Extrage ZIP-ul și citește rapoartele

---

## 🔍 Exemple Vizuale

### Exemplu 1: View Test Results

**Link direct:** https://github.com/me-suzy/Proiect-action-GitHub/actions

```
Actions → Run Tests #2 → Click pe job (e.g., "test ubuntu-latest 3.11")
→ Vezi output console → Verifică teste trecute ✅
```

**Sau accesează direct rularea:**
- Vezi numărul rulării în listă (e.g., "#2")
- Click pe rulare → Vezi pagina de detalii completă

### Exemplu 2: View Monitor Report

**Link direct:** https://github.com/me-suzy/Proiect-action-GitHub/actions/workflows/monitor.yml

```
Actions → Website Health Monitor #2 → Scroll jos → Artifacts
→ Download monitor-report-json.zip → Extrage → Deschide monitor_report.json
→ Vezi status toate site-urile 📊
```

**Link către workflow:** https://github.com/me-suzy/Proiect-action-GitHub/actions/workflows/monitor.yml

### Exemplu 3: View Logs

**Link direct către toate rulările:** https://github.com/me-suzy/Proiect-action-GitHub/actions

```
Actions → Click pe orice run → Click pe un job → Scroll jos
→ Vezi toate log-urile pas cu pas 🔍
```

### 📌 Links Rapide

- **All Actions:** https://github.com/me-suzy/Proiect-action-GitHub/actions
- **Test Workflow:** https://github.com/me-suzy/Proiect-action-GitHub/actions/workflows/test.yml
- **Monitor Workflow:** https://github.com/me-suzy/Proiect-action-GitHub/actions/workflows/monitor.yml
- **Repository:** https://github.com/me-suzy/Proiect-action-GitHub

---

## ⚙️ Cum Rulezi Manual un Workflow

### Opțiunea 1: Rulare Manuală (Workflow Dispatch)

1. Mergi în **Actions** tab
2. Click pe workflow-ul dorit (e.g., "Website Health Monitor")
3. Click pe butonul **"Run workflow"** (sus, dreapta)
4. Selectează branch (`main`)
5. Click **"Run workflow"**

Workflow-ul va rula imediat!

### Opțiunea 2: Modifică Fișier și Push

Pentru **Website Health Monitor**:
- Editează `sites.json` (adaugă/modifică un site)
- Commit și push
- Workflow-ul rulează automat

---

## 📈 Workflow Status Badge (Pe README)

Poți adăuga badge-uri în README care arată statusul workflow-urilor:

```markdown
![Tests](https://github.com/me-suzy/Proiect-action-GitHub/actions/workflows/test.yml/badge.svg)
![Monitor](https://github.com/me-suzy/Proiect-action-GitHub/actions/workflows/monitor.yml/badge.svg)
```

**Unde:** În fișierul `README.md`, adaugă badge-urile la început.

---

## 🔔 Notificări și Alerte

### Email Notificări (Implicit)

GitHub trimite automat email când:
- ❌ Un workflow eșuează
- ✅ Un workflow care eșuase anterior acum reușește

### Activează/Dezactivează:

1. Mergi pe: https://github.com/settings/notifications
2. Secțiunea **"Actions"**
3. Bifează/Dezactivează notificările dorite

---

## 🛠️ Cum Modifici un Workflow

### Locul Workflow-urilor:

```
.github/workflows/
├── monitor.yml    # Website Health Monitor
└── test.yml       # Run Tests
```

### Exemplu: Schimbă Intervalul de Monitorizare

Editează `.github/workflows/monitor.yml`:

```yaml
schedule:
  - cron: '0 */3 * * *'  # La fiecare 3 ore (în loc de 6)
```

Commit și push → Noua programare e activă!

### Exemplu: Adaugă un Nou Workflow

1. În `.github/workflows/`, creează `backup.yml`
2. Scrie workflow-ul (vezi exemple în workflow-urile existente)
3. Commit și push
4. Apare automat în tab-ul Actions!

---

## 📝 Ce Poți Face cu Actions În Acest Proiect

### Use Cases Practice:

1. **✅ Verificare Automată Site-uri**
   - Rulează la fiecare 6 ore
   - Rapoarte în artifacts
   - Vezi dacă site-urile tale sunt online

2. **✅ Testare Cod**
   - La fiecare commit
   - Verifică că codul funcționează pe multiple versiuni Python
   - Detalii în Actions logs

3. **✅ Tracking Uptime**
   - Descarcă rapoartele JSON
   - Analizează uptime-ul site-urilor
   - Vezi care site-uri au probleme

4. **✅ CI/CD Pipeline**
   - Testează înainte de merge
   - Blochează cod defect
   - Asigură calitate

---

## 🎓 Resurse de Învățare

- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **YAML Syntax:** https://yaml.org/
- **Workflow Examples:** https://github.com/actions/starter-workflows

---

## ❓ FAQ

**Q: Cât costă Actions?**
A: Pentru repository-uri publice = **GRATIS nelimitat!** Pentru private, ai 2000 minute/lună gratis.

**Q: Pot vedea istoricul rulărilor?**
A: Da! Tab-ul Actions arată toate rulările anterioare (păstrate permanent).

**Q: Cum șterg un workflow vechi?**
A: Șterge fișierul `.yml` din `.github/workflows/` și fă push.

**Q: Pot folosi Actions pentru deploy?**
A: Da! Poți configura deploy automat pe server când teste trec.

**Q: Unde văd toate workflow-urile?**
A: **Actions** tab → Left sidebar → Sub "All workflows" vezi lista completă.

---

**🎉 Acum ești pregătit să folosești Actions efectiv!**

