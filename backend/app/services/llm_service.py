from openai import OpenAI


class LLMService:
    def __init__(self):
        self.client = OpenAI()

    def generate_answer(self, question: str, context: str) -> str:
        """
        Generate a source-grounded answer using only the provided document context.
        """

        system_prompt = """
You are a helpful course document assistant.

Rules:
1. Answer only using the provided document context.
2. If the answer is not found in the context, say: "The answer could not be found in the document."
3. Do not use outside knowledge.
4. Keep the answer concise and clear.
5. Mention page numbers when they are available in the context.
"""

        user_prompt = f"""
Question:
{question}

Document Context:
{context}

Answer:
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0.2,
            max_tokens=200,
        )

        return response.choices[0].message.content