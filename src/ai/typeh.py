from dataclasses import dataclass


@dataclass
class AIChatResponse:
    input_tokens: int
    output_tokens: int
    content: str
