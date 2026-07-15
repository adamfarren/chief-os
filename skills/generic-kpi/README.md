# SaaS KPI Dashboard Generator (fictional data)

A one-command generator that builds a **shareable, self-contained SaaS KPI dashboard**
as a brand-new Google Sheet, filled with **entirely fictional** company/customer names and
realistic-but-made-up numbers. Nothing links to any real system, so it's safe to publish
publicly (e.g. on LinkedIn).

It mirrors a real internal operating dashboard — MRR/ARR, usage (MAU/Seats/Active Users),
retention (NRR), cash collection, autopay, and per-customer detail across a 42-month
history — rebranded to a fictional B2B SaaS company.

## What you get
A ~22-tab Google Sheet:
- **📕 How to Use** + **📖 Definitions & Sources** (self-documenting)
- Exec dashboards: Combined Summary, Compare, Revenue Dashboard, MRR & ARR Summary,
  Usage Summary, Churn & New Revenue, Autopay, Revenue → Cash, Collections & A/R,
  Invoiced Volume, Usage History, Over-Min History
- **📥 Paste Data Here** input tab + the data layer (Customers — MRR/ARR,
  Usage — MAU/Seats/Active Users, Minimum MAU, Pricing Engine)

Every dashboard is formula-driven off the data layer, so it stays internally consistent,
and it **resolves the latest/prior month dynamically by date** — so adding a month "just works."

## Requirements
- The **`gws`** Google Workspace CLI, authenticated to a Google account with Sheets/Drive
  scopes (the scripts drive the Google Sheets API through it).
- Python 3.

## Run
```bash
bash scripts/run.sh [seed] [n_customers]
```
- `seed` (optional) — integer; same seed → same data. Omit for a random dataset.
- `n_customers` (optional, default 35).

It creates a **new** sheet each run (never overwrites), enables anyone-with-link viewing,
and prints the shareable URL.

## Monthly use & robustness
See the **"Monthly update (adding a month) & month-add robustness"** section in `SKILL.md`,
and the **📕 How to Use** tab inside any generated sheet, for the monthly-close procedure and
the "double-check when adding a month / new customer" checklist.

## Everything is fictional
All company names, customers, and figures are made up, for illustration only.
