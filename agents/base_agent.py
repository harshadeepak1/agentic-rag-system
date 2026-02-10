"""Base agent class for the agentic system."""

from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod

from core.llm import llm
from core.vector_store import vector_store
from core.embeddings import embedding_generator
from utils.logger import logger


class BaseAgent(ABC):
    """Base class for all agents in the system."""
    
    def __init__(self, name: str, description: str):
        """
        Initialize base agent.
        
        Args:
            name: Agent name
            description: Agent description/purpose
        """
        self.name = name
        self.description = description
        self.llm = llm
        self.vector_store = vector_store
        self.embedding_generator = embedding_generator
        logger.info(f"Initialized {self.name}")
    
    @abstractmethod
    def process_query(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Process a user query.
        
        Args:
            query: User query string
            **kwargs: Additional arguments
            
        Returns:
            Dict with answer and metadata
        """
        pass
    
    def retrieve_context(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context from vector store.
        
        Args:
            query: User query
            top_k: Number of results to retrieve
            filter_metadata: Optional metadata filters
            
        Returns:
            List of retrieved documents
        """
        try:
            # Generate query embedding
            query_embedding = self.embedding_generator.generate_query_embedding(query)
            
            # Search vector store
            results = self.vector_store.search(
                query_embedding=query_embedding,
                top_k=top_k,
                filter_dict=filter_metadata
            )
            
            logger.info(f"Retrieved {len(results)} context chunks")
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []
    
    def rerank_results(
        self,
        query: str,
        results: List[Dict[str, Any]],
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Rerank results using LLM (simple relevance scoring).
        
        Args:
            query: User query
            results: Initial search results
            top_k: Number of top results to return
            
        Returns:
            Reranked results
        """
        if not results:
            return []
        
        try:
            # For now, just return top results based on similarity score
            # In production, you could use a reranking model
            sorted_results = sorted(
                results,
                key=lambda x: x.get('score', 0),
                reverse=True
            )
            
            return sorted_results[:top_k]
            
        except Exception as e:
            logger.error(f"Error reranking results: {e}")
            return results[:top_k]
    
    def generate_answer(
        self,
        query: str,
        context: List[Dict[str, Any]],
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate answer using LLM.
        
        Args:
            query: User query
            context: Retrieved context
            system_prompt: Optional system prompt
            
        Returns:
            Generated answer
        """
        try:
            answer = self.llm.generate_answer(
                query=query,
                context=context,
                system_prompt=system_prompt
            )
            return answer
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return "I apologize, but I encountered an error while generating the answer."
    
    def __str__(self) -> str:
        return f"{self.name}: {self.description}"
