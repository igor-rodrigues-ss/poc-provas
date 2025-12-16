from dataclasses import dataclass, field
from collections import OrderedDict
from typing import Optional


@dataclass
class AIGradeResponse:
    grade: int | float
    feedback: str
    notes: str
    corrections: str
    max_grade: Optional[float] = None


@dataclass
class GradeResponse:
    input_tokens: int = 0
    output_tokens: int = 0
    grades: OrderedDict[str, AIGradeResponse] = field(default_factory=OrderedDict)

    def add_tokens(self, input_tokens: int, output_tokens: int):
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
    
    @property
    def final_grade(self) -> float:
        if "AP" not in self.grades:
            return 0
        
        return ((self.grades["AP"].grade + self.grades["CR"].grade + self.grades["CS"].grade + self.grades["TT"].grade + self.grades["LG"].grade) + (self.grades["TM"].grade * 4)) / 3


class GradeEssayPrompt:

    def __init__(self, key: str, content: str, max_grade: Optional[float] = None):
        self.key = key
        self.content = content
        self.max_grade = max_grade

    def get_prompt(self, theme: str, essay: str):
        return self.content.format(theme=theme, essay=essay)