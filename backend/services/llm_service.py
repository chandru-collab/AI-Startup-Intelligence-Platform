import os
import logging
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from core.config import settings

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.grok_api_key = settings.GROK_API_KEY
        self.openrouter_api_key = settings.OPENROUTER_API_KEY
        
        # Prioritize OpenRouter with high-speed models (gpt-4o-mini) as primary for ultra-fast latency
        if self.openrouter_api_key:
            self.primary_llm = self._init_openrouter()
            self.fallback_llm = self._init_grok() if self.grok_api_key else None
        else:
            self.primary_llm = self._init_grok() if self.grok_api_key else None
            self.fallback_llm = None
        
        if not self.primary_llm and not self.fallback_llm:
            logger.warning("No LLM API keys provided. Agents will not function.")

    def _init_openrouter(self):
        return ChatOpenAI(
            api_key=self.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
            model="openai/gpt-4o-mini", # High-speed ~300ms model
            temperature=0,
            max_tokens=800,
            request_timeout=10
        )

    def _init_grok(self):
        # xAI Grok API is OpenAI compatible
        return ChatOpenAI(
            api_key=self.grok_api_key,
            base_url="https://api.x.ai/v1",
            model="grok-beta", 
            temperature=0,
            max_tokens=800,
            request_timeout=15
        )

    def get_llm(self):
        """
        Returns the primary LLM, or the fallback if primary is unavailable.
        Uses Langchain's `.with_fallbacks()` for automatic failover.
        """
        if self.primary_llm and self.fallback_llm:
            return self.primary_llm.with_fallbacks([self.fallback_llm])
        elif self.primary_llm:
            return self.primary_llm
        elif self.fallback_llm:
            return self.fallback_llm
        else:
            raise ValueError("No LLM configured. Please set GROK_API_KEY or OPENROUTER_API_KEY.")

llm_service = LLMService()

def get_llm():
    return llm_service.get_llm()
