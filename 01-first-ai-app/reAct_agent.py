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
print("Career Agent - Skills, Certificate, Salary")
print("=" * 50)

# Function-1 : Skills
def get_skills(goal: str):
    """
    Returns required skills for a role
    Parameters: goal(str) - Career role selected by user
    Return: dict: Required skills
    """

    return """
    Required skills:
    - Python
    - Machine Learning
    - Stats
    - Gen AI
    - Prompt Engineering
    - RAG
"""


def get_certificate(goal: str):
    """
    Returns Certification info
    Parameters: goal(str): Career role
    Returns: dict
    """

    return """
    - AI-102
    - AZ-204
    - AWS AI Practitioner
    - Google Gen AI
"""

def get_salary(goal: str):
    """
    Returns expected salary range
    Parameters: goal(str)
    Returns: dict
    """

    return """
    Salary Expectations:
    - Entry Level: 8-12 LPA
    - Mid Level: 15-25 LPA
    - Senior Level: 30+LPA
"""

def project_tool(goal: str):
    """
    Return project recommendations
    """
    return """
    Projects recommended:
    - AI Chatbot
    - PDG RAG Assistant
    - Reasearch Agent
    - Career Coach Agent
"""

TOOL_REGISTRY = {
    "SKILL_TOOL": get_skills,
    "CERTIFICATION_TOOL": get_certificate,
    "PROJECT_TOOL": project_tool,
    "SALARY_TOOL": get_salary
}


# Agent
class CareerCoachAgent:
    def __init__(self, goal):
        self.goal = goal
        self.observation = []
    
    # Think
    def think(self):
        prompt = f"""
        You are an AI career coach agent.
        User Goal: {self.goal}
        
        Available Tools:
        SKILL_TOOL
        CERTIFICATION_TOOL
        PROJECT_TOOL
        SALARY_TOOL

        Previous Observation : {self.observation}
        Think Carefully.
        Decide what information you still need.
        
        Return Only One of them:
        SKILL_TOOL
        CERTIFICATION_TOOL
        PROJECT_TOOL
        SALARY_TOOL
        FINISH
"""
        
        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = prompt
        )

        return response.text.strip()
    

    # Action
    def execute_action(self, action):
        tool = TOOL_REGISTRY.get(action)
        if tool:
            return tool(self.goal)

        return None
    

    # Final Response
    def generate_final_plan(self):
        prompt = f"""
        User Goal: {self.goal}
        Collected Information: {self.observation}
        Generate:
        1. Career Summary
        2. Skills Required
        3. Certifications
        4. Projects
        5. Salary expectations
        6. 90-Day learning roadmap
"""
        
        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = prompt
        )

        print("="*60)
        print("Final Career Plan")
        print("="*60)

        print(response.text)

    # ReAct Loop
    def run(self):
        step = 1
        while True:
            print("=" * 60)
            print(f"STEP : {step}")
            print("=" * 60)

            # Thought
            action = self.think()
            print("****THOUGHT****")
            print(action)

            # Finish
            if action == "FINISH":
                print("Enough Information Collected...")
                break

            # Action
            print("****ACTION****")
            result = self.execute_action(action)

            # Observation
            print("****OBSERVATION****")
            print(result)

            self.observation.append(result)
            step += 1
        
        self.generate_final_plan()


goal = input("Enter your career goal: ")
agent = CareerCoachAgent(goal)
agent.run()