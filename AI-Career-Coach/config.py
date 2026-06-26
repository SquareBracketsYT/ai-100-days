"""
Configuration module
Loads environment variables used accross the project
"""

import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

class Config:
    """
    Central Configuration class
    """

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gemini-3.5-flash")

    @staticmethod
    def validate() -> None:
        """
        Validate mandatory configuration
        """

        if not Config.GEMINI_API_KEY:
            raise ValueError (
                "GEMINI_API_KEY is missing. Please check your .env file"
            )