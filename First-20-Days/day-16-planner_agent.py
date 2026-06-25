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
        self.plan = []
    
    # Create Plan
    def create_plan(self):
        print(f"[PLANNER] Creating execution plan...")
        prompt = f"""
        You are a Planner Agent.
        User Goal: {self.goal}
        
        Available Tools:
        SKILL_TOOL
        CERTIFICATION_TOOL
        PROJECT_TOOL
        SALARY_TOOL

        Your task:
        Create the BEST execution plan.

        Rules:
        1. Use only required tools
        2. Do not use unneccessary tools
        3. Return one tool per line
        4. Return ONLY tool names
        
        Example:
        SKILL_TOOL
        CERTIFICATION_TOOL
        PROJECT_TOOL
        SALARY_TOOL
"""
        
        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = prompt
        )

        plan = []
        for line in response.text.split("\n"):
            tool = line.strip()
            if tool in TOOL_REGISTRY:
                plan.append(tool)
        
        return plan
    

    # Execute Plan
    def execute_plan(self):
        print(f"[EXECUTOR] Executing plan...")
        step = 1
        for tool_name in self.plan:
            print("=" * 60)
            print(f"STEP - {step}")
            print("=" * 60)

            tool = TOOL_REGISTRY.get(tool_name)
            result = tool(self.goal)
            print("\nOBSERVATION:\n", result)
            self.observation.append(result)
            step += 1
    

    # Final Response
    def generate_final_plan(self):
        print(f"[AGENT] Generating Final Career Plan...")
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

        Generate a professional roadmap
"""
        
        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = prompt
        )

        print("="*60)
        print("Final Career Plan")
        print("="*60)

        print(response.text)

    # Run Agent
    def run(self):
        # Create Plan
        self.plan = self.create_plan()
        
        print("="*60)
        print("EXECUTION PLAN")
        print("="*60)

        for index, tool in enumerate(self.plan, start=1):
            print(f"{index}, {tool}")

        # Execute Plan
        self.execute_plan()

        # Final Response
        self.generate_final_plan()


print("======PLANNER AGENT======")
goal = input("Enter your career goal: ")
agent = CareerCoachAgent(goal)
agent.run()