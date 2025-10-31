from __future__ import annotations

import re
from typing import Dict, Any, List, Optional

from .common import append_markdown, http_request, now_iso, save_json, cfg


def extract_meta_tags(html: bytes) -> Dict[str, Any]:
	text = html.decode("utf-8", errors="ignore").lower()
	metas: Dict[str, Any] = {}
	
	# Title
	title_match = re.search(r"<title>(.*?)</title>", text, re.DOTALL | re.IGNORECASE)
	if title_match:
		metas["title"] = title_match.group(1).strip()
	
	# Meta description
	desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', text, re.IGNORECASE)
	if desc_match:
		metas["description"] = desc_match.group(1).strip()
	
	# Open Graph tags
	og_tags = {}
	for tag in ["title", "description", "image", "url", "type"]:
		match = re.search(rf'<meta\s+property=["\']og:{tag}["\']\s+content=["\']([^"\']+)["\']', text, re.IGNORECASE)
		if match:
			og_tags[tag] = match.group(1).strip()
	if og_tags:
		metas["og"] = og_tags
	
	# Schema.org JSON-LD
	schema_matches = re.findall(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', text, re.DOTALL | re.IGNORECASE)
	if schema_matches:
		metas["schema_ld_count"] = len(schema_matches)
	
	return metas


def run() -> Dict[str, Any]:
	resp = http_request(cfg.SITE_URL)
	html = resp.body
	
	# Extract meta tags
	metas = extract_meta_tags(html)
	
	# Check for issues
	issues: List[str] = []
	warnings: List[str] = []
	
	if not metas.get("title"):
		issues.append("Missing <title> tag")
	elif len(metas["title"]) < 30:
		warnings.append(f"Title too short: {len(metas['title'])} chars (recommend 30-60)")
	elif len(metas["title"]) > 60:
		warnings.append(f"Title too long: {len(metas['title'])} chars (recommend 30-60)")
	
	if not metas.get("description"):
		issues.append("Missing meta description")
	elif len(metas["description"]) < 120:
		warnings.append(f"Description too short: {len(metas['description'])} chars (recommend 120-160)")
	elif len(metas["description"]) > 160:
		warnings.append(f"Description too long: {len(metas['description'])} chars (recommend 120-160)")
	
	if not metas.get("og"):
		warnings.append("Missing Open Graph tags (Facebook/LinkedIn sharing)")
	
	if not metas.get("schema_ld_count"):
		warnings.append("No Schema.org JSON-LD structured data")
	
	result: Dict[str, Any] = {
		"status": resp.status,
		"meta_tags": metas,
		"issues": issues,
		"warnings": warnings,
		"ok": len(issues) == 0,
		"timestamp": now_iso(),
	}
	
	save_json("seo_check", result)
	append_markdown("summary", f"- SEO: status={resp.status} issues={len(issues)} warnings={len(warnings)}")
	if issues:
		append_markdown("summary", "  Issues:")
		for issue in issues:
			append_markdown("summary", f"    - {issue}")
	if warnings:
		append_markdown("summary", "  Warnings:")
		for warn in warnings:
			append_markdown("summary", f"    - {warn}")
	
	return result


if __name__ == "__main__":
	print(run())

