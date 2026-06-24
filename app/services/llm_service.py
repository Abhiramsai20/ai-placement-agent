from ollama import chat


class LLMService:

    def generate(self, prompt):

        response = chat(
            model="qwen2.5:1.5b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]