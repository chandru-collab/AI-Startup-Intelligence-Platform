from pinecone import Pinecone, ServerlessSpec
from core.config import settings
import logging

logger = logging.getLogger(__name__)

class VectorStoreService:
    def __init__(self):
        self.api_key = settings.PINECONE_API_KEY
        self.environment = settings.PINECONE_ENVIRONMENT
        
        self.pc = Pinecone(api_key=self.api_key) if self.api_key else None
        self.index_name = "startup-intel"
        
        if not self.pc:
            logger.warning("PINECONE_API_KEY not set. Vector Store disabled.")
        else:
            self._ensure_index_exists()

    def _ensure_index_exists(self):
        try:
            if self.index_name not in self.pc.list_indexes().names():
                self.pc.create_index(
                    name=self.index_name,
                    dimension=1536, # Example: OpenAI embedding dimension. Adjust if using Grok embeddings.
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-east-1' # Use appropriate region based on env
                    )
                )
        except Exception as e:
            logger.error(f"Error ensuring Pinecone index exists: {e}")

    def upsert_vectors(self, vectors: list):
        if not self.pc:
            return False
            
        try:
            index = self.pc.Index(self.index_name)
            index.upsert(vectors=vectors)
            return True
        except Exception as e:
            logger.error(f"Error upserting to Pinecone: {e}")
            return False

vector_store = VectorStoreService()
