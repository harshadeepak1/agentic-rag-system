"""Document agent for handling general document queries."""

from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from utils.logger import logger


class DocumentAgent(BaseAgent):
    """Agent specialized in answering questions from general documents."""
    
    def __init__(self):
        super().__init__(
            name="DocumentAgent",
            description="Specialized in answering questions from PDF, DOCX, PPTX, and text documents"
        )
        
        self.system_prompt = """You are a document analysis expert. Your role is to:
1. Carefully read and understand the provided document context
2. Answer questions accurately based on the context
3. Cite specific sources when possible
4. Indicate when information is not available in the context

Be precise, factual, and helpful in your responses."""
    
    def process_query(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Process a query about documents.
        
        Args:
            query: User query
            **kwargs: Additional arguments (top_k, etc.)
            
        Returns:
            Dict with answer, context, and metadata
        """
        try:
            logger.info(f"DocumentAgent processing query: {query}")
            
            # Get parameters
            top_k = kwargs.get('top_k', 5)
            
            # Filter to only document types (exclude Excel)
            filter_metadata = {
                'file_type': ['.pdf', '.docx', '.pptx', '.txt']
            }
            
            # Retrieve context
            context = self.retrieve_context(
                query=query,
                top_k=top_k,
                filter_metadata=None  # Milvus filtering can be complex, retrieve all then filter
            )
            
            # Filter results by file type
            context = [
                c for c in context 
                if c.get('metadata', {}).get('file_type') in ['.pdf', '.docx', '.pptx', '.txt']
            ]
            
            if not context:
                return {
                    'answer': "I couldn't find any relevant information in the documents to answer your question.",
                    'context': [],
                    'agent': self.name,
                    'confidence': 0.0
                }
            
            # Rerank results
            context = self.rerank_results(query, context, top_k=3)
            
            # Generate answer
            answer = self.generate_answer(
                query=query,
                context=context,
                system_prompt=self.system_prompt
            )
            
            # Calculate confidence based on similarity scores
            avg_score = sum(c.get('score', 0) for c in context) / len(context) if context else 0
            
            return {
                'answer': answer,
                'context': context,
                'agent': self.name,
                'confidence': float(avg_score),
                'sources': list(set(c.get('metadata', {}).get('source', 'Unknown') for c in context))
            }
            
        except Exception as e:
            logger.error(f"Error in DocumentAgent.process_query: {e}")
            return {
                'answer': "I encountered an error while processing your question about the documents.",
                'context': [],
                'agent': self.name,
                'confidence': 0.0,
                'error': str(e)
            }


# Create singleton instance
document_agent = DocumentAgent()
