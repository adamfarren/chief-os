# Customer 360: Cascade Retail

**Date:** 2026-04-08
**Time Range:** Last 90 days (Jan 8 – Apr 8, 2026)
**Focus:** General review

---

## Executive Summary

Cascade Retail is a $165K ACV customer with a renewal in July 2026 (3 months). The account shows mixed signals: usage remains strong (active across all core modules) but support volume spiked 60% in the last 30 days, concentrated around their bank feed integration. Internal Slack discussions reflect growing concern about the renewal. Meeting cadence has dropped from weekly to biweekly, and the last two meetings were rescheduled by the customer. The combination of renewal proximity, rising support volume, and declining engagement warrants immediate attention.

[SIMULATED — all customer names, metrics, and data are fictional test data]

---

## I. Public Profile & Growth Drivers

### Company Overview

| Detail | Value |
|--------|-------|
| **Founded** | 2019, Portland, OR |
| **Leadership** | Dr. Sarah Chen (CEO), Marcus Webb (CTO), Lisa Park (COO) |
| **Website** | cascaderetail.com |
| **Total Funding** | $18M (Seed + Series A) |
| **Investors** | Flare Capital, 7wireVentures |

### What They Do

Cascade Retail operates a network of multi-brand e-commerce stores combining apparel, home goods, and specialty foods under one umbrella finance team. Their model targets digitally-native consumer brands in the Pacific Northwest who want consolidated back-office finance operations across multiple entities.

They've grown from 2 entities to 7 in 18 months, with plans to expand into California by Q3 2026. The expansion is partially funded by their Series A and partially by revenue from their existing entities.

### Public Growth Metrics

- 7 entities across Oregon and Washington
- 12,000+ active customers
- 85% repeat-purchase rate (self-reported)
- Recently announced partnership with Pacific Blue Logistics for fulfillment cost-pass-through pilot

### Key Public References

- Portland Business Journal: "Cascade Retail raises $12M Series A" (Sep 2025)
- Retail Dive: "Multi-brand e-commerce operators see renewed investor interest" (Jan 2026) — Cascade mentioned alongside 3 peers

---

## II. CRM / Account Overview

### Deal Summary

| Detail | Value |
|--------|-------|
| **Current Stage** | Closed Won |
| **ARR / ACV** | $165,000 |
| **Contract Start** | July 2024 |
| **Renewal Date** | July 2026 |
| **Deal Owner** | Priya Sharma |
| **Pipeline** | Sales Pipeline |

### Deal History

| Date | Event | Details |
|------|-------|---------|
| Apr 2024 | New Opportunity | Inbound from website, Dr. Chen attended webinar |
| Jun 2024 | Closed Won | $120K ACV, 2-year contract, 3 entities |
| Jan 2025 | Expansion | +$45K ACV for 4 additional entities, bringing total to $165K |

### Key Contacts

| Name | Title | Email | Role in Relationship |
|------|-------|-------|---------------------|
| Dr. Sarah Chen | CEO | s.chen@cascaderetail.com | Executive sponsor, involved in renewals |
| Marcus Webb | CTO | m.webb@cascaderetail.com | Technical decision maker, primary config contact |
| Amy Torres | Controller | a.torres@cascaderetail.com | Day-to-day operations, submits most support tickets |

### CRM Notes & Activity

- Last logged call: Mar 15, 2026 — Priya noted "customer flagged bank feed integration issues, asked about timeline for fix"
- No logged activity since Mar 15 (25 days gap)
- Expansion opportunity noted in HubSpot: "Cascade exploring adding 3 more CA entities, potential +$60K ACV"

---

## III. Meeting & Communication History

### Meeting Timeline

| Date | Meeting Title | Your Team | Their Team | Source |
|------|--------------|-----------|------------|--------|
| Jan 15 | Cascade Weekly Sync | Priya, David | Amy Torres, Marcus Webb | Calendar |
| Jan 22 | Cascade Weekly Sync | Priya | Amy Torres | Calendar |
| Feb 5 | Cascade Bank Feed Review | Priya, Engineering (Sam) | Marcus Webb, Amy Torres | Calendar |
| Feb 19 | Cascade Biweekly | Priya | Amy Torres | Calendar |
| Mar 5 | Cascade Biweekly | Priya | Amy Torres, Marcus Webb | Calendar |
| Mar 19 | Cascade Sync (rescheduled by customer) | — | — | Calendar |
| Apr 2 | Cascade Sync (rescheduled by customer) | — | — | Calendar |

### Key Meeting Summaries

**Feb 5 — Bank Feed Review:** Marcus Webb raised concerns about transaction sync errors affecting 3 of 7 entities. Sam from engineering diagnosed a configuration issue with their Ledgerlink bank feed mapping. Committed to a fix within 2 weeks. Customer tone: direct, professional, clearly frustrated but constructive.

**Mar 5 — Biweekly:** Amy Torres reported the bank feed fix resolved most issues but 1 entity (Bend, OR) still has intermittent failures. Marcus mentioned they're "evaluating their options" for the CA expansion — unclear if this refers to platform choice or operational planning. Meeting ended early.

### Email Highlights

- **Mar 22:** Dr. Chen emailed Priya directly — first CEO-level email in 6 months. Subject: "Quick question about our contract." Body asked about early termination terms. Priya responded same day with a meeting request, no response from Dr. Chen yet.
- **Apr 1:** Amy Torres emailed support about 4 failed bank feed syncs for Bend entity.

### Communication Pattern Analysis

Meeting cadence degraded from weekly to biweekly to rescheduled. The CEO engaging directly via email (bypassing the controller) about contract terms is a significant escalation signal. Email response time from the customer has lengthened from same-day to 3-5 days.

---

## IV. Internal Discussions (Slack)

### Bank Feed Integration Concerns (8 threads)
The team has been actively discussing Cascade's bank feed issues since February. Engineering traced the root cause to a Ledgerlink API change that affected multi-entity setups. The fix was partially deployed but the Bend entity remains affected due to a unique tax ID configuration.

### Renewal Risk (4 threads)
Priya flagged the Dr. Chen contract email in #customer-success. Discussion included whether to involve the VP of Sales. Consensus: Priya should schedule a call with Dr. Chen before escalating. No call has been logged yet.

### Expansion Opportunity (2 threads)
Before the bank feed issues, the team was optimistic about a $60K expansion for California entities. Recent threads suggest the expansion is "on hold" pending resolution of current issues.

---

## V. Support Activity

### Jira Tickets (8 found)

| Ticket | Summary | Status | Created | Assignee |
|--------|---------|--------|---------|----------|
| SUP-4521 | Bank feed sync failures — Bend entity | Open | Mar 28 | Sam Lee |
| SUP-4498 | Statement parsing errors for Pacific Blue Bank | Open | Mar 20 | Sam Lee |
| SUP-4412 | Multi-entity tax ID not populating on journal entries | Resolved | Feb 28 | Sam Lee |
| SUP-4389 | GL sync lag between entities | Resolved | Feb 15 | Maria Garcia |
| SUP-4356 | Customer portal SSO not working for new entity | Resolved | Feb 5 | David Kim |
| SUP-4301 | Ledgerlink mapping error — 3 entities | Resolved | Jan 22 | Sam Lee |
| SUP-4287 | Reporting dashboard timeout for multi-entity view | Resolved | Jan 15 | Maria Garcia |
| SUP-4265 | Account code mapping incorrect for cost-of-goods | Resolved | Jan 10 | Sam Lee |

### Support Platform (Pylon)

| Metric | Value |
|--------|-------|
| **Open Issues** | 3 |
| **Resolved (last 30d)** | 2 |
| **Avg Resolution Time** | 8.5 days |

### Key Takeaways

5 of 8 tickets are bank-feed-related, all assigned to Sam Lee. The pattern is clear: their multi-entity bank feed setup is the pain point, and the Bend entity issue (SUP-4521) is the current blocker. Average resolution time of 8.5 days is above the company-wide average of 4.2 days, reflecting the complexity of these issues. Two tickets remain open (SUP-4521, SUP-4498) — both bank-feed, both 10+ days old.

---

## VI. Internal Docs & Relationship Context (Notion)

**Customer Board entry:** Cascade Retail is classified as a "Growth" account. Internal notes from onboarding (Jul 2024) describe them as "highly engaged, technically sophisticated, fast adopter." The expansion to 7 entities is noted as a success story.

**Relationship dynamics:** Priya Sharma is the primary relationship owner. Dr. Chen is described as "hands-off until something matters, then very direct." The CTO (Marcus Webb) is the technical gatekeeper who evaluates all platform decisions.

**Historical context:** During onboarding, Cascade requested custom close workflows for their multi-brand model. The team delivered a custom configuration that worked well at 3 entities but has shown strain at 7.

---

## VII. Technical Signals (Sentry)

Skipped — no technical investigation dimension. The bank feed issues are configuration/integration problems, not platform errors.

---

## VIII. Risk Signals & Key Findings

### HIGH RISK
1. **CEO contract inquiry + renewal in 3 months.** Dr. Chen's email asking about early termination terms is the strongest churn signal. This is the first CEO-level engagement in 6 months, and it's about exit terms. (Sources: Gmail, CRM)
2. **Bank feed issues unresolved for 60+ days.** The Ledgerlink problems began in late January. While 6 of 8 tickets are resolved, the remaining 2 (Bend entity) are the ones the customer cares about most. This has been the dominant topic in every meeting and Slack thread. (Sources: Jira, Slack, Meetings)

### MEDIUM RISK
3. **Expansion on hold.** The $60K CA expansion was progressing before the bank feed issues. Internal Slack suggests it's now paused. If the current issues aren't resolved, the expansion is likely dead — and may take the base contract with it. (Sources: Slack, CRM)
4. **Meeting cadence declining.** Weekly to biweekly to cancelled. Two consecutive reschedules by the customer suggest disengagement, not scheduling conflicts. (Sources: Calendar)

### WATCH
5. **Single-engineer dependency.** All 5 bank feed tickets are assigned to Sam Lee. If Sam is unavailable or overloaded, resolution time will extend further. (Sources: Jira)
6. **Email responsiveness declining.** Customer response time has lengthened from same-day to 3-5 days. May indicate frustration or deprioritization of the relationship. (Sources: Gmail)

---

## IX. Proactive Recommendations

### Immediate (This Week)
1. **CEO-to-CEO call.** Jordan should call Dr. Chen directly. Frame it as "I saw you had a question about your contract — I want to make sure we're taking care of you." Don't wait for Priya to schedule it. The fact that Dr. Chen emailed about exit terms means this has escalated beyond the account manager level.
2. **Expedite SUP-4521 and SUP-4498.** Get Sam Lee a second engineer to pair on the Bend entity bank feed fix. Set a 48-hour target for resolution.

### Short-Term (Next 30 Days)
3. **Bank feed integration audit.** After the immediate fix, do a comprehensive audit of Cascade's bank feed setup across all 7 entities. Identify any other configurations that could break as they scale further.
4. **Re-engage on expansion.** Once bank feeds are resolved, Priya should reopen the CA expansion conversation. Position the bank feed fix as proof of commitment, not just damage control.
5. **Restore weekly meeting cadence.** Priya should propose returning to weekly syncs for the next 4 weeks, framed as "making sure the fixes are holding."

### Medium-Term (Next 90 Days)
6. **Multi-entity bank feed playbook.** The issues Cascade hit will affect other multi-entity customers. Engineering should productize the fix into a standard multi-entity bank feed configuration.
7. **Renewal prep.** Start renewal conversations 60 days out (May 2026). By then, bank feeds should be stable, and the expansion conversation should indicate whether the relationship is salvageable.

---

## X. Sources Searched

| Source | Results | Notes |
|--------|---------|-------|
| Web Search | 4 articles | Portland Business Journal, Retail Dive, company website |
| HubSpot (CRM) | 1 company, 2 deals, 3 contacts | Full deal history and contact details retrieved |
| Google Calendar | 7 events | Jan–Apr 2026, showing cadence decline |
| Gmail | 6 threads | Including CEO contract inquiry (Mar 22) |
| Slack | 14 threads | Across #customer-success, #engineering, #bank-feeds |
| Jira | 8 tickets | 5 bank-feed, 2 infrastructure, 1 access |
| Pylon | 3 open issues | Correlated with Jira tickets |
| Notion | 3 pages | Customer board entry, onboarding doc, relationship notes |
| Sentry | Skipped | No technical investigation needed |
