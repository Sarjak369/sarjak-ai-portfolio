"""
RAG (Retrieval-Augmented Generation) pipeline for portfolio knowledge base.
Uses LangChain v0.3+ syntax with Qdrant vector store.
"""

from typing import List
from pathlib import Path
import os

from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PyPDFLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from loguru import logger

from app.config import settings


class RAGPipeline:
    """RAG pipeline for document retrieval and context generation."""

    def __init__(self):
        """Initialize RAG pipeline with embeddings and vector store."""
        self.embeddings = None
        self.vector_store = None
        self.retriever = None
        self._initialized = False

    def initialize(self) -> None:
        """Initialize embeddings model and vector store."""
        if self._initialized:
            logger.info("RAG pipeline already initialized")
            return

        try:
            logger.info("Initializing RAG pipeline...")

            # Initialize embeddings model (runs locally)
            logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL,
                # Use 'mps' for M-series Mac if you want GPU
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )

            # Initialize Qdrant client (in-memory mode for development)
            logger.info("Initializing Qdrant vector store...")
            # In-memory for simplicity
            self.client = QdrantClient(location=":memory:")

            # Create collection if it doesn't exist
            collection_name = "portfolio_knowledge"
            try:
                self.client.get_collection(collection_name)
                logger.info(f"Collection '{collection_name}' already exists")
            except Exception:
                # Create new collection
                self.client.create_collection(
                    collection_name=collection_name,
                    # MiniLM produces 384-dim vectors
                    vectors_config=VectorParams(
                        size=384, distance=Distance.COSINE)
                )
                logger.info(f"Created new collection: '{collection_name}'")

            # Initialize vector store
            self.vector_store = QdrantVectorStore(
                client=self.client,
                collection_name=collection_name,
                embedding=self.embeddings
            )

            # Create retriever
            self.retriever = self.vector_store.as_retriever(
                search_kwargs={"k": settings.TOP_K_RETRIEVAL}
            )

            self._initialized = True
            logger.info("RAG pipeline initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing RAG pipeline: {e}")
            raise

    def load_and_index_documents(self) -> int:
        """Load documents from knowledge base and index them."""
        if not self._initialized:
            self.initialize()

        try:
            documents = []

            # Load markdown files
            logger.info("Loading markdown files...")
            md_loader = DirectoryLoader(
                settings.KNOWLEDGE_BASE_PATH,
                glob="**/*.md",
                loader_cls=TextLoader,
                loader_kwargs={'encoding': 'utf-8'}
            )
            md_docs = md_loader.load()
            documents.extend(md_docs)
            logger.info(f"Loaded {len(md_docs)} markdown documents")

            # Load PDF files if they exist
            pdf_path = Path(settings.DOCUMENTS_PATH)
            if pdf_path.exists():
                logger.info("Loading PDF files...")
                pdf_files = list(pdf_path.glob("*.pdf"))
                for pdf_file in pdf_files:
                    try:
                        pdf_loader = PyPDFLoader(str(pdf_file))
                        pdf_docs = pdf_loader.load()
                        documents.extend(pdf_docs)
                        logger.info(
                            f"Loaded PDF: {pdf_file.name} ({len(pdf_docs)} pages)")
                    except Exception as e:
                        logger.warning(
                            f"Failed to load PDF {pdf_file.name}: {e}")

            if not documents:
                logger.warning("No documents found to index!")
                return 0

            # Split documents into chunks
            logger.info("Splitting documents into chunks...")
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
                length_function=len,
                separators=["\n\n", "\n", " ", ""]
            )
            splits = text_splitter.split_documents(documents)
            logger.info(f"Created {len(splits)} chunks")

            # Add documents to vector store
            logger.info("Indexing documents in vector store...")
            if self.vector_store is None:
                raise RuntimeError("Vector store not properly initialized")
            self.vector_store.add_documents(splits)
            logger.info(f"Successfully indexed {len(splits)} document chunks")

            return len(splits)

        except Exception as e:
            logger.error(f"Error loading and indexing documents: {e}")
            raise

    def retrieve_context(self, query: str) -> str:
        """
        Retrieve relevant context for a query.

        Args:
            query: User's question

        Returns:
            Formatted context string from retrieved documents
        """
        if not self._initialized:
            self.initialize()

        try:
            if self.retriever is None:
                logger.error("Retriever not initialized")
                return ""

            # Retrieve relevant documents
            docs = self.retriever.invoke(query)

            if not docs:
                logger.warning(f"No documents retrieved for query: {query}")
                return ""

            # Format context
            context_parts = []
            for i, doc in enumerate(docs, 1):
                content = doc.page_content.strip()
                source = doc.metadata.get('source', 'Unknown')
                context_parts.append(
                    f"[Document {i} - {Path(source).name}]\n{content}")

            context = "\n\n".join(context_parts)
            logger.info(f"Retrieved {len(docs)} documents for query")

            return context

        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return ""

    def get_stats(self) -> dict:
        """Get statistics about the vector store."""
        if not self._initialized:
            return {"status": "not_initialized"}

        try:
            collection_info = self.client.get_collection("portfolio_knowledge")
            return {
                "status": "initialized",
                "total_vectors": collection_info.points_count,
                "embedding_model": settings.EMBEDDING_MODEL
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"status": "error", "error": str(e)}


# Global RAG pipeline instance
rag_pipeline = RAGPipeline()
