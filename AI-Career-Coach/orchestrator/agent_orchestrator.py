"""
Agent Orchestrator
Responsible for managing the execution of AI Agents
"""

from typing import List
from agents.base_agent import BaseAgent
from memory.shared_memory import SharedMemory


class AgentOrchestrator:
    """
    Executes AI Agents in sequence
    """

    def __init__(self, memory: SharedMemory, conversation_memory):
        self.memory = memory
        self.agents: List[BaseAgent] = []
        self.conversation_memory = conversation_memory

    def register(self, agent: BaseAgent) -> None:
        """
        Register an AI Agent.
        Args:
            agent:
                Agent to register
        """

        self.agents.append(agent)
    
    def execute(self):
        print("\nStarting Multi-Agent Workflow...")
        for agent in self.agents:
            print(f"Executing {agent.get_agent_name()} Agent...")
            response = agent.execute()
            print(f"{response.agent_name} completed successfully...")
        
        print("Workflow Completed...")
        return self.memory.get("reviewer")