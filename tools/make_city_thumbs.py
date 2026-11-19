"""Miniaturas de las webs locales (tarjetas «Tu ciudad, al día») a partir de sus banners.

Lee los banners móviles 3:1 de los repos hermanos (../cerdanyola-local, ../santcugat-local) y escribe
static/img/city-{cer,sc}-{day,night}.webp a 600x200. Solo hace falta volver a lanzarlo si cambian los banners.
Uso (Pillow solo está en `py`):  py tools/make_city_thumbs.py
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CITIES = {"cer": ROOT.parent / "cerdanyola-local", "sc": ROOT.parent / "santcugat-local"}
SIZE = (600, 200)


def main():
    out = ROOT / "static" / "img"
    out.mkdir(exist_ok=True)
    for key, repo in CITIES.items():
        for mode in ("day", "night"):
            im = Image.open(repo / "static" / "img" / f"banner-{mode}-m.webp").convert("RGB")
            im = im.resize(SIZE, Image.LANCZOS)
            dest = out / f"city-{key}-{mode}.webp"
            im.save(dest, "WEBP", quality=74, method=6)
            print(dest.name, dest.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
