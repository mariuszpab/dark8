# DARK8 OS - Web Search Engine
"""
Web search and browsing capabilities.
DuckDuckGo integration for privacy-respecting search.
"""

import re
from typing import Dict, List, Optional

from dark8_core.config import config
from dark8_core.logger import logger


class SearchEngine:
    """Search engine with DuckDuckGo integration"""

    def __init__(self):
        self.search_results_cache: Dict[str, List[Dict]] = {}

    async def search_duckduckgo(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search using DuckDuckGo API.

        Returns list of search results.
        """
        if not config.DUCKDUCKGO_ENABLED:
            return []

        try:
            import httpx

            params = {
                "q": query,
                "format": "json",
            }

            logger.info(f"[SEARCH] DuckDuckGo: {query}")

            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get("https://api.duckduckgo.com/", params=params)

                if response.status_code == 200:
                    data = response.json()

                    results = []

                    # Abstract results
                    if data.get("AbstractText"):
                        results.append(
                            {
                                "title": data.get("AbstractTitle", "Definition"),
                                "snippet": data.get("AbstractText"),
                                "url": data.get("AbstractURL", ""),
                            }
                        )

                    # Related results
                    for item in data.get("RelatedTopics", [])[:max_results]:
                        if "Text" in item:
                            results.append(
                                {
                                    "title": item.get("Text", "")[:100],
                                    "snippet": item.get("Text", ""),
                                    "url": item.get("FirstURL", ""),
                                }
                            )

                    return results[:max_results]

            return []
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []

    async def search_web(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Generic web search.
        Can be extended with other search engines.
        """
        # Try cache first
        cache_key = f"{query}:{max_results}"
        if cache_key in self.search_results_cache:
            return self.search_results_cache[cache_key]

        # Perform search
        results = await self.search_duckduckgo(query, max_results)

        # Cache results
        self.search_results_cache[cache_key] = results

        return results


class WebBrowser:
    """Lightweight web browser"""

    def __init__(self):
        self.current_url: Optional[str] = None
        self.history: List[str] = []
        self.cache: Dict[str, str] = {}

    async def fetch_page(self, url: str) -> str:
        """Fetch webpage content"""
        try:
            import httpx

            logger.info(f"[BROWSER] Fetching: {url}")

            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)

                if response.status_code == 200:
                    self.current_url = url
                    self.history.append(url)

                    # Cache content
                    self.cache[url] = response.text[:10000]  # First 10k chars

                    return response.text
                else:
                    return f"Error: HTTP {response.status_code}"
        except Exception as e:
            logger.error(f"Browser error: {e}")
            return f"Error: {e}"

    async def navigate(self, url: str) -> str:
        """Navigate to URL"""
        # Ensure URL has protocol
        if not url.startswith("http"):
            url = "https://" + url

        return await self.fetch_page(url)

    async def search_and_navigate(self, query: str) -> str:
        """Search query and navigate to first result"""
        search = SearchEngine()
        results = await search.search_web(query, max_results=1)

        if results and results[0].get("url"):
            return await self.navigate(results[0]["url"])

        return "No results found"

    def extract_text(self, html: str) -> str:
        """Extract readable text from HTML"""
        # Simple HTML stripping (in production use BeautifulSoup)
        text = re.sub("<[^<]+?>", "", html)
        text = re.sub("\s+", " ", text)
        return text.strip()[:1000]


class WebAnalyzer:
    """Analyze web content"""

    @staticmethod
    async def extract_links(html: str) -> List[str]:
        """Extract all links from HTML"""
        urls = re.findall(r'href=[\'"]?([^\'" >]+)', html)
        return list(set(urls))

    @staticmethod
    async def extract_text_blocks(html: str) -> List[str]:
        """Extract text blocks from HTML"""
        # Remove scripts and styles
        html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
        html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL)

        # Extract text from common elements
        blocks = re.findall(r"<(?:p|li|h[1-6])[^>]*>([^<]+)</(?:p|li|h[1-6])>", html)
        return [block.strip() for block in blocks if block.strip()]


# Singleton instances
_search_engine: Optional[SearchEngine] = None
_web_browser: Optional[WebBrowser] = None


def get_search_engine() -> SearchEngine:
    """Get search engine instance"""
    global _search_engine
    if _search_engine is None:
        _search_engine = SearchEngine()
    return _search_engine


def get_web_browser() -> WebBrowser:
    """Get web browser instance"""
    global _web_browser
    if _web_browser is None:
        _web_browser = WebBrowser()
    return _web_browser


__all__ = [
    "SearchEngine",
    "WebBrowser",
    "WebAnalyzer",
    "get_search_engine",
    "get_web_browser",
]
