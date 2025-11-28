import os


from openai import OpenAI

from src.ai.client.base import AIClient
from src.ai.typeh import AIChatResponse

from src.config import logger


class GPTImageClient(AIClient):

    def chat(self, base64_image: str, prompt: str) -> AIChatResponse:
        client = OpenAI(api_key=os.environ["OPEN_AI_API_KEY"])

        response = client.responses.create(
            model="gpt-4.1",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_image",  "image_url":  f"data:image/jpeg;base64,{base64_image}"},
                        {"type": "input_text", "text": prompt}
                    ]
                }
            ]
        )

        result = AIChatResponse(
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            content=response.output[0].content[0].text
        )

        logger.info(result)

        return result   
            