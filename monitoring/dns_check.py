from __future__ import annotations

import socket
from typing import Dict, Any, List
from urllib.parse import urlparse

from .common import append_markdown, now_iso, save_json, cfg


def check_dns(hostname: str) -> Dict[str, Any]:
	try:
		# Get IPv4
		ipv4 = socket.gethostbyname(hostname)
		
		# Get all addresses
		addr_info = socket.getaddrinfo(hostname, None)
		ips = list(set([info[4][0] for info in addr_info]))
		
		# Check reverse DNS (PTR)
		try:
			reverse_dns = socket.gethostbyaddr(ipv4)[0]
		except:
			reverse_dns = None
		
		return {
			"ipv4": ipv4,
			"all_ips": ips,
			"reverse_dns": reverse_dns,
			"ok": True,
			"error": None,
		}
	except Exception as e:
		return {
			"ipv4": None,
			"all_ips": [],
			"reverse_dns": None,
			"ok": False,
			"error": str(e),
		}


def run() -> Dict[str, Any]:
	host = urlparse(cfg.SITE_URL).hostname or ""
	
	dns_info = check_dns(host)
	
	result: Dict[str, Any] = {
		"host": host,
		**dns_info,
		"timestamp": now_iso(),
	}
	
	save_json("dns_check", result)
	status_line = f"- DNS: host={host} ipv4={result['ipv4']} ok={result['ok']}"
	if result["error"]:
		status_line += f" error={result['error']}"
	append_markdown("summary", status_line)
	
	return result


if __name__ == "__main__":
	print(run())

