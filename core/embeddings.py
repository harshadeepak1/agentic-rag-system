"""
Embedding generation module using SentenceTransformers (LOCAL MODEL)
Stable and recommended for RAG assignments.
"""

from typing import List
from sentence_transformers import SentenceTransformer
from utils.logger import logger


class EmbeddingGenerator:
    """Generate embeddings using local sentence-transformer model."""

    def __init__(self):
        """
        Initialize local embedding model.
        Downloads automatically first time (~90MB)
        """
        self.model_name = "all-MiniLM-L6-v2"

        logger.info(f"Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)

        logger.info("Embedding model loaded successfully")

    # --------------------------------------------------

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        try:
            embedding = self.model.encode(text)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Embedding error: {e}")
            raise

    # --------------------------------------------------

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        try:
            embeddings = self.model.encode(texts)
            return [emb.tolist() for emb in embeddings]
        except Exception as e:
            logger.error(f"Batch embedding error: {e}")
            raise

    # --------------------------------------------------

    def generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for search query."""
        return self.generate_embedding(query)


# Singleton
embedding_generator = EmbeddingGenerator()
