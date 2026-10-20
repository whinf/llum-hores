import json
import re
import sys
import tempfile
import unittest
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import i18n  # noqa: E402
import ree  # noqa: E402
import tz  # noqa: E402
from render import Site  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures"


def fixture(name):
    return json.loads((FIX / name).read_text(encoding="utf-8"))


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.alternates = [], {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ("href", "src"):
            if a.get(key):
                self.links.append(a[key])
        if tag == "link" and a.get("rel") == "alternate" and a.get("hreflang"):
            self.alternates[a["hreflang"]] = a["href"]


class TestI18n(unittest.TestCase):
    def test_same_keys(self):
        keys = set(i18n.STRINGS["es"])
        for lang in i18n.LANGS:
            self.assertEqual(set(i18n.STRINGS[lang]), keys, lang)

    def test_dates(self):
        d = date(2026, 10, 20)
        self.assertEqual(i18n.fmt_date("es", d), "martes, 20 de octubre de 2026")
        self.assertEqual(i18n.fmt_date("ca", d), "dimarts, 20 d'octubre de 2026")
        self.assertEqual(i18n.fmt_date("ca", date(2026, 3, 5), weekday=False), "5 de març de 2026")
        self.assertEqual(i18n.fmt_date("en", d), "Tuesday, 20 October 2026")
        self.assertEqual(i18n.fmt_price("es", 208.94), "0,2089")
        self.assertEqual(i18n.fmt_eur("en", 1.5), "€1.50")


class TestSite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        records = {}
        for name, d in (("ree_prices_2026-10-20.json", date(2026, 10, 20)),
                        ("ree_prices_2025-10-26.json", date(2025, 10, 26)),
                        ("ree_prices_2026-03-29.json", date(2026, 3, 29))):
            records[d] = {"date": d.isoformat(), "hours": ree.parse_pvpc(fixture(name), d)[d],
                          "prices_fetched": "2026-10-19T20:47:00+02:00"}
        mix = ree.parse_mix(fixture("ree_mix_2026-10-19.json"), fixture("ree_structure_2026-10-19.json"),
                            fixture("ree_co2_2026-10-19.json"))
        records[date(2026, 10, 19)] = {"date": "2026-10-19", "mix": mix[date(2026, 10, 19)]}
        cfg = json.loads((Path(__file__).resolve().parents[1] / "config.json").read_text(encoding="utf-8"))
        cfg["site_url"] = "https://example.github.io/llum-hores"
        cls.tmp = tempfile.TemporaryDirectory()
        now = tz.to_madrid(tz.parse_iso("2026-10-20T19:00:00+02:00"))
        cls.out = Site(cfg, records, cls.tmp.name, now).build()

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def parse(self, path):
        p = Links()
        p.feed(path.read_text(encoding="utf-8"))
        return p

    def resolve(self, url):
        prefix = "/llum-hores"
        url = url.split("#")[0]
        if url.startswith("https://example.github.io"):
            url = url[len("https://example.github.io"):]
        if not url.startswith(prefix + "/"):
            return None
        rel = url[len(prefix) + 1:]
        target = self.out / rel
        return target / "index.html" if url.endswith("/") else target

    def test_internal_links_exist(self):
        broken = []
        for page in self.out.rglob("*.html"):
            for link in self.parse(page).links:
                target = self.resolve(link)
                if target is not None and not target.exists():
                    broken.append(f"{page.relative_to(self.out)} -> {link}")
        self.assertEqual(broken, [])

    def test_hreflang_reciprocal(self):
        page = self.out / "ca/preu-llum/2025/10/26/index.html"
        alts = self.parse(page).alternates
        self.assertEqual(set(alts), {"es", "ca", "en", "x-default"})
        for lang in i18n.LANGS:
            other = self.parse(self.resolve(alts[lang])).alternates
            self.assertEqual(other[lang], alts[lang])
            self.assertEqual(other["ca"], alts["ca"])

    def test_api_and_seo_files(self):
        latest = json.loads((self.out / "api/v1/latest.json").read_text(encoding="utf-8"))
        self.assertEqual(latest["today"]["date"], "2026-10-20")
        self.assertIsNone(latest["tomorrow"])
        self.assertEqual(latest["today"]["cheapest"]["3"]["label"], "14:00–17:00")
        self.assertEqual(latest["latest_mix"]["date"], "2026-10-19")
        sitemap = (self.out / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("https://example.github.io/llum-hores/en/electricity-price/2026/03/29/", sitemap)
        self.assertIn("Sitemap: https://example.github.io/llum-hores/sitemap.xml",
                      (self.out / "robots.txt").read_text(encoding="utf-8"))
        self.assertTrue((self.out / "404.html").exists())

    def test_pages_are_complete(self):
        home = (self.out / "es/index.html").read_text(encoding="utf-8")
        self.assertIn("Los precios de mañana se publican", home)
        self.assertIn("43,3 %", home)
        self.assertEqual(len(re.findall(r'class="bar cheap"', home)), 3)
        spring = (self.out / "es/precio-luz/2026/03/29/index.html").read_text(encoding="utf-8")
        self.assertEqual(spring.count('<g class="bar'), 23)


if __name__ == "__main__":
    unittest.main()
