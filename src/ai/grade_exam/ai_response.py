import re

from src.ai.grade_exam.typeh import GradeResponse


def process(content: str) -> GradeResponse:
    RE_RESULT_V1 = r"grade:(.+)\|"
    RE_RESULT_V2 = r"(.+)\|"
    RE_FEEDBACK = r"feedback:(.+)"

    try:
        grade = re.search(RE_RESULT_V1, content, flags=re.S)

        if not grade:
            grade = re.search(RE_RESULT_V2, content, flags=re.S)

        feedback = re.search(RE_FEEDBACK, content, flags=re.S)

        grade = float(grade.group(1).strip())
        feedback = feedback.group(1).strip()

        if feedback.endswith("]"):
            feedback = feedback[:-1]

        return GradeResponse(grade=grade, feedback=feedback)

    except Exception as e:
        breakpoint()
        raise ValueError("Erro ao extrai dados da IA")