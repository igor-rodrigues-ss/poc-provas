from xhtml2pdf import pisa


def generate(html_content: str, output_path: str):
    with open(output_path, "wb") as pdf_file:
        pisa.CreatePDF(html_content, dest=pdf_file)

