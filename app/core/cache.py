"""
Caching system with semantic similarity matching.
Combines exact match caching with semantic similarity using embeddings.
"""

from typing import Optional, Tuple, Union
import hashlib
import torch
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from loguru import logger

from app.config import settings
from app.db.crud import (
    get_cached_response_by_question,
    create_cached_response,
    increment_cache_hit,
    get_all_cached_responses
)


class CacheManager:
    """Manages response caching with semantic similarity."""

    def __init__(self):
        """Initialize cache manager with embedding model."""
        self.embedding_model: Optional[SentenceTransformer] = None
        self._initialized = False
        self._cache_index = {}  # In-memory cache for fast lookup

    def initialize(self) -> None:
        """Initialize the embedding model for semantic similarity."""
        if self._initialized:
            logger.info("Cache manager already initialized")
            return

        try:
            logger.info("Initializing cache manager...")
            logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")

            # Load the same embedding model as RAG pipeline
            self.embedding_model = SentenceTransformer(
                settings.EMBEDDING_MODEL)

            self._initialized = True
            logger.info("Cache manager initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing cache manager: {e}")
            raise

    def _get_query_hash(self, query: str) -> str:
        """
        Generate a hash for exact match caching.

        Args:
            query: User's question

        Returns:
            MD5 hash of the normalized query
        """
        # Normalize: lowercase, strip whitespace
        normalized = query.lower().strip()
        return hashlib.md5(normalized.encode()).hexdigest()

    def _get_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a text string.

        Args:
            text: Text to embed

        Returns:
            Embedding vector as numpy array
        """
        # Ensure model is loaded
        if not self._initialized or self.embedding_model is None:
            self.initialize()

        if self.embedding_model is None:
            logger.error(
                "Embedding model not initialized - cannot encode text.")
            return np.array([])

        try:
            embedding: Union[np.ndarray, torch.Tensor] = self.embedding_model.encode(
                text,
                normalize_embeddings=True
            )

            # Convert to numpy if it's a torch tensor
            if isinstance(embedding, torch.Tensor):
                embedding = embedding.detach().cpu().numpy()

            return np.array(embedding, dtype=np.float32)

        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return np.array([])

    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.

        Args:
            vec1: First vector
            vec2: Second vector

        Returns:
            Similarity score (0-1)
        """
        if len(vec1) == 0 or len(vec2) == 0:
            return 0.0

        # Vectors are already normalized, so dot product = cosine similarity
        similarity = np.dot(vec1, vec2)
        return float(similarity)

    def check_exact_cache(self, db, query: str) -> Optional[Tuple[str, int]]:
        """
        Check for exact match in cache.

        Args:
            db: Database session
            query: User's question

        Returns:
            Tuple of (cached_answer, cache_id) if found, None otherwise
        """
        cached = get_cached_response_by_question(db, query)

        if cached:
            logger.info(f"Exact cache hit for query: {query[:50]}...")
            increment_cache_hit(db, cached.id)
            return (cached.answer, cached.id)

        return None

    def check_semantic_cache(
        self,
        db,
        query: str,
        threshold: Optional[float] = None
    ) -> Optional[Tuple[str, int, float]]:
        """
        Check for semantically similar cached responses.

        Args:
            db: Database session
            query: User's question
            threshold: Similarity threshold (default from settings)

        Returns:
            Tuple of (cached_answer, cache_id, similarity_score) if found, None otherwise
        """
        if not self._initialized:
            self.initialize()

        if threshold is None:
            threshold = settings.CACHE_SIMILARITY_THRESHOLD

        try:
            # Get query embedding
            query_embedding = self._get_embedding(query)

            if len(query_embedding) == 0:
                logger.warning("Failed to generate query embedding")
                return None

            # Get all cached responses
            cached_responses = get_all_cached_responses(db)

            if not cached_responses:
                logger.info(
                    "No cached responses available for semantic matching")
                return None

            best_match = None
            best_similarity = 0.0
            best_cache_id = None

            # Find best semantic match
            for cached in cached_responses:
                if not cached.embedding:
                    continue

                try:
                    # Parse stored embedding
                    cached_embedding = np.array(json.loads(cached.embedding))

                    # Calculate similarity
                    similarity = self._cosine_similarity(
                        query_embedding, cached_embedding)

                    # Update best match if better
                    if similarity > best_similarity and similarity >= threshold:
                        best_similarity = similarity
                        best_match = cached.answer
                        best_cache_id = cached.id

                except Exception as e:
                    logger.warning(f"Error processing cached embedding: {e}")
                    continue

            if best_match:
                logger.info(
                    f"Semantic cache hit! Similarity: {best_similarity:.3f} "
                    f"(threshold: {threshold})"
                )
                if best_match and best_cache_id is not None:
                    logger.info(
                        f"Semantic cache hit! Similarity: {best_similarity:.3f} "
                        f"(threshold: {threshold})"
                    )
                    increment_cache_hit(db, best_cache_id)
                    return (best_match, best_cache_id, best_similarity)

            logger.info(
                f"No semantic match found (best similarity: {best_similarity:.3f})")
            return None

        except Exception as e:
            logger.error(f"Error in semantic cache check: {e}")
            return None

    def add_to_cache(self, db, query: str, answer: str) -> None:
        """
        Add a new response to the cache with its embedding.

        Args:
            db: Database session
            query: User's question
            answer: Generated answer
        """
        if not self._initialized:
            self.initialize()

        try:
            # Generate embedding for the query
            query_embedding = self._get_embedding(query)

            # Convert embedding to JSON string for storage
            embedding_json = json.dumps(query_embedding.tolist())

            # Store in database
            create_cached_response(
                db=db,
                question=query,
                answer=answer,
                embedding=embedding_json
            )

            logger.info(f"Added response to cache for query: {query[:50]}...")

        except Exception as e:
            logger.error(f"Error adding to cache: {e}")

    def get_cache_stats(self, db) -> dict:
        """
        Get cache statistics.

        Args:
            db: Database session

        Returns:
            Dictionary with cache stats
        """
        cached_responses = get_all_cached_responses(db)

        total_cached = len(cached_responses)
        total_hits = sum(cached.hit_count for cached in cached_responses)

        # Most popular cached questions
        popular = sorted(cached_responses,
                         key=lambda x: x.hit_count, reverse=True)[:5]
        popular_questions = [
            {"question": cached.question[:100], "hits": cached.hit_count}
            for cached in popular
        ]

        return {
            "total_cached_responses": total_cached,
            "total_cache_hits": total_hits,
            "most_popular": popular_questions,
            "threshold": settings.CACHE_SIMILARITY_THRESHOLD
        }


# Global cache manager instance
cache_manager = CacheManager()
