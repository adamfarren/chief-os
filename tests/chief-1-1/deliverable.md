# Test Deliverable: chief-1-1

**Scenario:** "What should I talk to Jordan about today?"
**Employee:** Jordan Chen — Support Specialist, Ops Pillar, Meridian Ledger
**Test A:** Pylon connected | **Test B:** Pylon unavailable

---

## Test A Output (Pylon connected)

### 1-1 Prep: Jordan Chen — Support Specialist
**Today, Tuesday April 14 at 11:00am PT** | Ops / Support | Tenure: 8 months

**Context**
Jordan owns Tier 1 support ticket triage and resolution at Meridian Ledger. Their role sits at the intersection of customer health and product quality — every unresolved ticket is a signal about where the product or process has friction. Eight months in, Jordan has strong customer relationships but is still building the technical context needed to triage complex integration issues independently.

**Goals Alignment (Q2 2026)**
- Reduce average time-to-first-response to under 4 hours (support team OKR)
- Own the Cascade Retail integration support queue (post-go-live)
- No formal personal OKR doc found in Notion — recommend asking Jordan to bring Q2 priorities

---

**Impact This Week**

- 18 tickets worked, 5 closed (Apr 7–14) — steady volume across billing, reconciliation, portal, and integration issues (Pylon)
- Resolved a p1-high portal registration failure within 6 hours of intake (Pylon #4821, Apr 11)
- Filed and coordinated a Ledgerlink integration bug on behalf of Cascade Retail — bank feed sync failing after plugin upgrade to v0.1.2 (Pylon #4834, Slack Apr 12)
- Added to a new shared Slack channel with Cascade Retail's finance team for real-time integration triage (Slack, Apr 9)

---

**Talking Points**

1. **4 tickets currently "waiting on you" — any stuck on engineering?** #4829 (p2, journal entry display), #4831 (p2, invoice strikethrough), #4836 (p3, GL code config), #4838 (p2, tax ID eligibility). Surface whether any are blocked on an eng escalation vs. customer response.

2. **Cascade Retail Ledgerlink bug #4834 — status.** This is p2-medium and waiting on Jordan's next action. Ledgerlink responded with one question. Is Jordan unblocked? If the AI reconciliation failure is due to oversized transaction history, does this need an engineering ticket?

3. **Technical skills growth check.** Jordan wants to build deeper technical context to triage integration issues faster without needing to escalate. What's the most confusing category of tickets right now? What would help — pairing sessions, documentation, access to staging?

---

**Blockers & Watch Items**
- 1 p1-high ticket on hold (#4822, statement export failure) — last activity 2 days ago. What's holding it?
- Cascade Retail Ledgerlink bug active and customer-visible — needs resolution before weekly sync on Thursday
- No formal Q2 goals in Notion — Jordan may be operating without clear priorities

---

**Open from Last 1-1**
No prior Grain recording found. Recommend asking: "Anything open from last week?"

---

**Sources**
Grain: 0 direct 1-1s | Slack: 12 threads (Apr 7–14) | Notion: 1 doc | Pylon: **18 tickets** (5 closed, 4 waiting-on-you, 1 p1-high on hold) | Calendar: confirmed

[SIMULATED — all data derived from test context]

---

## Test B Output (Pylon unavailable)

```
⚠️  Can't prep this 1-1 — Pylon is unavailable.

Jordan Chen works in Support. Their primary system of record is Pylon — without it,
the brief would be missing ticket volume, resolution rate, open items, and priority
breakdowns that represent the majority of observable work for this role.

To fix: Re-auth Pylon by running /chief and completing the OAuth flow when prompted.

Proceed anyway without Pylon data? (yes / no)
```
