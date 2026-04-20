# Engineering Roadmap Progress
**As of 2026-04-11 | Q2 2026**

---

## Executive Summary

Engineering velocity is healthy overall — Agent SDK is ahead of schedule, SOC 2 is on track, and Infrastructure performance is consistently hitting targets. The concern is Enterprise Admin Console: the multi-entity architecture decision is now two weeks overdue and blocking three downstream tickets. The manufacturing vertical is the largest risk: the May 31 beta target is achievable only if the customer intake module ships by April 24. Marcus Webb has surfaced this in Slack but no mitigation plan exists yet.

---

## By Project

### Agent SDK
**Quarterly Goal:** General availability (GA) launch by June 30, 2026
**Monthly Target (April):** Ship developer preview to 10 external beta partners; complete auth and permissions layer
**Status:** 🟢 On Track — ahead of schedule

**Last 2 Weeks:**
- Closed: AUTH-112 (OAuth 2.0 token scoping), SDK-88 (tool registration API), SDK-91 (multi-agent orchestration primitives), SDK-95 (Python SDK client library v0.3 published to PyPI)
- In Progress: SDK-97 (rate limiting and quota enforcement), SDK-99 (webhook event system), DOCS-14 (developer quickstart guide)
- No active blockers. 8 of 10 beta partner accounts are provisioned; final 2 onboarding this week.

**Open / Closed This Month:** 9 open | 12 closed

---

### Enterprise Admin Console
**Quarterly Goal:** Multi-entity support for groups with 50+ finance team members by June 30, 2026
**Monthly Target (April):** Complete data model for multi-tenant hierarchy; begin role-based access control (RBAC) implementation
**Status:** 🟡 At Risk — architecture decision overdue

**Last 2 Weeks:**
- Closed: ENT-34 (single-org admin UI scaffolding), ENT-35 (user invite flow)
- In Progress: ENT-38 (multi-tenant data model — BLOCKED pending architecture review), ENT-40 (RBAC permission model)
- **Blocker:** ENT-38 architecture review was scheduled for April 3 and has not happened. Decision on tenant isolation strategy (shared schema vs. schema-per-tenant) is blocking ENT-40 and two subsequent tickets (ENT-41, ENT-42). Review needs to be scheduled this week.

**Open / Closed This Month:** 14 open | 4 closed

---

### SOC 2 Type II
**Quarterly Goal:** Achieve SOC 2 Type II certification by June 30, 2026
**Monthly Target (April):** Complete audit evidence collection for access control and availability controls; resolve 3 open auditor findings
**Status:** 🟢 On Track

**Last 2 Weeks:**
- Closed: SOC-22 (automated access log export to auditor portal), SOC-23 (MFA enforcement for admin roles), SOC-25 (incident response runbook updated), SOC-26 (encryption-at-rest validation complete)
- In Progress: SOC-27 (third-party vendor access review), SOC-28 (backup restoration test)
- Auditor meeting on April 17 confirmed. 2 of 3 open findings resolved; SOC-27 is the remaining finding and is on track to close by April 15.

**Open / Closed This Month:** 4 open | 9 closed

---

### Manufacturing Vertical
**Quarterly Goal:** Beta launch with 3 pilot customers by May 31, 2026
**Monthly Target (April):** Ship manufacturing-specific customer intake module; complete segment data schema
**Status:** 🟡 At Risk — intake module behind, beta deadline tight

**Last 2 Weeks:**
- Closed: MFG-08 (manufacturing terminology mapping), MFG-09 (ERP integration schema v1)
- In Progress: MFG-11 (customer intake module — 60% complete, targeted April 24), MFG-12 (segment dashboard layout)
- MFG-11 is the critical path item. If it slips past April 24, the May 31 beta date becomes very difficult — pilot customer onboarding needs 3 weeks of staging time. No formal escalation raised yet.

**Open / Closed This Month:** 7 open | 3 closed

---

### Infrastructure & Performance
**Quarterly Goal:** P95 API latency under 200ms for all core endpoints by June 30, 2026
**Monthly Target (April):** Baseline and profile top 10 slowest endpoints; implement connection pooling
**Status:** 🟢 On Track

**Last 2 Weeks:**
- Closed: INFRA-55 (database connection pooler deployed to prod), INFRA-56 (query plan analyzer added to CI), INFRA-58 (P95 latency baseline established: 340ms current, target 200ms)
- In Progress: INFRA-60 (index optimization for transaction search), INFRA-61 (caching layer for customer directory)
- Current P95: 287ms (down from 340ms baseline). Ahead of pace.

**Open / Closed This Month:** 5 open | 7 closed

---

## By Engineer

### Marcus Webb — CTO
**Last 2 Weeks:**
- Closed: SDK-88 (architecture review and merge), INFRA-58 (approved P95 baseline methodology)
- In Progress: ENT-38 architecture review (overdue — scheduled this week), SDK-97 (design review)
- Primary output is design and review, not direct coding. Notable: ENT-38 review is the blocker on Enterprise track and is Marcus's.

**This Month:** 3 closed | 4 in progress (reviews)

---

### David Chang — Lead Engineer, AI Platform
**Last 2 Weeks:**
- Closed: SDK-88 (tool registration API), SDK-91 (multi-agent orchestration primitives), AUTH-112 (OAuth 2.0 token scoping)
- In Progress: SDK-97 (rate limiting and quota enforcement)
- Highest individual output this sprint. Strong velocity on the Agent SDK critical path.

**This Month:** 6 closed | 2 in progress

---

### Elena Vasquez — Senior Engineer, Agent SDK
**Last 2 Weeks:**
- Closed: SDK-95 (Python SDK client library v0.3), SDK-99 design spec
- In Progress: SDK-99 (webhook event system), DOCS-14 (developer quickstart)
- Also carrying documentation load — important for developer preview launch.

**This Month:** 4 closed | 2 in progress

---

### Ryan Kim — Senior Engineer, Infrastructure
**Last 2 Weeks:**
- Closed: INFRA-55 (connection pooler), INFRA-56 (query plan analyzer), INFRA-58 (baseline)
- In Progress: INFRA-60 (index optimization), INFRA-61 (caching layer)
- Driving the entire performance initiative. Strong and consistent.

**This Month:** 5 closed | 2 in progress

---

### Tom Bennett — Engineer, Enterprise Features
**Last 2 Weeks:**
- Closed: ENT-34 (admin UI scaffolding), ENT-35 (user invite flow)
- In Progress: ENT-40 (RBAC model — waiting on ENT-38 architecture decision)
- Blocked downstream of ENT-38. Output will stall until Marcus completes the arch review.

**This Month:** 3 closed | 2 in progress (1 blocked)

---

### James Liu — Engineer, SOC 2 Compliance
**Last 2 Weeks:**
- Closed: SOC-22 (access log export), SOC-23 (MFA enforcement), SOC-25 (incident response runbook), SOC-26 (encryption-at-rest validation)
- In Progress: SOC-27 (vendor access review), SOC-28 (backup restoration test)
- Executing cleanly. Highest closed-ticket count relative to project scope this sprint.

**This Month:** 7 closed | 2 in progress

---

### Sofia Petrov — Engineer, Manufacturing Vertical
**Last 2 Weeks:**
- Closed: MFG-08 (terminology mapping), MFG-09 (ERP schema v1)
- In Progress: MFG-11 (customer intake module, 60% complete)
- MFG-11 is on the critical path for the May 31 beta. Progress is on pace for April 24 target but has no buffer.

**This Month:** 3 closed | 2 in progress

---

### Aisha Okafor — Engineer, Frontend
**Last 2 Weeks:**
- Closed: ENT-35 (invite flow UI, paired with Tom Bennett), MFG-12 (segment dashboard layout, in progress)
- In Progress: MFG-12 (manufacturing dashboard), SDK-frontend-01 (developer portal updates)
- Splitting time across three tracks. No single blocker, but context-switching load is high.

**This Month:** 2 closed | 3 in progress

---

## Blockers & Risks

- **ENT-38 architecture review (Enterprise Admin Console)** — Overdue by 8 days. Marcus Webb is the DRI. This is blocking RBAC implementation and two downstream tickets. Needs to be scheduled and closed this week or Enterprise April milestone is in jeopardy.

- **MFG-11 critical path (Manufacturing Vertical)** — Customer intake module must ship by April 24 to preserve the May 31 beta date. Currently at 60% with no buffer. Sofia Petrov is the only engineer on it. If she needs support, now is the time to assign a second engineer.

- **Aisha Okafor cross-track load** — Splitting time across Enterprise, Manufacturing, and SDK frontend. No formal prioritization. Recommend clarifying her primary track for the rest of April.

- **No Jira data found for: Mia Rodriguez** — No Jira issues assigned in the past 30 days. Verify manually — may indicate PTO, project rotation, or a Jira assignment gap.

---

## Data Coverage
- Notion roadmap: "Meridian Ledger — Q2 2026 Engineering Roadmap" (fetched 2026-04-11)
- Jira: via Notion AI search connected source (Jira project keys: SDK, AUTH, ENT, SOC, MFG, INFRA)
- Slack channels: #eng-general, #platform, #agent-sdk, #enterprise-track (last 14 days)
- Report date: 2026-04-11
- **Data gap:** No Jira activity found for Mia Rodriguez — verify manually.
