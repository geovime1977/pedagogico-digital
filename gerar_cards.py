import csv
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 630, 882

CORES = {
    "ATK": (230, 57,  70),
    "MID": (29,  53,  87),
    "DEF": (45,  106, 79),
    "GOL": (233, 196, 106),
}

POSICAO_LABEL = {
    "ATK": "ATACANTE",
    "MID": "MEIO-CAMPO",
    "DEF": "DEFENSOR",
    "GOL": "GOLEIRO",
}

STATS = ["VEL", "TEC", "FÍS", "MEN", "GOL"]
STATS_KEYS = ["vel", "tec", "fis", "men", "gol"]

FONTES_MACOS = [
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]


def carregar_fonte(tamanho):
    for path in FONTES_MACOS:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, tamanho)
            except Exception:
                continue
    return ImageFont.load_default()


def escurecer(cor, fator=0.55):
    return tuple(int(c * fator) for c in cor)


def desenhar_gradiente(img, cor_base):
    draw = ImageDraw.Draw(img)
    cor_escura = escurecer(cor_base)
    meio = H // 2
    for y in range(meio, H):
        t = (y - meio) / (H - meio)
        c = tuple(int(cor_base[i] * (1 - t) + cor_escura[i] * t) for i in range(3))
        draw.line([(0, y), (W, y)], fill=c)


def colar_foto(img, nome):
    foto_h = int(H * 0.52)
    paths = [
        Path("fotos") / f"{nome}.jpg",
        Path("fotos") / f"{nome}.jpeg",
        Path("fotos") / f"{nome}.png",
    ]
    for p in paths:
        if p.exists():
            try:
                foto = Image.open(p).convert("RGB")
                # Recortar centro da foto para preencher a zona
                ratio_card = W / foto_h
                ratio_foto = foto.width / foto.height
                if ratio_foto > ratio_card:
                    novo_w = int(foto.height * ratio_card)
                    offset = (foto.width - novo_w) // 2
                    foto = foto.crop((offset, 0, offset + novo_w, foto.height))
                else:
                    novo_h = int(foto.width / ratio_card)
                    offset = (foto.height - novo_h) // 2
                    foto = foto.crop((0, offset, foto.width, offset + novo_h))
                foto = foto.resize((W, foto_h), Image.LANCZOS)
                img.paste(foto, (0, 0))
                return foto_h
            except Exception:
                pass
    # Placeholder quando foto não existe
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, foto_h], fill=(30, 30, 30))
    fonte = carregar_fonte(28)
    draw.text((W // 2, foto_h // 2), "[ FOTO ]", font=fonte, fill=(100, 100, 100), anchor="mm")
    return foto_h


def desenhar_stat(draw, label, valor, y):
    fonte_label = carregar_fonte(24)
    fonte_val = carregar_fonte(28)

    bar_x = 100
    bar_w = W - 180
    bar_h = 16
    bar_y = y + 10

    draw.text((24, y + 2), label, font=fonte_label, fill="white")

    # Barra de fundo
    draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], radius=8, fill=(255, 255, 255, 50))

    # Barra preenchida
    fill_w = max(0, int(bar_w * valor / 99))
    if fill_w > 0:
        draw.rounded_rectangle([bar_x, bar_y, bar_x + fill_w, bar_y + bar_h], radius=8, fill="white")

    draw.text((W - 20, y + 2), str(valor), font=fonte_val, fill="white", anchor="rt")


def gerar_card(aluno, output_dir):
    nome = aluno["nome"].strip()
    posicao = aluno.get("posicao", "MID").strip().upper()
    numero = aluno.get("numero", "10").strip()

    cor = CORES.get(posicao, CORES["MID"])

    img = Image.new("RGB", (W, H), cor)
    desenhar_gradiente(img, cor)

    foto_h = colar_foto(img, nome)

    draw = ImageDraw.Draw(img)

    # Sombra suave abaixo da foto para separar
    for i in range(20):
        alpha = int(180 * (1 - i / 20))
        draw.line([(0, foto_h + i), (W, foto_h + i)], fill=(0, 0, 0, alpha))

    # Número da camisa
    fonte_num = carregar_fonte(68)
    draw.text((20, 10), numero, font=fonte_num, fill=(255, 255, 255))

    # Badge de posição
    pos_label = POSICAO_LABEL.get(posicao, posicao)
    fonte_pos = carregar_fonte(20)
    tw = draw.textlength(pos_label, font=fonte_pos)
    pad = 10
    badge_x = W - tw - pad * 2 - 16
    draw.rounded_rectangle([badge_x, 18, badge_x + tw + pad * 2, 18 + 30], radius=6, fill=(0, 0, 0, 120))
    draw.text((badge_x + pad, 22), pos_label, font=fonte_pos, fill="white")

    # Nome do aluno
    fonte_nome = carregar_fonte(48)
    draw.text((W // 2, foto_h + 36), nome.upper(), font=fonte_nome, fill="white", anchor="mm")

    # Stats
    stats_y = foto_h + 80
    for i, (label, key) in enumerate(zip(STATS, STATS_KEYS)):
        valor = min(99, max(0, int(aluno.get(key, 75))))
        desenhar_stat(draw, label, valor, stats_y + i * 38)

    # Ano
    fonte_ano = carregar_fonte(18)
    draw.text((W - 16, H - 20), "2026", font=fonte_ano, fill=(255, 255, 255), anchor="rb")

    saida = Path(output_dir) / f"{nome}.png"
    img.save(saida, "PNG", dpi=(240, 240))
    print(f"  ✓ {nome}.png")


def main():
    os.makedirs("cards", exist_ok=True)
    os.makedirs("fotos", exist_ok=True)

    csv_path = Path("alunos.csv")
    if not csv_path.exists():
        print("Erro: alunos.csv não encontrado.")
        return

    with open(csv_path, newline="", encoding="utf-8") as f:
        alunos = list(csv.DictReader(f))

    print(f"Gerando {len(alunos)} cards...\n")
    for aluno in alunos:
        gerar_card(aluno, "cards")

    print(f"\nPronto! {len(alunos)} cards salvos em cards/")


if __name__ == "__main__":
    main()
