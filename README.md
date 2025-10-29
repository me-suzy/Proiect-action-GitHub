# 🌐 Website Monitor & Health Checker

Monitor automat pentru verificarea statusului și sănătății site-urilor web. Rulează verificări periodice, generează rapoarte și notificări prin GitHub Actions.

## ✨ Funcționalități

- ✅ Verificare automată a mai multor site-uri
- 📊 Rapoarte JSON și Markdown
- ⏱️ Măsurare timp de răspuns
- 🔄 Monitorizare continuă prin GitHub Actions
- 📈 Tracking uptime și status codes
- 🚨 Notificări la probleme

## 📋 Cerințe

- Python 3.9+
- `requests` library

## 🚀 Instalare

```bash
# Clonează repository-ul
git clone <your-repo-url>
cd Proiect-action-GitHub

# Instalează dependențele
pip install -r requirements.txt
```

## 💻 Utilizare

### Rulare Locală

```bash
python website_monitor.py
```

Acest script va:
1. Citi lista de site-uri din `sites.json`
2. Verifica fiecare site
3. Genera rapoarte în `monitor_report.json` și `monitor_report.md`

### Configurare Site-uri

Editează `sites.json` pentru a adăuga/modifica site-uri:

```json
{
  "sites": [
    {
      "name": "GitHub",
      "url": "https://github.com",
      "expected_status": 200,
      "timeout": 10
    }
  ]
}
```

**Parametri:**
- `name`: Nume descriptiv pentru site
- `url`: URL-ul complet al site-ului
- `expected_status`: Cod status HTTP așteptat (default: 200)
- `timeout`: Timeout în secunde (default: 10)

## 🔄 GitHub Actions

> 📘 **Ghid Complet:** Vezi [`GHID_ACTIONS.md`](GHID_ACTIONS.md) pentru tutorial pas-cu-pas despre cum să folosești Actions!

Proiectul include două workflow-uri automate:

### 1. Website Health Monitor (`monitor.yml`)

**Când rulează:**
- La fiecare 6 ore (schedule)
- La fiecare push pe `main/master`
- La modificări în `sites.json` sau `website_monitor.py`
- Manual (workflow_dispatch)

**Ce face:**
- Rulează verificarea tuturor site-urilor
- Generează rapoarte JSON și Markdown
- Upload artifacte cu rapoarte (păstrate 30 zile)
- Comentează pe PR-uri cu rezultate
- Exit code 1 dacă există site-uri unhealthy

### 2. Run Tests (`test.yml`)

**Când rulează:**
- La fiecare push/PR pe `main/master`

**Ce face:**
- Rulează teste pe multiple Python versions (3.9, 3.10, 3.11)
- Rulează pe Ubuntu și Windows
- Generează coverage reports

## 📊 Exemple Rapoarte

### JSON Report (`monitor_report.json`)

```json
{
  "timestamp": "2025-01-29T12:00:00",
  "summary": {
    "total_sites": 4,
    "healthy_sites": 4,
    "unhealthy_sites": 0,
    "uptime_percentage": 100.0
  },
  "results": [...]
}
```

### Markdown Report (`monitor_report.md`)

Vezi `monitor_report.md` pentru exemplu complet.

## 🔍 Status Codes

- `online`: Site-ul răspunde corect ✅
- `timeout`: Request-ul a expirat ⏱️
- `connection_error`: Eroare de conexiune ❌
- `error`: Eroare neprevăzută ⚠️

## 📁 Structură Proiect

```
.
├── website_monitor.py       # Script principal
├── sites.json               # Configurație site-uri
├── requirements.txt         # Dependențe Python
├── README.md                # Această documentație
├── .github/
│   └── workflows/
│       ├── monitor.yml      # Workflow monitorizare
│       └── test.yml         # Workflow teste
└── monitor_report.json      # Raport generat (nu se comite)
```

## 🛠️ Dezvoltare

### Adăugare Teste

Creează folder `tests/` și adaugă teste:

```python
# tests/test_monitor.py
import pytest
from website_monitor import WebsiteMonitor

def test_load_config():
    monitor = WebsiteMonitor()
    assert len(monitor.sites) > 0
```

### Extindere Funcționalități

Poți extinde scriptul pentru:
- 📧 Notificări email la probleme
- 📱 Notificări Slack/Discord
- 📊 Dashboard vizual cu grafice
- 🔔 Alerting pe bază de threshold-uri

## 📝 Licență

Proiect open-source pentru monitorizare site-uri web.

## 🤝 Contribuții

Contribuțiile sunt binevenite! Deschide un issue sau pull request.

