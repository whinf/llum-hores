"""Gráficos SVG incrustados (sin JavaScript): barras por horas y mapa de calor."""
from html import escape
from math import ceil, floor

import i18n
import tz

RAMP = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]


def _nice_step(span):
    for step in (0.01, 0.02, 0.025, 0.05, 0.1, 0.2, 0.25, 0.5):
        if span / step <= 5:
            return step
    return 1.0


def _bar_path(x, y0, y1, w, r=4):
    """Barra con los extremos de datos redondeados, anclada a la línea base y0."""
    h = abs(y1 - y0)
    r = min(r, h / 2, w / 2)
    if y1 <= y0:  # hacia arriba
        return (f"M{x:.1f},{y0:.1f}V{y1 + r:.1f}Q{x:.1f},{y1:.1f} {x + r:.1f},{y1:.1f}"
                f"H{x + w - r:.1f}Q{x + w:.1f},{y1:.1f} {x + w:.1f},{y1 + r:.1f}V{y0:.1f}Z")
    return (f"M{x:.1f},{y0:.1f}V{y1 - r:.1f}Q{x:.1f},{y1:.1f} {x + r:.1f},{y1:.1f}"
            f"H{x + w - r:.1f}Q{x + w:.1f},{y1:.1f} {x + w:.1f},{y1 - r:.1f}V{y0:.1f}Z")


def hour_labels(hours):
    """Etiqueta "HH:00–HH:00" de cada hora; en el día de 25 h distingue CEST/CET."""
    starts = [tz.parse_iso(h["t"]) for h in hours]
    seen = [s.hour for s in starts]
    out = []
    for s in starts:
        label = f"{s.hour:02d}:00–{(s.hour + 1) % 24:02d}:00"
        if seen.count(s.hour) > 1:
            label += " CEST" if s.utcoffset().total_seconds() == 7200 else " CET"
        out.append(label)
    return out


def price_bars(lang, hours, window, uid):
    """Gráfico de barras de un día. `window` = (inicio, longitud) a destacar."""
    W, H = 720, 260
    left, right, top, bottom = 60, 8, 44, 30
    pw, ph = W - left - right, H - top - bottom
    prices = [h["p"] / 1000 for h in hours]
    lo = min(0.0, min(prices))
    hi = max(prices)
    step = _nice_step(hi - lo)
    y_min = floor(lo / step) * step
    y_max = ceil(hi / step) * step or step

    def y(v):
        return top + ph - (v - y_min) / (y_max - y_min) * ph

    n = len(prices)
    slot = pw / n
    labels = hour_labels(hours)
    ws, wl = window if window else (-1, 0)
    title = i18n.t(lang, "chart_title")
    desc = i18n.t(lang, "chart_desc", n=wl, start=labels[ws].split("–")[0] if window else "",
                  end=labels[ws + wl - 1].split("–")[1] if window else "")
    out = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-labelledby="{uid}-t {uid}-d">',
           f'<title id="{uid}-t">{escape(title)}</title><desc id="{uid}-d">{escape(desc)}</desc>']
    v = y_min
    while v <= y_max + 1e-9:
        yy = y(v)
        out.append(f'<line class="grid" x1="{left}" x2="{W - right}" y1="{yy:.1f}" y2="{yy:.1f}"/>'
                   f'<text class="tick" x="{left - 6}" y="{yy:.1f}" text-anchor="end" dominant-baseline="middle">'
                   f'{i18n.fmt_num(lang, v, 2)}</text>')
        v += step
    base = y(0)
    for i, p in enumerate(prices):
        x = left + i * slot + 1
        w = slot - 2
        s = tz.parse_iso(hours[i]["t"])
        cls = "bar cheap" if ws <= i < ws + wl else "bar"
        tip = f"{labels[i]} · {i18n.fmt_price(lang, hours[i]['p'])} €/kWh"
        out.append(
            f'<g class="{cls}" data-s="{int(s.timestamp() * 1000)}" tabindex="0">'
            f'<title>{escape(tip)}</title>'
            f'<rect class="hit" x="{x - 1:.1f}" y="{top}" width="{slot:.1f}" height="{ph}"/>'
            f'<path class="fill" d="{_bar_path(x, base, y(p), w)}"/>'
            f'<text class="tip" x="{x + w / 2:.1f}" y="{min(y(p), base) - 5:.1f}" text-anchor="middle">'
            f'{i18n.fmt_num(lang, p, 3)}</text></g>')
    out.append(f'<line class="axis" x1="{left}" x2="{W - right}" y1="{base:.1f}" y2="{base:.1f}"/>')
    for i in range(n):
        s = tz.parse_iso(hours[i]["t"])
        if s.hour % 3 == 0 and (i == 0 or tz.parse_iso(hours[i - 1]["t"]).hour != s.hour):
            out.append(f'<text class="tick" x="{left + (i + 0.5) * slot:.1f}" y="{H - 6}" '
                       f'text-anchor="middle">{s.hour:02d}h</text>')
    if window:
        x0 = left + ws * slot + 1
        x1 = left + (ws + wl) * slot - 1
        out.append(f'<path class="bracket" d="M{x0:.1f},{top - 8}V{top - 13}H{x1:.1f}V{top - 8}"/>'
                   f'<text class="annot" x="{(x0 + x1) / 2:.1f}" y="{top - 20}" text-anchor="middle">'
                   f'{escape(i18n.t(lang, "cheap_window", n=wl))}</text>')
    out.append("</svg>")
    return "".join(out)


def heatmap(lang, days, link):
    """Mapa de calor de un mes. `days` = [(fecha, horas)], `link(fecha)` = URL del día."""
    cell_w, cell_h, left, top = 27, 18, 44, 22
    W = left + 24 * cell_w + 4
    H = top + len(days) * cell_h + 6
    values = [h["p"] for _, hs in days for h in hs]
    lo, hi = min(values), max(values)
    span = (hi - lo) or 1

    def color(p):
        return RAMP[min(len(RAMP) - 1, int((p - lo) / span * len(RAMP)))]

    out = [f'<svg class="chart heat" viewBox="0 0 {W} {H}" role="img" aria-label="'
           f'{escape(i18n.t(lang, "heatmap_desc"))}">']
    for hcol in range(0, 24, 3):
        out.append(f'<text class="tick" x="{left + (hcol + 0.5) * cell_w:.1f}" y="{top - 7}" '
                   f'text-anchor="middle">{hcol:02d}h</text>')
    for r, (d, hours) in enumerate(days):
        yy = top + r * cell_h
        out.append(f'<a href="{link(d)}"><text class="tick day" x="{left - 8}" y="{yy + 13}" '
                   f'text-anchor="end">{d.day}</text></a>')
        by_hour = {}
        for h in hours:
            by_hour.setdefault(tz.parse_iso(h["t"]).hour, []).append(h["p"])
        for hour, ps in by_hour.items():
            p = sum(ps) / len(ps)
            tip = f"{d.day}/{d.month} {hour:02d}:00 · {i18n.fmt_price(lang, p)} €/kWh"
            out.append(f'<rect x="{left + hour * cell_w + 1}" y="{yy + 1}" width="{cell_w - 2}" '
                       f'height="{cell_h - 2}" rx="2" fill="{color(p)}"><title>{escape(tip)}</title></rect>')
    out.append("</svg>")
    legend = "".join(f'<span style="background:{c}"></span>' for c in RAMP)
    return (f'{"".join(out)}<p class="ramp-legend"><span class="lbl">'
            f'{i18n.fmt_price(lang, lo)} · {escape(i18n.t(lang, "heatmap_low"))}</span>'
            f'<span class="ramp">{legend}</span><span class="lbl">'
            f'{escape(i18n.t(lang, "heatmap_high"))} · {i18n.fmt_price(lang, hi)}</span></p>')
