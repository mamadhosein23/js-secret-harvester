import asyncio
from urllib.parse import urljoin, urlparse
import httpx
from bs4 import BeautifulSoup


class JSScraper:
    def __init__(self, concurrency_limit: int = 10, timeout: float = 10.0):
        # Semaphore restricts the number of concurrent tasks to prevent overloading
        self.semaphore = asyncio.Semaphore(concurrency_limit)
        self.timeout = httpx.Timeout(timeout)
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        }

    async def fetch_js_links(self, client: httpx.AsyncClient, base_url: str) -> list[str]:
        """Extract valid script sources from the HTML document."""
        try:
            response = await client.get(base_url)
            response.raise_for_status()

            # Using 'lxml' for superior parsing speed
            soup = BeautifulSoup(response.text, "lxml")
            js_urls = {
                urljoin(base_url, src)
                for tag in soup.find_all("script", src=True)
                if (src := tag.get("src"))
                and urlparse(urljoin(base_url, src)).scheme in ("http", "https")
            }
            return sorted(js_urls)
        except httpx.HTTPError as err:
            print(f"[!] Error fetching base URL ({base_url}): {err}")
            return []

    async def download_js_content(self, client: httpx.AsyncClient, js_url: str) -> tuple[str, str]:
        """Download JS content asynchronously with connection limiting."""
        async with self.semaphore:
            try:
                response = await client.get(js_url)
                response.raise_for_status()
                return js_url, response.text
            except httpx.HTTPError as err:
                print(f"[!] Failed to download ({js_url}): {err}")
                return js_url, ""

    async def run(self, base_url: str) -> dict[str, str]:
        """Orchestrates the scraping process using a persistent client."""
        async with httpx.AsyncClient(
            headers=self.headers,
            timeout=self.timeout,
            follow_redirects=True,
            http2=True,  # Enables HTTP/2 multiplexing
        ) as client:
            links = await self.fetch_js_links(client, base_url)
            if not links:
                return {}

            # Execute all download tasks concurrently
            tasks = [self.download_js_content(client, link) for link in links]
            results = await asyncio.gather(*tasks)
            return dict(results)

# Usage example:
# scraper = JSScraper(concurrency_limit=8)
# data = asyncio.run(scraper.run("https://example.com"))
