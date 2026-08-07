from openai import OpenAI

from app.core.config import OPENAI_API_KEY


class ChatService:
    def __init__(self) -> None:
        self._client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_response(self, message: str) -> str:
        completion = self._client.chat.completions.create(
            model="gpt-5.6-luna",
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
        )
        return completion.choices[0].message.content or ""
