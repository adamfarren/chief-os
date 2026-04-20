# MCP Health Check — Test Scenarios

Tests for the session startup health check that fires on the first `/chief` invocation.

The hook lives at `hooks/mcp-check.py` and is registered as a `UserPromptSubmit` hook in `~/.claude/settings.json`.

---

## Test 1: All servers healthy

**Prompt:** `/chief pipeline update`

**Setup:** All MCP servers connected and authenticated. `gws` CLI installed and authed.

**Expected behavior:**
1. Health check table printed first, all `[ OK ]`
2. Immediately proceeds to run `/chief-pipeline` — no pause, no questions

**Expected output:**
```
MCP Health Check
─────────────────────────────
Notion    [ OK ]
Slack     [ OK ]
HubSpot   [ OK ]
Grain     [ OK ]
Figma     [ OK ]
Pylon     [ OK ]
Jira      [ OK ]
Gmail     [ OK ]
GCal      [ OK ]
GDrive    [ OK ]
─────────────────────────────
```
Then pipeline output follows immediately.

---

## Test 2: One MCP server down

**Prompt:** `/chief what happened in customer meetings today`

**Setup:** Grain MCP is disconnected (auth expired or not configured).

**Expected behavior:**
1. Health check table printed with Grain `[ DOWN ]`
2. Lists which server failed: "Grain is unavailable — meeting transcripts and digest data will be missing."
3. Asks: "Proceed anyway, or fix the Grain connection first?"
4. Does NOT auto-proceed to `/chief-digest`

**Expected output:**
```
MCP Health Check
─────────────────────────────
Notion    [ OK ]
Slack     [ OK ]
HubSpot   [ OK ]
Grain     [ DOWN ]
Figma     [ OK ]
Pylon     [ OK ]
Jira      [ OK ]
Gmail     [ OK ]
GCal      [ OK ]
GDrive    [ OK ]
─────────────────────────────

Grain is down — meeting transcripts and digest data won't be available.
Proceed anyway, or fix the connection first?
```

---

## Test 3: gws CLI not installed

**Prompt:** `/chief what's on my calendar tomorrow`

**Setup:** `gws` binary is not installed or not in PATH.

**Expected behavior:**
1. Gmail, GCal, and GDrive all marked `[ DOWN ]`
2. Explains that gws CLI is required for Google Workspace tools
3. Provides install hint or asks whether to proceed

**Expected output:**
```
MCP Health Check
─────────────────────────────
...
Gmail     [ DOWN ]
GCal      [ DOWN ]
GDrive    [ DOWN ]
─────────────────────────────

Gmail, GCal, and GDrive are down — gws CLI is not installed or not in PATH.
Install: https://github.com/nicholasgasior/gws
Proceed anyway, or fix the connection first?
```

---

## Test 4: Health check runs only once per session

**Prompt 1:** `/chief pipeline update` → health check runs, table printed
**Prompt 2:** `/chief what shipped this sprint` → health check does NOT run again

**Expected behavior:**
- Second `/chief` invocation proceeds directly to `/chief-roadmap` — no duplicate health check table
- The `UserPromptSubmit` hook uses a session-scoped lockfile (`/tmp/.claude_mcp_validated_<session_id>`) to enforce this

---

## Test 5: Non-chief prompts skip the check

**Prompt:** `what is 2 + 2`

**Expected behavior:** No health check table printed. Hook exits early (prompt does not start with `/chief`).

---

## Test 6: GDrive-specific — auth expired

**Prompt:** `/chief find the board deck from last quarter`

**Setup:** gws is installed but Google Drive OAuth token has expired.

**Expected behavior:**
1. GDrive marked `[ DOWN ]` (other Google services may still be OK if their tokens are separate)
2. Message: "GDrive auth has expired — run `gws auth login` to re-authenticate."
3. Asks whether to proceed

---

## Success Criteria

| # | Criterion | Pass Condition |
|---|-----------|---------------|
| 1 | Table prints before any substantive output | Health check appears as first content in every `/chief` response |
| 2 | All-OK continues immediately | No confirmation prompt when all servers are healthy |
| 3 | Any DOWN prompts user | User is asked to proceed or fix before substantive work begins |
| 4 | Dedup works across same session | Second `/chief` call in same session skips the check |
| 5 | Non-chief prompts unaffected | Regular conversation prompts produce no health check output |
| 6 | GDrive tested via gws CLI | `gws drive about get --params '{"fields": "user"}'` used (not an MCP tool) |
| 7 | 10 servers checked | Notion, Slack, HubSpot, Grain, Figma, Pylon, Jira, Gmail, GCal, GDrive |
