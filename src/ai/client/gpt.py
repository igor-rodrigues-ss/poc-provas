import os
from src.ai.client.base import AIClient
from src.ai.typeh import AIChatResponse
from openai import OpenAI
from src.config import logger, AI_MODEL


class GPTClient(AIClient):

    def chat(self, prompt: str) -> AIChatResponse:
        client = OpenAI(api_key=os.environ["OPEN_AI_API_KEY"])

        response = client.chat.completions.create(
            model=AI_MODEL,
            store=False,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        result = AIChatResponse(
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
            content=response.choices[0].message.content
        )

        logger.debug(result)

        return result
