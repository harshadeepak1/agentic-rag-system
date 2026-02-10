"""Configuration management for the Agentic RAG System."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for the application."""
    
    # API Keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # Milvus Configuration
    MILVUS_HOST: str = os.getenv("MILVUS_HOST", "localhost")
    MILVUS_PORT: int = int(os.getenv("MILVUS_PORT", "19530"))
    MILVUS_COLLECTION: str = os.getenv("MILVUS_COLLECTION", "document_collection")
    
    # Model Configuration
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "models/embedding-001")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-1.5-flash-latest")

    
    # Embedding Dimensions
    EMBEDDING_DIM: int = 384  # Google embedding dimension
    
    # Chunk Configuration
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # Retrieval Configuration
    TOP_K: int = int(os.getenv("TOP_K", "5"))
    SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
    
    # File Upload Configuration
    MAX_FILE_SIZE_MB: int = 50
    ALLOWED_EXTENSIONS: set = {'.pdf', '.docx', '.pptx', '.xlsx', '.txt'}
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is required. Please set it in .env file")
        return True


# Create a singleton instance
config = Config()
