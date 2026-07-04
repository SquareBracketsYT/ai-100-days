"""
Agent Execution Result

Represent the execution details of AI Agent

Reponsibilities:
1. Store execution status
2. Store retry attempts
3. Store execution duration
4. Store any execution error
5. Display execution summary
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class AgentExecutionResult:
    """
    Stores execution details for an AI Agent
    """

    agent_name: str
    status: str
    attempts: int
    execution_time: float
    error_message: Optional[str] = None

    def display(self) -> None:
        """
        Display execution details
        """

        print(f"Agent           : {self.agent_name}")
        print(f"Status          : {self.status}")
        print(f"Attempts        : {self.attempts}")
        print(f"Exeuction Time  : {self.execution_time:.2f} sec")

        if self.error_message:
            print(f"Error message   : {self.error_message}")

