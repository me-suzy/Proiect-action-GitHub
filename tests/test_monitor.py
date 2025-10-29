"""
Teste pentru WebsiteMonitor
"""

import pytest
import json
import os
import sys

# Adaugă folderul părinte la path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from website_monitor import WebsiteMonitor

def test_load_config():
    """Testează încărcarea configurației."""
    monitor = WebsiteMonitor()
    assert len(monitor.sites) > 0
    assert isinstance(monitor.sites, list)

def test_site_structure():
    """Testează structura unui site din config."""
    monitor = WebsiteMonitor()
    if len(monitor.sites) > 0:
        site = monitor.sites[0]
        assert "name" in site
        assert "url" in site
        assert "expected_status" in site
        assert "timeout" in site

def test_check_site_structure():
    """Testează că result-ul are toate câmpurile necesare."""
    monitor = WebsiteMonitor()
    if len(monitor.sites) > 0:
        result = monitor.check_site(monitor.sites[0])
        assert "name" in result
        assert "url" in result
        assert "timestamp" in result
        assert "status" in result
        assert "healthy" in result

def test_report_generation():
    """Testează generarea raportului."""
    monitor = WebsiteMonitor()
    monitor.results = [
        {
            "name": "Test Site",
            "url": "https://example.com",
            "status": "online",
            "healthy": True,
            "response_time": 100
        }
    ]
    
    report = monitor.generate_report("test_report.json")
    assert "summary" in report
    assert "results" in report
    assert report["summary"]["total_sites"] == 1
    assert report["summary"]["healthy_sites"] == 1
    
    # Cleanup
    if os.path.exists("test_report.json"):
        os.remove("test_report.json")

