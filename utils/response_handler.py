from phi.agent import Agent
from typing import Any

def extract_agent_response(run_response: Any) -> str:
    """Extract the clean response content from agent's run response"""
    assistant_messages = [
        msg for msg in run_response.messages 
        if msg.role == 'assistant' and msg.content is not None
    ]
    return assistant_messages[-1].content if assistant_messages else "No response generated" 