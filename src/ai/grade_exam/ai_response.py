import re

from src.ai.exceptions import AIContentExtraction
from src.ai.grade_exam.typeh import AIGradeResponse

from src.config import logger


def process(raw_content: str) -> AIGradeResponse:
    RE_RESULT_V1 = r"grade:([^|]+)"
    RE_RESULT_V2 = r"(^[^|]+)"
    RE_FEEDBACK = r"feedback:([^|]+)"
    RE_NOTES = r"notes:([^|]+)"
    RE_CORRECTIONS = r"corrections:([^|]+)"

    try:
        content = raw_content.replace(">>", ">").replace("<<", "<")

        raw_grade = re.search(RE_RESULT_V1, content, flags=re.S)

        if not raw_grade:
            raw_grade = re.search(RE_RESULT_V2, content, flags=re.S)

        raw_feedback = re.search(RE_FEEDBACK, content, flags=re.S)
        raw_notes = re.search(RE_NOTES, content, flags=re.S)
        raw_corrections = re.search(RE_CORRECTIONS, content, flags=re.S)

        grade = float(raw_grade.group(1).strip())
        feedback = raw_feedback.group(1).strip()
        notes = raw_notes.group(1).strip()
        corrections = raw_corrections.group(1).strip()

        if corrections.endswith("]"):
            corrections = corrections[:-1]

        if not notes or notes.lower() in ("nulo", "null", "none"):
            notes = ""
        
        if not corrections or corrections.lower() in ("nulo", "null", "none"):
            corrections = ""

        return AIGradeResponse(grade=grade, feedback=feedback, notes=notes, corrections=corrections)

    except Exception as e:
        logger.exception(e)

        breakpoint()

        raise AIContentExtraction("Error to extract grade and feedback from AI response")