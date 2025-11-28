from dataclasses import dataclass
from typing import TypedDict


@dataclass
class GradeResponse:
    grade: int | float
    feedback: str


class GradeEssayPrompt:

    def __init__(self, key: str, content: str):
        self.key = key
        self.content = content

    def get_prompt(self, theme: str, essay: str):
        return self.content.format(theme=theme, essay=essay)


class GradeDict(TypedDict):
    AP: int | float
    CR: int | float
    CS: int | float
    TT: int | float
    LG: int | float
    TM: int | float
