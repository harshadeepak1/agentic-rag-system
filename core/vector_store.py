"""
Vector store implementation using Milvus.
Stable version for sentence-transformers embeddings.
"""

from typing import List, Dict, Any, Optional
from pymilvus import (
    connections,
    Collection,
    CollectionSchema,
    FieldSchema,
    DataType,
    utility
)

from utils.config import config
from utils.logger import logger


class VectorStore:
    """Milvus vector store for document embeddings."""

    def __init__(self):
        self.collection_name = config.MILVUS_COLLECTION
        self.dim = config.EMBEDDING_DIM
        self.collection: Optional[Collection] = None

        try:
            connections.connect(
                alias="default",
                host=config.MILVUS_HOST,
                port=config.MILVUS_PORT
            )

            logger.info(
                f"Connected to Milvus at {config.MILVUS_HOST}:{config.MILVUS_PORT}"
            )

            self._initialize_collection()

        except Exception as e:
            logger.error(f"Milvus connection failed: {e}")
            raise

    # -----------------------------------------------------

    def _initialize_collection(self):
        """Load or create collection."""

        if utility.has_collection(self.collection_name):
            logger.info(f"Loading existing collection: {self.collection_name}")
            self.collection = Collection(self.collection_name)
        else:
            logger.info(f"Creating new collection: {self.collection_name}")
            self._create_collection()

        self.collection.load()
        logger.info("Collection ready")

    # -----------------------------------------------------

    def _create_collection(self):
        """Create Milvus collection schema."""

        fields = [
            FieldSchema(
                name="id",
                dtype=DataType.INT64,
                is_primary=True,
                auto_id=True
            ),
            FieldSchema(
                name="embedding",
                dtype=DataType.FLOAT_VECTOR,
                dim=self.dim
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535
            ),
            FieldSchema(
                name="metadata",
                dtype=DataType.VARCHAR,
                max_length=65535
            ),
        ]

        schema = CollectionSchema(
            fields,
            description="RAG document embeddings"
        )

        self.collection = Collection(
            name=self.collection_name,
            schema=schema
        )

        index_params = {
            "metric_type": "COSINE",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128}
        }

        self.collection.create_index(
            field_name="embedding",
            index_params=index_params
        )

        logger.info("Collection created with index")

    # -----------------------------------------------------

    def insert(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]]
    ) -> bool:

        try:
            if not texts:
                return False

            if not (len(texts) == len(embeddings) == len(metadatas)):
                logger.error("Length mismatch in insert data")
                return False

            import json
            metadata_strs = [json.dumps(m) for m in metadatas]

            data = [
                embeddings,
                texts,
                metadata_strs
            ]

            logger.info(f"Inserting {len(texts)} docs into Milvus")

            self.collection.insert(data)
            self.collection.flush()

            logger.info("Insert successful")
            return True

        except Exception as e:
            logger.error(f"Insertion failed: {e}")
            return False

    # -----------------------------------------------------

    def search(
        self,
        query_embedding: List[float],
        top_k: int = None,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:

        try:
            if top_k is None:
                top_k = config.TOP_K

            search_params = {
                "metric_type": "COSINE",
                "params": {"nprobe": 10}
            }

            results = self.collection.search(
                data=[query_embedding],
                anns_field="embedding",
                param=search_params,
                limit=top_k,
                output_fields=["text", "metadata"]
            )

            import json
            formatted = []

            for hits in results:
                for hit in hits:
                    metadata_raw = hit.entity.get("metadata")
                    metadata = json.loads(metadata_raw) if metadata_raw else {}

                    formatted.append({
                        "text": hit.entity.get("text"),
                        "metadata": metadata,
                        "score": float(hit.score)
                    })

            logger.info(f"Retrieved {len(formatted)} results")
            return formatted

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    # -----------------------------------------------------

    def delete_all(self) -> bool:
        """Drop and recreate collection."""

        try:
            if utility.has_collection(self.collection_name):
                utility.drop_collection(self.collection_name)
                logger.info("Collection dropped")

            self._create_collection()
            self.collection.load()

            return True

        except Exception as e:
            logger.error(f"Delete failed: {e}")
            return False

    # -----------------------------------------------------

    def get_stats(self) -> Dict[str, Any]:

        try:
            self.collection.flush()

            return {
                "collection": self.collection_name,
                "documents": self.collection.num_entities,
                "dimension": self.dim
            }

        except Exception as e:
            logger.error(f"Stats error: {e}")
            return {}

    # -----------------------------------------------------

    def close(self):
        connections.disconnect("default")
        logger.info("Milvus disconnected")


# Singleton
vector_store = VectorStore()
