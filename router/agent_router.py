from typing import List, Dict, Any
import json
from agents.agent_factory import AgentFactory
from agents.query_router import get_query_router
from utils.response_handler import extract_agent_response

class AgentRouter:
    def __init__(self):
        self.router = get_query_router()
        self.agent_factory = AgentFactory()
    
    def _parse_router_response(self, response: str) -> Dict:
        """Extract JSON from router response"""
        try:
            # Find JSON content between ```json and ``` if present
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            else:
                json_str = response
            return json.loads(json_str)
        except Exception as e:
            raise ValueError(f"Failed to parse router response: {e}")
    
    def _execute_sub_query(self, sub_query: Dict) -> Dict:
        """Execute a single sub-query using the appropriate agent"""
        agent_type = sub_query["agent"]
        query = sub_query["sub_query"]
        
        agent = self.agent_factory.get_agent(agent_type)
        response = agent.run(query)
        
        return {
            "sub_query": query,
            "agent": agent_type,
            "response": extract_agent_response(response)
        }
    
    def process_query(self, query: str) -> Dict:
        """Process a query through the router and execute sub-queries"""
        # Get routing decision
        router_response = self.router.run(query)
        routing_result = self._parse_router_response(
            extract_agent_response(router_response)
        )
        
        # Check if clarification is needed
        if routing_result.get("needs_clarification", False):
            return {
                "status": "clarification_needed",
                "message": routing_result["clarification_question"]
            }
        
        # Execute each sub-query
        results = []
        for sub_query in routing_result["decomposition"]:
            result = self._execute_sub_query(sub_query)
            results.append(result)
        
        return {
            "status": "success",
            "results": results,
            "decomposition": routing_result["decomposition"]
        } 