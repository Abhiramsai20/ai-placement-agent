import os
from dotenv import load_dotenv
from groq import Groq

import sys

# Ensure UTF-8 output encoding across environments (especially Windows consoles)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Load environment variables from .env file if available
load_dotenv()


class LLMService:

    def __init__(self, model=None):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable is not set. "
                "Please configure GROQ_API_KEY in your .env file or environment variables."
            )

        self.client = Groq(api_key=api_key)
        self.model = model or os.environ.get(
            "GROQ_MODEL",
            "openai/gpt-oss-20b"
        )

    def generate(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content
        return content if content is not None else ""