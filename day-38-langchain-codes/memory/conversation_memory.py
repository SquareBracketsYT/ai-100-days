from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

class ConversationMemory:
    def __init__(self):
        self.messages = []

    def add_user_message(self, question):
        self.messages.append(
            HumanMessage(content=question)
        )

    def add_ai_message(self, answer):
        self.messages.append(
            AIMessage(content=answer)
        )

    def get_messages(self):
        return self.messages
    
    def clear(self):
        self.messages.clear()