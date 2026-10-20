"""Generate a realistic (simulated) acquisition funnel for a B2B online business account.

Funnel: website visit -> sign-up started -> sign-up completed -> account opened
(identity checks passed) -> activated (first transaction within 30 days).

Each channel has its own volume, conversion rates and monthly spend, so the
analysis has real differences to find. Output: data/visitors.csv, data/funnel_events.csv,
data/channel_spend.csv. The random seed is fixed, so results are reproducible.
"""

import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path

random.seed(42)
OUT = Path(__file__).parent
MONTHS = [date(2026, m, 1) for m in range(5, 11)]  # May to October 2026

# channel: monthly visitors, step conversion rates, monthly spend in euros
CHANNELS = {
    "Paid Search":  {"visitors": 9000, "rates": [0.14, 0.62, 0.70, 0.55], "spend": 42000},
    "Paid Social":  {"visitors": 12000, "rates": [0.09, 0.48, 0.58, 0.38], "spend": 36000},
    "SEO":          {"visitors": 15000, "rates": [0.07, 0.60, 0.72, 0.58], "spend": 9000},
    "Partnerships": {"visitors": 2500, "rates": [0.20, 0.70, 0.80, 0.66], "spend": 15000},
    "Referral":     {"visitors": 1800, "rates": [0.26, 0.74, 0.82, 0.70], "spend": 6000},
}
STEPS = ["visit", "signup_started", "signup_completed", "account_opened", "activated"]
DEVICES = [("desktop", 0.55), ("mobile", 0.45)]


def pick(options):
    r, total = random.random(), 0
    for value, weight in options:
        total += weight
        if r <= total:
            return value
    return options[-1][0]


def main():
    visitors, events, spend = [], [], []
    visitor_id = 0
    for month_index, month in enumerate(MONTHS):
        for channel, cfg in CHANNELS.items():
            # small growth over time, plus a Paid Social creative change in August
            volume = int(cfg["visitors"] * (1 + 0.04 * month_index) * random.uniform(0.92, 1.08))
            rates = list(cfg["rates"])
            if channel == "Paid Social" and month >= date(2026, 8, 1):
                rates[0] *= 1.25  # better landing page: more sign-ups started
            spend.append({"month": month.isoformat(), "channel": channel,
                          "spend_eur": round(cfg["spend"] * (1 + 0.03 * month_index), 2)})

            for _ in range(volume):
                visitor_id += 1
                device = pick(DEVICES)
                ts = datetime.combine(month, datetime.min.time()) + timedelta(
                    days=random.randint(0, 27), hours=random.randint(7, 22), minutes=random.randint(0, 59))
                visitors.append({"visitor_id": visitor_id, "channel": channel, "device": device,
                                 "first_visit_at": ts.isoformat(sep=" ")})
                events.append({"visitor_id": visitor_id, "step": "visit", "event_at": ts.isoformat(sep=" ")})

                for step_index, step in enumerate(STEPS[1:]):
                    rate = rates[step_index]
                    if device == "mobile" and step == "signup_completed":
                        rate *= 0.85  # mobile sign-up form loses more people
                    if random.random() > rate:
                        break
                    ts += timedelta(minutes=random.randint(2, 60) if step_index < 2 else random.randint(600, 30000))
                    events.append({"visitor_id": visitor_id, "step": step, "event_at": ts.isoformat(sep=" ")})

    for name, rows in [("visitors", visitors), ("funnel_events", events), ("channel_spend", spend)]:
        with open(OUT / f"{name}.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        print(f"{name}.csv: {len(rows)} rows")


if __name__ == "__main__":
    main()
