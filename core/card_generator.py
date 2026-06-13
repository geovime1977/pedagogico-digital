import io
import zipfile
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 630, 882

_ASSETS_FONTS = Path(__file__).parent.parent / "assets" / "fonts"

CORES = {
    "ATK": (230, 57, 70),
    "MID": (29, 53, 87),
    "DEF": (45, 106, 79),
    "GOL": (233, 196, 106),
}

POSICAO_LABEL = {
    "ATK": "ATACANTE",
    "MID": "MEIO-CAMPO",
    "DEF": "DEFENSOR",
    "GOL": "GOLEIRO",
}

STATS = ["VEL", "TEC", "FIS", "MEN", "GOL"]
STATS_KEYS = ["vel", "tec", "fis", "men", "gol"]

_FONTES = [
    str(_ASSETS_FONTS / "DejaVuSans-Bold.ttf"),
    str(_ASSETS_FONTS / "DejaVuSans.ttf"),
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]


def _fonte(size):
    for p in _FONTES:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _escurecer(cor, f=0.5):
    return tuple(int(c * f) for c in cor)


def _gradiente(img, cor):
    draw = ImageDraw.Draw(img)
    escura = _escurecer(cor)
    meio = H // 2
    for y in range(meio, H):
        t = (y - meio) / (H - meio)
        c = tuple(int(cor[i] * (1 - t) + escura[i] * t) for i in range(3))
        draw.line([(0, y), (W, y)], fill=c)


def _stat(draw, label, valor, y):
    bx, bw, bh = 100, W - 180, 16
    by = y + 10
    draw.text((24, y + 2), label, font=_fonte(24), fill="white")
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=8, fill=(60, 60, 60))
    fw = max(0, int(bw * valor / 99))
    if fw:
        draw.rounded_rectangle([bx, by, bx + fw, by + bh], radius=8, fill="white")
    draw.text((W - 20, y + 2), str(valor), font=_fonte(28), fill="white", anchor="rt")


def gerar_card(aluno: dict, foto_bytes: bytes | None = None) -> bytes:
    nome = str(aluno.get("nome", "Aluno")).strip()
    posicao = str(aluno.get("posicao", "MID")).strip().upper()
    numero = str(aluno.get("numero", "10")).strip()
    cor = CORES.get(posicao, CORES["MID"])

    img = Image.new("RGB", (W, H), cor)
    _gradiente(img, cor)
    draw = ImageDraw.Draw(img)

    foto_h = int(H * 0.52)
    if foto_bytes:
        try:
            foto = Image.open(io.BytesIO(foto_bytes)).convert("RGB")
            rc = W / foto_h
            rf = foto.width / foto.height
            if rf > rc:
                nw = int(foto.height * rc)
                off = (foto.width - nw) // 2
                foto = foto.crop((off, 0, off + nw, foto.height))
            else:
                nh = int(foto.width / rc)
                off = (foto.height - nh) // 2
                foto = foto.crop((0, off, foto.width, off + nh))
            foto = foto.resize((W, foto_h), Image.LANCZOS)
            img.paste(foto, (0, 0))
        except Exception:
            _placeholder(draw, W, foto_h)
    else:
        _placeholder(draw, W, foto_h)

    for i in range(20):
        draw.line([(0, foto_h + i), (W, foto_h + i)], fill=(0, 0, 0))

    draw.text((20, 10), numero, font=_fonte(68), fill=(255, 255, 255))

    pos_lbl = POSICAO_LABEL.get(posicao, posicao)
    f_pos = _fonte(20)
    tw = int(draw.textlength(pos_lbl, font=f_pos))
    bx = W - tw - 36
    draw.rounded_rectangle([bx, 18, bx + tw + 20, 50], radius=6, fill=(0, 0, 0))
    draw.text((bx + 10, 22), pos_lbl, font=f_pos, fill="white")

    draw.text((W // 2, foto_h + 36), nome.upper(), font=_fonte(46), fill="white", anchor="mm")

    sy = foto_h + 80
    for i, (lbl, key) in enumerate(zip(STATS, STATS_KEYS)):
        v = min(99, max(0, int(float(aluno.get(key, 75)))))
        _stat(draw, lbl, v, sy + i * 38)

    draw.text((W - 16, H - 20), "2026", font=_fonte(18), fill=(200, 200, 200), anchor="rb")

    buf = io.BytesIO()
    img.save(buf, "PNG", dpi=(240, 240))
    return buf.getvalue()


def _placeholder(draw, w, h):
    draw.rectangle([0, 0, w, h], fill=(25, 25, 25))
    draw.text((w // 2, h // 2), "[ FOTO ]", font=_fonte(28), fill=(80, 80, 80), anchor="mm")


def gerar_zip(alunos: list, fotos: dict) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for aluno in alunos:
            nome = str(aluno.get("nome", "Aluno")).strip()
            card = gerar_card(aluno, fotos.get(nome))
            zf.writestr(f"{nome}.png", card)
    return buf.getvalue()
