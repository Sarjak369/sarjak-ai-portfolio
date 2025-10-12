"""
ChromaDB vector store management with LangChain
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from src.utils.logger import logger
import config


class VectorStoreManager:
    """Manage ChromaDB vector store for RAG using LangChain"""

    def __init__(self, persist_directory: Optional[str] = None):
        """
        Initialize ChromaDB with LangChain

        Args:
            persist_directory: Directory to persist the database
        """
        if persist_directory is None:
            persist_directory = str(config.CHROMA_DB_DIR)

        self.persist_directory = persist_directory
        self.collection_name = config.COLLECTION_NAME

        # Initialize embeddings
        logger.info(f"Loading embedding model: {config.EMBEDDING_MODEL}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )

        self.vectorstore: Optional[Chroma] = None

        logger.info(f"✅ VectorStore initialized at {persist_directory}")

    def create_from_documents(self, documents: List[Dict[str, Any]], reset: bool = False):
        """
        Create vector store from documents using LangChain

        Args:
            documents: List of document dicts with 'content' and 'metadata'
            reset: If True, delete existing and create new
        """
        # Convert to LangChain documents
        lc_documents = [
            Document(
                page_content=doc["content"],
                metadata=doc["metadata"]
            )
            for doc in documents
        ]

        logger.info(
            f"Creating vector store with {len(lc_documents)} documents...")

        # Create vector store
        self.vectorstore = Chroma.from_documents(
            documents=lc_documents,
            embedding=self.embeddings,
            collection_name=self.collection_name,
            persist_directory=self.persist_directory
        )

        logger.info(f"✅ Vector store created with {len(documents)} documents")

    def load_existing(self):
        """Load existing vector store"""
        try:
            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )
            logger.info("✅ Loaded existing vector store")
        except Exception as e:
            logger.error(f"Failed to load vector store: {e}")
            raise

    def similarity_search(self, query: str, k: int = 3) -> List[str]:
        """
        Search for similar documents

        Args:
            query: Query text
            k: Number of results

        Returns:
            List of document contents
        """
        if not self.vectorstore:
            self.load_existing()

        if self.vectorstore:
            results = self.vectorstore.similarity_search(query, k=k)
            return [doc.page_content for doc in results]

        return []

    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics"""
        if not self.vectorstore:
            return {"error": "Vector store not initialized"}

        try:
            # Get collection
            collection = self.vectorstore._collection  # type: ignore
            count = collection.count()

            return {
                "name": self.collection_name,
                "document_count": count,
                "status": "ready"
            }
        except Exception as e:
            return {"error": str(e)}
