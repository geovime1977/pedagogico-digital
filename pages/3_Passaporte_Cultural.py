import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import io
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="Passaporte Cultural", page_icon="📖", layout="wide")
st.title("Passaporte Cultural Copa 2026")
st.caption("Material educativo sobre EUA, Mexico e Canada — paises-sede da Copa 2026")

ASSET = Path(__file__).parent.parent / "assets" / "capa_passaporte_copa_2026.png"

_ASSETS_FONTS = Path(__file__).parent.parent / "assets" / "fonts"
FONTES = [
    str(_ASSETS_FONTS / "DejaVuSans-Bold.ttf"),
    str(_ASSETS_FONTS / "DejaVuSans.ttf"),
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def _fonte(size):
    for p in FONTES:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def personalizar_capa(escola: str, turma: str) -> bytes:
    img = Image.open(ASSET).convert("RGB")
    draw = ImageDraw.Draw(img)
    w, h = img.size

    # Faixa no rodape
    faixa_h = int(h * 0.08)
    draw.rectangle([0, h - faixa_h, w, h], fill=(10, 20, 60))

    fonte_escola = _fonte(max(24, int(w * 0.025)))
    fonte_turma = _fonte(max(18, int(w * 0.018)))

    texto = escola.upper()
    draw.text((w // 2, h - faixa_h + faixa_h // 3), texto, font=fonte_escola, fill=(255, 215, 0), anchor="mm")
    if turma:
        draw.text((w // 2, h - faixa_h + (faixa_h * 2) // 3), turma, font=fonte_turma, fill=(200, 200, 200), anchor="mm")

    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()


col_img, col_info = st.columns([1, 1])

with col_img:
    st.subheader("Capa do produto")
    if ASSET.exists():
        st.image(str(ASSET), use_container_width=True)
    else:
        st.warning("Imagem da capa nao encontrada em assets/")

with col_info:
    st.subheader("Sobre o produto")
    st.markdown("""
**O que e?**
Material didatico editavel sobre os 3 paises-sede da Copa 2026:
EUA, Mexico e Canada. Formato passaporte com atividades pedagogicas.

**Conteudo:**
- Historia e cultura de cada pais
- Curiosidades geograficas
- Vocabulario em ingles e espanhol
- Atividades de interpretacao e pesquisa
- Espaco para o aluno preencher

**Publico-alvo:** Fundamental I e II (6–14 anos)

**Formato:** Digital editavel — professora personaliza com nome da escola e turma
""")

    st.subheader("Precificacao")
    st.markdown("""
| Modelo | Preco |
|---|---|
| Digital (uso proprio) | R$ 19,90 |
| Licenca revenda (turma) | R$ 37,00 |
| Licenca escola (todas as turmas) | R$ 97,00 |
""")

st.divider()

if ASSET.exists():
    st.subheader("Personalizar capa com nome da escola")
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        escola = st.text_input("Nome da escola", placeholder="E.M. Professora Ana Lima")
    with col2:
        turma = st.text_input("Turma (opcional)", placeholder="3o ano A — 2026")
    with col3:
        st.write("")
        st.write("")
        gerar = st.button("Personalizar", type="primary", use_container_width=True)

    if gerar and escola:
        with st.spinner("Gerando capa personalizada..."):
            img_bytes = personalizar_capa(escola, turma)
        col_prev, col_down = st.columns([2, 1])
        with col_prev:
            st.image(img_bytes, caption=f"Capa — {escola}", use_container_width=True)
        with col_down:
            st.download_button(
                "Baixar capa personalizada",
                data=img_bytes,
                file_name=f"passaporte_{escola.replace(' ', '_')}.png",
                mime="image/png",
                use_container_width=True,
            )
    elif gerar:
        st.warning("Digite o nome da escola.")

st.divider()
st.subheader("Script de venda — WhatsApp")
st.code("""Oi, [Nome]! Tudo bem?

Com a Copa 2026 chegando, lancei um material que ta fazendo sucesso:
o Passaporte Cultural Copa 2026 — um livro educativo sobre EUA, Mexico
e Canada para usar em sala de aula.

A capa ja vem com o nome da sua escola e o professor personaliza
em minutos. Tenho em formato digital para imprimir na escola.

Posso te mandar a capa de exemplo?""", language=None)
