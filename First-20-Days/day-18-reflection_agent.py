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


class ReflectionAgent:
    """
    Reflection Agent
    Responsibilities:
    1. Review the first draft
    2. Identify weaknesses
    3. Suggest improvements
    4. Generate improved reports
    """

    def __init__(self):
        pass

    # Review Draft
    def review_draft(self, draft):
        print("="*70)
        print("Reviewing Draft")
        print("="*70)

        prompt = f"""
        You are a senior AI reviewer.
        Review the following career report.
        Career Report: {draft}

        Evaluate the report on:
        1. Accuracy
        2. Completeness
        3. Clarity
        4. Practicality
        5. Missing Information
        6. Actionable Advice

        Rules:
        - Do not rewrite the report
        - Only provide feedback
        - Mention strengths
        - Mention weakness
        - Suggest improvements
"""
        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = prompt
        )

        print("="*60)
        print("Reviewer Feedback...")
        print("="*60)
        print(response.text)

    # Improve Draft
    def improve_draft(self, draft, feedback):
        print("="*70)
        print("Improving Draft")
        print("="*70)

        prompt = f"""
        You are Expert AI Career Consultant.
        Below is the original report:
        ---------------------
        {draft}
        ---------------------
        Reviewer Feedback:
        ---------------------
        {feedback}
        ---------------------
        Your task:
        Rewrite the report.
        Requirements:
        - Address every reviewer comment.
        - Keep the good parts
        - Improve weak sections
        - Add missing information
        - Make recommendation more practical
        - Make roadmap more actionable
"""
        
        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = prompt
        )

        print("="*60)
        print("Improved Report...")
        print("="*60)
        print(response.text)

    # Reflect
    def reflect(self, draft):
        "Draft -> Review -> Improve -> Final Report"
        
        feedback = self.review_draft(draft)
        final_report = self.improve_draft(draft, feedback)

        return final_report

