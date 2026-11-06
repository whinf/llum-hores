"""Genera src/icons.py a partir de los SVG de Lucide (https://lucide.dev, licencia ISC).

Uso (una sola vez, en local):  python -I tools/make_icons.py <carpeta_con_svg_de_lucide>

Solo se incluyen los iconos de NAMES. El módulo resultante se commitea; los SVG no.
"""
import re
import sys
from pathlib import Path

NAMES = """zap train-front banknote fuel plug-zap party-popper ticket link construction megaphone telescope
building briefcase piggy-bank sparkles utensils siren calendar bell clock baby hourglass map-pin sprout heart
trees footprints landmark drama coffee moon trophy handshake monitor sun chevron-down gamepad-2 wand-sparkles
clapperboard message-circle arrow-right arrow-left trending-down trending-up thermometer droplets wind cloud-sun
info""".split()

HEADER = '''"""Iconos SVG como sprite por página.

Lucide Icons (https://lucide.dev), licencia ISC: Copyright (c) for portions of Lucide are held by
Cole Bemis 2013-2022 as part of Feather (MIT). All other copyright (c) for Lucide are held by
Lucide Contributors 2022. Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above copyright notice and this
permission notice appear in all copies.

Generado por tools/make_icons.py; no editar a mano.
"""
from html import escape as esc

'''


def body(svg_text):
    inner = re.search(r"<svg[^>]*>(.*)</svg>", svg_text, re.S).group(1)
    return re.sub(r"\s+", " ", inner).strip().replace("> <", "><")


def main():
    src = Path(sys.argv[1])
    icons = {}
    for name in NAMES:
        icons[name] = body((src / f"{name}.svg").read_text("utf-8"))
    out = [HEADER, "LUCIDE = {\n"]
    for name, inner in icons.items():
        out.append(f"    {name!r}: {inner!r},\n")
    out.append("}\n\n")
    out.append('''
def icon(used, name, label=None, cls="i"):
    """<svg><use> de un icono Lucide; `used` acumula los nombres para el sprite de la página."""
    if name not in LUCIDE:
        raise KeyError(f"icono desconocido: {name}")
    used.add(name)
    a = f'role="img" aria-label="{esc(label, quote=True)}"' if label else 'aria-hidden="true"'
    return f'<svg class="{cls}" {a}><use href="#i-{name}"/></svg>'


def sprite(used):
    """Sprite oculto con solo los símbolos usados en la página (caja 0x0, no display:none)."""
    if not used:
        return ""
    syms = "".join(f'<symbol id="i-{n}" viewBox="0 0 24 24">{LUCIDE[n]}</symbol>' for n in sorted(used))
    return (f'<svg class="sprite" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{syms}</svg>')
''')
    Path(__file__).resolve().parent.parent.joinpath("src", "icons.py").write_text("".join(out), "utf-8")
    print("ok", len(icons), "iconos")


if __name__ == "__main__":
    main()
