from xhtml2pdf import pisa
from src.ai.grade_exam.typeh import GradeResponse
from src.config import ASPECT_LABEL


def generate(grade_response: GradeResponse, essay: str, output_path: str):
    MARGIN_TOP_BOTTOM = "4px"

    pdf_content = f"""
        <b style="display: block;">Resposta do Aluno</b>

        {essay}

        <br/>

        <b style="display: block; margin: 0 0 {MARGIN_TOP_BOTTOM} 0;">Nota Final: {round(grade_response.final_grade, 2)}/10</b>
    """

    for key, value in grade_response.grades.items():
        pdf_content += f"""
        <b>{ASPECT_LABEL[key]} ({key}):</b>

        <b style="display: block; margin: {MARGIN_TOP_BOTTOM} 0 {MARGIN_TOP_BOTTOM} 24px;">&#10003; Nota: {value.grade}/{float(value.max_grade)}</b>

        <b>Feedback:</b>

        <br/>

        {value.feedback}
        """

        if value.notes:
            pdf_content += f"""
            <br/>

            <b>Pontos Importantes:</b>

            <br/>

            {value.notes}
            """


        if value.corrections:
            pdf_content += f"""
            <br/>

            <b>Correções:</b>

            <br/>

            {value.corrections}
            """

        if not pdf_content.endswith("<br/>"):
            pdf_content += "<br/>"


    html_content = f"""

    <!DOCTYPE html>
    <head>
        <style>
            @page {{
                margin: 112px;
            }}
            
            b {{
                font-size: 11pt;
            }}

            p, li {{
                text-align: justify;
                font-size: 11pt;
            }}
        </style>
    </head>

    <html>
        <body>

        {pdf_content}

        </body>
    </html>
    """ 

    with open(output_path, "wb") as pdf_file:
        pisa.CreatePDF(html_content, dest=pdf_file)

