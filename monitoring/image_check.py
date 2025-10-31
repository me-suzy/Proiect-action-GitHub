from __future__ import annotations

import re
from typing import Dict, Any, List, Tuple, Optional
from urllib.parse import urlparse, urljoin

from .common import append_markdown, http_request, now_iso, save_json, cfg


def extract_images(html: bytes, base_url: str) -> List[str]:
	text = html.decode("utf-8", errors="ignore")
	urls: List[str] = []
	
	# Extract img src and srcset
	for pattern in (
		r'<img[^>]+src=["\']([^"\']+)["\']',
		r'<img[^>]+srcset=["\']([^"\']+)["\']',
		r"<img[^>]+src=([^\s>]+)",
	):
		for match in re.findall(pattern, text, re.IGNORECASE):
			urls.append(urljoin(base_url, match))
	
	# Extract background-image from inline CSS
	for match in re.findall(r'background-image:\s*url\(["\']?([^"\')]+)["\']?\)', text, re.IGNORECASE):
		urls.append(urljoin(base_url, match))
	
	return urls


def check_image(url: str) -> Tuple[bool, Optional[str], Optional[Dict[str, str]]]:
	try:
		resp = http_request(url, timeout=10)
		if resp.status != 200:
			return False, f"HTTP {resp.status}", None
		
		content_type = resp.headers.get("content-type", "")
		if not content_type.startswith("image/"):
			return False, f"Not an image: {content_type}", None
		
		# Check for modern formats
		modern_formats = ["image/webp", "image/avif"]
		is_modern = any(fmt in content_type for fmt in modern_formats)
		
		# Check for loading="lazy"
		# This would require parsing the HTML where the image is referenced
		# For now, just check if it exists
		
		return True, None, {
			"content_type": content_type,
			"size_bytes": len(resp.body),
			"is_modern_format": is_modern,
		}
	except Exception as e:
		return False, str(e), None


def run() -> Dict[str, Any]:
	resp = http_request(cfg.SITE_URL)
	if resp.status != 200:
		return {
			"error": f"Failed to fetch homepage: HTTP {resp.status}",
			"timestamp": now_iso(),
		}
	
	# Extract images from homepage
	img_urls = extract_images(resp.body, cfg.SITE_URL)
	
	# Check first 20 images
	checked = 0
	issues: List[Dict[str, Any]] = []
	warnings: List[Dict[str, Any]] = []
	
	for img_url in img_urls[:20]:
		checked += 1
		ok, error, info = check_image(img_url)
		
		if not ok:
			issues.append({"url": img_url, "error": error})
		elif info:
			# Warning for large images without modern format
			if info["size_bytes"] > 500_000 and not info["is_modern_format"]:  # > 500KB
				warnings.append({
					"url": img_url,
					"size_kb": round(info["size_bytes"] / 1024, 1),
					"format": info["content_type"],
				})
	
	result: Dict[str, Any] = {
		"total_images_found": len(img_urls),
		"images_checked": checked,
		"issues": issues,
		"warnings": warnings,
		"ok": len(issues) == 0,
		"timestamp": now_iso(),
	}
	
	save_json("image_check", result)
	append_markdown("summary", f"- Images: found={result['total_images_found']} checked={checked} issues={len(issues)} warnings={len(warnings)}")
	
	return result


if __name__ == "__main__":
	print(run())

