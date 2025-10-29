"""
Website Monitor & Health Checker
Monitorizează mai multe site-uri, verifică statusul, timpul de răspuns și generează rapoarte.
Perfect pentru monitorizarea serviciilor web.
"""

import requests
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
import os
import sys

class WebsiteMonitor:
    def __init__(self, config_file: str = "sites.json"):
        """Inițializează monitorul cu lista de site-uri."""
        self.config_file = config_file
        self.sites = self.load_config()
        self.results = []
        
    def load_config(self) -> List[Dict]:
        """Încarcă configurația site-urilor din JSON."""
        if not os.path.exists(self.config_file):
            # Creează un fișier de configurație exemplu
            default_config = {
                "sites": [
                    {
                        "name": "GitHub",
                        "url": "https://github.com",
                        "expected_status": 200,
                        "timeout": 10
                    },
                    {
                        "name": "Google",
                        "url": "https://www.google.com",
                        "expected_status": 200,
                        "timeout": 10
                    }
                ]
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            return default_config["sites"]
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get("sites", [])
    
    def check_site(self, site: Dict) -> Dict:
        """Verifică un singur site și returnează rezultatul."""
        name = site.get("name", "Unknown")
        url = site.get("url", "")
        expected_status = site.get("expected_status", 200)
        timeout = site.get("timeout", 10)
        
        result = {
            "name": name,
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "status": "unknown",
            "status_code": None,
            "response_time": None,
            "error": None,
            "healthy": False
        }
        
        try:
            start_time = time.time()
            response = requests.get(url, timeout=timeout, allow_redirects=True)
            response_time = round((time.time() - start_time) * 1000, 2)  # în milisecunde
            
            result["status_code"] = response.status_code
            result["response_time"] = response_time
            result["status"] = "online"
            result["healthy"] = (
                response.status_code == expected_status and 
                response_time < (timeout * 1000)
            )
            
            if not result["healthy"]:
                if response.status_code != expected_status:
                    result["error"] = f"Status code {response.status_code} != {expected_status}"
                else:
                    result["error"] = f"Response time {response_time}ms > {timeout * 1000}ms"
            
        except requests.exceptions.Timeout:
            result["status"] = "timeout"
            result["error"] = f"Request timeout after {timeout}s"
        except requests.exceptions.ConnectionError:
            result["status"] = "connection_error"
            result["error"] = "Connection refused or DNS error"
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def check_all_sites(self) -> List[Dict]:
        """Verifică toate site-urile din configurație."""
        print(f"\n🔍 Verificare {len(self.sites)} site-uri...\n")
        self.results = []
        
        for site in self.sites:
            print(f"  ⏳ Verificare: {site['name']} ({site['url']})")
            result = self.check_site(site)
            self.results.append(result)
            
            if result["healthy"]:
                print(f"     ✅ Online - {result['response_time']}ms")
            else:
                status_icon = "⚠️" if result["status"] == "online" else "❌"
                print(f"     {status_icon} {result['status']} - {result.get('error', 'N/A')}")
        
        return self.results
    
    def generate_report(self, output_file: str = "monitor_report.json") -> Dict:
        """Generează un raport JSON cu toate rezultatele."""
        healthy_count = sum(1 for r in self.results if r["healthy"])
        total_count = len(self.results)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_sites": total_count,
                "healthy_sites": healthy_count,
                "unhealthy_sites": total_count - healthy_count,
                "uptime_percentage": round((healthy_count / total_count * 100), 2) if total_count > 0 else 0
            },
            "results": self.results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 Raport generat: {output_file}")
        print(f"   ✅ Site-uri sănătoase: {healthy_count}/{total_count}")
        print(f"   📈 Uptime: {report['summary']['uptime_percentage']}%")
        
        return report
    
    def generate_markdown_report(self, output_file: str = "monitor_report.md") -> str:
        """Generează un raport Markdown frumos formatat."""
        healthy_count = sum(1 for r in self.results if r["healthy"])
        total_count = len(self.results)
        uptime_percent = round((healthy_count / total_count * 100), 2) if total_count > 0 else 0
        
        md_content = f"""# 📊 Website Monitor Report

**Generat:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📈 Summary

| Metric | Value |
|--------|-------|
| Total Sites | {total_count} |
| ✅ Healthy | {healthy_count} |
| ❌ Unhealthy | {total_count - healthy_count} |
| 📊 Uptime | {uptime_percent}% |

## 🔍 Detailed Results

"""
        
        for result in self.results:
            status_icon = "✅" if result["healthy"] else "❌"
            status_badge = "🟢 ONLINE" if result["healthy"] else f"🔴 {result['status'].upper()}"
            
            md_content += f"""### {status_icon} {result['name']}

- **URL:** {result['url']}
- **Status:** {status_badge}
- **Status Code:** {result.get('status_code', 'N/A')}
- **Response Time:** {result.get('response_time', 'N/A')}ms
"""
            
            if result.get('error'):
                md_content += f"- **Error:** `{result['error']}`\n"
            
            md_content += f"- **Timestamp:** {result['timestamp']}\n\n"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"📝 Markdown report generat: {output_file}")
        return output_file

def main():
    """Funcție principală."""
    monitor = WebsiteMonitor()
    
    print("🌐 Website Monitor & Health Checker")
    print("=" * 50)
    
    # Verifică toate site-urile
    monitor.check_all_sites()
    
    # Generează rapoarte
    monitor.generate_report()
    monitor.generate_markdown_report()
    
    # Exit code pentru GitHub Actions
    healthy_count = sum(1 for r in monitor.results if r["healthy"])
    total_count = len(monitor.results)
    
    if healthy_count < total_count:
        print("\n⚠️  Unele site-uri nu sunt sănătoase!")
        sys.exit(1)  # Eșec pentru Actions
    else:
        print("\n✅ Toate site-urile sunt sănătoase!")
        sys.exit(0)  # Succes

if __name__ == "__main__":
    main()

