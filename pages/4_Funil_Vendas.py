import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd
from core.data import carregar, salvar, add_lead, update_etapa, delete_lead, ETAPAS, PRODUTOS, SEGMENTOS

st.set_page_config(page_title="Funil de Vendas", page_icon="📈", layout="wide")
st.title("Funil de Vendas")

# Adicionar lead
with st.expander("+ Adicionar novo lead", expanded=False):
    with st.form("form_lead", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            nome = st.text_input("Nome do contato *")
            whatsapp = st.text_input("WhatsApp", placeholder="21999999999")
            segmento = st.selectbox("Segmento", SEGMENTOS)
        with c2:
            produto = st.selectbox("Produto", PRODUTOS)
            valor = st.number_input("Valor esperado (R$)", min_value=0.0, value=27.0, step=1.0)
        submitted = st.form_submit_button("Adicionar lead", type="primary")
        if submitted:
            if not nome:
                st.error("Nome e obrigatorio.")
            else:
                add_lead(nome, whatsapp, segmento, produto, valor)
                st.success(f"Lead '{nome}' adicionado!")
                st.rerun()

st.divider()

# Kanban por etapas
data = carregar()
leads = data.get("leads", [])

cols = st.columns(4)
etapa_cores = {
    "Contato": "#1A3A5C",
    "Amostra": "#2D4A1E",
    "Proposta": "#4A2D00",
    "Fechado": "#1A1A1A",
}

for col, etapa in zip(cols, ETAPAS):
    leads_etapa = [l for l in leads if l["etapa"] == etapa]
    with col:
        st.markdown(f"**{etapa}** · {len(leads_etapa)}")
        st.divider()
        for lead in leads_etapa:
            with st.container(border=True):
                st.markdown(f"**{lead['nome']}**")
                st.caption(f"{lead['produto']} · R$ {lead['valor']:.2f}")
                st.caption(f"{lead['segmento']} · {lead['data']}")

                nova_etapa = st.selectbox(
                    "Mover para",
                    ETAPAS,
                    index=ETAPAS.index(lead["etapa"]),
                    key=f"etapa_{lead['id']}",
                    label_visibility="collapsed",
                )
                if nova_etapa != lead["etapa"]:
                    update_etapa(lead["id"], nova_etapa)
                    st.rerun()

                if st.button("Remover", key=f"del_{lead['id']}", use_container_width=True):
                    delete_lead(lead["id"])
                    st.rerun()

st.divider()

if leads:
    st.subheader("Tabela completa")
    df = pd.DataFrame(leads)
    cols_show = ["nome", "produto", "etapa", "valor", "segmento", "whatsapp", "data"]
    cols_show = [c for c in cols_show if c in df.columns]
    st.dataframe(df[cols_show], use_container_width=True, hide_index=True)
