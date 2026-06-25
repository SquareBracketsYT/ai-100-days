from google import genai
from dotenv import load_dotenv
import os
import time

# Load the environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


# Agent
class RoadMapAgent:
    def __init__(self, goal):
        # Goal = User Input
        self.goal = goal
    
    # Step-1: Reasoning
    def reason(self):
        print("[Agent] Understanding Goal...")
        prompt = f"""
        User Goal: {self.goal}
        Identify all required skills.
        Return only the skills
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    # Step-2: Planning
    def plan(self, skills):
        print("[Agent] Creating Plan...")
        prompt = f"""
        Goal: {self.goal}
        Skills: {skills}
        Arrange these skills in the best learning order
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text
    
    # Step-3: Execute
    def execute(self, plan):
        print("[Agent] Executing Plan...")
        prompt = f"""
        Goal: {self.goal}
        Learning Plan: {plan}
        Create a detailed 90-day roadmap
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    # Run Agent
    def run(self):
        skills = self.reason()
        time.sleep(1)

        plan = self.plan(skills)
        time.sleep(1)

        roadmap = self.execute(plan)

        print("\n" + "=" * 50)
        print("Final Roadmap")
        print("=" * 50)
        print(roadmap)

print("="*50)
print("Welcome to Roadmap Agent")
print("="*50)
goal = input("Enter your goal: ")
agent = RoadMapAgent(goal)
agent.run()