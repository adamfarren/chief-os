# Funnel Report — Apr 15, 2026

**Periods:** Recent: Mar 1 – Apr 15, 2026 | Prior: Jan 15 – Mar 1, 2026

---

## Headline

Lead volume is up 30% and qualification pace is holding, but qualified-to-deal conversion fell sharply (19% vs 28%) — 79 contacts entered Opportunity stage in 45 days while only 15 deals got created, suggesting a deal-creation backlog.

---

## Funnel Comparison

| Step | Prior (45 days) | Recent (45 days) | Change |
|------|-----------------|-------------------|--------|
| **Leads created** | 273 | 356 | +30% |
| **Qualified leads (activity)** | 64 | 79 | +23% |
| Lead → Qualified rate (activity) | 23.4% | 22.2% | -1.2pp |
| **Qualified leads (cohort)** | 60 of 273 created | 64 of 356 created | — |
| Lead → Qualified rate (cohort) | 22.0% | 18.0% | -4.0pp |
| **Deals created** | 18 | 15 | -17% |
| Qualified → Deal rate | 28.1% | 19.0% | -9.1pp |
| Overall Lead → Deal rate | 6.6% | 4.2% | -2.4pp |

> *Cohort rate for the recent period is understated — leads created late in the window haven't had time to qualify. The activity view (22.2%) is the better signal for current period health.*

---

## Lead Sources

> Source data is tracked at the **company object** (`lead_source`) — manually set when a company enters the funnel. Contact-level counts (356 recent / 273 prior) are higher because multiple contacts per company are created at intake. Company-level counts (73 recent / 69 prior) represent unique organizations.

| Source | Prior (69 cos) | Recent (73 cos) | Change |
|--------|---------------|-----------------|--------|
| free_trial | 26 (38%) | 23 (32%) | -12% |
| website_form | 15 (22%) | 16 (22%) | +7% |
| sales_outbound | 1 (1%) | 4 (5%) | +300% |
| partner | 3 (4%) | 4 (5%) | +33% |
| email | 3 (4%) | 0 | — |
| social_referral | 0 | 1 (1%) | — |
| **untagged** | **21 (30%)** | **25 (34%)** | +4 |
| **Total** | **69** | **73** | +6% |

Free trial and website form together account for ~54% of tagged leads — the funnel is primarily inbound/product-led, not outbound. `sales_outbound` (the AE's direct prospecting) is a small but growing channel (1 → 4 companies). The email channel dropped to zero. **30–34% of companies have no source tagged** — a growing admin gap that distorts source mix reporting.

---

## Conversion Analysis

### Lead → Qualified

Activity rate is essentially flat at 22.2% vs 23.4% — qualification pace is keeping up with the higher lead volume. The AE is working through the larger pipeline at the same conversion rate. The cohort view (18% vs 22%) looks weaker but is misleading: leads created in March and April haven't had the same runway to progress as the prior cohort, which by now is fully mature.

### Qualified → Deal

This is the flag. 79 contacts entered Opportunity stage in the recent period, but only 15 deals got created — a 19% conversion rate vs. 28.1% in the prior period. In the prior period, roughly 1-in-3.6 qualified leads became a deal; now it's 1-in-5.3. This gap (roughly 6–8 deals below prior pace) is the most likely explanation for a "stale" pipeline feel.

### Qualification Velocity

| Metric | Prior (Jan 15–Mar 1) | Recent (Mar 1–Apr 15) |
|--------|---------------------|----------------------|
| Contacts qualified | 64 | 79 |
| Same-day batch qualified | 28 (44%) | 48 (61%) |
| Mean velocity — active leads (excl. zombie) | 8.3 days | 4.7 days |
| Median velocity | 0 days | 0 days |
| Zombie leads re-qualified | 8 leads (max 1,106 days) | 4 leads (max 1,421 days) |

Velocity is not the bottleneck. 61% of recent qualifications happen same-day — the AE batch-imports contacts from the same organization and qualifies them simultaneously. For leads requiring follow-up, mean lag was **4.7 days** in the recent period, faster than the prior period (8.3 days) — a positive signal. Both periods include zombie leads (contacts created 2022–2023 now being re-qualified), which inflate raw averages but don't reflect current funnel health.

---

## Deal Quality (Funnel Output)

| | Prior Cohort | Recent Cohort |
|--|--|--|
| Deals created | 18 | 15 |
| Stage distribution | Requires /chief-pipeline | Requires /chief-pipeline |
| Total pipeline value | Available in HubSpot | Available in HubSpot |

*Run `/chief-pipeline` for full deal-level stage distribution and pipeline value on these cohorts.*

---

## Flags & Recommendations

**Working well:**
- Lead volume is up 30% — AE prospecting activity has accelerated meaningfully
- Qualification rate is holding (22.2% activity) — volume increase isn't degrading quality

**Watch:**
- Qualified → Deal conversion dropped 9 points (28% → 19%) — 79 opportunities were created in 45 days but only 15 deals materialized. The gap represents qualified accounts where a deal record hasn't been created in HubSpot, or deals that were verbally worked but never formalized.
- Email channel dropped to zero (3 → 0 companies) — was a minor but real source last period.
- Untagged `lead_source` is growing (21 → 25 companies, 30% → 34%) — the source mix is increasingly opaque. Free trial and website form together dominate tagged leads (~54%), meaning PLG/inbound is likely the real volume driver, but the gap makes it hard to confirm.

**AE priority:**
- Audit the 79 contacts who entered Opportunity stage between Mar 1 – Apr 15. For any account without an associated deal record, create it now. If the deal is dead, mark it closed lost so pipeline coverage is accurate. This sweep will either surface real pipeline (good news) or confirm deals aren't progressing (clear signal to address).
