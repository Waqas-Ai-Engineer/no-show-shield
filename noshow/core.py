"""Score upcoming appointments for no-show risk and build a reminder plan."""
import csv, io
from datetime import datetime

def _dt(s):
    return datetime.strptime(s.strip(), "%Y-%m-%d %H:%M")

def _i(v):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return 0

def score(row):
    """Return (score 0-100, reasons). Transparent rule-based heuristic."""
    s, why = 10, []
    prior_ns, prior_total = _i(row.get("past_no_shows")), _i(row.get("past_visits"))
    if prior_ns:
        add = min(40, prior_ns * 20); s += add; why.append(f"{prior_ns} past no-show(s) (+{add})")
    if prior_total == 0:
        s += 15; why.append("first-time client (+15)")
    lead = (_dt(row["appointment"]) - _dt(row["booked_at"])).days
    if lead >= 14:
        s += 15; why.append(f"booked {lead} days ahead (+15)")
    if (row.get("confirmed") or "").strip().lower() in ("yes", "y", "true", "1"):
        s -= 20; why.append("already confirmed (-20)")
    if (row.get("deposit_paid") or "").strip().lower() in ("yes", "y", "true", "1"):
        s -= 15; why.append("deposit paid (-15)")
    if _dt(row["appointment"]).weekday() == 0:
        s += 5; why.append("Monday slot (+5)")
    return max(0, min(100, s)), why

def plan(s):
    if s >= 60: return "Call + SMS 48h before, SMS 2h before; offer waitlist backfill"
    if s >= 35: return "SMS 24h before asking for reply-to-confirm"
    return "Standard single reminder 24h before"

def analyze(text, avg_value=0.0):
    rows = []
    for r in csv.DictReader(io.StringIO(text)):
        sc, why = score(r)
        rows.append({"client": r["client"], "appointment": r["appointment"],
                     "score": sc, "reasons": why, "action": plan(sc)})
    rows.sort(key=lambda x: -x["score"])
    high = [r for r in rows if r["score"] >= 60]
    return {"rows": rows, "high": len(high), "at_risk_value": round(len(high) * avg_value, 2)}

def render(res, avg_value=0.0):
    out = ["NO-SHOW SHIELD - upcoming appointment risk", "=" * 44]
    for r in res["rows"]:
        out.append(f"[{r['score']:3d}] {r['client']:<16} {r['appointment']}  -> {r['action']}")
        for w in r["reasons"]:
            out.append(f"        - {w}")
    out.append("")
    out.append(f"High-risk appointments: {res['high']}")
    if avg_value:
        out.append(f"Revenue exposed if all high-risk no-show (at {avg_value:g} each): {res['at_risk_value']:g}")
    out.append("Scores are a heuristic, not a prediction; tune weights in core.py.")
    return "\n".join(out)
