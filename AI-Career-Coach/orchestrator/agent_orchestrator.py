"""
Agent Orchestrator
Responsible for managing the execution of AI Agents

Responsibilities:
1. Register AI Agents
2. Execute selected workflow
3. Retry failed agents
4. Track execution details
5. Return the final response
"""

from typing import List, Dict
from agents.base_agent import BaseAgent
from memory.shared_memory import SharedMemory
from models.agent_response import AgentResponse
from models.agent_execution_results import AgentExecutionResult
import time


class AgentOrchestrator:
    """
    Executes AI Agents in sequence
    """

    MAX_RETRIES = 3

    def __init__(self, memory: SharedMemory, conversation_memory):
        self.memory = memory
        self.agents: List[BaseAgent] = []
        self.conversation_memory = conversation_memory
        self._agents: Dict[str, BaseAgent] = {}
        self._execution_results: List[AgentExecutionResult] = []

    def register(self, agent: BaseAgent) -> None:
        """
        Register an AI Agent.
        Args:
            agent:
                Agent to register
        """

        # self.agents.append(agent)
        self._agents[
            agent.get_agent_name().lower()
        ] = agent
    
    # def execute(self):
    #     print("\nStarting Multi-Agent Workflow...")
    #     for agent in self.agents:
    #         print(f"Executing {agent.get_agent_name()} Agent...")
    #         response = agent.execute()
    #         print(f"{response.agent_name} completed successfully...")
        
    #     print("Workflow Completed...")
    #     return self.memory.get("reviewer")

    def execute(self, workflow: List[str]) -> AgentResponse:
        """
        Execute the selected workflow
        Args:
            workflow: Ordered list of agent names
        
        Returns:
            Final AgentResponse
        """

        print("\nStarting Multi-Agent Workflow...")

        self._execution_results.clear()
        
        final_response = None
        for step, agent_name in enumerate(workflow, start=1):
            agent = self._agents.get(agent_name.lower())
            if agent is None:
                raise ValueError(f"Agent {agent_name} is not registered")

            print(f"\nStep {step}: Executing {agent.get_agent_name()} Agent...")

            # final_response = agent.execute()
            final_response = self._execute_with_retry(agent)
            print(f"{agent.get_agent_name()} completed successfully...")
        
        print("Workflow Completed...")

        return final_response
    
    
    def _execute_with_retry(self, agent: BaseAgent) -> AgentResponse:
        """
        Execute an AI Agent with Retry Mechanism
        Args:
            agent:
                AI Agent Instance
        
        Returns:
            AgentResponse
        """

        start_time = time.perf_counter()
        last_exception = None

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                print(f"Attempt ; {attempt}")
                response = agent.execute()

                execution_time = (time.perf_counter() - start_time)
                self._execution_results.append(
                    AgentExecutionResult(
                        agent_name=agent.get_agent_name(),
                        status="SUCCESS",
                        attempts=attempt,
                        execution_time=execution_time
                    )
                )

                print("Success")
                return response
            except Exception as ex:
                last_exception = ex
                print(f"Attempt {attempt} Failed...")

                if attempt < self.MAX_RETRIES:
                    print("Retrying...")

        execution_time = (
            time.perf_counter() - start_time
        )
        self._execution_results.append(
            AgentExecutionResult(
                agent_name=agent.get_agent_name(),
                status="FAILED",
                attempts=self.MAX_RETRIES,
                execution_time=execution_time,
                error_message=str(last_exception)
            )
        )

        raise RuntimeError(
            f"{agent.get_agent_name()}"
            f"after {self.MAX_RETRIES} attempts"
        ) from last_exception


    def get_execution_results(self) -> List[AgentExecutionResult]:
        """
        Return execution summary
        """
        return self._execution_results
    
    def display_execution_summary(self) -> None:
        """
        Display execution summary
        """
        print("=" * 70)
        print("AGENT EXECUTION SUMMARY")
        print("=" * 70)

        for result in self._execution_results:
            result.display()
            print("-" * 70)

        print("=" * 70)