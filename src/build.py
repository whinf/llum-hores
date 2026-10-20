"""Actualiza los datos de REE y genera el sitio estático en _site/.

  python src/build.py                        descarga lo que falte y genera la web
  python src/build.py --offline              solo genera, sin conexión
  python src/build.py --backfill 2025-01-01  carga el histórico desde esa fecha
  python src/build.py --check                falla si falta un dato importante
  --site-url URL                             URL pública (Actions pasa la de Pages)
  --now 2026-10-20T21:00                     simula otra hora de Madrid
"""
import argparse
import json
import os
import sys
import time
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ree  # noqa: E402
import tz  # noqa: E402
from render import ROOT, Site  # noqa: E402
from store import Store  # noqa: E402

PUBLISH_HOUR = 20  # REE publica los precios de mañana hacia las 20:30


def load_config(site_url=None):
    cfg = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    if site_url:
        cfg["site_url"] = site_url
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not cfg.get("repo_url") and repo:
        cfg["repo_url"] = f"https://github.com/{repo}"
    return cfg


def stamp():
    return tz.now_madrid().isoformat(timespec="seconds")


def has_prices(store, d):
    return bool((store.load(d) or {}).get("hours"))


def update(store, now):
    today = now.date()
    for d in (today, today + timedelta(days=1)):
        if has_prices(store, d) or (d > today and now.hour < PUBLISH_HOUR):
            continue
        hours, source = ree.fetch_pvpc(d)
        if hours:
            store.update(d, hours=hours, prices_source=source, prices_fetched=stamp())
            print(f"precios {d}: {len(hours)} horas ({source})")
        else:
            print(f"precios {d}: todavía no publicados")
    for d in (today - timedelta(days=1), today - timedelta(days=2)):
        rec = store.load(d) or {}
        final_after = tz.local_midnight(d + timedelta(days=1)) + timedelta(hours=6)
        fetched = rec.get("mix_fetched")
        if rec.get("mix") and fetched and tz.parse_iso(fetched) >= final_after:
            continue
        try:
            mix = ree.fetch_mix(d, d).get(d)
        except ree.FetchError as exc:
            print("aviso:", exc)
            continue
        if mix:
            store.update(d, mix=mix, mix_fetched=stamp())
            print(f"mix {d}: {mix['renewable_pct']} % renovable")


def backfill(store, start, end):
    today = tz.now_madrid().date()
    for a, b in ree.month_chunks(start, end):
        prices = ree.fetch_pvpc_range(a, b)
        time.sleep(1)
        mixes = ree.fetch_mix(a, min(b, today - timedelta(days=1))) if a < today else {}
        time.sleep(1)
        d = a
        while d <= b:
            if d in prices and not has_prices(store, d):
                store.update(d, hours=prices[d], prices_source="apidatos", prices_fetched=stamp())
            if d in mixes:
                store.update(d, mix=mixes[d], mix_fetched=stamp())
            d += timedelta(days=1)
        print(f"{a} a {b}: {len(prices)} días con precios, {len(mixes)} con mix")


def check(store, now):
    problems = []
    if not has_prices(store, now.date()):
        problems.append(f"faltan los precios de hoy ({now.date()})")
    if (now.hour, now.minute) >= (22, 30) and not has_prices(store, now.date() + timedelta(days=1)):
        problems.append("a las 22:30 todavía faltan los precios de mañana")
    for p in problems:
        print("ERROR:", p)
    return 1 if problems else 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--backfill", metavar="AAAA-MM-DD")
    ap.add_argument("--site-url")
    ap.add_argument("--now")
    ap.add_argument("--out", default=str(ROOT / "_site"))
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    store = Store()
    now = tz.now_madrid()
    if args.now:
        given = tz.parse_iso(args.now)
        if given.tzinfo is None:  # hora local de Madrid
            given = given.replace(tzinfo=tz.offset_at(given.replace(tzinfo=tz.CET)))
        now = tz.to_madrid(given)
    if args.check:
        return check(store, now)
    if args.backfill:
        from datetime import date
        backfill(store, date.fromisoformat(args.backfill), now.date() + timedelta(days=1))
    elif not args.offline:
        update(store, now)
    out = Site(load_config(args.site_url), store.all(), args.out, now).build()
    print("sitio generado en", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
