import re

from src.ai.exceptions import AIContentExtraction
from src.ai.grade_exam.typeh import AIGradeResponse

from src.config import logger


def process(raw_content: str) -> AIGradeResponse:
    split_fail = False

    try:
        content = raw_content.replace(">>", ">").replace("<<", "<")

        grade, feedback, notes, corrections = _get_by_split(content)

        if grade is None or grade == "":
            split_fail = True
            grade = _get_grade(content)
        
        if not feedback:
            split_fail = True
            feedback = _get_feedback(content)
        
        if split_fail:
            notes = _get_notes(content)
        
        if split_fail:
            corrections = _get_corrections(content)

        return AIGradeResponse(grade=grade, feedback=feedback, notes=notes, corrections=corrections)

    except Exception as exc:
        logger.exception(exc)

        breakpoint()

        raise AIContentExtraction("Error to data from AI response")


def _get_by_split(raw_content: str) -> tuple[float, str, str, str]:
    items = raw_content.split("|")

    grade = float(items[0].replace("grade: ", "").replace(" ", "").replace("\n", "").replace("[", "").replace("]", "").replace("(", "").replace(")", ""))

    feedback = items[1].replace("feedback:", "").strip()
    
    notes = items[2].replace("notes:", "").strip()

    corrections = items[3].replace("corrections:", "").strip()

    if not notes or notes.lower() in ("nulo", "null", "none"):
        notes = ""

    if corrections.endswith("]"):
        corrections = corrections[:-1]
    
    if not corrections or corrections.lower() in ("nulo", "null", "none"):
        corrections = ""
    
    return grade, feedback, notes, corrections



def _to_float(match: re.Match) -> float:
    try:
        raw_value = match.group(1).strip().replace(",", ".")

        if "\n" in raw_value:
            raw_value = raw_value.replace("\n", "")

        return float(raw_value)
    
    except Exception as exc:
        logger.exception(exc)
        
        return None


def _get_grade(raw_content: str) -> float:
    RE_RESULTS = (
        r"grade:([^|]+)",
        r"(^[^|]+)",
        r"grade:(.+)feedback",
        r"(^[^|]+):feedback",
    )

    for re_result in RE_RESULTS:
        raw_grade = re.search(re_result, raw_content, flags=re.S)

        grade = _to_float(raw_grade)

        if grade or grade == 0 or grade == 0.0:
            return grade

    raise AIContentExtraction("Error to extract grade from AI response")

def _get_feedback(raw_content: str) -> str:
    RE_FEEDBACK = (
        r"feedback:([^|]+)",
        r"\|\s*(.*?)\s*\|",
    )

    for re_feedback in RE_FEEDBACK:
        raw_feedback = re.search(re_feedback, raw_content, flags=re.S)

        if raw_feedback:
            return raw_feedback.group(1).strip()
    
    raise AIContentExtraction("Error to extract feedback from AI response")


def _get_notes(raw_content: str) -> str:
    RE_NOTES = r"notes:([^|]+)"
    
    raw_notes = re.search(RE_NOTES, raw_content, flags=re.S)
    
    notes = raw_notes.group(1).strip()

    if not notes or notes.lower() in ("nulo", "null", "none"):
        notes = ""
    
    return notes

def _get_corrections(raw_content: str) -> str:
    RE_CORRECTIONS = r"corrections:([^|]+)"
    
    raw_corrections = re.search(RE_CORRECTIONS, raw_content, flags=re.S)
    
    corrections = raw_corrections.group(1).strip()
    
    if corrections.endswith("]"):
        corrections = corrections[:-1]
    
    if not corrections or corrections.lower() in ("nulo", "null", "none"):
        corrections = ""

    return corrections
