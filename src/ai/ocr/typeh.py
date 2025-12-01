from dataclasses import dataclass


@dataclass
class OCRContentResponse:
    score: int
    text: str


@dataclass
class OCRResponse:
    input_tokens: int
    output_tokens: int
    ocr: OCRContentResponse
