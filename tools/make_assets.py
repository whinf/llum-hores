"""Genera los PNG de static/ (iconos PWA, apple-touch-icon y og:image). Requiere Pillow; se ejecuta en local:

py tools/make_assets.py

Dibuja el mismo logotipo que static/favicon.svg (disco verde con rayo amarillo).
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "static"
GREEN, YELLOW, BG = (11, 107, 58), (245, 213, 71), (249, 249, 247)
NAME, TAGLINE = "Hora Verda", "Precio de la luz hoy por horas · Preu de la llum per hores"
BOLT = [(18.5, 4), (9, 18), (15, 18), (13, 28), (23, 13), (16.8, 13)]  # igual que el path del favicon (caja 32)


def logo(size, pad=0.0):
    """Disco verde con rayo; `pad` = margen relativo (para iconos maskable)."""
    s = 4  # supermuestreo
    im = Image.new("RGBA", (size * s, size * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    k = size * s / 32
    m = pad * size * s
    d.ellipse((m, m, size * s - m, size * s - m), fill=GREEN)
    scale = (size * s - 2 * m) / (size * s)
    pts = [((x - 16) * k * scale + size * s / 2, (y - 16) * k * scale + size * s / 2) for x, y in BOLT]
    d.polygon(pts, fill=YELLOW)
    return im.resize((size, size), Image.LANCZOS)


def font(size, bold=True):
    for name in ("segoeuib.ttf" if bold else "segoeui.ttf", "arialbd.ttf" if bold else "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


logo(512, 0.1).save(OUT / "icon-512.png", optimize=True)
logo(192, 0.1).save(OUT / "icon-192.png", optimize=True)
bg = Image.new("RGBA", (180, 180), GREEN)
bg.alpha_composite(logo(180))
bg.convert("RGB").save(OUT / "apple-touch-icon.png", optimize=True)

og = Image.new("RGB", (1200, 630), BG)
og.paste(logo(300), (90, 165), logo(300))
d = ImageDraw.Draw(og)
d.text((450, 215), NAME, fill=(26, 25, 23), font=font(96))
d.text((452, 345), TAGLINE, fill=(82, 81, 78), font=font(30, bold=False))
d.rectangle((0, 610, 1200, 630), fill=GREEN)
og.save(OUT / "og.png", optimize=True)
print("ok", [p.name for p in OUT.glob("*.png")])
