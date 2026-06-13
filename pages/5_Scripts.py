import streamlit as st

st.set_page_config(page_title="Scripts WhatsApp", page_icon="💬", layout="wide")
st.title("Scripts WhatsApp")
st.caption("Copie e adapte com o nome do contato antes de enviar")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Abordagem fria",
    "Apos amostra",
    "Proposta revenda",
    "Urgencia Copa",
    "Passaporte Cultural",
])

with tab1:
    st.subheader("Abordagem fria — Professor")
    nome = st.text_input("Nome do contato", value="[Nome]", key="n1")
    st.code(f"""Oi, {nome}! Tudo bem?

Sou o Geovane, trabalho com materiais pedagogicos digitais.

Vi que voce e professora e queria te mostrar algo que ta fazendo
muito sucesso nas escolas agora — um card personalizado estilo FIFA
com as fotos dos proprios alunos da turma.

Posso te mandar um exemplo?""", language=None)

with tab2:
    st.subheader("Apos enviar amostra")
    nome2 = st.text_input("Nome do contato", value="[Nome]", key="n2")
    st.code(f"""{nome2}, o que achou?

E tudo editavel — voce coloca o nome, a foto e os dados de cada aluno.
Uma turma de 30 cardinhos fica pronta em menos de 5 minutos.

Tenho uma condicao especial essa semana pra professores.
Quer saber o valor?""", language=None)

with tab3:
    st.subheader("Proposta de revenda")
    nome3 = st.text_input("Nome do contato", value="[Nome]", key="n3")
    st.code(f"""{nome3}, tenho uma ideia que pode te render uma grana extra:

Voce compra o pacote uma vez e revende para os pais dos seus alunos.

Uma turma de 30 alunos:
- Voce cobra R$15 de cada = R$450 bruto
- O pacote custa R$27
- Lucro liquido: R$423

Quer ver como funciona?""", language=None)

with tab4:
    st.subheader("Urgencia — Copa comeca em junho")
    nome4 = st.text_input("Nome do contato", value="[Nome]", key="n4")
    st.code(f"""{nome4}, so avisando que estou fechando as vendas essa semana.

A Copa comeca em junho e depois disso o produto perde o timing
para usar em sala de aula.

Ainda da tempo de voce encomendar e usar com sua turma.
Posso garantir o seu ate sexta?""", language=None)

with tab5:
    st.subheader("Passaporte Cultural Copa 2026")
    nome5 = st.text_input("Nome do contato", value="[Nome]", key="n5")
    st.code(f"""Oi, {nome5}! Tudo bem?

Com a Copa 2026 chegando, lancei um material educativo que ta chamando
muita atencao: o Passaporte Cultural Copa 2026.

E um livro didatico sobre EUA, Mexico e Canada com atividades de
interpretacao, vocabulario e curiosidades geograficas — tudo no
tema da Copa.

A capa vem personalizada com o nome da sua escola.
Posso te mandar a previa?""", language=None)

st.divider()
st.subheader("Respostas para objecoes")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**'Nao sei usar o Canva'**")
    st.code("Nao precisa saber! O sistema gera todos os cards automaticamente — voce so manda o arquivo com os dados e recebe os cards prontos.", language=None)

    st.markdown("**'Ta caro'**")
    st.code("Uma turma de 30 alunos a R$15 cada te da R$450. O pacote custa R$27. Voce ja lucra na primeira turma.", language=None)

with col2:
    st.markdown("**'Vou pensar'**")
    st.code("Claro! Posso segurar esse preco ate sexta. Depois da Copa o produto perde o timing e eu precisaria cobrar o preco cheio.", language=None)

    st.markdown("**'Ja tenho algo parecido'**")
    st.code("Posso ver o que voce tem? Se for melhor que o meu, te indico o concorrente mesmo. A ideia e que voce use o melhor material.", language=None)
