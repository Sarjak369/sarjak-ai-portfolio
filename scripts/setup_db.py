from loguru import logger
from app.core.rag import rag_pipeline
from app.db.database import init_db, engine
from pathlib import Path
import sys

"""
Database setup script.
Initializes database and loads knowledge base into vector store.
"""


# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def main():
    """Initialize database and RAG pipeline."""
    logger.info("Starting database setup...")

    # Initialize database tables
    logger.info("Creating database tables...")
    init_db()
    logger.info("Database tables created successfully")

    # Initialize and populate RAG pipeline
    logger.info("Initializing RAG pipeline...")
    rag_pipeline.initialize()

    logger.info("Loading and indexing knowledge base...")
    num_chunks = rag_pipeline.load_and_index_documents()
    logger.info(f"Indexed {num_chunks} document chunks")

    # Get stats
    stats = rag_pipeline.get_stats()
    logger.info(f"RAG Pipeline Stats: {stats}")

    logger.info("Setup completed successfully!")


if __name__ == "__main__":
    main()
