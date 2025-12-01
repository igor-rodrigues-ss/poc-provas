from src.ai.client.gpt import GPTClient
from src.ai.grade_exam import prompts
from src.ai.grade_exam.typeh import AIGradeResponse, GradeResponse
from src.config import logger
from src.ai.grade_exam import ai_response


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

    input_tokens, output_tokens, grade_response = _ai_chat(prompts.CONDITION_PROMPT.get_prompt(theme=theme, essay=essay))

    if grade_response.grade == 0:  # Retry        
        input_tokens, output_tokens, grade_response = _ai_chat(prompts.CONDITION_PROMPT.get_prompt(theme=theme, essay=essay))
        
        result.add_tokens(input_tokens, output_tokens)

        if grade_response.grade == 0:
            logger.info("Redação reprovada")
            return result
    
    result.add_tokens(input_tokens, output_tokens)

    for prompt in prompts.GRADE_PROMPT_CHAIN:
        input_tokens, output_tokens, grade_response = _ai_chat(prompt.get_prompt(theme=theme, essay=essay))

        result.add_tokens(input_tokens, output_tokens)

        if prompt.max_grade and grade_response.grade > prompt.max_grade:
            grade_response.grade = prompt.max_grade

        result.grades[prompt.key] = grade_response

    return result


def _ai_chat(prompt: str) -> tuple[int, int, AIGradeResponse]:
    response = GPTClient().chat(prompt)

    return response.input_tokens, response.output_tokens, ai_response.process(response.content)

    


