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

    def generate(self, prompt, max_tokens=4096):
        models_to_try = [self.model]
        for fallback in ["llama-3.1-8b-instant", "gemma2-9b-it"]:
            if fallback not in models_to_try:
                models_to_try.append(fallback)

        last_err = None
        for m in models_to_try:
            try:
                response = self.client.chat.completions.create(
                    model=m,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.2,
                    max_tokens=max_tokens
                )

                content = response.choices[0].message.content
                return content if content is not None else ""
            except Exception as e:
                err_str = str(e)
                last_err = e
                if "401" in err_str or "invalid_api_key" in err_str:
                    raise ValueError(
                        "Your GROQ_API_KEY is invalid or expired. "
                        "Please configure GROQ_API_KEY in your Render Environment settings."
                    ) from e
                print(f"Notice: Model {m} returned {err_str}. Trying next fallback model...")
                continue

        raise last_err

