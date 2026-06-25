from google import genai
from dotenv import load_dotenv
import os

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

while True:
    user_input = input("Prompt: ")
    if user_input.lower() in ["bye", "quit", "exit"]:
        break

    # Store user message
    history.append(f"User : {user_input}")

    conversation_context = system_prompt + "\n"
    conversation_context += "\n".join(history)

    try:
        # Call Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=conversation_context
        )

        bot_response = response.text
        print(f"\n Gemini : {bot_response}")

        # Store bot response
        history.append(f"Assistant: {bot_response}")

    except Exception as ex:
        print("Gemini service temporarily unavailable")
        print(ex)
        continue

