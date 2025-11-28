"""
Usage:
    python3 -m src.main Tecnologia "files/696026296050_Analista Técnico_Comunicação .pdf"
"""
import sys
from src.ai.ocr import ai_ocr
from src.ai.grade_exam import ai_grade_exam
from src.config import logger
from datetime import datetime


def main(theme: str, essay_path: str):
    in_tokens_result = 0
    out_tokens_result = 0

    logger.info("Realizando OCR")

    in_tokens, out_tokens, essay = ai_ocr.pdf_to_text(essay_path)

    in_tokens_result += in_tokens
    out_tokens_result += out_tokens

    logger.info("Validando Resultado")
    in_tokens, out_tokens, final_grade = ai_grade_exam.execute(theme, essay)
    
    in_tokens_result += in_tokens
    out_tokens_result += out_tokens
    
    logger.info(f"nota: {round(final_grade, 2)}")
    logger.info(f"input tokens: {in_tokens_result}")
    logger.info(f"output tokens: {out_tokens_result}")    


if __name__ == "__main__":
    start = datetime.now()

    main(sys.argv[1], sys.argv[2])

    print(datetime.now() - start)










"""
696026296050_Analista Técnico_Comunicação .pdf
Nota MIIA: 9,33/10.0

AP: 1.5/2.0
CR: 2.0/2.0
CS: 1.0/2.0
TT: 2.0/2.0
LG: 1.5/2.0
TM: 5.0/5.0

Nota POC: (gpt-4.1-nano)
nota:  8.17/10.0 (9,67 / 8,0 / 8,33)
AP: 2.00
CR: 1.50
CS: 1.00
TT: 2.00
LG: 2.00
TM: 4.00
"""



"""
696026451823_Analista Técnico_Tecnico_Administrativo.pdf
MIIA: https://mail.google.com/mail/u/0/#inbox/FMfcgzQcqtlTftCFxlRZmDKhjwdmWqrR?projector=1&messagePartId=0.1

Nota MIIA: 8.5/10.0

AP: 2.0/2.0
CR: 2.0/2.0
CS: 2.0/2.0
TT: 2.0/2.0
LG: 1.5/2.0
TM: 4.0/5.0

Nota POC: (gpt-4.1-nano)
nota:  8.17/10.0
AP: 1.50
CR: 1.50
CS: 1.00
TT: 1.50
LG: 1.50
TM: 3.00
"""
