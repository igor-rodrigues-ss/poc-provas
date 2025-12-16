from src.ai.client.gpt import GPTClient
from src.ai.grade_exam import prompts
from src.ai.grade_exam.typeh import AIGradeResponse, GradeResponse
from src.config import logger
from src.ai.grade_exam import ai_response
from src.ai.grade_exam.typeh import GradeEssayPrompt


def execute(theme: str, essay: str, max_retries: int = 3) -> GradeResponse:
    attempt = 1

    while attempt <= max_retries:
        try:
            return _execute(theme, essay)
        
        except Exception as exc:
            logger.exception(exc)
            
            logger.warning(f"Attempt {attempt} of {max_retries}")

            if attempt == max_retries:
                raise exc

            attempt += 1


def _execute(theme: str, essay: str) -> GradeResponse:
    result = GradeResponse()

    prompt_init = prompts.CONDITION_PROMPT

    input_tokens, output_tokens, grade_response = _ai_chat(prompt_init, theme, essay)


    if grade_response.grade == 0:  # Retry
        input_tokens, output_tokens, grade_response = _ai_chat(prompt_init, theme, essay)

        result.add_tokens(input_tokens, output_tokens)

        if grade_response.grade == 0:
            logger.info("Redação reprovada")

            result.grades[prompt_init.key] = grade_response

            return result
    
    result.add_tokens(input_tokens, output_tokens)

    for prompt in prompts.GRADE_PROMPT_CHAIN:
        input_tokens, output_tokens, grade_response = _ai_chat(prompt, theme, essay)

        result.add_tokens(input_tokens, output_tokens)

        if prompt.max_grade and grade_response.grade > prompt.max_grade:
            grade_response.grade = prompt.max_grade

        result.grades[prompt.key] = grade_response

    return result


def _ai_chat(prompt: GradeEssayPrompt, theme: str, essay: str) -> tuple[int, int, AIGradeResponse]:
    response = GPTClient().chat(prompt.get_prompt(theme=theme, essay=essay))

    grade_response = ai_response.process(response.content)

    grade_response.max_grade = prompt.max_grade

    return response.input_tokens, response.output_tokens, grade_response

    


