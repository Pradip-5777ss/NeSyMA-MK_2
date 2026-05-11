import os
from abc import ABC, abstractmethod
import google.generativeai as genai
from dotenv import load_dotenv

class BaseLLMProvider(ABC):
    @abstractmethod
    def generate_code(self, prompt: str) -> str:
        pass

class GeminiProvider(BaseLLMProvider):
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_code(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text
