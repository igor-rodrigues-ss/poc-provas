from dataclasses import dataclass
from bs4 import BeautifulSoup


@dataclass
class OCRContentResponse:
    score: int
    html: str

    def __post_init__(self):
        soup = BeautifulSoup(self.html, "html.parser")
        self._text = soup.get_text("\n", strip=True)
    
    @property
    def text(self):
        return self._text


@dataclass
class OCRResponse:
    input_tokens: int
    output_tokens: int
    ocr: OCRContentResponse

