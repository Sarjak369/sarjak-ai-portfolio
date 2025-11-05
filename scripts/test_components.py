"""Test LLM, cache, and command components."""

import sys
from app.core.llm import llm_handler
from app.core.cache import cache_manager
from app.core.commands import command_handler
from app.core.rag import rag_pipeline
from app.db.database import SessionLocal
from loguru import logger
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_llm():
    """Test LLM initialization and generation."""
    logger.info("=== Testing LLM ===")
    llm_handler.initialize()

    # Test simple generation
    context = "Sarjak is an AI Data Scientist with 4+ years of experience."
    query = "What does Sarjak do?"

    response = llm_handler.generate_response(query, context)
    logger.info(f"LLM Response: {response[:200]}...")
    logger.info("✓ LLM test passed")


def test_cache():
    """Test cache manager."""
    logger.info("=== Testing Cache Manager ===")
    cache_manager.initialize()

    db = SessionLocal()

    # Add to cache
    cache_manager.add_to_cache(
        db,
        "What are your skills?",
        "I have expertise in Python, ML, and AI."
    )

    # Test semantic matching
    result = cache_manager.check_semantic_cache(db, "Tell me your skills")
    if result:
        logger.info(f"Semantic cache hit with similarity: {result[2]:.3f}")

    db.close()
    logger.info("✓ Cache test passed")


def test_commands():
    """Test command handler."""
    logger.info("=== Testing Commands ===")

    commands_to_test = ["/help", "/skills", "/projects", "/contact"]

    for cmd in commands_to_test:
        is_cmd, response = command_handler.handle_command(cmd)
        if is_cmd and response:
            logger.info(f"✓ {cmd}: {response[:50]}...")
        else:
            logger.error(f"✗ {cmd} failed or returned no response")

    logger.info("✓ Commands test passed")


def test_rag():
    """Test RAG retrieval."""
    logger.info("=== Testing RAG Retrieval ===")

    if not rag_pipeline._initialized:
        rag_pipeline.initialize()
        rag_pipeline.load_and_index_documents()

    context = rag_pipeline.retrieve_context("What projects has Sarjak built?")
    logger.info(f"Retrieved context length: {len(context)} chars")
    logger.info("✓ RAG test passed")


def main():
    """Run all tests."""
    logger.info("Starting component tests...")

    try:
        test_commands()
        test_cache()
        test_rag()
        test_llm()

        logger.info("\n✅ All tests passed!")

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        raise


if __name__ == "__main__":
    main()
