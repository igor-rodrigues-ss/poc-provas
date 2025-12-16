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


OCR_THRESHOLD = 60

"""TODO: Gerar regex para este caso

'2.00 | <p>A redação apresenta uma estrutura geral organizada, com parágrafos que abordam o tema de forma compreensível, garantindo a legibilidade e respeito às margens delimitaras do texto.</p> | <ol><li>Ausência de parágrafos claramente marcados, dificultando a leitura e compreensão.</li></ol> | nulo'

grade: 2.00feedback: <p>A redação demonstra excelente coesão: as ideias seguem uma progressão lógica (apresentação do tema. discussão do papel do smartphone. adaptação da estrutura informativa. mudança nos critérios de noticiabilidade e conclusão). há uso adequado e variado de mecanismos de ligação (advérbios de tempo. locuções correlativas "por um lado... por outro lado". conectivos conclusivos) e os parágrafos mantêm conexão temática clara. permitindo fácil acompanhamento do leitor.</p>notes: <ol><li>Progressão temática clara e linear entre parágrafos.</li><li>Uso diversificado de mecanismos de ligação (temporal. correlativo e conclusivo).</li><li>Parágrafos bem demarcados. cada um com função informativa específica.</li><li>Conclusão retoma e sintetiza as ideias centrais do texto.</li></ol>corrections: <ol><li>Aprimorar transições pontuais entre o segundo e o terceiro parágrafo para explicitar melhor como o uso do smartphone traduz-se diretamente na mudança da estrutura informativa.</li><li>Variar ainda mais os marcadores discursivos e pronomes de referência em alguns períodos para evitar pequenas repetições da palavra "notícia".</li><li>Eventualmente articular com um exemplo curto (mesmo hipotético) para fortalecer a ligação entre mudança tecnológica e alteração dos critérios de noticiabilidade.</li></ol>

'grade: 1.50\nfeedback: <p>O texto demonstra domínio do léxico e coerência global, mas apresenta problemas pontuais de pontuação, colocação pronominal e uma construção final ambígua que comprometem a correção formal; com pequenos ajustes de pontuação (principalmente no período com "se por um lado... por outro lado"), remoção de vírgulas desnecessárias e reformulação da frase conclusiva, a redação atingiria um padrão culto adequado.</p>\nnotes: <ol><li>Pontuação inadequada em locuções como "Se por um lado...; por outro lado..." (uso de vírgulas e ponto e vírgula).</li><li>Construção final ambígua/estrutural: "exija, por exemplo, as agências de checagem..." (problema de regência e clareza).</li><li>Uso desnecessário de aspas em "smartphone" em texto formal.</li><li>Vírgula desnecessária antes de "ou não" no período sobre aprofundamento na notícia.</li></ol>\ncorrections: <ol><li>Reescrever o período com contraste: "Se, por um lado, o leitor espera hipertextualidade em uma notícia publicada na internet, por outro o jornalista produz material multimídia para atender às expectativas da audiência."</li><li>Eliminar aspas: "Atualmente, o smartphone pode ser considerado um instrumento fundamental para o trabalho do jornalista."</li><li>Retirar a vírgula desnecessária: "o leitor escolhe se quer se aprofundar na notícia ou não."</li><li>Corrigir a frase final para maior clareza: "Portanto, as mudanças constantes na tecnologia fazem com que o jornalismo também mude e exija, por exemplo, a atuação de agências de checagem de notícias, que fazem parte da era digital da informação."</li></ol>'

grade: 2.00\nfeedback: <p>Texto claro, coeso e escrito em registro formal adequado ao padrão culto da língua; o vocabulário é preciso e não há erros ortográficos relevantes; observam-se apenas pequenas escolhas de pontuação e construção que afetam minimamente a fluidez (como o uso de ponto e vírgula e de vírgulas desnecessárias), além de algumas alternativas estilísticas que podem ser aprimoradas, mas que não comprometem o padrão culto.</p>\nnotes: <ol><li>Pontuação e uso de conectores em orações coordenadas e subordinadas (ex.: "Se por um lado... por outro lado...").</li><li>Vírgulas desnecessárias em locuções como "ou não".</li><li>Escolha de preposição com o verbo "influenciar" ("influencia diretamente nas escolhas" vs. "influencia diretamente as escolhas").</li><li>Construção final que pede maior clareza na concordância e na introdução do verbo no subjuntivo ("...façam com que o jornalismo também mude e que surjam...").</li><li>Uso desnecessário de aspas em smartphone (palavra já consagrada no português).</li></ol>\ncorrections: <ol><li>Corrigir a frase: "Se por um lado, o leitor espera que haja hipertextualidade em uma notícia publicada na internet; por outro lado é o jornalista que produz material multimídia para alimentar as expectativas da audiência." Sugestão: "Se, por um lado, o leitor espera que haja hipertextualidade em uma notícia publicada na internet, por outro lado é o jornalista quem produz material multimídia para alimentar as expectativas da audiência."</li><li>Eliminar vírgulas desnecessárias: em "o leitor escolhe se quer se aprofundar, ou não, na notícia" usar "o leitor escolhe se quer se aprofundar ou não na notícia".</li><li>Ajustar preposição com "influenciar": substituir "influencia diretamente nas escolhas das redações a partir das redes sociais digitais" por "influencia diretamente as escolhas das redações por meio das redes sociais digitais".</li><li>Aprimorar a construção final para resolver a concordância: substituir "Portanto, as mudanças constantes na tecnologia fazem com que o jornalismo também mude e surjam, por exemplo, as agências de checagem de notícias" por "Portanto, as mudanças constantes na tecnologia fazem com que o jornalismo mude e que surjam, por exemplo, agências de checagem de notícias".</li><li>Retirar as aspas em torno de smartphone: "Atualmente, o smartphone pode ser considerado um instrumento fundamental para o trabalho do jornalista."</li></ol>
"""

def main(theme: str, essay_path: str):
    logger.info("Realizando OCR")

    essay = ai_ocr.pdf_to_text(essay_path)

    if essay.ocr.score < OCR_THRESHOLD:
        logger.info(f"Impossível compreender o texto, {essay.ocr.score}%")
        
        logger.info(f"input tokens: {essay.input_tokens}")
        logger.info(f"output tokens: {essay.output_tokens}")    
        return

    logger.info("Validando Resultado")

    grade_response = ai_grade_exam.execute(theme, essay.ocr.text)

    pdf.generate(grade_response, essay.ocr.html, "output.pdf")

    
    input_tokens = essay.input_tokens + grade_response.input_tokens
    output_tokens = essay.output_tokens + grade_response.output_tokens
    
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
