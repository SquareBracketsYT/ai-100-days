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

# Store Chat History
history = []

# Context management
MAX_HISTORY = 20

system_prompt = """
You are a friendly AI assistant.
Rules:
1. Be helpful
2. Be professional
3. Keep answers clean and concise
4. Remember previous conversation context
"""

print("=" * 50)
print("Gemini Chatbot")
print("=" * 50)


def get_current_time():
    return datetime.now().strftime("%I:%M:%S, %p")


def calculator(expression):
    try:
        return eval(expression)
    except Exception as ex:
        return "Invalid expression"


def motivational_quotes():
    quotes = [
        "Consistency is the key to success",
        "Hard work beats talent when talent doesn't work hard",
        "Action speaks more than words",
        "Dream big, Start small, Act now..."
    ]
    return random.choice(quotes)


def route_tool(query):
    query = query.lower()
    if "time" in query:
        return "time"
    elif "calculate" in query:
        return "calculator"
    elif "motivation" in query or "quote" in query:
        return "quote"
    return "gemini"


while True:
    user_input = input("Prompt: ")
    if user_input.lower() in ["bye", "quit", "exit"]:
        break

    tool = route_tool(user_input)
    if tool == "time":
        result = get_current_time()
        print(f"Assistant: Current time : {result}")
    
    elif tool == "calculator":
        expression = (user_input.replace("calculate","").strip())
        result = calculator(expression)
        print(f"Assistant: Result = {result}")
    
    elif tool == "quote":
        result = motivational_quotes()
        print(f"Assistant: Quote of the day = {result}")

    else:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input
        )

        print(f"Assistant: {response.text}")
