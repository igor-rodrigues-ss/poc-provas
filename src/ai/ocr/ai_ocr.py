import os
import dotenv

dotenv.load_dotenv()

import base64

from src.image import essay_processing
from src.ai.client.gpt_image import GPTImageClient
from src.ai.ocr import ai_response
from src.ai.ocr.typeh import OCRResponse
from src.config import logger


def pdf_to_text(path: str, max_retries: int = 3) -> OCRResponse:
    attempt = 1

    while attempt <= max_retries:
        try:
            return _pdf_to_text(path)

        except Exception as exc:
            logger.warning(f"Attempt {attempt} of {max_retries}")

            if attempt == max_retries:
                raise exc

            attempt += 1

def _pdf_to_text(path: str) -> OCRResponse:
    png_path = "processed_redaction.png"

    essay_processing.pre_processing(path, png_path)

    base64_image = _encode_image(png_path)

    client = GPTImageClient()

    resp = client.chat(base64_image, "Transcreva exatamente o texto da imagem em html mantendo a acentuação, paragrafos e pontuações. Quero também um percentual de 0 a 100 para mostrar o quanto você entendeu do texto transcrito. Retorne os dados na seguinte estrutura: [score: percentual | text: texto transcrito em html somente com tags <p>].")

    ocr_response = ai_response.process(resp.content)

    logger.info(f"ocr score: {ocr_response.score}%")

    os.remove(png_path)

    return OCRResponse(resp.input_tokens, resp.output_tokens, ocr_response)


def _encode_image(image_path):
    with open(image_path, "rb") as image_file:

        return base64.b64encode(image_file.read()).decode("utf-8")


