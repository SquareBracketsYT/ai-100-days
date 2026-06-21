from google import genai
from dotenv import load_dotenv
import os
import time
from datetime import datetime
import random


# Load environment variables
# GEMINI API KEY is store in .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Gemini API Key not found...")


# Create Gemini Client
client = genai.Client(api_key=API_KEY)


print("=" * 50)
print("Gemini Chatbot")
print("=" * 50)


def get_current_time(query=None):
    return datetime.now().strftime("%I:%M:%S, %p")


def calculator(expression):
    try:
        return eval(expression)
    except Exception as ex:
        return "Invalid expression"


def motivational_quotes(query=None):
    quotes = [
        "Consistency is the key to success",
        "Hard work beats talent when talent doesn't work hard",
        "Action speaks more than words",
        "Dream big, Start small, Act now..."
    ]
    return random.choice(quotes)



def generate_roadmap(topic):
    return f"""
    Roadmap for {topic}:
    1. Learn Fundamentals
    2. Practice Projects
    3. Build Portfolio
    4. Apply for Jobs
"""


# Tool Registery
TOOLS = {
    "TIME_TOOL": get_current_time,
    "CALCULATOR_TOOL": calculator,
    "QUOTE_TOOL": motivational_quotes,
    "ROADMAP_TOO": generate_roadmap
}


def select_tool(query):
    prompt = f"""
    You are a tool selector.
    Available Tools:
    TIME_TOOL
    CALCULATOR_TOOL
    QUOTE_TOOL
    ROADMAP_TOOL
    
    Return ONLY tool name
    User Query: {query}
"""
    
    response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

    # print(f"Assistant: {response.text}")
    return response.text.strip()
    

def execute_tool(tool_name, query):
    tool = TOOLS.get(tool_name)

    if not tool:
        return "Tool not found"
    
    return tool(query)


while True:
    query = input("\nYou: ")
    if query.lower() == "exit":
        break
    
    tool = select_tool(query)
    print(f"\n[Selected Tool]: {tool}")

    result = execute_tool(tool, query)
    print(f"\nAssistant: {result}")