"""Router agent that orchestrates and delegates to specialized agents."""

from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from agents.document_agent import document_agent
from agents.excel_agent import excel_agent
from agents.qa_agent import qa_agent
from utils.logger import logger


class RouterAgent(BaseAgent):
    """Agent that routes queries to appropriate specialized agents."""
    
    def __init__(self):
        super().__init__(
            name="RouterAgent",
            description="Routes queries to the most appropriate specialized agent"
        )
        
        # Register available agents
        self.agents = {
            'document': document_agent,
            'excel': excel_agent,
            'qa': qa_agent
        }
        
        logger.info(f"RouterAgent initialized with {len(self.agents)} specialized agents")
    
    def process_query(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Route query to appropriate agent and return result.
        
        Args:
            query: User query
            **kwargs: Additional arguments
            
        Returns:
            Dict with answer, routing decision, and metadata
        """
        try:
            logger.info(f"RouterAgent analyzing query: {query}")
            
            # Analyze query and route to appropriate agent
            agent_choice = self._route_query(query)
            
            logger.info(f"Routing to: {agent_choice}")
            
            # Get the selected agent
            selected_agent = self.agents.get(agent_choice, qa_agent)
            
            # Process query with selected agent
            result = selected_agent.process_query(query, **kwargs)
            
            # Add routing information
            result['router_decision'] = agent_choice
            result['available_agents'] = list(self.agents.keys())
            
            return result
            
        except Exception as e:
            logger.error(f"Error in RouterAgent.process_query: {e}")
            return {
                'answer': "I encountered an error while routing your question.",
                'context': [],
                'agent': self.name,
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _route_query(self, query: str) -> str:
        """
        Determine which agent should handle the query.
        
        Args:
            query: User query
            
        Returns:
            Agent name to route to
        """
        try:
            # Use LLM to classify the query
            classification_prompt = f"""Analyze the following user query and determine which type of agent should handle it.

Available agent types:
1. document - For questions about general documents (PDF, Word, PowerPoint, text files)
2. excel - For questions about spreadsheet data, tables, statistics, or numerical analysis
3. qa - For general questions that don't require specific document analysis

Query: {query}

Important guidelines:
- Choose 'excel' if the query mentions data, numbers, statistics, tables, sheets, or analysis
- Choose 'document' if the query asks about text content, policies, presentations, or written information
- Choose 'qa' for general questions or when the type is unclear

Respond with ONLY one word: document, excel, or qa"""

            response = self.llm.generate(
                classification_prompt,
                temperature=0.1,
                max_tokens=10
            ).strip().lower()
            
            # Validate response
            valid_agents = ['document', 'excel', 'qa']
            
            # Check if response contains any valid agent name
            for agent in valid_agents:
                if agent in response:
                    return agent
            
            # Default to document agent if unclear
            logger.warning(f"Could not determine agent from response: {response}, defaulting to 'document'")
            return 'document'
            
        except Exception as e:
            logger.error(f"Error routing query: {e}")
            return 'qa'  # Safe fallback
    
    def get_agent_info(self) -> List[Dict[str, str]]:
        """
        Get information about all available agents.
        
        Returns:
            List of agent information dicts
        """
        return [
            {
                'name': agent.name,
                'description': agent.description
            }
            for agent in self.agents.values()
        ]


# Create singleton instance
router_agent = RouterAgent()
