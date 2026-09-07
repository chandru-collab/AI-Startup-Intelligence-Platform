from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Startup Intelligence Platform"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your_super_secret_jwt_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DATABASE_URL: str = "sqlite:///./startup_intel.db"
    
    # API Keys
    GROK_API_KEY: str | None = None
    OPENROUTER_API_KEY: str | None = None
    TAVILY_API_KEY: str | None = None
    FIRECRAWL_API_KEY: str | None = None
    JINA_API_KEY: str | None = None
    
    # LangSmith Observability
    LANGCHAIN_TRACING_V2: str = "true"
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGCHAIN_API_KEY: str | None = None
    LANGCHAIN_PROJECT: str = "ai-startup-intelligence"
    
    PINECONE_API_KEY: str | None = None
    PINECONE_ENVIRONMENT: str | None = None
    
    JWT_SECRET: str | None = None

    class Config:
        env_file = "../.env"
        extra = "ignore"

settings = Settings()
