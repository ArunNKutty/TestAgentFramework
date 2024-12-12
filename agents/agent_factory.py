from typing import Dict, Type
from .finance_agent import get_finance_agent
from .news_agent import get_news_agent

class AgentFactory:
    _agents = {
        "finance": get_finance_agent,
        "news": get_news_agent
    }
    
    @classmethod
    def get_agent(cls, agent_type: str):
        agent_creator = cls._agents.get(agent_type.lower())
        if not agent_creator:
            raise ValueError(f"Unknown agent type: {agent_type}")
        return agent_creator()
    
    @classmethod
    def get_available_agents(cls) -> list[str]:
        return list(cls._agents.keys()) 