import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def fetch_js_links(base_url: str, timeout: int = 10) -> list[str]:
    """دریافت تمام لینک‌های اسکریپت JS از سورس صفحه HTML."""
    js_urls = set()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        with httpx.Client(timeout=timeout, verify=False, follow_redirects=True, headers=headers) as client:
            response = client.get(base_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            for script_tag in soup.find_all("script"):
                src = script_tag.get("src")
                if src:
                    full_url = urljoin(base_url, src)
                    parsed = urlparse(full_url)
                    if parsed.scheme in ("http", "https"):
                        js_urls.add(full_url)

    except httpx.HTTPError as err:
        print(f"[!] Error fetching base URL {base_url}: {err}")

    return sorted(list(js_urls))


def download_js_content(js_url: str, timeout: int = 10) -> str:
    """دانلود محتوای خام یک فایل JS."""
    try:
        with httpx.Client(timeout=timeout, verify=False, follow_redirects=True) as client:
            response = client.get(js_url)
            response.raise_for_status()
            return response.text
    except httpx.HTTPError as err:
        print(f"[!] Failed to download JS from {js_url}: {err}")
        return ""
