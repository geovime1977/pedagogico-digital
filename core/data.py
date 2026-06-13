import json
from pathlib import Path
from datetime import date

DATA_FILE = Path(__file__).parent.parent / "data" / "vendas.json"

ETAPAS = ["Contato", "Amostra", "Proposta", "Fechado"]
PRODUTOS = ["Card de Jogador", "Passaporte Cultural", "Álbum Copa 2026", "Diploma Formatura"]
SEGMENTOS = ["Professor", "Coordenador", "Pai/Mãe", "Escola"]


def carregar() -> dict:
    if DATA_FILE.exists():
        with open(DATA_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"leads": []}


def salvar(data: dict):
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_lead(nome, whatsapp, segmento, produto, valor):
    data = carregar()
    novo_id = max((l["id"] for l in data["leads"]), default=0) + 1
    data["leads"].append({
        "id": novo_id,
        "nome": nome,
        "whatsapp": whatsapp,
        "segmento": segmento,
        "produto": produto,
        "etapa": "Contato",
        "valor": float(valor),
        "data": str(date.today()),
        "notas": "",
    })
    salvar(data)
    return novo_id


def update_etapa(lead_id, etapa):
    data = carregar()
    for lead in data["leads"]:
        if lead["id"] == lead_id:
            lead["etapa"] = etapa
            break
    salvar(data)


def delete_lead(lead_id):
    data = carregar()
    data["leads"] = [l for l in data["leads"] if l["id"] != lead_id]
    salvar(data)


def metricas() -> dict:
    data = carregar()
    leads = data["leads"]
    fechados = [l for l in leads if l["etapa"] == "Fechado"]
    return {
        "total_leads": len(leads),
        "em_proposta": sum(1 for l in leads if l["etapa"] == "Proposta"),
        "fechados": len(fechados),
        "receita": sum(l["valor"] for l in fechados),
        "por_etapa": {e: sum(1 for l in leads if l["etapa"] == e) for e in ETAPAS},
    }
