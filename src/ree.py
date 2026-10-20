"""Descarga y lectura de datos públicos de Red Eléctrica (REE).

Precios: término de energía del PVPC 2.0TD (indicador 1001) en €/MWh, con
peajes y cargos, sin impuestos. Fuente principal apidatos.ree.es; respaldo,
el archivo 70 de ESIOS. Ninguna de las dos pide token.
"""
import json
import time
import urllib.error
import urllib.request
from datetime import date, timedelta

import tz

APIDATOS = "https://apidatos.ree.es/es/datos"
ESIOS_70 = "https://api.esios.ree.es/archives/70/download_json?locale=es&date={day}"
USER_AGENT = "Mozilla/5.0 (compatible; llum-hores/1.0; +https://github.com/)"

# Agrupación de tecnologías de "estructura-generacion" (por id de REE).
SOURCES = {
    "10291": "wind", "1458": "solar", "1459": "solar", "10288": "hydro",
    "10292": "other_renewable", "10295": "other_renewable",
    "1446": "nuclear", "1454": "gas", "1450": "gas", "1451": "other_fossil",
    "10293": "cogeneration", "10289": "coal", "10344": "other_fossil",
    "10294": "other_fossil",
}
RENEWABLE = {"wind", "solar", "hydro", "other_renewable"}


class FetchError(Exception):
    pass


def get_json(url, tries=3, timeout=40):
    last = None
    for attempt in range(tries):
        req = urllib.request.Request(url, headers={
            "User-Agent": USER_AGENT, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last = exc
            if isinstance(exc, urllib.error.HTTPError) and exc.code < 500:
                break
            time.sleep(3 * (attempt + 1))
    raise FetchError(f"{url}: {last}")


def _range_url(path, start, end, trunc):
    return (f"{APIDATOS}/{path}?start_date={start.isoformat()}T00:00"
            f"&end_date={end.isoformat()}T23:59&time_trunc={trunc}")


def _included(doc, pred):
    for inc in (doc or {}).get("included", []):
        if pred(inc):
            return inc
    return None


def parse_pvpc(doc, start, end=None):
    """{día: [{"t": iso, "p": €/MWh}]} solo para días completos."""
    end = end or start
    inc = _included(doc, lambda i: i.get("id") == "1001")
    if not inc:
        return {}
    by_day = {}
    for v in inc["attributes"]["values"]:
        t = tz.parse_iso(v["datetime"])
        by_day.setdefault(t.date(), []).append(
            {"t": t.isoformat(), "p": round(float(v["value"]), 2)})
    out = {}
    d = start
    while d <= end:
        hours = by_day.get(d, [])
        if hours and len(hours) == len(tz.day_hours(d)):
            out[d] = sorted(hours, key=lambda h: tz.parse_iso(h["t"]))
        d += timedelta(days=1)
    return out


def parse_esios70(doc, day):
    rows = [r for r in (doc or {}).get("PVPC", [])
            if r.get("Dia") == day.strftime("%d/%m/%Y")]
    starts = tz.day_hours(day)
    if not rows or len(rows) != len(starts):
        return None
    return [{"t": s.isoformat(), "p": round(float(r["PCB"].replace(".", "").replace(",", ".")), 2)}
            for s, r in zip(starts, rows)]


def fetch_pvpc(day):
    """(horas, fuente) del día, o (None, None) si aún no se ha publicado."""
    try:
        doc = get_json(_range_url("mercados/precios-mercados-tiempo-real", day, day, "hour"))
        hours = parse_pvpc(doc, day).get(day)
        if hours:
            return hours, "apidatos"
    except FetchError as exc:
        print("aviso:", exc)
    try:
        hours = parse_esios70(get_json(ESIOS_70.format(day=day.isoformat())), day)
        if hours:
            return hours, "esios"
    except FetchError as exc:
        print("aviso:", exc)
    return None, None


def fetch_pvpc_range(start, end):
    doc = get_json(_range_url("mercados/precios-mercados-tiempo-real", start, end, "hour"))
    return parse_pvpc(doc, start, end)


def parse_mix(ren_doc, struct_doc, co2_doc):
    """{día: {"renewable_pct", "co2_g_kwh", "sources": {grupo: %}}}."""
    out = {}

    def day_of(v):
        return tz.parse_iso(v["datetime"]).date()

    ren = _included(ren_doc, lambda i: i.get("type") == "Renovable")
    for v in (ren or {}).get("attributes", {}).get("values", []):
        out.setdefault(day_of(v), {})["renewable_pct"] = round(v["percentage"] * 100, 1)

    generated = {}
    for inc in (struct_doc or {}).get("included", []):
        group = SOURCES.get(inc.get("id"))
        if group is None:
            if inc.get("id") == "10296":  # generación total
                generated = {day_of(v): v["value"] for v in inc["attributes"]["values"]}
                continue
            group = ("other_renewable" if inc["attributes"].get("type") == "Renovable"
                     else "other_fossil")
        for v in inc["attributes"]["values"]:
            src = out.setdefault(day_of(v), {}).setdefault("sources", {})
            src[group] = round(src.get(group, 0) + v["percentage"] * 100, 1)

    # La serie "tCO2 eq./MWh" de REE llega con las fechas cambiadas cuando se
    # piden varios días, así que calculamos la intensidad: total tCO2 / MWh generados.
    co2 = _included(co2_doc, lambda i: i.get("id") == "tCO2 eq.")
    for v in (co2 or {}).get("attributes", {}).get("values", []):
        d = day_of(v)
        if generated.get(d):
            out.setdefault(d, {})["co2_g_kwh"] = round(v["value"] / generated[d] * 1000)

    return {d: m for d, m in out.items() if "renewable_pct" in m}


def fetch_mix(start, end):
    docs = [get_json(_range_url(p, start, end, "day")) for p in (
        "generacion/evolucion-renovable-no-renovable",
        "generacion/estructura-generacion",
        "generacion/no-renovables-detalle-emisiones-CO2")]
    return parse_mix(*docs)


def month_chunks(start, end):
    d = start
    while d <= end:
        nxt = date(d.year + (d.month == 12), d.month % 12 + 1, 1)
        yield d, min(end, nxt - timedelta(days=1))
        d = nxt
