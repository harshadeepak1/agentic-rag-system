"""General QA agent for questions that don't require specific document context."""

from typing import Dict, Any
from agents.base_agent import BaseAgent
from utils.logger import logger


class QAAgent(BaseAgent):
    """Agent for general question answering."""
    
    def __init__(self):
        super().__init__(
            name="QAAgent",
            description="Handles general questions and provides context-aware answers"
        )
        
        self.system_prompt = """You are a helpful AI assistant. Your role is to:
1. Answer questions clearly and concisely
2. Use provided context when available
3. Admit when you don't have enough information
4. Be helpful and informative

Provide accurate and useful responses."""
    
    def process_query(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Process a general query.
        
        Args:
            query: User query
            **kwargs: Additional arguments
            
        Returns:
            Dict with answer and metadata
        """
        try:
            logger.info(f"QAAgent processing query: {query}")
            
            # Get parameters
            top_k = kwargs.get('top_k', 5)
            
            # Try to retrieve any relevant context
            context = self.retrieve_context(
                query=query,
                top_k=top_k
            )
            
            # Rerank if we have context
            if context:
                context = self.rerank_results(query, context, top_k=3)
                avg_score = sum(c.get('score', 0) for c in context) / len(context)
            else:
                avg_score = 0.0
            
            # Generate answer
            if context:
                answer = self.generate_answer(
                    query=query,
                    context=context,
                    system_prompt=self.system_prompt
                )
            else:
                # No context available, use LLM directly
                answer = self.llm.generate(
                    f"{self.system_prompt}\n\nQuestion: {query}\n\nAnswer:",
                    temperature=0.7
                )
            
            sources = []
            if context:
                sources = list(set(
                    c.get('metadata', {}).get('source', 'Unknown')
                    for c in context
                ))
            
            return {
                'answer': answer,
                'context': context,
                'agent': self.name,
                'confidence': float(avg_score),
                'sources': sources
            }
            
        except Exception as e:
            logger.error(f"Error in QAAgent.process_query: {e}")
            return {
                'answer': "I encountered an error while processing your question.",
                'context': [],
                'agent': self.name,
                'confidence': 0.0,
                'error': str(e)
            }


# Create singleton instance
qa_agent = QAAgent()
