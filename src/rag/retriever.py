"""
RAG retrieval system using LangChain
"""
from typing import List, Dict, Any, Optional
from src.rag.data_loader import DataLoader
from src.rag.vectorstore import VectorStoreManager
from src.llm.model import LLMInterface
from src.utils.logger import logger
import config


class RAGRetriever:
    """LangChain-based RAG system for intelligent query answering"""

    def __init__(self, reset_db: bool = False, llm_provider: Optional[str] = None):
        """
        Initialize RAG retriever with LangChain

        Args:
            reset_db: If True, rebuild vector database
            llm_provider: "openai" or "ollama" (optional, uses config if not specified)
        """
        logger.info("Initializing LangChain RAG system...")

        # Initialize components
        self.data_loader = DataLoader()
        self.vector_store = VectorStoreManager()
        self.llm = LLMInterface(provider=llm_provider)

        # Setup vector store
        if reset_db:
            self._build_vector_store()
        else:
            try:
                self.vector_store.load_existing()
                stats = self.vector_store.get_stats()
                if stats.get("document_count", 0) == 0:
                    logger.info("Vector store empty, building...")
                    self._build_vector_store()
            except Exception as e:
                logger.info(f"Building new vector store: {e}")
                self._build_vector_store()

        logger.info("✅ LangChain RAG system ready!")

    def _build_vector_store(self):
        """Build vector store from data"""
        logger.info("Building vector store from data files...")

        # Load all documents
        documents = self.data_loader.get_all_documents()

        # Create vector store with LangChain
        self.vector_store.create_from_documents(documents, reset=True)

        stats = self.vector_store.get_stats()
        logger.info(f"✅ Vector store built: {stats}")

    def retrieve(self, query: str, k: Optional[int] = None) -> List[str]:
        """
        Retrieve relevant documents for query

        Args:
            query: User query
            k: Number of results to retrieve

        Returns:
            List of retrieved document texts
        """
        if k is None:
            k = config.RAG_TOP_K

        documents = self.vector_store.similarity_search(query, k=k)
        return documents

    def answer_query(self, query: str) -> str:
        """
        Answer user query using LangChain RAG

        Args:
            query: User question

        Returns:
            Generated answer
        """
        logger.info(f"Processing query: {query}")

        # Retrieve relevant context
        context_docs = self.retrieve(query)

        if not context_docs:
            return "I don't have enough information to answer that question."

        # Combine context
        context = "\n\n".join(context_docs)

        # Generate answer using LangChain
        answer = self.llm.generate_with_context(query, context)

        logger.info("✅ Query answered successfully")
        return answer

    def get_stats(self) -> Dict[str, Any]:
        """Get RAG system statistics"""
        return {
            "vector_store": self.vector_store.get_stats(),
            "llm": self.llm.get_provider_info(),
            "framework": "LangChain"
        }
