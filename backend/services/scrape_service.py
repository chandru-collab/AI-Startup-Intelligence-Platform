from firecrawl import FirecrawlApp
import requests
from core.config import settings
import logging

logger = logging.getLogger(__name__)

class ScrapeService:
    def __init__(self):
        self.firecrawl_key = settings.FIRECRAWL_API_KEY
        self.jina_key = settings.JINA_API_KEY
        
        self.firecrawl = FirecrawlApp(api_key=self.firecrawl_key) if self.firecrawl_key else None
        
        if not self.firecrawl:
            logger.warning("FIRECRAWL_API_KEY not set. Firecrawl scraping disabled.")

    def scrape_url_firecrawl(self, url: str) -> dict:
        """
        Scrape a URL using Firecrawl.
        """
        if not self.firecrawl:
            return {"error": "Firecrawl not initialized."}
            
        try:
            # Using scrape_url directly from FirecrawlApp
            result = self.firecrawl.scrape_url(url, params={'pageOptions': {'onlyMainContent': True}})
            return result
        except Exception as e:
            logger.error(f"Firecrawl error scraping {url}: {e}")
            return {"error": str(e)}

    def read_url_jina(self, url: str) -> str:
        """
        Extract clean content from a URL using Jina AI Reader.
        """
        try:
            headers = {}
            if self.jina_key:
                headers["Authorization"] = f"Bearer {self.jina_key}"
                
            response = requests.get(f"https://r.jina.ai/{url}", headers=headers, timeout=3)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.warning(f"Jina Reader timeout/error for {url}: {e}")
            return ""

scrape_service = ScrapeService()
