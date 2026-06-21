from google import genai
from google.genai import types
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


print("=" * 50)
print("Gemini Chatbot for Career roadmap - Skills, Certificate, Salary")
print("=" * 50)

# Function-1 : Skills
def get_skills(role: str):
    """
    Returns required skills for a role
    Parameters: role(str) - Career role selected by user
    Return: dict: Required skills
    """

    return {
        "role": role,
        "skills": [
            "Python", "Machine Learning", "Data Science", "Deep Learning", "LLMs"
        ]
    }


def get_certificate(role: str):
    """
    Returns Certification info
    Parameters: rol(str): Career role
    Returns: dict
    """

    return {
        "role": role,
        "certifications": [
            "AI-102", "AZ-104", "DP-300", "AWS Cloud Practitioner", "Google Gen AI"
        ]
    }

def get_salary(role: str):
    """
    Returns expected salary range
    Parameters: role(str)
    Returns: dict
    """

    return {
        "role": role,
        "salary_range": "15-20LPA"
    }


# Register Functions
tools = [
    get_skills, get_certificate, get_salary
]

query = input("Prompt: ")

response = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents=query,
    config=types.GenerateContentConfig(
        tools=tools
    )
)

print(response.text)