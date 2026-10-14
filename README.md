# No-Show Shield

![python](https://img.shields.io/badge/python-3.8%2B-blue) ![deps](https://img.shields.io/badge/dependencies-zero-brightgreen) ![license](https://img.shields.io/badge/license-MIT-lightgrey)

**Turn your appointment list into a no-show risk report and a reminder plan - in one command.** Built for clinics, salons, HVAC/roofing estimate bookings and real-estate viewings.

## Quickstart (under 2 minutes, offline)

```bash
git clone https://github.com/Waqas-Ai-Engineer/no-show-shield && cd no-show-shield
python -m noshow --avg-value 120
python -m unittest discover -s tests
```

Pass your own CSV: `python -m noshow my_appointments.csv`. Columns: `client, appointment, booked_at, past_visits, past_no_shows, confirmed, deposit_paid` (dates as `YYYY-MM-DD HH:MM`).

## What it does
- Transparent rule-based score (0-100) with the reasons listed per appointment
- Suggests a reminder strategy per risk tier (SMS / call / waitlist backfill)
- Shows revenue exposed by high-risk slots when you pass `--avg-value`

The weights are a simple heuristic you can tune in `noshow/core.py` - not a trained model, and the sample data is invented.

## Hire me / Need this built?
**Muhammad Waqas - AI Agents & Business Automation.** I build WhatsApp/SMS reminder bots, CRM automations and AI receptionists for service businesses. Contact me via my GitHub profile: [@Waqas-Ai-Engineer](https://github.com/Waqas-Ai-Engineer).
