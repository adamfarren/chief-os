---
name: claude-usage
description: Pull the latest Claude Usage report from Slack, add it as a new tab to the usage spreadsheet, and run the weekly insights analysis. Use when asked "claude usage", "usage report", "add usage tab", "usage analysis", or "how is the team using claude". Reads the automated weekly canvas from your engineering leadership Slack channel, writes to a Google Sheet, and produces a tiered performance memo.
user-invocable: true
---

# Claude Usage — Weekly Ingestion + Analysis

You ingest the latest Claude usage report from Slack and produce a tiered performance analysis across all historical weeks.

## Setup (One-Time)

Before first use, configure the constants below in your local copy of this skill:

| Item | How to Set |
|------|-----------|
| `SPREADSHEET_ID` | Create a Google Sheet and copy the ID from the URL |
| `SLACK_CHANNEL_ID` | Right-click your source channel in Slack → Copy link → extract the channel ID |
| `COMPANY_DOMAIN` | Your company email domain (e.g., `yourcompany.com`) |
| Sheets auth token | Run `python3 ~/sheets_auth.py` once to authenticate (see auth setup below) |

### Auth Setup

Create `~/sheets_auth.py` with your GCP project's OAuth client credentials:

```python
#!/usr/bin/env python3
import os, pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CLIENT_SECRET = os.path.expanduser('~/.config/gws/client_secret.json')
TOKEN_FILE = os.path.expanduser('~/.config/gws/sheets_token.pkl')

def get_creds():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as f:
            return pickle.load(f)
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
    creds = flow.run_local_server(port=0)
    with open(TOKEN_FILE, 'wb') as f:
        pickle.dump(creds, f)
    return creds

creds = get_creds()
service = build('sheets', 'v4', credentials=creds)
SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID'
meta = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID, fields='sheets.properties').execute()
print([s['properties']['title'] for s in meta['sheets']])
print("Auth successful!")
```

Requires: `pip install google-auth google-auth-oauthlib google-api-python-client`

## Constants

Replace these with your values:

```
SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID'
SLACK_CHANNEL_ID = 'YOUR_CHANNEL_ID'        # e.g., C01ABCDEF23
COMPANY_DOMAIN = 'yourcompany.com'
TOKEN_FILE = '~/.config/gws/sheets_token.pkl'
```

## Expected Slack Source

This skill expects an automated bot to post a weekly Claude usage canvas in a Slack channel. The canvas should contain a table with per-user metrics. The default column format from the Claude Code usage reporting bot is:

`User | CC Sessions | Lines +/- | Commits | CC Cost | Inv Sessions | Inv Runs | Inv Turns | Inv Cost`

Where:
- **CC** = Claude Code (the IDE tool)
- **Inv** = Investigator (the AI search/research tool)
- `api:*` rows = automated accounts, not individual users

The bot message pattern to search for: `:chart_with_upwards_trend: *Claude Usage:*`

## Step 1 — Find the Canvas

Search Slack for the most recent Claude usage report:

```
slack_search_public_and_private:
  query: "Claude Usage in:<SLACK_CHANNEL_ID>"
  sort: timestamp
  sort_dir: desc
  include_bots: true
  limit: 5
```

From the results, identify:
- The **period** (e.g., `2026-04-06 to 2026-04-13`) from the message text
- The **canvas ID** from the linked URL (`https://app.slack.com/docs/<WORKSPACE_ID>/<CANVAS_ID>`)

If the user specified a date range, match against that. Otherwise use the most recent result.

**Check for duplicates first:** Before writing, verify a tab with this period name doesn't already exist in the spreadsheet. If it does, skip Step 3 and go straight to Step 4 (analysis only).

## Step 2 — Read the Canvas

```
slack_read_canvas: canvas_id=<CANVAS_ID>
```

Parse from the canvas markdown:
- **Period string** — e.g., `2026-04-06 to 2026-04-13`
- **Total spend line** — e.g., `Total spend: $6,765.99 (includes $188.60 investigator)`
- **Data table** — the full user table with all 9 columns

Capture all rows including `Automated (alerts)`. Skip the header row itself.

## Step 3 — Write the New Tab

Use Bash to run a Python script that creates and populates the tab:

```python
import pickle
from googleapiclient.discovery import build

TOKEN_FILE = '/Users/you/.config/gws/sheets_token.pkl'  # adjust path
with open(TOKEN_FILE, 'rb') as f:
    creds = pickle.load(f)

service = build('sheets', 'v4', credentials=creds)
SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID'
SHEET = '<PERIOD_STRING>'   # e.g., '2026-04-06 to 2026-04-13'

# 1. Create tab at position 0 (newest first)
resp = service.spreadsheets().batchUpdate(
    spreadsheetId=SPREADSHEET_ID,
    body={"requests": [{"addSheet": {"properties": {"title": SHEET, "index": 0}}}]}
).execute()
sheet_id = resp['replies'][0]['addSheet']['properties']['sheetId']

# 2. Write data — header block + data rows + footer
rows = [
    [SHEET, '', '', '', '', '', '', '', ''],
    [TOTAL_SPEND_STRING, '', '', '', '', '', '', '', ''],
    [],
    ['User', 'CC Sessions', 'Lines +/-', 'Commits', 'CC Cost',
     'Inv Sessions', 'Inv Runs', 'Inv Turns', 'Inv Cost'],
    # ... data rows from canvas, in canvas order ...
    [],
    ['Claude.ai Teams usage is not included — the Teams plan does not expose an API. '
     'Review manually at console.anthropic.com.'],
]
service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range=f"'{SHEET}'!A1",
    valueInputOption='USER_ENTERED',
    body={'values': rows}
).execute()

# 3. Format: bold rows 1-2, dark header row 4 (index 3), freeze, auto-resize, italic footer
total_rows = len(rows)
header_row = 3   # 0-indexed

requests = [
    {"repeatCell": {   # bold period title
        "range": {"sheetId": sheet_id, "startRowIndex": 0, "endRowIndex": 1,
                  "startColumnIndex": 0, "endColumnIndex": 9},
        "cell": {"userEnteredFormat": {"textFormat": {"bold": True, "fontSize": 12}}},
        "fields": "userEnteredFormat.textFormat"
    }},
    {"repeatCell": {   # bold total spend
        "range": {"sheetId": sheet_id, "startRowIndex": 1, "endRowIndex": 2,
                  "startColumnIndex": 0, "endColumnIndex": 9},
        "cell": {"userEnteredFormat": {"textFormat": {"bold": True}}},
        "fields": "userEnteredFormat.textFormat"
    }},
    {"repeatCell": {   # dark header row with white text
        "range": {"sheetId": sheet_id, "startRowIndex": header_row, "endRowIndex": header_row + 1,
                  "startColumnIndex": 0, "endColumnIndex": 9},
        "cell": {"userEnteredFormat": {
            "textFormat": {"bold": True, "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}},
            "backgroundColor": {"red": 0.204, "green": 0.204, "blue": 0.204},
        }},
        "fields": "userEnteredFormat(textFormat,backgroundColor)"
    }},
    {"updateSheetProperties": {   # freeze through header
        "properties": {"sheetId": sheet_id, "gridProperties": {"frozenRowCount": header_row + 1}},
        "fields": "gridProperties.frozenRowCount"
    }},
    {"autoResizeDimensions": {   # auto-resize columns
        "dimensions": {"sheetId": sheet_id, "dimension": "COLUMNS",
                       "startIndex": 0, "endIndex": 9}
    }},
    {"repeatCell": {   # italic footer
        "range": {"sheetId": sheet_id, "startRowIndex": total_rows - 1, "endRowIndex": total_rows,
                  "startColumnIndex": 0, "endColumnIndex": 9},
        "cell": {"userEnteredFormat": {"textFormat": {"italic": True}, "wrapStrategy": "WRAP"}},
        "fields": "userEnteredFormat(textFormat,wrapStrategy)"
    }},
]
service.spreadsheets().batchUpdate(
    spreadsheetId=SPREADSHEET_ID, body={"requests": requests}
).execute()
```

**If the script fails** with a token error, tell the user:
> "Sheets auth token is expired. Run `python3 ~/sheets_auth.py` to refresh it, then try again."

## Step 4 — Pull Historical Data

Read all existing tabs to get multi-week context for the analysis:

```python
meta = service.spreadsheets().get(
    spreadsheetId=SPREADSHEET_ID, fields='sheets.properties'
).execute()

tabs = [s['properties']['title'] for s in meta['sheets']]
all_data = {}
for tab in tabs:
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, range=f"'{tab}'"
    ).execute()
    all_data[tab] = result.get('values', [])
```

Note: If you're migrating from an older 7-column format (`User | Sessions | Lines +/- | Commits | PRs | Accept Rate | Est. Cost`), map `Sessions` → `CC Sessions` and `Est. Cost` → `CC Cost` when normalizing. Treat `Inv Cost` as `$0.00` for those weeks.

## Step 5 — Run the Analysis

Apply the `chief-performance` tier framework across all weeks.

### Normalization

- Strip `api:` prefix rows from tier analysis — classify separately as "Automated Accounts"
- Strip external accounts (non-company-domain emails) — note them but don't tier
- Parse `$` cost strings to floats for calculation

### Tier Framework

| Tier | Label | Weekly CC Cost | Consistency |
|------|-------|----------------|-------------|
| 1 | Heavy Adoption | ≥$200/wk avg | ≥5 of last 7 weeks |
| 2 | Moderate Adoption | $75–$200/wk avg | ≥4 of last 7 weeks |
| 3 | Light Adoption | $15–$75/wk avg | Sporadic |
| 4 | Minimal Adoption | <$15/wk avg | Rare |

Adjust thresholds based on your team size. For smaller teams (< 10 engineers), scale down proportionally.

Use trend (accelerating / stable / decelerating) as a secondary signal. A $50/week person with 4 consecutive weeks of growth is more interesting than a flat $200/week person.

### Output Structure

```
# Claude Usage: <PERIOD>

**Total spend: $X,XXX (includes $XXX investigator)**

## Executive Summary
3-4 sentences: overall spend trend vs. prior week, biggest mover up, biggest mover down, one structural pattern.

## This Week at a Glance

| Metric | This Week | Prior Week | Trend |
|--------|-----------|------------|-------|
| Total Spend | | | |
| Human CC Spend | | | |
| Automated API Spend | | | |
| Investigator Spend | | | |
| Active Human Users | | | |

## Tier Breakdown

### Tier 1 — Heavy Adoption (N people)
| Name | This Week | N-Wk Avg | Trend | Notable |
|------|-----------|----------|-------|---------|

### Tier 2 — Moderate Adoption (N people)
...

### Tier 3 — Light Adoption (N people)
...

### Tier 4 — Minimal Adoption (N people)
...

### Automated Accounts
| Account | Sessions | CC Cost | Purpose (inferred) |
|---------|----------|---------|-------------------|

## Patterns

**Accelerators** — People whose spend increased >50% week-over-week.
**Decelerators** — People whose spend dropped >40% week-over-week.
**Cost outliers** — Anyone with unusually high cost-per-session (>$30/session).
**New adopters** — People appearing for the first time.
**Investigator usage** — Top Investigator users and what it signals.

## Recommendations

1. **[Action]** — Owner: [person]. [Why. Expected impact.]
(3–5 recommendations, specific and named)

---
*Data caveats: Claude.ai Teams usage not captured. [Note any missing columns.]*
```

## Step 6 — Post to Slack Thread

After producing the analysis, post a condensed version as a reply to the original canvas message in the source Slack channel.

Use `slack_send_message` with:
- `channel_id`: the source channel
- `thread_ts`: the timestamp of the Platform Automation bot message that linked the canvas
- `reply_broadcast`: false (keep it in the thread)

Format for Slack mrkdwn — no `---` horizontal rules (they cause validation errors). Use blank lines between sections instead. Keep under 4000 chars. Structure:

```
*Claude Usage Analysis: [Period]* | <SPREADSHEET_URL|Full Spreadsheet>

*$X,XXX total — [record/+N% vs. last week]*
$X human CC · $X automated APIs · $X investigator

*Tier 1 — Heavy Adoption*
• *name* $X ↑↓→ — one-line note

*Tier 2 — Moderate Adoption*
• *name* $X ↑↓→ — one-line note
...

*Tier 3 — Light Adoption*
name $X · name $X · ...

*New this week:* name ($X, N sessions) · ...

*Automated APIs:* api:name $X · ...

*Top Recommendations*

1. *Action* — why it matters.
2. ...
(3–5 max)
```

Use ↑↑ for >50% growth, ↑ for 10–50%, → for flat, ↓ for -10 to -40%, ↓↓ for >40% decline.

## Rules

- **Always check for existing tab before writing.** If the tab exists, skip creation, go straight to analysis.
- **Preserve canvas order** in the tab — don't re-sort rows. The canvas already sorts by CC Cost descending.
- **Include Automated (alerts) row** — it carries Investigator data for the alerting system.
- **External accounts** — include in the tab but exclude from tier analysis.
- **Never fabricate spend numbers.** If a week's data is missing for a person, mark as `—` not `$0`.
- **Link the spreadsheet** in your output so the user can verify.

## MCP Dependencies

| Tool | Role | Required? |
|------|------|-----------|
| Slack MCP | Find and read the usage canvas | Required |
| Bash (Python + google-api-python-client) | Write and read Google Sheets | Required |
| `~/sheets_auth.py` | Auth setup (run once if token missing) | Setup only |
