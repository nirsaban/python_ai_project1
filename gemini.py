from google import genai
import os
from dotenv import load_dotenv
from google.genai import Client

# Load environment variables from .env file
load_dotenv()

class Gemini:
    def __init__(self):
        # Explicitly define the attribute before checking
        self.instant = None

        # Initialize Gemini API client only once
        self.instant = self.init_gemini_api()


    def init_gemini_api(self) -> Client:
        return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


    def ask_gemini(self,prompt: str):
        response = self.instant.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        return response.text

    def build_gemini_prompt(self, name: str, age: float, sex: str, fare: float, survival_chance: float) -> str:
        prompt = f"""
        You are an AI storyteller and analyst enriching a Titanic passenger ticket system.
        Given a passenger’s data, write a creative summary about them in plain text.

        ### Passenger Information
        Name: {name}
        Age: {age}
        Sex: {sex}
        Fare: {fare}
        Survival Probability: {survival_chance:.1f}%

        ### Instructions
        1. Write 3 short paragraphs:
           - Paragraph 1: Describe the passenger’s personality and background.
           - Paragraph 2: Give a short travel tip or advice for their voyage.
           - Paragraph 3: End with a dramatic or fun prediction about their survival.

        2. Use a warm, cinematic tone (as if describing a 1912 ocean voyage).
        3. Do **not** use bullet points, lists, or JSON. Write as a single, continuous story-like text.

        ### Example Output
        Mr. Thomas is a thoughtful young man of 29, traveling in first class with a sense of quiet curiosity.
        He should spend time on the upper deck, where the sea breeze may calm his restless mind.
        Though fate may test him, his calm instincts and kindness might just earn him a place among the survivors.
        """

        return prompt.strip()


