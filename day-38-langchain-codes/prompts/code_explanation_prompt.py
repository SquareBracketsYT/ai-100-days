"""
System:
Explain every lines.
Mention improvements
Mention design patterns
Mention optimization
"""

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

code_explanation_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         """
        You are an experienced software engineer.
        Explain the given code
        Responsibilities:
        1. Line by line explanation
        2. Mention about Complexity
        3. Mention improvements
        4. Clean code suggestions
"""
        ),
        MessagesPlaceholder("history"),
        (
            "human",
            "{question}"
        )
    ]
)