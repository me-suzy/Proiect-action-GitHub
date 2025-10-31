from __future__ import annotations

import re
from collections import deque
from typing import Dict, Any, List
from urllib.parse import urlparse, urljoin

from .common import append_markdown, extract_links, http_request, is_allowed_url, now_iso, save_json, cfg


def extract_meta_tags(html: bytes) -> Dict[str, Any]:
	text = html.decode("utf-8", errors="ignore")
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


def check_seo_for_url(url: str) -> Dict[str, Any]:
	issues: List[str] = []
	warnings: List[str] = []
	
	try:
		resp = http_request(url)
		if resp.status != 200:
			return {"url": url, "status": resp.status, "error": f"HTTP {resp.status}"}
		
		# Skip non-HTML files
		content_type = resp.headers.get("content-type", "")
		if not content_type.startswith("text/html"):
			return None  # Skip CSS, JS, images, etc.
		
		metas = extract_meta_tags(resp.body)
		
		# Check title
		if not metas.get("title"):
			issues.append("Missing <title> tag")
		else:
			title_len = len(metas["title"])
			if title_len < 30:
				warnings.append(f"Title too short: {title_len} chars (recommend 30-60)")
			elif title_len > 60:
				warnings.append(f"Title too long: {title_len} chars (recommend 30-60)")
		
		# Check description
		if not metas.get("description"):
			issues.append("Missing meta description")
		else:
			desc_len = len(metas["description"])
			if desc_len < 120:
				warnings.append(f"Description too short: {desc_len} chars (recommend 120-160)")
			elif desc_len > 160:
				warnings.append(f"Description too long: {desc_len} chars (recommend 120-160)")
		
		# Check OG tags
		if not metas.get("og"):
			warnings.append("Missing Open Graph tags")
		
		# Check Schema.org
		if not metas.get("schema_ld_count"):
			warnings.append("No Schema.org JSON-LD")
		
		return {
			"url": url,
			"meta_tags": metas,
			"issues": issues,
			"warnings": warnings,
			"ok": len(issues) == 0,
		}
	except Exception as e:
		return {"url": url, "error": str(e)}


def run() -> Dict[str, Any]:
	# Start URLs: homepage + /en/ page
	start_urls = [cfg.SITE_URL]
	parsed_base = urlparse(cfg.SITE_URL)
	if parsed_base.path == "/" or parsed_base.path == "":
		start_urls.append(f"{parsed_base.scheme}://{parsed_base.netloc}/en/")
	
	queue: deque[str] = deque(start_urls)
	visited: set[str] = set()
	all_results: List[Dict[str, Any]] = []
	global_issues: List[Dict[str, Any]] = []
	global_warnings: List[Dict[str, Any]] = []
	count = 0
	max_pages = cfg.MAX_PAGES_CRAWL if hasattr(cfg, 'MAX_PAGES_CRAWL') else 100
	
	while queue and count < max_pages:
		url = queue.popleft()
		if url in visited:
			continue
		visited.add(url)
		count += 1
		
		# Check SEO for this URL
		result = check_seo_for_url(url)
		
		# Skip None results (non-HTML files)
		if result is None:
			visited.discard(url)  # Don't count as visited since we skipped it
			continue
		
		if "error" not in result or result["error"] is None:
			all_results.append(result)
			
			# Collect issues/warnings with URL
			if result.get("issues"):
				for issue in result["issues"]:
					global_issues.append({"url": url, "issue": issue})
			if result.get("warnings"):
				for warn in result["warnings"]:
					global_warnings.append({"url": url, "warning": warn})
			
			# Follow links from this page
			if "error" not in result:
				try:
					resp = http_request(url)
					for link in extract_links(resp.body, url):
						if is_allowed_url(link) and link not in visited:
							queue.append(link)
				except:
					pass
	
	final = {
		"total_pages_scanned": len(visited),
		"pages_with_seo_data": len(all_results),
		"global_issues_count": len(global_issues),
		"global_warnings_count": len(global_warnings),
		"detailed_results": all_results,
		"issues_by_url": global_issues,
		"warnings_by_url": global_warnings,
		"timestamp": now_iso(),
	}
	
	save_json("seo_crawler", final)
	append_markdown("summary", f"- SEO Crawler: scanned={final['total_pages_scanned']} issues={final['global_issues_count']} warnings={final['global_warnings_count']}")
	
	if global_issues:
		append_markdown("summary", "  Top issues:")
		for item in global_issues[:10]:
			append_markdown("summary", f"    - {item['url']}: {item['issue']}")
	
	if global_warnings:
		append_markdown("summary", "  Top warnings:")
		for item in global_warnings[:10]:
			append_markdown("summary", f"    - {item['url']}: {item['warning']}")
	
	return final


if __name__ == "__main__":
	print(run())

