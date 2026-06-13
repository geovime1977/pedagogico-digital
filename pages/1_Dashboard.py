import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd
from core.data import carregar, metricas, ETAPAS

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.title("Dashboard")

m = metricas()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Leads no funil", m["total_leads"])
c2.metric("Em proposta", m["em_proposta"])
c3.metric("Vendas fechadas", m["fechados"])
c4.metric("Receita total", f"R$ {m['receita']:.2f}")

st.divider()

col_chart, col_tab = st.columns([1, 2])

with col_chart:
    st.subheader("Leads por etapa")
    df_etapas = pd.DataFrame({
        "Etapa": list(m["por_etapa"].keys()),
        "Leads": list(m["por_etapa"].values()),
    })
    st.bar_chart(df_etapas.set_index("Etapa"))

with col_tab:
    st.subheader("Todos os leads")
    data = carregar()
    leads = data.get("leads", [])
    if leads:
        df = pd.DataFrame(leads)
        cols_show = ["nome", "produto", "etapa", "valor", "data", "segmento"]
        cols_show = [c for c in cols_show if c in df.columns]
        st.dataframe(df[cols_show], use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum lead cadastrado ainda. Acesse Funil de Vendas para adicionar.")

st.divider()

receita_meta = 500.0
pct = min(100, int(m["receita"] / receita_meta * 100))
st.subheader(f"Meta semanal: R$ {receita_meta:.0f}")
st.progress(pct, text=f"R$ {m['receita']:.2f} / R$ {receita_meta:.2f} ({pct}%)")
