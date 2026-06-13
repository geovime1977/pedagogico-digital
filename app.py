import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from core.data import metricas

st.set_page_config(
    page_title="Pedagógico Digital | Eixo Estratégico",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("⚽ Pedagógico Digital")
st.sidebar.caption("Eixo Estratégico — Copa 2026")

m = metricas()

st.title("Pedagógico Digital — Copa 2026")
st.caption("Plataforma de gestão e geração de produtos pedagógicos digitais")
st.divider()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Leads no funil", m["total_leads"])
c2.metric("Em proposta", m["em_proposta"])
c3.metric("Vendas fechadas", m["fechados"])
c4.metric("Receita total", f"R$ {m['receita']:.2f}")

st.divider()
st.subheader("Produtos disponíveis")

col1, col2 = st.columns(2)

with col1:
    st.info("""
**Card de Jogador**
Cards personalizados no estilo FIFA para toda a turma.
Upload do CSV com dados dos alunos e fotos — gera PNG de cada aluno.

Preco: R$ 9,90 (unitario) · R$ 19,90 (turma completa)
""")

with col2:
    st.info("""
**Passaporte Cultural Copa 2026**
Livro educativo sobre EUA, Mexico e Canada — paises-sede da Copa.
Capa personalizavel com nome da escola.

Preco: R$ 19,90 (digital) · R$ 37,00 (com revenda)
""")

st.divider()
st.subheader("Navegacao")
st.markdown("""
- **Dashboard** — metricas do funil e receita
- **Card de Jogador** — gerar cards da turma
- **Passaporte Cultural** — produto Copa 2026
- **Funil de Vendas** — gestao de leads
- **Scripts WhatsApp** — abordagens prontas
""")
