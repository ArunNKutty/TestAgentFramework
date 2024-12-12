from phi.agent import Agent
from phi.model.openai import OpenAIChat
from typing import List, Dict

def get_query_router():
    router_instructions = """You are a Query Router that analyzes user queries and determines which specialized agent should handle them.
    
    Available Agents and their capabilities:
    1. Finance Agent:
       - Stock prices and market data
       - Company financial information
       - Analyst recommendations
       - Company news
    
    2. News Agent:
       - General news updates
       - News summaries
       - Topic-specific news coverage
    
    Rules:
    - If a query involves multiple domains, decompose it into sub-queries
    - For each sub-query, specify which agent should handle it
    - If a query is ambiguous, ask for clarification
    - Return results in a structured format
    
    Output Format:
    {
        "decomposition": [
            {
                "sub_query": "the specific question or task",
                "agent": "finance|news",
                "reasoning": "brief explanation of why this agent was chosen"
            }
        ],
        "needs_clarification": false,
        "clarification_question": null
    }
    """
    
    return Agent(
        name="Query Router",
        model=OpenAIChat(id="gpt-4o-mini"),
        instructions=[router_instructions],
        markdown=True,
        verbose=True
    ) 