from abc import ABC, abstractmethod
from src.ai.typeh import AIChatResponse


class AIClient(ABC):

    @abstractmethod
    def chat(self, prompt: str) -> AIChatResponse:
        pass