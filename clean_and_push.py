"""
Script pentru curățarea completă a istoricului Git și push curat
Șterge toate commit-urile vechi care conțin token-ul.
"""

import subprocess
import os
import sys

def run_cmd(command, check=True):
    """Rulează o comandă shell."""
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True, encoding='utf-8')
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        return None, str(e)

def main():
    print("=" * 60)
    print("🧹 Curățare Completă Istoric Git")
    print("=" * 60)
    print()
    
    # 1. Șterge toate commit-urile (păstrează fișierele)
    print("🗑️  Ștergere istoric Git complet...")
    run_cmd("git update-ref -d HEAD")
    print("✅ Istoric șters")
    
    # 2. Verifică că token-ul nu e în fișiere (doar working directory, NU istoric)
    print("\n🔍 Verificare token în fișiere...")
    import glob
    found_token = False
    for py_file in glob.glob("*.py"):
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'ghp_' in content:
                print(f"⚠️  Token găsit în: {py_file}")
                found_token = True
    if found_token:
        print("⚠️  ATENȚIE: Token încă găsit în fișiere!")
        print("   Verifică push_to_github.py - trebuie să fie gol TOKEN_GITHUB = \"\"")
        response = input("   Continuăm oricum? (y/N): ")
        if response.lower() != 'y':
            print("❌ Anulat")
            sys.exit(1)
    else:
        print("✅ Nu s-a găsit token în fișiere")
    
    # 3. Adaugă toate fișierele
    print("\n📝 Adăugare fișiere...")
    run_cmd("git add .")
    
    # Verifică ce s-a adăugat
    stdout, _ = run_cmd("git status --short")
    if stdout:
        print("✅ Fișiere adăugate:")
        for line in stdout.split('\n'):
            if line.strip():
                print(f"   {line}")
    
    # 4. Commit nou curat
    print("\n💾 Creare commit curat...")
    commit_msg = "Initial commit: Website Monitor & Health Checker (clean history)"
    run_cmd(f'git commit -m "{commit_msg}"')
    print("✅ Commit creat")
    
    # 5. Force push (suprascrie tot pe remote)
    print("\n🚀 Force push pe GitHub...")
    print("⚠️  ATENȚIE: Această operație va șterge complet istoricul de pe GitHub!")
    response = input("   Continui cu force push? (y/N): ")
    
    if response.lower() == 'y':
        stdout, stderr = run_cmd("git push origin main --force", check=False)
        if stdout or "Everything up-to-date" in (stderr or ""):
            print("✅ Push reușit!")
            print("\n🎉 Repository curat și disponibil la:")
            print("   https://github.com/me-suzy/Proiect-action-GitHub")
        else:
            print("❌ Push eșuat!")
            print(f"   Eroare: {stderr}")
            print("\n💡 Încearcă opțiunea de mai jos: Ștergere repository complet")
    else:
        print("❌ Anulat. Istoricul local este curat, dar nu s-a făcut push.")
        print("\n💡 Pentru a face push manual:")
        print("   git push origin main --force")

    print("\n" + "=" * 60)
    print("✅ COMPLET!")
    print("=" * 60)

if __name__ == "__main__":
    main()

