import os
WD=os.environ.get("GKPI_WORKDIR","/tmp/generic-kpi")
#!/usr/bin/env python3
"""Deterministic fake-data generator for the generic SaaS KPI dashboard.
Produces data.json consumed by build.py. Seedable so the skill can regenerate
a fresh-but-realistic dataset each run. NO real customer data anywhere."""
import json, random, sys, datetime as dt

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 42
N_CUST = int(sys.argv[2]) if len(sys.argv) > 2 else 35
rng = random.Random(SEED)

# ---- time axis: 42 months, Jan 2023 .. Jun 2026 (columns E..AT on the data tabs) ----
START = dt.date(2023, 1, 1)
def add_months(d, n):
    m = d.month - 1 + n
    return dt.date(d.year + m // 12, m % 12 + 1, 1)
MONTHS = [add_months(START, i) for i in range(42)]           # 42 first-of-month dates
MONTHS_ISO = [m.isoformat() for m in MONTHS]
def midx(d): return MONTHS.index(d)

# ---- fictional B2B SaaS customer names (obviously sample data) ----
# The default pool riffs on evocative English words (freight, solar, media, etc.) so the
# names read as clearly playful placeholders. Swap for any set that makes sense to you.
NAMES_POOL = [
    "Fearless Freight", "Wonderstruck Technologies", "August Foods", "Invisible String Software",
    "Paper Rings Co.", "Evermore Holdings", "Daylight Solar", "The Alchemy Labs",
    "Cruel Summer Imports", "Midnights Media", "Sweet Nothing Confections", "Willow Health",
    "New Romantics Agency", "Long Live Entertainment", "Vigilante Defense", "Getaway Car Logistics",
    "State of Grace Systems", "Wildest Dreams Labs", "Fortnight Trading", "Mastermind Analytics",
    "Karma Global", "Gold Rush Bank", "Style Retail", "Champagne Ventures",
    "Cardigan Studio", "Reputation Capital", "Bejeweled & Co", "Betty's Kitchen",
    "Begin Again Logistics", "Enchanted Enterprises", "Bad Blood Security", "Cornelia Street Realty",
    "Sparks Industrial", "Anti-Hero Robotics", "Ivy Organics",
]

TIERS = [  # (weight, min_mrr, max_mrr, min_mau, max_mau)
    ("Enterprise", 3, 18000, 60000, 8000, 40000),
    ("Mid-Market", 10, 3000, 15000, 1500, 9000),
    ("SMB",        22, 500, 3000, 200, 1800),
]
def pick_tier():
    r = rng.random() * sum(t[1] for t in TIERS)
    acc = 0
    for t in TIERS:
        acc += t[1]
        if r <= acc: return t
    return TIERS[-1]

customers = []
used = set()
for i in range(N_CUST):
    name = NAMES_POOL[i % len(NAMES_POOL)]
    tier, _, mn, mx, mmn, mmx = pick_tier()
    # start month: weighted toward more recent cohorts
    start_i = int(min(41, max(0, rng.triangular(0, 41, 30))))
    base_mrr = round(rng.uniform(mn, mx), -1)  # round to $10
    # churn: ~18% churn at some point, at least 3 months after start
    churn_i = None
    if rng.random() < 0.18 and start_i < 36:
        churn_i = rng.randint(start_i + 3, min(41, start_i + rng.randint(6, 24)))
    growth = rng.uniform(0.004, 0.020)   # monthly expansion
    disc_pct = rng.choice([0, 0, 0, 0.05, 0.10, 0.15, 0.20]) if rng.random() < 0.45 else 0
    billfreq = "Q" if (tier == "Enterprise" and rng.random() < 0.5) else "M"
    autopay = rng.random() < 0.5
    seats_ratio = rng.uniform(0.01, 0.05)      # seats per MAU
    users_ratio = rng.uniform(0.6, 0.95)       # active users as frac of seats*something

    mrr, mau, seats, users = [], [], [], []
    for k in range(42):
        if k < start_i or (churn_i is not None and k >= churn_i):
            mrr.append(None); mau.append(None); seats.append(None); users.append(None); continue
        months_live = k - start_i
        m = base_mrr * (1 + growth) ** months_live
        m *= rng.uniform(0.98, 1.02)
        mrr.append(round(m, -1))
        cur_mau = max(mmn * 0.5, (mmn + (mmx - mmn) * min(1, months_live / 18)) * rng.uniform(0.7, 1.15))
        mau.append(int(round(cur_mau, -1)))
        s = max(2, int(cur_mau * seats_ratio * rng.uniform(0.85, 1.15)))
        seats.append(s)
        users.append(max(1, int(s * users_ratio * rng.uniform(0.8, 1.0))))

    # commitment floor relative to LATEST usage so ~1/3 of customers sit under it (realistic)
    live_mau = [x for x in mau if x is not None] or [mmn]
    ref_mau = live_mau[-1]
    min_mau = max(100, int(round(ref_mau * rng.uniform(0.60, 1.20), -2)))
    customers.append({
        "name": name, "tier": tier, "start_i": start_i, "churn_i": churn_i,
        "disc_pct": disc_pct, "billfreq": billfreq, "autopay": autopay,
        "min_mau": min_mau, "mrr": mrr, "mau": mau, "seats": seats, "users": users,
        "start_iso": MONTHS_ISO[start_i],
        "churn_iso": (MONTHS_ISO[churn_i] if churn_i is not None else None),
    })

# guarantee a handful of quarterly billers (drives the invoice-timing narrative)
n_q = sum(1 for c in customers if c["billfreq"] == "Q")
if n_q < 4:
    live_big = sorted([c for c in customers if c["churn_i"] is None],
                      key=lambda c: -(c["mrr"][41] or 0))
    for c in live_big[:4 - n_q]:
        c["billfreq"] = "Q"

# sort: live customers first (by start), churned last (a common operating convention)
customers.sort(key=lambda c: (c["churn_i"] is not None, c["start_i"]))

out = {
    "seed": SEED, "company": "ErasCloud AI",
    "months_iso": MONTHS_ISO,
    "n_months": 42,
    "customers": customers,
}
json.dump(out, open(f"{WD}/data.json", "w"), indent=1)
# quick sanity
live = [c for c in customers if c["churn_i"] is None]
last = 41
tot_mrr = sum(c["mrr"][last] or 0 for c in customers)
tot_mau = sum(c["mau"][last] or 0 for c in customers)
print(f"seed={SEED} customers={len(customers)} live={len(live)} churned={len(customers)-len(live)}")
print(f"latest-month (Jun 2026): MRR=${tot_mrr:,.0f}  ARR=${tot_mrr*12:,.0f}  MAU={tot_mau:,}")
print(f"quarterly={sum(1 for c in customers if c['billfreq']=='Q')} autopay={sum(1 for c in customers if c['autopay'])}")
