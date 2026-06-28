"""
Conversation Memory
Maintains the conversation history b/w the user and AI application

Responsibilities:
1. Store user messages
2. Store AI responses
3. Retrieve complete conversation history
4. Build conversation context for AI Agents
"""

from typing import List


class ConversationMemory:
    """
    Maintains conversation history.
    The stored messages are later included inside prompts so that AI Agents can
    understand the previous conversation
    """

    def __init__(self):
        """
        Initialize an empty conversation history
        """
        self._messages: List[str] = []

    def add_user_message(self, message:str) -> None:
        """
        Store a user message
        Args:
            message:
                User input.
        """
        self._messages.append(f"User: {message}")
    
    def add_ai_message(self, message:str) -> None:
        """
        Store AI response
        Args:
            message:
                AI generated response
        """
        self._messages.append(f"AI: {message}")

    def get_context(self) -> str:
        """
        Return the complete conversation
        Returns:
            Conversation history as a string
        """

        return "\n".join(self._messages)
    
    def clear(self) -> None:
        """
        Clear conversation history
        """

        self._messages.clear()

    def display(self, max_length:int = 120) -> None:
        """
        Display the stored conversation
        Userful while debugging
        Args:
            max_length:
                Maximum number of characters to display for each AI response.
        """

        print("\n" + "=" * 60)
        print("CONVERSATION MEMORY")
        print("=" * 60)
        
        if not self._messages:
            print("No conversation available")
        else:
            for message in self._messages:
                preview = message[:max_length] + "..."
                print(preview)

        print("=" * 60)
        