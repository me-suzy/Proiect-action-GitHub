"""
Script Python pentru push automat pe GitHub
- Creează (dacă lipsește) repository-ul pe GitHub prin API
- Asigură structura de foldere (.github/workflows)
- Face commit și push pe branch-ul main

ATENȚIE: Setează USER_GITHUB și TOKEN_GITHUB mai jos sau prin variabile
         de mediu GITHUB_USER / GITHUB_TOKEN.
"""

import subprocess
import os
import sys
from pathlib import Path
import json
import urllib.request
import urllib.error

# ========================================
# CONFIGURARE - NU PUNE TOKEN-UL AICI! Folosește doar variabile de mediu sau config.py
# ========================================
USER_GITHUB = "me-suzy"            # Ex: "ME-SUZY" sau "me-suzy"
TOKEN_GITHUB = ""                  # LASĂ GOL! Folosește GITHUB_TOKEN env var sau config.py
REPO_NAME = "Proiect-action-GitHub"  # Numele repository-ului pe GitHub
REPO_OWNER = ""                    # Lasă gol dacă e același cu USER_GITHUB
PRIVATE_REPO = False               # True pentru privat
REPO_DESCRIPTION = "Website Monitor & Health Checker (automatizare cu GitHub Actions)"
# ========================================

REQUIRED_DIRS = [
    ".github",
    ".github/workflows"
]

REQUIRED_FILES = {
    ".gitignore": "# Rapoarte generate\nmonitor_report.json\nmonitor_report.md\n\n# Config local\nconfig.py\n\n# Python\n__pycache__/\n*.py[cod]\n*$py.class\n\n# Venv\nvenv/\nENV/\nenv/\n\n# IDE\n.vscode/\n.idea/\n\n# OS\n.DS_Store\nThumbs.db\n\n# Test\n.pytest_cache/\n.coverage\nhtmlcov/\n",
}

def load_config():
    """Încarcă configurația din variabile de mediu, config.py sau variabilele de mai sus."""
    global USER_GITHUB, TOKEN_GITHUB, REPO_NAME, REPO_OWNER

    # Încearcă să citească din fișier config.py local (dacă există, nu se comite)
    try:
        if os.path.exists("config.py"):
            import importlib.util
            spec = importlib.util.spec_from_file_location("config", "config.py")
            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)
            if hasattr(config_module, "TOKEN_GITHUB") and config_module.TOKEN_GITHUB:
                TOKEN_GITHUB = config_module.TOKEN_GITHUB
            if hasattr(config_module, "USER_GITHUB") and config_module.USER_GITHUB:
                USER_GITHUB = config_module.USER_GITHUB
    except Exception:
        pass  # Ignoră erori la încărcarea config.py

    # Încearcă să citească din variabile de mediu (prioritate maximă)
    USER_GITHUB = os.getenv("GITHUB_USER", USER_GITHUB)
    TOKEN_GITHUB = os.getenv("GITHUB_TOKEN", TOKEN_GITHUB)
    REPO_OWNER = os.getenv("GITHUB_REPO_OWNER", REPO_OWNER if REPO_OWNER else USER_GITHUB)

    if not USER_GITHUB:
        print("❌ ERROR: USER_GITHUB nu este setat!")
        print("   Setează-l prin variabilă de mediu: GITHUB_USER")
        print("   Sau creează config.py cu: USER_GITHUB = 'me-suzy'")
        sys.exit(1)

    if not TOKEN_GITHUB:
        print("❌ ERROR: TOKEN_GITHUB nu este setat!")
        print("   Setează-l prin variabilă de mediu: GITHUB_TOKEN")
        print("   Sau creează config.py cu: TOKEN_GITHUB = 'ghp_xxxxx'")
        print("   (config.py este deja în .gitignore, nu se va comita)")
        sys.exit(1)

    return USER_GITHUB, TOKEN_GITHUB, REPO_NAME, REPO_OWNER

def run_command(command: str, check: bool = True, capture_output: bool = False):
    """Rulează o comandă shell și returnează rezultatul."""
    try:
        if capture_output:
            result = subprocess.run(
                command,
                shell=True,
                check=check,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            return result.stdout.strip(), result.stderr.strip()
        else:
            subprocess.run(command, shell=True, check=check)
            return None, None
    except subprocess.CalledProcessError as e:
        print(f"❌ Eroare la comanda: {command}")
        print(f"   Mesaj: {getattr(e, 'stderr', '') or str(e)}")
        if check:
            sys.exit(1)
        return None, str(e)

def check_git_installed() -> bool:
    stdout, _ = run_command("git --version", check=False, capture_output=True)
    if stdout and "git version" in stdout:
        print(f"✅ Git instalat: {stdout}")
        return True
    print("❌ Git nu este instalat! Instalează Git: https://git-scm.com/")
    return False

def ensure_structure():
    """Creează folderele necesare și fișiere minime dacă lipsesc."""
    for d in REQUIRED_DIRS:
        Path(d).mkdir(parents=True, exist_ok=True)
    for path, content in REQUIRED_FILES.items():
        p = Path(path)
        if not p.exists():
            p.write_text(content, encoding='utf-8')


def github_api_request(method: str, url: str, token: str, data: dict | None = None):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "repo-bootstrap-script"
    }
    req = urllib.request.Request(url, method=method, headers=headers)
    if data is not None:
        body = json.dumps(data).encode('utf-8')
        req.add_header("Content-Type", "application/json")
    else:
        body = None

    try:
        with urllib.request.urlopen(req, data=body) as resp:
            payload = resp.read().decode('utf-8')
            return resp.getcode(), json.loads(payload) if payload else {}
    except urllib.error.HTTPError as e:
        try:
            payload = e.read().decode('utf-8')
            return e.code, json.loads(payload) if payload else {}
        except Exception:
            return e.code, {"message": str(e)}
    except Exception as e:
        return 0, {"message": str(e)}


def ensure_github_repo(owner: str, repo: str, token: str, private: bool = False, description: str = ""):
    """Creează repository-ul dacă nu există. Returnează True dacă există/creat OK."""
    repo_url = f"https://api.github.com/repos/{owner}/{repo}"
    status, _ = github_api_request("GET", repo_url, token)
    if status == 200:
        print(f"✅ Repository există deja: {owner}/{repo}")
        return True
    if status not in (404, 0):
        print(f"⚠️  Nu am putut verifica repo (status {status}). Încerc să-l creez…")

    # POST /user/repos creează în contul autenticat
    create_url = "https://api.github.com/user/repos"
    payload = {
        "name": repo,
        "private": private,
        "description": description or REPO_DESCRIPTION,
        "auto_init": False,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True
    }
    status, resp = github_api_request("POST", create_url, token, payload)
    if status in (201, 202):
        print(f"✅ Repository creat: https://github.com/{owner}/{repo}")
        return True
    elif status == 422 and isinstance(resp, dict) and "already exists" in str(resp):
        print("ℹ️  Repo pare să existe deja. Continui…")
        return True
    else:
        print(f"❌ Creare repo eșuată (status {status}): {resp}")
        print("   Verifică dacă token-ul are scope 'repo' și owner-ul e corect.")
        return False


def init_repo():
    if os.path.exists(".git"):
        print("✅ Repository Git există deja")
        return
    print("📦 Inițializare repository Git…")
    run_command("git init")
    print("✅ Repository inițializat")


def setup_git_config():
    stdout, _ = run_command("git config user.name", check=False, capture_output=True)
    if not stdout:
        print("⚠️  Git user.name/email nu sunt setate. Exemplu:")
        print("   git config --global user.name \"Numele Tău\"")
        print("   git config --global user.email \"email@exemplu.com\"")


def add_all_files():
    print("📝 Adăugare fișiere…")
    run_command("git add .")
    stdout, _ = run_command("git status --short", capture_output=True)
    if stdout:
        print("✅ Fișiere adăugate:")
        for line in stdout.split("\n"):
            if line.strip():
                print(f"   {line}")
    else:
        print("ℹ️  Nu s-au găsit fișiere noi")


def create_commit(message: str = "Initial commit"):
    print(f"💾 Creare commit: '{message}'…")
    run_command(f"git commit -m \"{message}\"")
    print("✅ Commit creat")


def setup_remote(owner: str, repo_name: str):
    remote_url = f"https://{USER_GITHUB}:{TOKEN_GITHUB}@github.com/{owner}/{repo_name}.git"
    stdout, _ = run_command("git remote -v", check=False, capture_output=True)
    if "origin" in (stdout or ""):
        print("🔄 Actualizare remote 'origin'…")
        run_command(f"git remote set-url origin {remote_url}")
    else:
        print("➕ Adăugare remote 'origin'…")
        run_command(f"git remote add origin {remote_url}")
    print(f"✅ Remote configurat: github.com/{owner}/{repo_name}")


def create_branch(branch_name: str = "main"):
    print(f"🌿 Creare branch '{branch_name}'…")
    run_command(f"git branch -M {branch_name}")
    print(f"✅ Branch '{branch_name}' setat")


def push_to_github(branch_name: str = "main"):
    print(f"🚀 Push pe GitHub (branch: {branch_name})…")
    run_command(f"git push -u origin {branch_name}")
    print("✅ Push reușit!")
    print("\n🎉 Repository disponibil la:")
    print(f"   https://github.com/{REPO_OWNER}/{REPO_NAME}")


def main():
    print("=" * 60)
    print("🚀 GitHub Push Script – auto-create repo")
    print("=" * 60)
    print()

    # Încarcă config + verificări
    load_config()
    if not check_git_installed():
        sys.exit(1)

    # Creează structura minimă locală
    ensure_structure()

    # Creează repository-ul pe GitHub dacă lipsește
    owner = REPO_OWNER or USER_GITHUB
    if not ensure_github_repo(owner, REPO_NAME, TOKEN_GITHUB, PRIVATE_REPO, REPO_DESCRIPTION):
        sys.exit(1)

    # Inițializează git, commit și push
    setup_git_config()
    init_repo()
    add_all_files()

    # Mesaj commit
    commit_message = input("\n💬 Mesaj commit (Enter pentru 'Initial commit'): ").strip() or \
                     "Initial commit: Website Monitor & Health Checker"
    create_commit(commit_message)

    setup_remote(owner, REPO_NAME)
    create_branch("main")
    push_to_github("main")

    print("\n" + "=" * 60)
    print("✅ COMPLET!")
    print("=" * 60)


if __name__ == "__main__":
    main()


