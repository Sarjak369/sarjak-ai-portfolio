"""
ChromaDB vector store management with LangChain
"""
import shutil
from pathlib import Path
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
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        self.vectorstore: Optional[Chroma] = None
        logger.info(f"✅ VectorStore initialized at {self.persist_directory}")

    # --------------------------------------------------------------------- #
    # Internal helpers
    # --------------------------------------------------------------------- #
    def _as_lc_documents(self, documents: List[Dict[str, Any]]) -> List[Document]:
        return [
            Document(
                page_content=str(doc.get("content", "")),
                metadata=dict(doc.get("metadata", {})),
            )
            for doc in documents
            if str(doc.get("content", "")).strip()
        ]

    def _ensure_loaded(self) -> None:
        """Load existing store if not already loaded."""
        if self.vectorstore is not None:
            return
        self.load_existing()

    # --------------------------------------------------------------------- #
    # Build / load
    # --------------------------------------------------------------------- #
    def create_from_documents(self, documents: List[Dict[str, Any]], reset: bool = False):
        """
        Create vector store from documents (optionally resetting existing data).
        """
        if reset:
            try:
                p = Path(self.persist_directory)
                if p.exists():
                    shutil.rmtree(p)
                    logger.info(
                        "🧹 Removed existing Chroma directory for reset")
            except Exception as e:
                logger.error(f"Failed to reset Chroma directory: {e}")

        lc_documents = self._as_lc_documents(documents)
        logger.info(
            f"Creating vector store with {len(lc_documents)} documents...")

        # Build fresh collection
        self.vectorstore = Chroma.from_documents(
            documents=lc_documents,
            embedding=self.embeddings,
            collection_name=self.collection_name,
            persist_directory=self.persist_directory,
        )
        # Persist to disk (works, though 0.4+ often auto-persists)
        assert self.vectorstore is not None
        try:
            self.vectorstore.persist()
        except Exception:
            # Safe to ignore if auto-persisting
            pass

        logger.info(
            f"✅ Vector store created with {len(lc_documents)} documents")

    def add_documents(self, documents: List[Dict[str, Any]]):
        """
        Incrementally add (or update) documents to the existing vector store.
        """
        lc_documents = self._as_lc_documents(documents)
        if not lc_documents:
            return

        self._ensure_loaded()
        if self.vectorstore is None:
            # If still None, create an empty collection and then add.
            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory,
            )

        assert self.vectorstore is not None
        try:
            self.vectorstore.add_documents(lc_documents)
            try:
                self.vectorstore.persist()
            except Exception:
                pass
            logger.info(
                f"➕ Added {len(lc_documents)} documents to vector store")
        except Exception as e:
            logger.error(f"Failed adding documents: {e}")

    def load_existing(self):
        """Load existing vector store (no-op if already loaded)."""
        if self.vectorstore is not None:
            return

        self.vectorstore = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory,
        )
        logger.info("✅ Loaded existing vector store")

    # --------------------------------------------------------------------- #
    # Query / stats
    # --------------------------------------------------------------------- #
    def similarity_search(self, query: str, k: int = 3) -> List[str]:
        """
        Search for similar documents and return their page_content strings.
        """
        self._ensure_loaded()
        if self.vectorstore is None:
            return []

        assert self.vectorstore is not None
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            return [doc.page_content for doc in results]
        except Exception as e:
            logger.error(f"Similarity search failed: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics."""
        try:
            self._ensure_loaded()
            if self.vectorstore is None:
                return {"name": self.collection_name, "document_count": 0, "status": "empty"}

            # Chroma exposes the underlying collection via a private attribute; use carefully.
            # type: ignore[attr-defined]
            collection = self.vectorstore._collection
            count = collection.count()
            return {
                "name": self.collection_name,
                "document_count": count,
                "status": "ready",
            }
        except Exception as e:
            return {"error": str(e)}
