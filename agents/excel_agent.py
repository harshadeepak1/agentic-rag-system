"""Excel agent for handling spreadsheet data queries."""

from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from utils.logger import logger


class ExcelAgent(BaseAgent):
    """Agent specialized in answering questions from Excel spreadsheets."""
    
    def __init__(self):
        super().__init__(
            name="ExcelAgent",
            description="Specialized in analyzing and answering questions about Excel spreadsheet data"
        )
        
        self.system_prompt = """You are a data analysis expert specializing in spreadsheet data. Your role is to:
1. Analyze tabular data and statistics from Excel files
2. Answer questions about data trends, patterns, and specific values
3. Perform calculations and comparisons when needed
4. Provide insights based on the data presented

Be analytical, precise with numbers, and clear in your explanations."""
    
    def process_query(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Process a query about Excel data.
        
        Args:
            query: User query
            **kwargs: Additional arguments
            
        Returns:
            Dict with answer, context, and metadata
        """
        try:
            logger.info(f"ExcelAgent processing query: {query}")
            
            # Get parameters
            top_k = kwargs.get('top_k', 5)
            
            # Retrieve context - filter for Excel files
            context = self.retrieve_context(
                query=query,
                top_k=top_k
            )
            
            # Filter for Excel files only
            context = [
                c for c in context 
                if c.get('metadata', {}).get('file_type') == '.xlsx'
            ]
            
            if not context:
                return {
                    'answer': "I couldn't find any relevant information in the Excel files to answer your question.",
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
            
            # Calculate confidence
            avg_score = sum(c.get('score', 0) for c in context) / len(context) if context else 0
            
            # Extract sheet names from context
            sheets = list(set(
                c.get('metadata', {}).get('source', 'Unknown')
                for c in context
            ))
            
            return {
                'answer': answer,
                'context': context,
                'agent': self.name,
                'confidence': float(avg_score),
                'sources': sheets,
                'data_type': 'spreadsheet'
            }
            
        except Exception as e:
            logger.error(f"Error in ExcelAgent.process_query: {e}")
            return {
                'answer': "I encountered an error while analyzing the Excel data.",
                'context': [],
                'agent': self.name,
                'confidence': 0.0,
                'error': str(e)
            }


# Create singleton instance
excel_agent = ExcelAgent()
