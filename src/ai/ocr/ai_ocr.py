import os
import dotenv

dotenv.load_dotenv()

import base64

from src.image import essay_processing
from src.ai.client.gpt_image import GPTImageClient
import re


def encode_image(image_path):
    with open(image_path, "rb") as image_file:

        return base64.b64encode(image_file.read()).decode("utf-8")


def pdf_to_text(path: str):
    png_path = "processed_redaction.png"

    essay_processing.pre_processing(path, png_path)

    base64_image = encode_image(png_path)

    client = GPTImageClient()

    resp = client.chat(base64_image, "Transcreva exatamente o texto da imagem dentro de colchetes [texto] mantendo a acentuação, paragrafos e pontuações.")

    os.remove(png_path)

    result = re.search(r"\[(.+)\]", resp.content, re.S).group(0)

    return resp.input_tokens, resp.output_tokens, result