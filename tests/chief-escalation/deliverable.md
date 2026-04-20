# Escalation Digest: Week of 2026-04-07

## Summary

Support volume is flat week-over-week (38 tickets vs. 36) despite adding 3 new customers. Resolution time improved to 4.2 hours (from 5.1). One escalation requires CEO attention: Pacific Software has 8 open tickets across 3 categories with a renewal in 4 months. The biggest win this week was resolving the Coastal Commerce calendar sync issue that had been open for 12 days.

[SIMULATED — all customer names, ticket volumes, and metrics are fictional test data]

## Key Metrics

| Metric | This Week | Last Week | Trend |
|--------|-----------|-----------|-------|
| Total Tickets | 38 | 36 | → Flat |
| Avg Resolution Time | 4.2 hrs | 5.1 hrs | ↓ Improved |
| Open Escalations | 3 | 2 | ↑ Watch |
| P1 Tickets Open >48hrs | 0 | 1 | ↓ Improved |
| CES (weekly) | 4.4/5.0 | 4.3/5.0 | ↑ |

## Escalations Requiring CEO Attention

### Pacific Software — Bank Feed Integration Failures
**Deal Size:** $180K ACV | **Renewal:** August 2026 (4 months) | **Severity:** P1
**Context:** 8 tickets this week across bank feed sync, transaction routing, and controller notifications. The root cause is a configuration issue with their bank vendor's API (Plaid endpoint). Our support team identified the fix but needs the customer's IT team to update their firewall rules. The customer's IT team is unresponsive.
**Recommended Action:** Jordan — call Maria (CFO) directly. Frame it as "we've diagnosed the issue and have the fix ready, but need your IT team's help to implement." A CEO-to-CFO call will get their IT team moving. Amy Torres can brief you in 5 minutes.

## At-Risk Accounts

| Customer | ARR | Renewal | Tickets (7d) | Risk Factor |
|----------|-----|---------|-------------|-------------|
| Pacific Software | $180K | Aug 2026 | 8 | Bank feed integration failures, unresponsive IT, renewal in 4 months |
| Mountain View Manufacturing | $95K | Oct 2026 | 5 | New invoice approval workflow causing finance team friction. Training issue. |
| Lakeside Retail | $120K | Jun 2026 | 4 | Billing module errors after their ERP upgrade. Renewal in 2 months. |

**Not at-risk but watch:** Summit Manufacturing ($210K, new Q1 customer) filed 3 tickets this week — all onboarding questions, not product issues. Normal for week 3 of implementation.

## Build Opportunities

| Pattern | Tickets/Week | Customers Affected | Recommended Fix |
|---------|-------------|-------------------|----------------|
| Bank feed vendor API configuration errors | 6 tickets/week | 4 customers (Pacific Software, Mountain View, 2 others) | Build a self-service bank feed diagnostic tool. Detects misconfigured endpoints, suggests fixes, and can auto-remediate common issues. Would eliminate ~80% of bank-feed-related tickets. |
| Invoice approval workflow confusion | 4 tickets/week | 3 customers | The approval workflow has 6 steps that could be 2. Priya Sharma's team should redesign the approval flow — this is a product issue, not a training issue. |

## Resolved This Week

- **Coastal Commerce** ($280K ACV) — Calendar sync issue between our close workflow and their Google Workspace resolved after 12 days. Root cause: timezone handling in the sync API. Fix deployed in v3.5.2. Marcus Webb's team patched it within 24 hours of diagnosis.
- **Valley Services** ($75K ACV) — Customer portal login issues affecting 30+ users. Traced to an SSL certificate rotation. Fixed same-day by the platform team.
