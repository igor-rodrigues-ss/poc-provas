"""
Usage:
    python3 -m src.main Tecnologia "files/696026296050_Analista Técnico_Comunicação .pdf"
"""
import sys
from src.ai.ocr import ai_ocr
from src.ai.grade_exam import ai_grade_exam
from src.config import logger, ASPECT_LABEL
from datetime import datetime
from src.pdf import pdf


OCR_THRESHOLD = 70


def main(theme: str, essay_path: str):
    logger.info("Realizando OCR")

    ocr_response = ai_ocr.pdf_to_text(essay_path)

    if ocr_response.ocr.score < OCR_THRESHOLD:
        print(f"Impossível compreender o texto, {ocr_response.ocr.score}%")
        
        logger.info(f"input tokens: {ocr_response.input_tokens}")
        logger.info(f"output tokens: {ocr_response.output_tokens}")    
        return

    essay = ocr_response.ocr.text

    logger.info("Validando Resultado")
    grade_response = ai_grade_exam.execute(theme, essay)

    FONT_SIZE = "8pt"
    MARGIN_TOP_BOTTOM = "4px"

    pdf_content = f"""
        <b style="display: block; font-size: {FONT_SIZE}; margin: 0 0 {MARGIN_TOP_BOTTOM} 0;">Nota Final: {round(grade_response.final_grade, 2)}/10</b>
    """

    for key, value in grade_response.grades.items():
        pdf_content += f"""
        <b style="font-size: {FONT_SIZE};">{ASPECT_LABEL[key]} ({key}):</b>

        <b style="display: block; font-size: {FONT_SIZE}; margin: {MARGIN_TOP_BOTTOM} 0 {MARGIN_TOP_BOTTOM} 24px;">&#10003; Nota: {value.grade}</b>

        <b style="font-size: {FONT_SIZE};">Feedback:</b>

        <br/>

        {value.feedback}
        """

        if value.notes:
            pdf_content += f"""
            <br/>

            <b style="font-size: {FONT_SIZE};">Pontos Importantes:</b>

            <br/>

            {value.notes}
            """


        if value.corrections:
            pdf_content += f"""
            <br/>

            <b style="font-size: {FONT_SIZE};">Correções:</b>

            <br/>

            {value.corrections}
            """

        if not pdf_content.endswith("<br/>"):
            pdf_content += "<br/>"

    pdf.generate(pdf_content, "output.pdf")
    
    input_tokens = ocr_response.input_tokens + grade_response.input_tokens
    output_tokens = ocr_response.output_tokens + grade_response.output_tokens
    
    logger.info(f"nota: {round(grade_response.final_grade, 2)}")
    logger.info(f"input tokens: {input_tokens}")
    logger.info(f"output tokens: {output_tokens}")    


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
