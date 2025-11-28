from src.ai.grade_exam.typeh import GradeEssayPrompt


CONDITION_PROMPT = GradeEssayPrompt("", """
Avalie esta redação baseado nos critérios abaixo:

O tema esperado da redação é: ""{theme}""

Redação: ""{essay}""

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

Devolva a nota numéria e feedback em html na seguinte estrutura:

0 = reprovado
1 = aprovado

[grade: nota | feedback: feedback em html]
""")


GRADE_PROMPT_CHAIN: tuple[GradeEssayPrompt, ...] = (
    GradeEssayPrompt("AP", """
Avalie a redação abaixo de forma muito amigável, tolerante e nada rigorosa.

Sempre que houver dúvida entre notas, escolha as notas mais altas.

O tema esperado da redação é: ""{theme}""

Redação: ""{essay}""

===========================================================

Critério: Apresentação (AP)

descrição: Serão avaliados o respeito às margens
delimitadoras do texto, a estruturação dos
parágrafos (sobretudo a indicação de
parágrafos) e a legibilidade.

Possíveis notas: 0.00, 0.50, 1.00, 1.50, 2.00

Devolva a nota numéria e feedback em html na seguinte estrutura:

[grade: nota | feedback: feedback em html]
"""),
    GradeEssayPrompt("CR", """
Avalie a redação abaixo de forma muito amigável, tolerante e nada rigorosa.

Sempre que houver dúvida entre notas, escolha as notas mais altas.

O tema esperado da redação é: ""{theme}""

Redação: ""{essay}""

===========================================================

Critério: Coerência (CR)

descrição: Serão avaliados a clareza do texto e o nexo
entre as ideias apresentadas. O texto deve ser
construído com linguagem adequada e clara, de
modo que a compreensão não seja prejudicada
por obstáculos como obscuridade,
contradições, falta de articulação entre ideias e
falha na construção de sentidos.

Possíveis notas: 0.00, 0.50, 1.00, 1.50, 2.00

Devolva a nota numéria e feedback em html na seguinte estrutura:

[grade: nota | feedback: feedback em html]
"""),

    GradeEssayPrompt("CS", """
Avalie a redação abaixo de forma muito amigável, tolerante e nada rigorosa.

Sempre que houver dúvida entre notas, escolha as notas mais altas.

O tema esperado : ""{theme}""

Redação: ""{essay}""

Criterio: Coesão (CS)

Será avaliada a conexão entre os elementos
formadores do texto (parágrafos, ideias,
períodos, orações e argumentos). A conexão
deve ser estabelecida pelo emprego adequado
e diversificado dos mecanismos linguísticos
necessários para a construção do texto.

Possíveis notas: 0.00, 0.50, 1.00, 1.50, 2.00

Devolva a nota numéria e feedback em html na seguinte estrutura:

[grade: nota | feedback: feedback em html]
"""),

    GradeEssayPrompt("TT", """
Avalie a redação abaixo de forma muito amigável, tolerante e nada rigorosa.

Sempre que houver dúvida entre notas, escolha as notas mais altas.

O tema esperado da redação é: ""{theme}""

Redação: ""{essay}""

Criterio: Tipo Textual (TT)


Será avaliado o atendimento ao tipo textual
dissertativo, o que inclui a estruturação
adequada do texto, o qual deve apresentar, de
forma bem definida, introdução,
desenvolvimento e conclusão. O texto não deve
apresentar divisão em itens ou tópicos, e não
devem ser feitas menções diretas às partes que
o compõem.

Possíveis notas: 0.00, 0.50, 1.00, 1.50, 2.00

Devolva a nota numéria e feedback em html na seguinte estrutura:

[grade: nota | feedback: feedback em html]
"""),

    GradeEssayPrompt("LG", """
Avalie a redação abaixo de forma muito amigável, tolerante e nada rigorosa.

O tema esperado da redação é: ""{theme}""

Redação: ""{essay}""

Criterio: Linguagem (LG)

Será avaliado o uso adequado da língua portuguesa em seu padrão culto.

Possíveis notas: 0.00, 0.50, 1.00, 1.50, 2.00

Devolva a nota numéria e feedback em html na seguinte estrutura:

[grade: nota | feedback: feedback em html]
"""),

    GradeEssayPrompt("TM", """
Avalie a redação abaixo de forma muito amigável, tolerante e nada rigorosa.

Sempre que houver dúvida entre notas, escolha as notas mais altas.

O tema esperado: ""{theme}""

Redação: ""{essay}""

Criterio: Tema (TM)

Avalie:
- Serão avaliadas a adequação e a pertinência das
informações ao tema proposto, bem como a
ordem de desenvolvimento, a qualidade e a
força dos argumentos apresentados.

Possíveis notas: 0.00, 1.00, 2.00, 3.00, 4.00, 5.00

Devolva a nota numéria e feedback em html na seguinte estrutura:

[grade: nota | feedback: feedback em html]
""")
)

