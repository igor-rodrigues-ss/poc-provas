from src.ai.grade_exam.typeh import GradeEssayPrompt


RESPONSE_STRUCTURE = """
Devolva a nota numéria, feedback como um texto direto em html e sem cumprimentos, pontos importantes como uma lista ordenada em html e correções como uma lista ordenada em html na seguinte estrutura:

grade: nota numérica
feedback: feedback um texto de um único parágrafo em html, sem cumprimentos, sem emojis e sem estilização css.
notes: pontos importantes a serem observados sem cumprimentos, sem emojis e sem estilização css. caso não tenha pontos importantes a serem observados deverá ser retornado o valor "nulo".
corrections: correções a serem realizadas, sem emojis e sem estilização css, caso não tenha correções a serem feitas deverá ser retornado o valor "nulo".

[grade: nota | feedback: feedback | notes: lista html ou nulo | corrections: lista html ou nulo]
"""


CONDITION_PROMPT = GradeEssayPrompt("", f"""
Avalie esta redação baseado nos critérios abaixo:

O tema esperado da redação é: ""{{theme}}""

Redação: ""{{essay}}""

Caso a redação apresente as condições abaixo, todos os critérios serão zerados:

a) não desenvolver o tema proposto, ou seja, fugir ao tema proposto;
b) não desenvolver o tema na tipologia textual exigida, ou seja, fugir ao tipo textual;
c) folha de texto definitivo em branco;
d) desenvolver o texto com quantidade inferior a 20 linhas;
e) desenvolver o texto predominantemente em língua estrangeira;
f) redigir o texto com letra ilegível;
g) redigir o texto com espaçamento excessivo entre letras, palavras, parágrafos e margens;
h) utilizar expressões injuriantes, discriminatórias ou abusivas;
i) apresentar identificação em local indevido de qualquer natureza (nome parcial, nome completo, outro
nome qualquer, número(s), letra(s), sinais, desenhos ou códigos);
j) apresentar textos sob forma não articulada verbalmente, apenas com desenho(s), número(s) e/ou
palavras soltas.

{RESPONSE_STRUCTURE}
""")


GRADE_PROMPT_CHAIN: tuple[GradeEssayPrompt, ...] = (
    GradeEssayPrompt("AP", f"""
Avalie a redação abaixo.

Sempre que houver dúvida entre notas, escolha as notas mais altas.

O tema esperado da redação é: ""{{theme}}""

Redação: ""{{essay}}""

===========================================================

Critério: Apresentação (AP)

descrição: Serão avaliados o respeito às margens
delimitadoras do texto, a estruturação dos
parágrafos (sobretudo a indicação de
parágrafos) e a legibilidade.

Possíveis notas (valor do campo grade): 0.00, 0.50, 1.00, 1.50, 2.00

{RESPONSE_STRUCTURE}

""", max_grade=2),
    GradeEssayPrompt("CR", f"""
Avalie a redação abaixo.

Sempre que houver dúvida entre notas, escolha as notas mais altas.

O tema esperado da redação é: ""{{theme}}""

Redação: ""{{essay}}""

===========================================================

Critério: Coerência (CR)

descrição: Serão avaliados a clareza do texto e o nexo
entre as ideias apresentadas. O texto deve ser
construído com linguagem adequada e clara, de
modo que a compreensão não seja prejudicada
por obstáculos como obscuridade,
contradições, falta de articulação entre ideias e
falha na construção de sentidos.

Possíveis notas (valor do campo grade): 0.00, 0.50, 1.00, 1.50, 2.00

{RESPONSE_STRUCTURE}
""", max_grade=2),

    GradeEssayPrompt("CS", f"""
Avalie a redação abaixo.

Sempre que houver dúvida entre notas, escolha as notas mais altas.

O tema esperado : ""{{theme}}""

Redação: ""{{essay}}""

Criterio: Coesão (CS)

Será avaliada a conexão entre os elementos
formadores do texto (parágrafos, ideias,
períodos, orações e argumentos). A conexão
deve ser estabelecida pelo emprego adequado
e diversificado dos mecanismos linguísticos
necessários para a construção do texto.

Possíveis notas (valor do campo grade): 0.00, 0.50, 1.00, 1.50, 2.00

{RESPONSE_STRUCTURE}
""", max_grade=2),

    GradeEssayPrompt("TT", f"""
Avalie a redação abaixo.

Sempre que houver dúvida entre notas, escolha as notas mais altas.

O tema esperado da redação é: ""{{theme}}""

Redação: ""{{essay}}""

Criterio: Tipo Textual (TT)


Será avaliado o atendimento ao tipo textual
dissertativo, o que inclui a estruturação
adequada do texto, o qual deve apresentar, de
forma bem definida, introdução,
desenvolvimento e conclusão. O texto não deve
apresentar divisão em itens ou tópicos, e não
devem ser feitas menções diretas às partes que
o compõem.

Possíveis notas (valor do campo grade): 0.00, 0.50, 1.00, 1.50, 2.00

{RESPONSE_STRUCTURE}
""", max_grade=2),

    GradeEssayPrompt("LG", f"""
Avalie a redação abaixo.

O tema esperado da redação é: ""{{theme}}""

Redação: ""{{essay}}""

Criterio: Linguagem (LG)

Será avaliado o uso adequado da língua portuguesa em seu padrão culto.

Possíveis notas (valor do campo grade): 0.00, 0.50, 1.00, 1.50, 2.00

{RESPONSE_STRUCTURE}
""", max_grade=2),

    GradeEssayPrompt("TM", f"""
Avalie a redação abaixo.

Sempre que houver dúvida entre notas, escolha as notas mais altas.

O tema esperado: ""{{theme}}""

Redação: ""{{essay}}""

Criterio: Tema (TM)

Avalie:
- Serão avaliadas a adequação e a pertinência das
informações ao tema proposto, bem como a
ordem de desenvolvimento, a qualidade e a
força dos argumentos apresentados.

Possíveis notas (valor do campo grade): 0.00, 1.00, 2.00, 3.00, 4.00, 5.00

{RESPONSE_STRUCTURE}
""", max_grade=5)
)

