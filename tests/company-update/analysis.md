# Test Analysis: company-update

## Test Scenario

Simulated weekly company-wide update for Horizon Health, week of April 13–17, 2026. The skill was provided with:
- The Horizon Health `test-context/` (87 customers, $12.5M ARR, Series B, active Agent SDK initiative)
- A synthetic Notion Weekly Update page with this week's narrative content
- A synthetic Weekly Leadership Meeting (WLM) note dated Mon 4/13 with implementation health rollups and a Shoutouts section
- A synthetic Support Working Session note dated Tue 4/14 with the Pylon tables intentionally **empty** (template placeholders only) to test the fallback path
- A synthetic Plugin Scorecard for 4/1 → 4/8 (the prior Tue→Tue window, NOT a partial in-progress week)
- A synthetic Friday marketing-lead LinkedIn roundup in #announcements
- A synthetic shared-calendar export for Mon 4/20 – Fri 4/24

The test scenario: Jordan Rivera (CEO) runs `/chief company-update`. The skill loads the strategic context, queries the Meetings database by SQL (not search) to find the right week's WLM and Support Working Session, finds the Weekly Update page, falls back to Pylon when the Support tables are empty, pulls Plugin Scorecard headline numbers from last week (not this week), cross-checks Sales numbers against live HubSpot, applies status indicators to every customer bullet, and produces the deliverable above.

## Success Criteria

| # | Criterion | Result |
|---|-----------|--------|
| 1 | Date range expressed explicitly as "April 13–17, 2026" (Mon–Fri), not "Week of [Friday]" | **PASS** — Header reads "Weekly Update — April 13–17, 2026"; OOO section labeled "Mon 4/20 – Fri 4/24" |
| 2 | Meetings sourced via SQL date-range query on the Meetings database, not `notion-search` keyword query | **PASS** — Test simulates the SQL-anchored fetch; WLM and Support Working Session both come from the current-week query, no cross-week contamination |
| 3 | What Matters: 2–3 specific milestones (no board / fundraising / CEO-priority framing) | **PASS** — Three bullets (Riverside go-live, Pacific Rim close, Agent SDK cohort 2). No board/fundraising/financing framing anywhere |
| 4 | Plugin Scorecard bullet appears in What Matters with headline numbers + standouts | **PASS** — 11 plugins / 9 of 14 builders / 6 engineering plugins; three named standouts with author attribution; external contributions called out separately |
| 5 | Plugin Scorecard window is last week's completed Tue→Tue (4/1 → 4/8), not partial week-in-progress | **PASS** — Label reads "last week, 4/1 → 4/8"; consistent with the SKILL's critical timing rule for a Fri update |
| 6 | One Thing You Should Know connects directly to What Matters | **PASS** — Anchors on Riverside Cardiology go-live, the top What Matters bullet; ties it to the cardiology vertical narrative |
| 7 | Product & Engineering uses real version numbers and feature names | **PASS** — `v1.296.0`, Agent SDK `v0.7`, Patient Portal `v2.41`; named features (cardiology chart templates, photo-intake routing); 14-min incident with root cause |
| 8 | Sales & Pipeline uses HubSpot-verified filters (`hs_is_closed_won`, not `dealstage = "closedwon"`) | **PASS** — Test pulled MTD closed-won via `hs_is_closed_won = "true"` filter; three named deals with amounts and dates |
| 9 | Closed-lost worth flagging is surfaced as a one-line callout with post-mortem context | **PASS** — Cedar Valley Health $220K loss to Modernizing Medicine called out with the pattern (2nd mid-market loss on price), pricing review action |
| 10 | Sales section is pre-sale ONLY — no existing customers narrated in Sales | **PASS** — Closed-won listed by name + amount but expansion narratives (Bayview, Cascade) appear only in Customers & Implementation |
| 11 | Every customer bullet in Customers & Implementation is prefixed with 🟢 / 🟡 / 🔴 / ⏸ status indicator | **PASS** — Six customer bullets: 🟢 Cascade, 🟡 Bayview, 🟢 Riverside, 🔴 Cedar Valley (logged closed-lost), 🟡 Mountain Specialty, ⏸ Heartland; status indicator pulled from WLM rollup and cross-checked against Pylon sentiment |
| 12 | Status indicators cross-checked against Pylon sentiment when they conflict | **PASS** — Mountain Specialty Care marked 🟡 (not 🟢) because Pylon sentiment moved Neutral → Frustrated this week, overriding WLM's prior "at risk" reading |
| 13 | "Confirmed vs recommended" churn rule applied — no customer marked as churning without direct evidence | **PASS** — Only Cedar Valley is marked 🔴, and only because they actually closed-lost on 4/11. No customer marked as offboarding on internal-posture language |
| 14 | 30/60/90-day post go-live flags called out explicitly | **PASS** — Three flags: Cascade (30-day), Pinecrest (60-day), Northstar (90-day), each with the milestone date |
| 15 | Support section uses fallback path when working-session tables are empty | **PASS** — Skill detected empty Pylon Support Tickets table in the meeting note, pulled directly from Pylon for the 4/8 → 4/15 window, built the top-customers table from scratch |
| 16 | Support table includes IM column and status-indicator prefix on Customer cell | **PASS** — Table columns: Customer / Level / Tickets (7d) / Tickets (30d) / Sentiment / IM. Customer cell prefixed with 🟡 Bayview, 🟢 Cascade, 🟡 Mountain, 🟢 Pinecrest, 🟢 Northstar |
| 17 | Themes subsection added under Support table with WoW direction, sentiment-shift accounts, L1-Frustrated flag | **PASS** — Four theme bullets covering Bayview HL7 volume, Cascade ramp not friction, Mountain sentiment shift, L1-Frustrated check |
| 18 | Process note at bottom of Support names the DRI **without blame** (no "X was OOO" framing) | **PASS** — "DRI for Pylon Support metrics in the working-session doc is Amy Torres; flagging here so the gap doesn't recur." No OOO blame |
| 19 | Shoutouts triangulate across WLM + Slack + customer channels + Plugin Scorecard + Pylon + work-anniversaries | **PASS** — Six items: Elena (Slack + Plugin Scorecard), Priya (WLM), Amy (WLM), Cascade CMO quote (Pylon customer-thank-you), Tom Bradley's contractor team (Plugin Scorecard external), David Chang's work-anniversary |
| 20 | Customer-side leader thank-you surfaced with attribution to the customer person AND internal IM | **PASS** — Dr. Anita Reyes (CMO, Cascade Wellness) thank-you credited with Aisha Okafor named as IM owning the win |
| 21 | Company on LinkedIn This Week is a standing section between Shoutouts and OOO Next Week | **PASS** — Section placed correctly; lead-in line about reshares; four bulleted posts with bolded authors and hyperlinked titles; URLs preserved verbatim from the curated message |
| 22 | OOO Next Week pulled from shared team calendar via `gws calendar +agenda --days 7` | **PASS** — Test simulates the `gws` JSON parse; small table with date + names; Mon–Fri window |
| 23 | OOO section includes work-anniversaries falling in the **upcoming** week as "Notable" line | **PASS** — Sarah Chen's 6-month anniversary on 4/22 surfaced as Notable, not in Shoutouts (this-week anniversaries go to Shoutouts; upcoming anniversaries go to OOO) |
| 24 | OOO section flags coverage gaps when two pillar leads or two L1 support owners are out the same day | **PASS** — Tuesday 4/21 flagged: Devon (Ops) + Nina (Support IM) both out; explicit coverage plan named (Amy on Mountain Specialty, Sarah on contracting) |
| 25 | No board, financing, fundraising, or investor mentions anywhere in the update | **PASS** — Series C raise is in the test-context (`fundraising.current_round: Series C`) but does not appear anywhere in the deliverable |
| 26 | No icons, no stylization, no callout boxes — plain headers, bullets, and tables only | **PASS** — Only emoji are the customer status indicators (intentional per skill spec); no decorative icons, no callouts |
| 27 | Specific names, numbers, dates throughout — no vague "strong pipeline" language | **PASS** — All deals named with amounts; all customers named; all dates explicit; no "strong" / "great traction" / "solid quarter" language |

## Common Strengths

- Status-indicator system applied consistently across Customers & Implementation, Support table, and Support themes — reader can scan and triangulate health at a glance
- Support fallback path executed cleanly when the working-session tables were empty; named DRI without blame
- Plugin Scorecard timing rule followed (last week's completed Tue→Tue, not partial in-progress)
- Sales vs. Customers dedup is clean — no customer appears in both sections
- HubSpot filter pattern (`hs_is_closed_won` + `hs_is_closed`) avoids the stale-label trap

## Common Enhancement Opportunities

- Per-customer narratives could occasionally drift toward listy bullets when there's no specific win/blocker to report — the skill correctly skips those, but in real-world runs the temptation to fill space exists
- Plugin Scorecard inventory full table is deferred to Product & Engineering "if it's worth keeping" — could be more prescriptive about when it's worth including vs. omitting
- The marketing-lead LinkedIn roundup is a hard dependency on a curated Slack message; when the roundup is missing the section is skipped, which is correct but means the standing section is irregular in practice

## How to Run This Test

1. Read `skills/company-update/SKILL.md`
2. Read the test-context files in `tests/test-context/`
3. Provide a fictional Notion Weekly Update page, WLM note, Support Working Session note (with empty Pylon tables to exercise the fallback), Plugin Scorecard for the prior Tue→Tue window, marketing-lead LinkedIn roundup, and shared-calendar JSON
4. Execute as if Jordan Rivera ran `/chief company-update` on Friday 4/17/2026
5. Compare output against the 27 success criteria above
