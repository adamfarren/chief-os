---
name: generic-kpi
description: Generate a shareable, generic SaaS KPI dashboard as a brand-new standalone Google Sheet, filled with FICTIONAL sample data (no real company or customer data, no external links). Produces a fully-formed B2B SaaS operating workbook — MRR/ARR, MAU usage, retention (NRR), cash collection, autopay, A/R aging, and per-customer detail across a 42-month history — safe to publish publicly (e.g. on LinkedIn or in a portfolio). Use when someone says "make a generic KPI dashboard", "create a shareable SaaS KPI dashboard", "generate a sample/demo dashboard with fake data", "regenerate the generic dashboard", or "refresh the LinkedIn dashboard".
---

# Generic SaaS KPI Dashboard (fictional data)

Builds a self-contained, shareable SaaS operating dashboard using **entirely made-up
data** — a fictional B2B SaaS company (default: "ErasCloud AI"), fictional customer names,
and randomly-generated-but-realistic revenue/usage numbers. Nothing links to any real
sheet, customer, or system, so the result is safe to share publicly.

Standard SaaS terminology throughout: **MAU** (Monthly Active Users), **Seats**,
**Active Users**, MRR/ARR, NRR, autopay, A/R aging.

## What it produces

A new Google Sheet with 21 tabs, in this order:

1. **📕 How to Use** — directions so anyone who opens it knows how to read/refresh it
2. **📖 Definitions & Sources** — every metric defined + where each number comes from (live)
3. **📊 Combined Summary** — one-screen exec snapshot (accrual + cash revenue, usage, autopay)
4. **🔍 Compare** — pick any metric + two periods, see the delta (dropdown-driven)
5. **📊 Revenue Dashboard** — headline KPIs, MoM deltas, movers, new/churned lists
6. **📊 MRR & ARR Summary** — monthly revenue cascade (ARR → discounts → net → NRR)
7. **📊 Usage Summary** — MAU, over-minimum, seats, active users
8. **📉 Churn & New Revenue** — MRR bridge (start + new − churn ± expansion = end)
9. **💳 Autopay Collections** — recurring auto-collected, net of discounts
10. **💵 Revenue → Cash** — accrual → invoiced → cash cascade
11. **⏱ Collections & A/R** — A/R aging + on-time collection
12. **💵 Invoiced Volume** — monthly cash-out schedule (quarterly billers land as lumps)
13. **📈 Usage Monthly History** — MAU/Seats/Active Users over time
14. **Over-Min History** — % of customers over their MAU minimum, over time
15–21. **Data layer** — Customers — MRR / ARR, Usage — MAU/Seats/Active Users per Customer,
    Minimum MAU, Pricing Engine

Every dashboard reads from the data-layer tabs with formulas, so the whole thing is
internally consistent and recomputes if a number changes. History spans 42 months
(Jan 2023 → **Jun 2026**), and downstream formulas resolve the latest/prior month
**dynamically by date** — so adding a month "just works" (see *Monthly update* below).

## Monthly update (adding a month) & month-add robustness

Every "this month / last month" figure resolves the latest/prior month **by its row-1
date**, not by a fixed column (`AT`). So when you add a new month column, all dashboards,
MoM growth, cash, churn, and per-customer "current month" cells follow automatically —
nothing to re-point. Build these refs with the `wb.py` helpers:

- `wb.latest(tab,row)` / `wb.prior(tab,row)` — cross-tab latest / prior-month cell
- `wb.latest_range(tab,r1,r2)` / `wb.prior_range(...)` — whole latest/prior column (for SUM/SUMPRODUCT/N)
- `wb.nth(tab,row,k)` / `wb.nth_date(tab,k)` / `wb.nth_range(tab,r1,r2,k)` — the k-th most-recent month (k=1 latest). Use these for **recent-first tables** (row 1 = latest), so every row auto-shifts when a month is added.
- `wb.colbyname(tab,row,"Disc %")` — a structural column by header name (survives column shifts)
- `wb.latest_self(row)` / `wb.prior_self(row)` — same-sheet (e.g. MoM-Growth columns, if added to the data tabs)

Leave **column-aligned month mirrors alone** (e.g. Customers — ARR month cells that
reference their own column) — those auto-adjust on a column insert; only the
*off-grid pins* need the helpers.

**To add a month (monthly close):**
1. On each data tab (Customers — MRR, Usage — MAU/Seats/Active Users): if the current
   latest month is fed by a formula, freeze it (Copy → Paste values-only), then **insert
   one column** right after the last month (before the "MoM Growth" column).
2. Set the new column's row-1 header to `=EDATE(<prev month cell>,1)`.
3. Enter that month's numbers in the new column (or point 📥 Paste Data Here at it). Copy
   the **Customers — ARR** ×12 mirror and the **Customers — MRR** totals-block formulas
   into the new column.
4. Done — every dashboard, growth, cash, churn and per-customer "current month" cell
   updates itself (it finds the newest month by date).

**Generator month-add hardening.** All build scripts emit dynamic month refs:
single-latest cells (Combined Summary, Usage Summary, Minimum MAU, Pricing Engine,
Autopay, Revenue Dashboard movers, Revenue → Cash top) use `wb.latest()/wb.prior()`;
recent-first tables (MRR & ARR Summary, Usage Monthly History, Over-Min History, Churn,
Revenue → Cash trailing) use `wb.nth()/wb.nth_date()/wb.nth_range()`. Chronological
tables (Compare model, Invoiced Volume) stay column-aligned (append a row per month).
The same monthly-close procedure is written on the generated sheet's 📕 How to Use tab.
Keep using these helpers for any new month-referencing formula — never hard-code the
column letter of the current latest month.

## How to run

```bash
bash ~/.claude/skills/generic-kpi/scripts/run.sh [seed] [n_customers]
```

- `seed` (optional) — integer; same seed → same data. Omit for a random fresh dataset.
- `n_customers` (optional, default 35) — keep it in the ~30–40 range for a clean look.

The script generates the data, builds all tabs, turns on **link sharing (anyone with the
link can view)**, and prints the shareable URL. It creates a **brand-new** sheet each run —
it never overwrites a previous one. Requires the authenticated `gws` CLI.

## Notes / how it works

- **Engine:** `scripts/gen_data.py` (deterministic fake-data generator, seedable) →
  `build.py` (data layer) → `build2.py`/`build3.py` (dashboards) → `build4.py`
  (How-to-Use + Definitions + tab order) → `fmt_pass.py` (final number-format pass,
  applied last so percent/pp formats stick). `wb.py` is the shared Sheets-API helper.
- The data generator guarantees a few quarterly billers (so the "invoice timing vs
  recurring MRR" story shows), ~⅓ of customers under their usage minimum, some churn,
  and ~half on autopay — so the dashboards look realistic.
- To change the fictional company name, metric labels, customer-name pool, or number
  ranges, edit `scripts/gen_data.py` and `scripts/wb.py`; do not edit the output sheet
  by hand (a regen would overwrite your edits — change the scripts instead).
- **Everything is fictional.** The How-to-Use and Combined Summary tabs both carry an
  explicit "sample data" disclaimer.
