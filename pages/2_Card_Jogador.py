import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd
import io
from core.card_generator import gerar_card, gerar_zip

st.set_page_config(page_title="Card de Jogador", page_icon="🃏", layout="wide")
st.title("Card de Jogador")
st.caption("Gere cards estilo FIFA personalizados para toda a turma")

st.divider()

col_esq, col_dir = st.columns([3, 2])

with col_esq:
    st.subheader("1. Dados dos alunos")

    uploaded_csv = st.file_uploader(
        "Upload do CSV (nome, posicao, numero, vel, tec, fis, men, gol)",
        type=["csv"],
        help="Posicoes: ATK, MID, DEF, GOL",
    )

    if uploaded_csv:
        df = pd.read_csv(uploaded_csv)
        st.success(f"{len(df)} alunos carregados")
    else:
        st.caption("Sem CSV? Edite a tabela abaixo diretamente:")
        df_default = pd.DataFrame({
            "nome": ["Joao Silva", "Maria Santos", "Pedro Lima"],
            "posicao": ["ATK", "MID", "DEF"],
            "numero": [9, 10, 4],
            "vel": [88, 75, 65],
            "tec": [72, 90, 78],
            "fis": [85, 68, 82],
            "men": [70, 88, 85],
            "gol": [91, 82, 70],
        })
        df = st.data_editor(
            df_default,
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "posicao": st.column_config.SelectboxColumn(
                    "Posicao", options=["ATK", "MID", "DEF", "GOL"]
                ),
                "numero": st.column_config.NumberColumn("Camisa", min_value=1, max_value=99),
                "vel": st.column_config.NumberColumn("VEL", min_value=0, max_value=99),
                "tec": st.column_config.NumberColumn("TEC", min_value=0, max_value=99),
                "fis": st.column_config.NumberColumn("FIS", min_value=0, max_value=99),
                "men": st.column_config.NumberColumn("MEN", min_value=0, max_value=99),
                "gol": st.column_config.NumberColumn("GOL", min_value=0, max_value=99),
            },
        )

    st.subheader("2. Fotos dos alunos (opcional)")
    uploaded_fotos = st.file_uploader(
        "Upload das fotos (nome do arquivo = nome do aluno)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
    )
    fotos = {}
    if uploaded_fotos:
        for f in uploaded_fotos:
            nome_foto = os.path.splitext(f.name)[0]
            fotos[nome_foto] = f.read()
        st.caption(f"{len(fotos)} fotos carregadas: {', '.join(fotos.keys())}")

with col_dir:
    st.subheader("3. Preview")

    if len(df) > 0:
        nomes = df["nome"].astype(str).tolist()
        aluno_sel = st.selectbox("Selecionar aluno", nomes)
        row = df[df["nome"].astype(str) == aluno_sel].iloc[0].to_dict()
        aluno_dict = {k: str(v) for k, v in row.items()}
        foto_bytes = fotos.get(aluno_sel)
        with st.spinner("Gerando preview..."):
            card_bytes = gerar_card(aluno_dict, foto_bytes)
        st.image(card_bytes, width=280, caption=aluno_sel)
    else:
        st.info("Adicione alunos na tabela para ver o preview")

st.divider()

col_btn, col_info = st.columns([1, 2])

with col_btn:
    st.subheader("4. Gerar todos")
    st.metric("Alunos", len(df))
    st.metric("Fotos", len(fotos))

    if st.button("Gerar ZIP com todos os cards", type="primary", use_container_width=True):
        if len(df) == 0:
            st.error("Adicione alunos antes de gerar.")
        else:
            alunos = [{k: str(v) for k, v in row.items()} for row in df.to_dict("records")]
            with st.spinner(f"Gerando {len(alunos)} cards..."):
                zip_bytes = gerar_zip(alunos, fotos)
            st.download_button(
                label=f"Baixar {len(alunos)} cards (ZIP)",
                data=zip_bytes,
                file_name="cards_turma.zip",
                mime="application/zip",
                use_container_width=True,
            )
            st.success(f"{len(alunos)} cards prontos!")

with col_info:
    st.subheader("Referencia de cores")
    st.markdown("""
| Posicao | Codigo | Cor |
|---|---|---|
| ATK | Atacante | Vermelho |
| MID | Meio-campo | Azul escuro |
| DEF | Defensor | Verde |
| GOL | Goleiro | Dourado |
""")
    st.subheader("Formato do CSV")
    st.code("nome,posicao,numero,vel,tec,fis,men,gol\nJoao,ATK,9,88,72,85,70,91", language="csv")
