"""Genera el sitio estático completo a partir del histórico diario."""
import json
import shutil
from datetime import date, timedelta
from html import escape as esc
from pathlib import Path
from urllib.parse import urlparse

import i18n
import svg
import tz
import windows
from i18n import LANGS, t

ROOT = Path(__file__).resolve().parent.parent
WINDOW = 3  # horas de la franja destacada


def fmt_dt(iso):
    if not iso:
        return ""
    d = tz.to_madrid(tz.parse_iso(iso))
    return f"{d.day:02d}/{d.month:02d}/{d.year} {d.hour:02d}:{d.minute:02d}"


class Site:
    def __init__(self, cfg, records, out_dir, now):
        self.cfg = cfg
        self.records = {d: r for d, r in records.items() if r and r.get("hours")}
        self.mixes = {d: r["mix"] for d, r in records.items() if r and r.get("mix")}
        self.out = Path(out_dir)
        self.now = now
        self.base_url = cfg["site_url"].rstrip("/")
        self.prefix = urlparse(self.base_url).path.rstrip("/")
        self.name = cfg["site_name"]
        self.days = sorted(self.records)

    # ---------- URLs ----------
    def path(self, lang, kind, d=None):
        slug = t(lang, "slug_price")
        if kind == "home":
            return f"/{lang}/"
        if kind == "archive":
            return f"/{lang}/{slug}/"
        if kind == "month":
            return f"/{lang}/{slug}/{d.year:04d}/{d.month:02d}/"
        if kind == "day":
            return f"/{lang}/{slug}/{d.year:04d}/{d.month:02d}/{d.day:02d}/"
        if kind == "feed":
            return f"/{lang}/feed.xml"
        return f"/{lang}/{t(lang, 'slug_' + kind)}/"

    def href(self, path):
        return self.prefix + path

    def absolute(self, path):
        return self.base_url + path

    def write(self, path, text):
        target = self.out / path.lstrip("/")
        if path.endswith("/"):
            target = target / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    # ---------- plantilla común ----------
    def layout(self, lang, kind, d, title, desc, body, jsonld=None, noindex=False, bare=False):
        here = self.path(lang, kind, d)
        alts = "".join(f'<link rel="alternate" hreflang="{lg}" href="{self.absolute(self.path(lg, kind, d))}">'
                       for lg in LANGS)
        x_default = self.absolute("/") if kind == "home" else self.absolute(self.path("es", kind, d))
        alts += f'<link rel="alternate" hreflang="x-default" href="{x_default}">'
        ld = "".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>'
                     for j in (jsonld or []))
        head = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{'<meta name="robots" content="noindex">' if noindex else ''}
<link rel="canonical" href="{self.absolute(here)}">
{alts}
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{self.absolute(here)}">
<meta property="og:locale" content="{t(lang, 'locale')}">
<meta property="og:site_name" content="{esc(self.name)}">
<meta name="theme-color" content="#0b6b3a">
<link rel="icon" href="{self.href('/static/favicon.svg')}" type="image/svg+xml">
<link rel="stylesheet" href="{self.href('/static/style.css')}">
<link rel="alternate" type="application/rss+xml" title="{esc(t(lang, 'feed_title'))}" href="{self.href(self.path(lang, 'feed'))}">
{ld}
<script src="{self.href('/static/now.js')}" defer></script>
</head>"""
        if bare:
            return f'{head}\n<body class="widget">{body}</body>\n</html>\n'
        switch = " · ".join(
            f'<a href="{self.href(self.path(lg, kind, d))}" hreflang="{lg}" lang="{lg}"'
            f'{" aria-current=\"true\"" if lg == lang else ""}>{t(lg, "lang_name")}</a>' for lg in LANGS)
        donate = (f'<a class="donate" href="{esc(self.cfg["donate_url"])}" rel="noopener">{t(lang, "donate")}</a>'
                  if self.cfg.get("donate_url") else "")
        sister_url = self.cfg.get("sister_url")
        sister = (f'<a class="sister" href="{esc(sister_url.rstrip("/"))}/{lang}/">📍 {t(lang, "sister")}</a>'
                  if sister_url else "")
        updated = self.records[self.days[-1]].get("prices_fetched") if self.days else None
        links = " · ".join(f'<a href="{self.href(self.path(lang, k))}">{t(lang, k)}</a>'
                           for k in ("about", "legal", "privacy"))
        links += f' · <a href="https://onestudioman.horaverda.es/{lang}/">{t(lang, "studio")}</a>'
        return f"""{head}
<body>
<a class="skip" href="#main">{t(lang, "skip")}</a>
<header class="top"><div class="wrap">
<a class="brand" href="{self.href(self.path(lang, 'home'))}"><img src="{self.href('/static/favicon.svg')}" alt="" width="28" height="28"> {esc(self.name)}</a>
<nav class="langs" aria-label="{t(lang, 'language')}">{switch}</nav>
</div>{f'<div class="wrap sister-bar">{sister}</div>' if sister else ""}</header>
<main id="main" class="wrap">
{body}
</main>
<footer class="foot"><div class="wrap">
<p>{t(lang, "source_line", t=fmt_dt(updated))}</p>
{f"<p>{sister}</p>" if sister else ""}
<p>{links} · <a href="{self.href(self.path(lang, 'archive'))}">{t(lang, "archive_title")}</a> · <a href="{self.href('/api/v1/latest.json')}">{t(lang, "api")}</a> · <a href="{self.href(self.path(lang, 'feed'))}">{t(lang, "feed")}</a> {donate}</p>
</div></footer>
</body>
</html>
"""

    # ---------- piezas ----------
    def prices(self, d):
        return [h["p"] for h in self.records[d]["hours"]]

    def stat_tiles(self, lang, d):
        hours = self.records[d]["hours"]
        labels = svg.hour_labels(hours)
        s = windows.summary(self.prices(d))
        return f"""<div class="tiles">
<div class="tile"><span class="k">{t(lang, "avg")}</span><span class="v">{i18n.fmt_price(lang, s["avg"])}</span><span class="u">{t(lang, "unit")}</span></div>
<div class="tile good"><span class="k">{t(lang, "min")}</span><span class="v">{labels[s["min_i"]].split("–")[0]}</span><span class="u">{i18n.fmt_price(lang, s["min"])} {t(lang, "unit")}</span></div>
<div class="tile bad"><span class="k">{t(lang, "max")}</span><span class="v">{labels[s["max_i"]].split("–")[0]}</span><span class="u">{i18n.fmt_price(lang, s["max"])} {t(lang, "unit")}</span></div>
</div>"""

    def appliances(self, lang, d):
        prices = self.prices(d)
        labels = svg.hour_labels(self.records[d]["hours"])
        rows = []
        for a in self.cfg["appliances"]:
            plan = windows.plan_appliance(prices, a["hours"], a["kwh"])
            if not plan:
                continue
            start = labels[plan["start"]].split("–")[0]
            end = labels[plan["start"] + a["hours"] - 1].split("–")[1]
            rows.append(
                f'<li><span class="what">{t(lang, "appliance_" + a["id"])} '
                f'<small>({a["hours"]} h, ~{i18n.fmt_num(lang, a["kwh"], 1)} kWh)</small></span>'
                f'<span class="when">{start}–{end}</span>'
                f'<span class="money">{t(lang, "cost", x=i18n.fmt_eur(lang, plan["cost"]))} · '
                f'<strong>{t(lang, "saving", x=i18n.fmt_eur(lang, plan["saving"]))}</strong></span></li>')
        return (f'<h3>{t(lang, "best_for")}</h3><ul class="plan">{"".join(rows)}</ul>'
                f'<p class="note">{t(lang, "best_for_note")}</p>')

    def table(self, lang, d):
        hours = self.records[d]["hours"]
        labels = svg.hour_labels(hours)
        tiers = windows.tiers(self.prices(d))
        rows = []
        for h, label, tier in zip(hours, labels, tiers):
            s = int(tz.parse_iso(h["t"]).timestamp() * 1000)
            price = i18n.fmt_price(lang, h["p"])
            rows.append(f'<tr data-s="{s}" data-p="{price}" data-l="{esc(label)} · {t(lang, f"tier_{tier}")}">'
                        f'<td>{label}</td><td class="num">{price}</td>'
                        f'<td><span class="tier t{tier}">{t(lang, f"tier_{tier}")}</span></td></tr>')
        return (f'<details class="table"><summary>{t(lang, "table_show")}</summary><table>'
                f'<thead><tr><th>{t(lang, "table_hour")}</th><th class="num">{t(lang, "table_price")}</th>'
                f'<th>{t(lang, "table_level")}</th></tr></thead><tbody>{"".join(rows)}</tbody></table></details>')

    def day_block(self, lang, d, uid):
        prices = self.prices(d)
        best = windows.cheapest(prices, WINDOW)
        chart = svg.price_bars(lang, self.records[d]["hours"], (best[0], WINDOW) if best else None, uid)
        return (f'{self.stat_tiles(lang, d)}<figure class="fig">{chart}</figure>'
                f'{self.appliances(lang, d)}{self.table(lang, d)}')

    def mix_block(self, lang, d):
        mix = self.mixes.get(d)
        if not mix:
            return ""
        text = t(lang, "mix_text", date=i18n.fmt_date(lang, d, weekday=False),
                 pct=i18n.fmt_pct(lang, mix["renewable_pct"]),
                 co2=mix.get("co2_g_kwh", "–"))
        rows = []
        for key, pct in sorted(mix.get("sources", {}).items(), key=lambda kv: -kv[1]):
            if pct < 0.5:
                continue
            ren = "ren" if key in ("wind", "solar", "hydro", "other_renewable") else "fos"
            rows.append(f'<li class="{ren}"><span class="name">{t(lang, "src_" + key)}</span>'
                        f'<span class="track"><span style="width:{min(100, pct):.1f}%"></span></span>'
                        f'<span class="pct">{i18n.fmt_pct(lang, pct)}</span></li>')
        legend = f'<p class="mix-legend"><span class="sw ren"></span>{t(lang, "renewable")}</p>'
        return (f'<section class="mix"><h2>{t(lang, "mix_title")}</h2><p>{text}</p>'
                f'<h3>{t(lang, "mix_sources")}</h3>{legend}<ul class="bars">{"".join(rows)}</ul></section>')

    def change(self, lang, d, other, key):
        if other not in self.records:
            return ""
        a = windows.summary(self.prices(d))["avg"]
        b = windows.summary(self.prices(other))["avg"]
        if not b:
            return ""
        pct = (a - b) / abs(b) * 100
        word = t(lang, "more" if pct >= 0 else "less")
        return f"<li>{t(lang, key, x=f'{i18n.fmt_pct(lang, abs(pct))} {word}')}</li>"

    def recent_table(self, lang, upto, n=7):
        days = [d for d in self.days if d <= upto][-n:][::-1]
        rows = []
        for d in days:
            s = windows.summary(self.prices(d))
            mix = self.mixes.get(d)
            rows.append(f'<tr><td><a href="{self.href(self.path(lang, "day", d))}">'
                        f'{i18n.fmt_date(lang, d, year=False)}</a></td>'
                        f'<td class="num">{i18n.fmt_price(lang, s["avg"])}</td>'
                        f'<td class="num">{i18n.fmt_price(lang, s["min"])}</td>'
                        f'<td class="num">{i18n.fmt_pct(lang, mix["renewable_pct"], 0) if mix else "–"}</td></tr>')
        return (f'<table class="recent"><thead><tr><th>{t(lang, "day")}</th><th class="num">{t(lang, "avg")}</th>'
                f'<th class="num">{t(lang, "min")}</th><th class="num">{t(lang, "renewable")}</th></tr></thead>'
                f'<tbody>{"".join(rows)}</tbody></table>')

    # ---------- páginas ----------
    def home(self, lang):
        today = self.now.date()
        shown = today if today in self.records else max((d for d in self.days if d <= today), default=None)
        tomorrow = today + timedelta(days=1)
        body = [f'<h1>{t(lang, "home_title")}</h1><p class="lede">{t(lang, "tagline")}</p>']
        if shown:
            label = t(lang, "today") if shown == today else ""
            body.append(f'<p class="nowbox" data-now hidden><span class="k">{t(lang, "now")}</span> '
                        f'<span class="v"></span> {t(lang, "unit")} <span class="l"></span></p>')
            body.append(f'<section><h2>{label + " · " if label else ""}{i18n.fmt_date(lang, shown)}</h2>'
                        f'{self.day_block(lang, shown, "today")}'
                        f'<p><a href="{self.href(self.path(lang, "day", shown))}">{t(lang, "see_day")} →</a></p></section>')
        body.append(f'<section><h2>{t(lang, "tomorrow")} · {i18n.fmt_date(lang, tomorrow)}</h2>')
        if tomorrow in self.records:
            body.append(self.day_block(lang, tomorrow, "tomorrow"))
        else:
            body.append(f'<p class="pending">{t(lang, "tomorrow_pending")}</p>')
        body.append("</section>")
        body.append(f'<aside class="tip">🌱 {t(lang, "green_tip")}</aside>')
        mix_days = [d for d in self.mixes if d <= today]
        if mix_days:
            body.append(self.mix_block(lang, max(mix_days)))
        if shown:
            body.append(f'<section><h2>{t(lang, "last_days")}</h2>{self.recent_table(lang, shown)}'
                        f'<p><a href="{self.href(self.path(lang, "archive"))}">{t(lang, "see_archive")} →</a></p></section>')
        body.append(f'<section class="about-pvpc"><p>{t(lang, "what_pvpc")}</p></section>')
        ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": self.name,
               "url": self.absolute(self.path(lang, "home")), "inLanguage": lang,
               "description": t(lang, "home_desc")}]
        title = f'{t(lang, "home_title")} · {self.name}'
        return self.layout(lang, "home", None, title, t(lang, "home_desc"), "\n".join(body), ld)

    def breadcrumbs(self, lang, d, kind):
        items = [(t(lang, "home"), self.path(lang, "home")),
                 (t(lang, "archive_title"), self.path(lang, "archive"))]
        if kind in ("month", "day"):
            items.append((i18n.fmt_month(lang, d.year, d.month), self.path(lang, "month", d)))
        if kind == "day":
            items.append((i18n.fmt_date(lang, d, weekday=False), self.path(lang, "day", d)))
        html = " › ".join(f'<a href="{self.href(p)}">{esc(n)}</a>' for n, p in items[:-1])
        html = f'<nav class="crumbs" aria-label="breadcrumb">{html} › <span>{esc(items[-1][0])}</span></nav>'
        ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": self.absolute(p)}
            for i, (n, p) in enumerate(items)]}
        return html, ld

    def day_page(self, lang, d):
        s = windows.summary(self.prices(d))
        labels = svg.hour_labels(self.records[d]["hours"])
        nice = i18n.fmt_date(lang, d)
        title = t(lang, "day_title", date=nice)
        desc = t(lang, "day_desc", date=i18n.fmt_date(lang, d, weekday=False),
                 avg=i18n.fmt_price(lang, s["avg"]), cheap=labels[s["min_i"]], dear=labels[s["max_i"]])
        crumbs, crumbs_ld = self.breadcrumbs(lang, d, "day")
        changes = (self.change(lang, d, d - timedelta(days=1), "vs_prev")
                   + self.change(lang, d, d - timedelta(days=7), "vs_week"))
        year_ago = d.replace(year=d.year - 1) if not (d.month == 2 and d.day == 29) else None
        if year_ago in self.records:
            changes += "<li>" + t(lang, "vs_year", x=i18n.fmt_price(
                lang, windows.summary(self.prices(year_ago))["avg"])) + "</li>"
        idx = self.days.index(d)
        nav = []
        if idx > 0:
            nav.append(f'<a rel="prev" href="{self.href(self.path(lang, "day", self.days[idx - 1]))}">← {t(lang, "prev_day")}</a>')
        if idx + 1 < len(self.days):
            nav.append(f'<a rel="next" href="{self.href(self.path(lang, "day", self.days[idx + 1]))}">{t(lang, "next_day")} →</a>')
        body = (f'{crumbs}<h1>{esc(title)}</h1>{self.day_block(lang, d, "day")}'
                f'{"<ul class=changes>" + changes + "</ul>" if changes else ""}'
                f'<aside class="tip">🌱 {t(lang, "green_tip")}</aside>{self.mix_block(lang, d)}'
                f'<section class="about-pvpc"><p>{t(lang, "what_pvpc")}</p></section>'
                f'<nav class="pager">{"".join(nav)}</nav>')
        dataset = {"@context": "https://schema.org", "@type": "Dataset", "name": title, "description": desc,
                   "temporalCoverage": d.isoformat(), "inLanguage": lang,
                   "creator": {"@type": "Organization", "name": self.name, "url": self.absolute("/")},
                   "isBasedOn": "https://www.ree.es/",
                   "distribution": {"@type": "DataDownload", "encodingFormat": "application/json",
                                    "contentUrl": self.absolute(f"/api/v1/days/{d.isoformat()}.json")}}
        return self.layout(lang, "day", d, f"{title} · {self.name}", desc, body, [dataset, crumbs_ld])

    def months(self):
        out = {}
        for d in self.days:
            out.setdefault((d.year, d.month), []).append(d)
        return out

    def month_page(self, lang, ym, days):
        first = date(ym[0], ym[1], 1)
        name = i18n.fmt_month(lang, *ym)
        title = t(lang, "month_title", month=name)
        crumbs, crumbs_ld = self.breadcrumbs(lang, first, "month")
        heat = svg.heatmap(lang, [(d, self.records[d]["hours"]) for d in days],
                           lambda d: self.href(self.path(lang, "day", d)))
        rows = []
        for d in days:
            s = windows.summary(self.prices(d))
            mix = self.mixes.get(d)
            rows.append(f'<tr><td><a href="{self.href(self.path(lang, "day", d))}">{i18n.fmt_date(lang, d, year=False)}</a></td>'
                        f'<td class="num">{i18n.fmt_price(lang, s["avg"])}</td><td class="num">{i18n.fmt_price(lang, s["min"])}</td>'
                        f'<td class="num">{i18n.fmt_price(lang, s["max"])}</td>'
                        f'<td class="num">{i18n.fmt_pct(lang, mix["renewable_pct"], 0) if mix else "–"}</td></tr>')
        keys = sorted(self.months())
        i = keys.index(ym)
        nav = []
        if i > 0:
            nav.append(f'<a rel="prev" href="{self.href(self.path(lang, "month", date(*keys[i - 1], 1)))}">← {t(lang, "prev_month")}</a>')
        if i + 1 < len(keys):
            nav.append(f'<a rel="next" href="{self.href(self.path(lang, "month", date(*keys[i + 1], 1)))}">{t(lang, "next_month")} →</a>')
        body = (f'{crumbs}<h1>{esc(title)}</h1><h2>{t(lang, "heatmap_title")}</h2><figure class="fig scroll">{heat}</figure>'
                f'<h2>{t(lang, "month_days")}</h2><table class="recent"><thead><tr><th>{t(lang, "day")}</th>'
                f'<th class="num">{t(lang, "avg")}</th><th class="num">{t(lang, "min")}</th>'
                f'<th class="num">{t(lang, "max")}</th><th class="num">{t(lang, "renewable")}</th></tr></thead>'
                f'<tbody>{"".join(rows)}</tbody></table><nav class="pager">{"".join(nav)}</nav>')
        return self.layout(lang, "month", first, f"{title} · {self.name}",
                           t(lang, "month_desc", month=name), body, [crumbs_ld])

    def archive_page(self, lang):
        by_year = {}
        for (y, m), days in sorted(self.months().items(), reverse=True):
            avg = sum(windows.summary(self.prices(d))["avg"] for d in days) / len(days)
            by_year.setdefault(y, []).append(
                f'<li><a href="{self.href(self.path(lang, "month", date(y, m, 1)))}">{i18n.fmt_month(lang, y, m)}</a>'
                f' <span class="muted">{t(lang, "avg").lower()} {i18n.fmt_price(lang, avg)} {t(lang, "unit")}</span></li>')
        body = f'<h1>{t(lang, "archive_title")}</h1>' + "".join(
            f'<h2>{y}</h2><ul class="months">{"".join(items)}</ul>' for y, items in by_year.items())
        return self.layout(lang, "archive", None, f'{t(lang, "archive_title")} · {self.name}',
                           t(lang, "archive_desc"), body)

    def text_page(self, lang, kind):
        repo = self.cfg.get("repo_url") or "https://github.com/"
        owner = self.cfg.get("owner") or {}
        if owner.get("name"):
            owner_html = esc(owner["name"]) + (f" · NIF {esc(owner['nif'])}" if owner.get("nif") else "") + (
                f' · <a href="mailto:{esc(owner["email"])}">{esc(owner["email"])}</a>' if owner.get("email") else "")
        else:
            owner_html = t(lang, "owner_missing", repo=repo)
        body = t(lang, f"{kind}_body", site=esc(self.name), repo=repo, owner=owner_html,
                 api=self.absolute("/api/v1/latest.json"),
                 widget=self.absolute(self.path(lang, "widget")), widget_title=t(lang, "widget_title"))
        return self.layout(lang, kind, None, f'{t(lang, kind)} · {self.name}', t(lang, "home_desc"),
                           f'<article class="prose"><h1>{t(lang, kind)}</h1>{body}</article>')

    def widget_page(self, lang):
        today = self.now.date()
        d = today if today in self.records else (self.days[-1] if self.days else None)
        if not d:
            return self.layout(lang, "widget", None, t(lang, "widget_title"), "", "", noindex=True, bare=True)
        hours = self.records[d]["hours"]
        labels = svg.hour_labels(hours)
        order = sorted(range(len(hours)), key=lambda i: (hours[i]["p"], i))[:6]
        rows = "".join(f'<tr data-s="{int(tz.parse_iso(hours[i]["t"]).timestamp() * 1000)}"><td>{labels[i]}</td>'
                       f'<td class="num">{i18n.fmt_price(lang, hours[i]["p"])}</td></tr>' for i in sorted(order))
        body = (f'<p class="wtitle">{t(lang, "widget_title")}<br><small>{i18n.fmt_date(lang, d)}</small></p>'
                f'<table class="recent"><tbody>{rows}</tbody></table>'
                f'<p><a href="{self.absolute(self.path(lang, "home"))}" target="_blank" rel="noopener">'
                f'{t(lang, "widget_more")} · {esc(self.name)}</a></p>')
        return self.layout(lang, "widget", None, t(lang, "widget_title"), "", body, noindex=True, bare=True)

    def root_page(self):
        links = "".join(f'<li><a href="{self.href(self.path(lg, "home"))}" hreflang="{lg}" lang="{lg}">'
                        f'{t(lg, "lang_name")} — {t(lg, "home_title")}</a></li>' for lg in LANGS)
        alts = "".join(f'<link rel="alternate" hreflang="{lg}" href="{self.absolute(self.path(lg, "home"))}">'
                       for lg in LANGS)
        return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(self.name)} · {esc(t("es", "home_title"))}</title>
<meta name="description" content="{esc(t('es', 'home_desc'))}">
<link rel="canonical" href="{self.absolute('/')}">
{alts}<link rel="alternate" hreflang="x-default" href="{self.absolute('/')}">
<link rel="icon" href="{self.href('/static/favicon.svg')}" type="image/svg+xml">
<link rel="stylesheet" href="{self.href('/static/style.css')}">
<script>
(function(){{var m={{ca:"ca",es:"es",gl:"es",eu:"es",en:"en"}};var l=(navigator.languages||[navigator.language||"es"]);
for(var i=0;i<l.length;i++){{var k=m[(l[i]||"").slice(0,2).toLowerCase()];if(k){{location.replace("{self.prefix}/"+k+"/");return;}}}}
location.replace("{self.prefix}/es/");}})();
</script>
</head>
<body><main class="wrap"><h1>{esc(self.name)}</h1><p>{t("es", "choose")} · {t("ca", "choose")} · {t("en", "choose")}</p><ul class="months">{links}</ul></main></body>
</html>
"""

    def not_found(self):
        body = "".join(f'<p lang="{lg}"><strong>{t(lg, "notfound_title")}.</strong> '
                       f'<a href="{self.href(self.path(lg, "home"))}">{t(lg, "notfound_text")}</a></p>' for lg in LANGS)
        return self.layout("es", "home", None, t("es", "notfound_title"), "", body, noindex=True)

    # ---------- datos y SEO ----------
    def day_api(self, d):
        rec = self.records[d]
        prices = self.prices(d)
        labels = svg.hour_labels(rec["hours"])
        best = {}
        for n in (1, 2, 3, 4, 6):
            w = windows.cheapest(prices, n)
            if w:
                best[str(n)] = {"start": rec["hours"][w[0]]["t"], "label": f'{labels[w[0]].split("–")[0]}–{labels[w[0] + n - 1].split("–")[1]}',
                                "avg_eur_kwh": round(w[1] / 1000, 5)}
        s = windows.summary(prices)
        return {"date": d.isoformat(), "unit": "EUR/kWh",
                "hours": [{"start": h["t"], "label": lb, "price": round(h["p"] / 1000, 5)}
                          for h, lb in zip(rec["hours"], labels)],
                "avg": round(s["avg"] / 1000, 5), "min": round(s["min"] / 1000, 5), "max": round(s["max"] / 1000, 5),
                "cheapest": best, "mix": self.mixes.get(d)}

    def latest_api(self):
        today = self.now.date()
        mix_days = [d for d in self.mixes if d <= today]
        return {"source": "Red Eléctrica (REE): apidatos.ree.es / esios.ree.es — PVPC 2.0TD",
                "attribution": "Datos de Red Eléctrica (REE), uso informativo",
                "site": self.absolute("/"), "generated": self.now.isoformat(timespec="minutes"),
                "today": self.day_api(today) if today in self.records else None,
                "tomorrow": self.day_api(today + timedelta(days=1)) if today + timedelta(days=1) in self.records else None,
                "latest_mix": ({"date": max(mix_days).isoformat(), **self.mixes[max(mix_days)]} if mix_days else None)}

    def feed(self, lang):
        items = []
        for d in self.days[-14:][::-1]:
            s = windows.summary(self.prices(d))
            labels = svg.hour_labels(self.records[d]["hours"])
            title = t(lang, "feed_item", date=i18n.fmt_date(lang, d), h=labels[s["min_i"]],
                      p=i18n.fmt_price(lang, s["min"]))
            url = self.absolute(self.path(lang, "day", d))
            pub = tz.local_midnight(d).strftime("%a, %d %b %Y %H:%M:%S %z")
            items.append(f"<item><title>{esc(title)}</title><link>{url}</link><guid>{url}</guid>"
                         f"<pubDate>{pub}</pubDate></item>")
        return (f'<?xml version="1.0" encoding="utf-8"?>\n<rss version="2.0"><channel>'
                f'<title>{esc(self.name)} · {esc(t(lang, "feed_title"))}</title>'
                f'<link>{self.absolute(self.path(lang, "home"))}</link>'
                f'<description>{esc(t(lang, "home_desc"))}</description><language>{lang}</language>'
                f'{"".join(items)}</channel></rss>\n')

    def sitemap(self, entries):
        urls = []
        for kind, d, lastmod in entries:
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{lg}" href="{self.absolute(self.path(lg, kind, d))}"/>'
                           for lg in LANGS)
            for lg in LANGS:
                urls.append(f"<url><loc>{self.absolute(self.path(lg, kind, d))}</loc>"
                            f"{f'<lastmod>{lastmod}</lastmod>' if lastmod else ''}{alts}</url>")
        return ('<?xml version="1.0" encoding="utf-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                'xmlns:xhtml="http://www.w3.org/1999/xhtml">' + "".join(urls) + "</urlset>\n")

    # ---------- todo ----------
    def build(self):
        if self.out.exists():
            shutil.rmtree(self.out)
        self.out.mkdir(parents=True)
        shutil.copytree(ROOT / "static", self.out / "static")
        today = self.now.date().isoformat()
        entries = [("home", None, today), ("archive", None, today)]
        for lang in LANGS:
            self.write(self.path(lang, "home"), self.home(lang))
            self.write(self.path(lang, "archive"), self.archive_page(lang))
            self.write(self.path(lang, "widget"), self.widget_page(lang))
            self.write(self.path(lang, "feed"), self.feed(lang))
            for kind in ("about", "legal", "privacy"):
                self.write(self.path(lang, kind), self.text_page(lang, kind))
            for d in self.days:
                self.write(self.path(lang, "day", d), self.day_page(lang, d))
            for ym, days in self.months().items():
                self.write(self.path(lang, "month", date(*ym, 1)), self.month_page(lang, ym, days))
        entries += [("about", None, None), ("legal", None, None), ("privacy", None, None)]
        entries += [("month", date(*ym, 1), max(days).isoformat()) for ym, days in self.months().items()]
        entries += [("day", d, d.isoformat()) for d in self.days]
        for d in self.days:
            self.write(f"/api/v1/days/{d.isoformat()}.json", json.dumps(self.day_api(d), ensure_ascii=False))
        self.write("/api/v1/latest.json", json.dumps(self.latest_api(), ensure_ascii=False, indent=1))
        self.write("/", self.root_page())
        self.write("/404.html", self.not_found())
        self.write("/sitemap.xml", self.sitemap(entries))
        self.write("/robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {self.absolute('/sitemap.xml')}\n")
        self.write("/.nojekyll", "")
        return self.out
