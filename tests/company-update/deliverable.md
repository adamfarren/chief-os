# Weekly Update — April 13–17, 2026

## What Matters This Week

- **Riverside Cardiology go-live is on for Thursday 4/16.** First cardiology vertical launch — Priya's team has been embedded on-site since Monday. Day-of coverage rotation is in #riverside-launch; Amy is lead, Marcus on engineering standby.
- **Pacific Rim Specialty walks to close Friday at $312K ACV.** Largest single deal of the quarter. Sarah on the redline; legal turn expected Wed evening. If it slips past Friday it lands in Q2, not Q1.
- **Agent SDK private beta opens to the second cohort Wednesday.** 12 new builder accounts (mix of existing customers and design partners). Marcus is the DRI; success criterion is at least one customer-shipped plugin from the cohort by 4/30.
- **Plugin Scorecard (last week, 4/1 → 4/8).** 11 unique plugins from 9 of 14 customer-facing builders hit target (1/wk); 6 engineering plugins from 8 of 18 engineers hit (target 0.5/wk each = 9/wk team — miss). Standouts:
  - `derm-photo-router` — Elena Vasquez — auto-routes photo intake to the right derm provider by lesion location
  - `cardio-prior-auth` — Priya Sharma — pre-fills cardiology prior-auth packets from the chart
  - `intake-spanish-v2` — David Chang — bilingual intake with structured chief-complaint capture
  - Plus 2 external contributions from Tom Bradley's contractor team (not on Horizon HC).

## One Thing You Should Know

The Riverside go-live is not just a launch — it's the first proof that Horizon's specialty-specific approach travels beyond derm and ortho. Jordan was in the Mon and Wed working sessions and has been on the #riverside-launch channel daily. If Thursday lands cleanly, the cardiology vertical narrative we're telling investors becomes a *demonstrated capability* instead of a roadmap claim. If it stumbles, we need to be honest about it on next week's board prep call.

---

## Product & Engineering

**Shipped:** Practice OS v1.296.0 (cardiology chart templates, photo-intake routing), Agent SDK v0.7 (auth flow simplification, two new sample plugins), Patient Portal v2.41 (multi-location switcher for 50+ provider groups).

**In Progress:** Cardiology lab-result ingestion (Priya — needed for Riverside week-2 expansion), enterprise admin v1 multi-location billing (blocked on SOC 2 audit logging — Devon coordinating), Agent SDK marketplace search redesign (Marcus / Sofia — beta cohort feedback driving this).

**Notes:** One 14-min incident Wednesday 4/15 — chart-template service returned 500s on cardiology pages for ~3% of traffic. Root cause: a missing migration on the new lab-result table. Caught by alerts, rolled forward with the migration, no customer-reported impact. Postmortem in #eng-incidents.

## Sales & Pipeline

**Closed-won MTD (April):** Bayview Orthopedics expansion +$48K ACV (4/2), Heartland Family Medicine new logo $87K ACV (4/9), Northwest Spine Specialists new logo $54K ACV (4/14). Three deals, $189K new ACV booked.

**Closed-lost worth flagging:** Cedar Valley Health $220K ACV (4/11) — went with Modernizing Medicine on price + a multi-year discount we declined to match. Post-mortem on #sales-postmortems: this is the second mid-market loss to MM in the quarter on the same lever; Sarah convening a pricing review next week.

**Walk to Close (named):**
- Pacific Rim Specialty Network — $312K ACV — close target Fri 4/17 (in redline)
- Lakeshore Dermatology Partners — $94K ACV — close target Wed 4/22 (verbal yes, paperwork out)
- Summit Orthopedic Group — $128K ACV — close target Fri 4/24
- Mesa Cardiology Associates — $76K ACV — close target Tue 4/28

Pipeline coverage for Q2 sits at $1.42M weighted against a $1.2M target. Quarter-progress against the $20M ARR annual goal: $13.1M committed ARR (Q1 actuals + April MTD), tracking to plan.

**Partnership note:** First Round Capital intro for ChronoAudit (documentation auditing) scheduled Mon 4/20 — Sarah is taking the first call.

## Customers & Implementation

- 🟢 **Cascade Wellness (L2) — week-3 of go-live, adoption ahead of plan.** Provider activation at 88% (target was 75% by EOW3); patient-message turnaround down to 4.2h from 11.6h pre-Horizon. Amy and Aisha are running a workflow review session Friday to identify expansion levers. **30-day milestone hits 4/24** — expect a strong NPS read.
- 🟡 **Bayview Orthopedics (L1) — at risk on the lab-integration rollout.** Bayview's reference lab (HealthEdge) is dragging on the HL7 spec finalization; we're now 2 weeks behind on the lab-results module that was the expansion lever. James is paired with their CTO daily. If HealthEdge doesn't commit to a date by 4/22, we escalate to their account exec.
- 🟢 **Riverside Cardiology (L1) — go-live Thursday 4/16, all gates green.** Templates loaded, providers trained, on-call rotation set. Priya, Amy, and Marcus on-site Wed–Fri. **This is the first cardiology launch — eyes on this one.**
- 🔴 **Cedar Valley Health (former L2) — closed lost 4/11.** Not a customer anymore; logging here so we don't surface them in next week's customer narrative. (See Sales for post-mortem context.)
- 🟡 **Mountain Specialty Care (L2) — sentiment slipping on Agent SDK access.** They're in the second beta cohort starting Wed but were expecting access two weeks ago. Marcus sent the acknowledgment Monday; Amy is owning the rebuild of trust through 4/30.
- ⏸ **Heartland Family Medicine (L1) — stalled on kickoff scheduling.** Closed 4/9, kickoff was supposed to be this week, slipped to 4/27 because their practice manager is OOO. Tracking but no action needed yet.

**30/60/90-day post go-live flags:**
- Cascade Wellness — 30-day on 4/24
- Pinecrest Dermatology — 60-day on 4/19 (Aisha sending the structured check-in form)
- Northstar Family Care — 90-day on 4/17 (Amy doing the in-person renewal conversation)

## Support

Pylon Support Working Session (Tue 4/14) tables were unpopulated this week — pulled directly from Pylon for the window 4/8 → 4/15.

| Customer | Level | Tickets (7d) | Tickets (30d) | Sentiment | IM |
|---|---|---|---|---|---|
| 🟡 Bayview Orthopedics | L1 | 18 | 47 | Frustrated | James Liu |
| 🟢 Cascade Wellness | L2 | 14 | 14 | Positive | Aisha Okafor |
| 🟡 Mountain Specialty Care | L2 | 11 | 38 | Neutral → Frustrated | Nina Patel |
| 🟢 Pinecrest Dermatology | L2 | 7 | 22 | Positive | Aisha Okafor |
| 🟢 Northstar Family Care | L1 | 5 | 19 | Positive | Sofia Petrov |

**Themes:**
- 🟡 **Bayview's volume is HL7-driven, not regression-driven.** 12 of the 18 tickets are HealthEdge integration questions. Real, but not a product-quality signal.
- 🟢 **Cascade's 14 tickets are go-live ramp, not friction.** All resolved within SLA; sentiment is positive. Expected to taper next week.
- 🟡 **Mountain Specialty Care sentiment moved Neutral → Frustrated this week** — driven by the Agent SDK access delay (see Customers section). Marcus's Monday acknowledgment will show up in next week's sentiment read.
- L1 accounts in Frustrated: none right now. Watching Bayview closely.

**Escalations this week:** 1 — Bayview to engineering leadership on the HL7 spec.

**Top bugs prioritized:** Photo-intake duplicate detection (Elena, ETA 4/22), enterprise admin permissions cache (Tom, ETA 4/24), Agent SDK rate-limit headers missing (Marcus, ETA 4/18).

**Process note:** DRI for Pylon Support metrics in the working-session doc is Amy Torres; flagging here so the gap doesn't recur. Pulled the data directly this week so the section is complete.

## Shoutouts

- **Elena Vasquez** shipped `derm-photo-router` AND helped two design partners ship their first plugins this week. Her Agent SDK migration playbook (posted in #agent-sdk-builders Wed) is the model for how we onboard the next cohort.
- **Priya Sharma** lived in Riverside this week — three trips, two weekend prep sessions, no drama. Cardiology vertical launches because she made it personal.
- **Amy Torres** turned the Mountain Specialty Care relationship around in 48 hours after the Agent SDK delay. The Monday acknowledgment + Tuesday recovery plan is how this is supposed to work.
- **Dr. Anita Reyes (Chief Medical Officer at Cascade Wellness)** sent us an unprompted thank-you Tuesday: *"Our providers are getting home for dinner again. That's the metric."* Aisha is the IM; this is her win as much as ours.
- **Tom Bradley's contractor team** merged two external plugins to the marketplace this week — they don't roll up under team targets but they shipped customer-impacting work.
- **Work anniversary: David Chang — 3 years at Horizon (4/15).** Three years of being the most-helpful engineer on the team. Quietly, every week.

## Company on LinkedIn This Week

Reshares from your own network travel furthest — please take 30 seconds to like, comment, or reshare these:

- **Jordan Rivera** — [The EHR is dead. The agent-powered practice OS is next.](https://linkedin.com/posts/example-jordan-ehr-dead)
- **Marcus Webb** — [What we learned shipping 47 customer-built plugins in 90 days](https://linkedin.com/posts/example-marcus-plugins)
- **Sarah Chen** — [Why specialty groups outgrow generic EHRs in year two](https://linkedin.com/posts/example-sarah-specialty)
- **Priya Sharma** — [Cardiology workflows aren't dermatology workflows. Stop pretending.](https://linkedin.com/posts/example-priya-cardio)

## OOO Next Week (Mon 4/20 – Fri 4/24)

| Date | Who |
|---|---|
| Mon 4/20 | Devon Park (PTO) |
| Tue 4/21 | Devon Park (PTO), Nina Patel (PTO) |
| Wed 4/22 | Nina Patel (PTO) |
| Thu 4/23 | — |
| Fri 4/24 | James Liu (half-day, family) |

- **Notable:** Riverside Cardiology onsite Wed–Thu 4/22–4/23 (Priya, Marcus). Work-anniversary: Sarah Chen — 6 months at Horizon (4/22).
- **Coverage flags to watch:** Tuesday 4/21 has both Devon (Ops) and Nina (Support IM for Mountain Specialty) out the same day. Amy is covering the Mountain Specialty check-in; Sarah handling any contracting urgency.
