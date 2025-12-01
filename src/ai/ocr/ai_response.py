import re

from src.config import logger
from src.ai.exceptions import AIContentExtraction
from src.ai.ocr.typeh import OCRContentResponse


def process(content: str) -> OCRContentResponse:
    RE_RESULT_V1 = r"score:(.+)\|"
    RE_RESULT_V2 = r"(.+)\|"
    RE_FEEDBACK = r"text:(.+)"

    try:
        score = re.search(RE_RESULT_V1, content, flags=re.S)

        if not score:
            score = re.search(RE_RESULT_V2, content, flags=re.S)

        text = re.search(RE_FEEDBACK, content, flags=re.S)

        raw_score = score.group(1).strip()

        if raw_score.endswith("%"):
            score = int(raw_score[:-1])
        else:
            score = int(raw_score)
        
        text = text.group(1).strip()

        if text.endswith("]"):
            text = text[:-1]

        return OCRContentResponse(score=score, text=text)

    except Exception as exc:
        logger.exception(exc)

        raise AIContentExtraction("Error to extract OCR content")