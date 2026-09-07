from tavily import TavilyClient
from core.config import settings
import logging

logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self):
        self.api_key = settings.TAVILY_API_KEY
        self.client = TavilyClient(api_key=self.api_key) if self.api_key else None
        
        if not self.client:
            logger.warning("TAVILY_API_KEY not set. Search Service will be disabled.")

    def search_startup_info(self, startup_name: str) -> dict:
        """
        Perform a comprehensive search for a startup.
        """
        if not self.client:
            return {"error": "Tavily client not initialized."}
            
        try:
            query = f"{startup_name} startup company profile funding founders product"
            response = self.client.search(query=query, search_depth="basic", max_results=4)
            return response
        except Exception as e:
            logger.error(f"Error searching for {startup_name}: {e}")
            return {"error": str(e)}

    def search(self, query: str) -> dict:
        """
        Perform a general search query.
        """
        if not self.client:
            return {"error": "Tavily client not initialized."}
            
        try:
            response = self.client.search(query=query, search_depth="basic")
            return response
        except Exception as e:
            logger.error(f"Error executing search query '{query}': {e}")
            with open("search_error.log", "a") as f:
                f.write(f"Query: {query}, Error: {str(e)}\n")
            return {"error": str(e)}

search_service = SearchService()
