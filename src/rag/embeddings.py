"""
Embedding management for RAG
"""
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.utils.logger import logger
import config


class EmbeddingManager:
    """Manage embeddings for vector store"""

    def __init__(self):
        """Initialize HuggingFace embeddings"""
        logger.info(f"Loading embedding model: {config.EMBEDDING_MODEL}")

        self.embeddings = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )

        logger.info("✅ Embedding model loaded")

    def get_embeddings(self):
        """Get embeddings instance"""
        return self.embeddings
