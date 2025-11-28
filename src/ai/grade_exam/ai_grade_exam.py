from src.ai.client.gpt import GPTClient
from src.ai.grade_exam import prompts
from src.ai.grade_exam.typeh import GradeDict, GradeResponse
from src.config import logger
from src.ai.grade_exam import ai_response


def execute(theme: str, essay: str):
    in_tokens = 0
    out_tokens = 0
    grade: GradeDict = {}

    input_tokens, output_tokens, grade_response = _ai_chat(prompts.CONDITION_PROMPT.get_prompt(theme=theme, essay=essay))

    if grade_response.grade == 0:
        logger.info("Redação reprovada")
        return in_tokens, out_tokens, 0

    in_tokens += input_tokens
    out_tokens += output_tokens

    for prompt in prompts.GRADE_PROMPT_CHAIN:
        input_tokens, output_tokens, grade_response = _ai_chat(prompt.get_prompt(theme=theme, essay=essay))

        in_tokens += input_tokens
        out_tokens += output_tokens
        grade[prompt.key] = grade_response.grade

    final_grade = _calculate_final_grade(grade)

    return in_tokens, out_tokens, final_grade


def _calculate_final_grade(grade: GradeDict) -> float:
    return ((grade["AP"] + grade["CR"] + grade["CS"] + grade["TT"] + grade["LG"]) + (grade["TM"] * 4)) / 3


def _ai_chat(prompt: str) -> tuple[int, int, GradeResponse]:
    response = GPTClient().chat(prompt)

    return response.input_tokens, response.output_tokens, ai_response.process(response.content)

    


