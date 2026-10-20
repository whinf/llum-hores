import json
import sys
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import ree  # noqa: E402
import tz  # noqa: E402
import windows  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures"


def fixture(name):
    return json.loads((FIX / name).read_text(encoding="utf-8"))


class TestTz(unittest.TestCase):
    def test_dst_bounds(self):
        self.assertEqual(tz.dst_bounds(2026), (
            datetime(2026, 3, 29, 1, tzinfo=tz.UTC), datetime(2026, 10, 25, 1, tzinfo=tz.UTC)))
        self.assertEqual(tz.dst_bounds(2025)[1], datetime(2025, 10, 26, 1, tzinfo=tz.UTC))

    def test_hours_per_day(self):
        self.assertEqual(len(tz.day_hours(date(2026, 10, 20))), 24)
        self.assertEqual(len(tz.day_hours(date(2026, 3, 29))), 23)
        self.assertEqual(len(tz.day_hours(date(2025, 10, 26))), 25)
        self.assertEqual(len(tz.day_hours(date(2026, 12, 31))), 24)

    def test_offsets(self):
        self.assertEqual(tz.local_midnight(date(2026, 7, 1)).utcoffset(), timedelta(hours=2))
        self.assertEqual(tz.local_midnight(date(2026, 1, 1)).utcoffset(), timedelta(hours=1))
        fall = tz.day_hours(date(2025, 10, 26))
        self.assertEqual([h.strftime("%H%z") for h in fall[2:4]], ["02+0200", "02+0100"])


class TestWindows(unittest.TestCase):
    def test_cheapest_and_ties(self):
        p = [5, 1, 1, 5, 1, 1, 9]
        self.assertEqual(windows.cheapest(p, 2), (1, 1.0))
        self.assertEqual(windows.cheapest(p, 1), (1, 1.0))
        self.assertEqual(windows.priciest(p, 1), (6, 9.0))
        self.assertIsNone(windows.cheapest(p, 8))

    def test_negative_prices(self):
        p = [10, -5, -3, 4]
        self.assertEqual(windows.cheapest(p, 2), (1, -4.0))
        s = windows.summary(p)
        self.assertEqual((s["min"], s["min_i"], s["max_i"]), (-5, 1, 0))

    def test_tiers(self):
        t = windows.tiers(list(range(24)))
        self.assertEqual(t.count(0), 8)
        self.assertEqual(t[0], 0)
        self.assertEqual(t[23], 2)

    def test_plan_appliance(self):
        plan = windows.plan_appliance([100, 200, 300, 100, 100], 2, 2)
        self.assertEqual(plan["start"], 3)
        self.assertAlmostEqual(plan["cost"], 0.2)
        self.assertAlmostEqual(plan["saving"], 0.3)


class TestParse(unittest.TestCase):
    def test_pvpc_normal_day(self):
        d = date(2026, 10, 20)
        hours = ree.parse_pvpc(fixture("ree_prices_2026-10-20.json"), d)[d]
        self.assertEqual(len(hours), 24)
        self.assertEqual(hours[0], {"t": "2026-10-20T00:00:00+02:00", "p": 208.94})

    def test_pvpc_dst_days(self):
        fall, spring = date(2025, 10, 26), date(2026, 3, 29)
        self.assertEqual(len(ree.parse_pvpc(fixture("ree_prices_2025-10-26.json"), fall)[fall]), 25)
        self.assertEqual(len(ree.parse_pvpc(fixture("ree_prices_2026-03-29.json"), spring)[spring]), 23)

    def test_pvpc_missing_day(self):
        self.assertEqual(ree.parse_pvpc(fixture("ree_prices_2026-10-20.json"), date(2026, 10, 21)), {})
        self.assertEqual(ree.parse_pvpc({"included": []}, date(2026, 10, 21)), {})

    def test_esios_matches_apidatos(self):
        d = date(2026, 10, 20)
        self.assertEqual(ree.parse_esios70(fixture("esios_70_2026-10-20.json"), d),
                         ree.parse_pvpc(fixture("ree_prices_2026-10-20.json"), d)[d])
        self.assertIsNone(ree.parse_esios70({"message": "No values"}, d))

    def test_mix(self):
        d = date(2026, 10, 19)
        mix = ree.parse_mix(fixture("ree_mix_2026-10-19.json"),
                            fixture("ree_structure_2026-10-19.json"),
                            fixture("ree_co2_2026-10-19.json"))[d]
        self.assertEqual(mix["renewable_pct"], 43.3)
        self.assertEqual(mix["co2_g_kwh"], 140)
        self.assertAlmostEqual(mix["sources"]["wind"], 18.1, places=1)
        self.assertAlmostEqual(sum(mix["sources"].values()), 100, delta=0.5)

    def test_month_chunks(self):
        chunks = list(ree.month_chunks(date(2025, 12, 15), date(2026, 2, 3)))
        self.assertEqual(chunks, [(date(2025, 12, 15), date(2025, 12, 31)),
                                  (date(2026, 1, 1), date(2026, 1, 31)),
                                  (date(2026, 2, 1), date(2026, 2, 3))])


if __name__ == "__main__":
    unittest.main()
