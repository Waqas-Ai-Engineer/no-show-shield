import unittest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from noshow.core import score, analyze

BASE = {"appointment": "2026-10-20 10:00", "booked_at": "2026-10-18 10:00",
        "past_visits": "5", "past_no_shows": "0"}

class T(unittest.TestCase):
    def test_baseline(self): self.assertEqual(score(BASE)[0], 10)
    def test_repeat_offender(self):
        self.assertEqual(score({**BASE, "past_no_shows": "2"})[0], 50)
    def test_confirmed_lowers(self):
        self.assertEqual(score({**BASE, "confirmed": "yes"})[0], 0)
    def test_first_time_far(self):
        self.assertEqual(score({**BASE, "past_visits": "0", "booked_at": "2026-09-01 10:00"})[0], 40)
    def test_sorted_and_exposure(self):
        txt = open(os.path.join(os.path.dirname(__file__), "..", "examples", "appointments.csv")).read()
        r = analyze(txt, 100)
        self.assertEqual([x["score"] for x in r["rows"]], sorted([x["score"] for x in r["rows"]], reverse=True))
        self.assertEqual(r["at_risk_value"], r["high"] * 100)
unittest.main() if __name__ == "__main__" else None
