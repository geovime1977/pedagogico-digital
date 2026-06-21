# pedagogico-digital

Plataforma da Eixo Estratégico para gestão e geração de **produtos pedagógicos
digitais** voltados à Copa 2026.

## Produtos

- **Card de Jogador** — cards no estilo FIFA para alunos, gerados em PNG a partir
  de CSV com dados e fotos da turma.
  R$ 9,90 (unitário) · R$ 19,90 (turma completa)
- **Passaporte Cultural Copa 2026** — livro educativo sobre EUA, México e Canadá,
  com capa personalizável por escola.
  R$ 19,90 (digital) · R$ 37,00 (com revenda)

## Páginas (Streamlit)

- `Dashboard` — métricas do funil e receita
- `Card de Jogador` — geração em lote dos cards
- `Passaporte Cultural` — produto Copa 2026
- `Funil de Vendas` — gestão de leads
- `Scripts WhatsApp` — abordagens prontas

## Estrutura

```
pedagogico-digital/
├── app.py                # Home Streamlit
├── pages/                # Dashboard, Card, Passaporte, Funil, Scripts
├── core/                 # card_generator + data layer
├── data/vendas.json      # Persistência do funil
├── assets/               # Imagens base e templates
├── alunos.csv            # Exemplo de entrada para Card de Jogador
└── gerar_cards.py        # Script CLI para gerar cards fora do app
```

## Uso

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (Render)

`render.yaml` + `start.sh` já prontos. Push para o repo e Render faz deploy
automático em Python 3.11.

## Stack

Streamlit · pandas · Pillow
