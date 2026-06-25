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
class ResearchAgent:
    def __init__(self, goal):
        self.goal = goal
        self.observation = []
        self.plan = []
        self.evidence = []
    
    # Create Research Plan
    def create_research_plan(self):
        # print(f"[PLANNER] Creating execution plan...")
        print(f"[RESEARCH] Creating research plan...")
        prompt = f"""
        You are a Research Planner.
        User Goal: {self.goal}
        
        Available Tools:
        SKILL_TOOL
        CERTIFICATION_TOOL
        PROJECT_TOOL
        SALARY_TOOL

        Your task:
        Create the BEST research plan.

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
    

    # Gather Evidence
    def gather_evidence(self):
        print(f"Gathering Evidence...")
        for tool_name in self.plan:

            tool = TOOL_REGISTRY.get(tool_name)
            result = tool(self.goal)
            
            print("=" * 60)
            print(tool_name)
            print("=" * 60)

            print(result)

            self.evidence.append(f"{tool_name}\n{result}")
    

    # Analyze evidence
    def analyze_evidence(self):
        print("ANALYZING EVIDENCE")
        prompt = f"""
        You are an AI Career Analyst
        Goal:
        {self.goal}

        Evidence:
        {self.evidence}

        Generate:
        1. Key findings
        2. Opportunities
        3. Challenges

        Return Analysis
"""
        
        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = prompt
        )

        return response.text

    # Final Response
    def generate_recommendation(self, analysis):
        print(f"Generating Recommendation")
        prompt = f"""
        User Goal: {self.goal}
        Analysis: {analysis}
        Generate:
        - Executive summary
        - Recommendations
        - Learning Path
        - Final Verdict
"""
        
        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = prompt
        )

        print("="*60)
        print("Final Recommendation")
        print("="*60)

        print(response.text)

    # Run Agent
    def run(self):
        # Create Plan
        self.plan = self.create_research_plan()
        
        print("="*60)
        print("RESEARCH PLAN")
        print("="*60)

        for index, tool in enumerate(self.plan, start=1):
            print(f"{index}, {tool}")

        # Gather evidence
        analysis = self.gather_evidence()
        print("ANALYSIS:")
        print(analysis)

        # Final Response
        self.generate_recommendation(analysis)


print("======PLANNER AGENT======")
goal = input("Enter your career goal: ")
agent = ResearchAgent(goal)
agent.run()