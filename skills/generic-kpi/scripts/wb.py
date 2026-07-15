import os
WD=os.environ.get("GKPI_WORKDIR","/tmp/generic-kpi")
"""Helpers to drive Google Sheets via the authenticated `gws` CLI."""
import json, subprocess, tempfile, os

SID_FILE = f"{WD}/spreadsheet_id.txt"

def _run(args):
    p = subprocess.run(args, capture_output=True, text=True)
    out = p.stdout
    if "{" in out:
        out = out[out.index("{"):]
    if p.returncode != 0 and not out.strip().startswith("{"):
        raise RuntimeError(f"gws failed: {p.returncode}\n{p.stderr}\n{p.stdout[:800]}")
    try:
        res = json.loads(out)
    except Exception:
        raise RuntimeError(f"bad json from gws:\n{p.stdout[:800]}\n{p.stderr[:400]}")
    if isinstance(res, dict) and "error" in res:
        raise RuntimeError(f"API error: {json.dumps(res['error'])[:600]}")
    return res

def _json_arg(body):
    # pass large bodies via a temp file substitution is not possible; gws takes a string.
    return json.dumps(body)

def create(title, sheet_titles):
    """Create a spreadsheet with the given tab titles. Returns (sid, {title: sheetId})."""
    body = {"properties": {"title": title},
            "sheets": [{"properties": {"title": t, "gridProperties": {"rowCount": 400, "columnCount": 60}}}
                       for t in sheet_titles]}
    r = _run(["gws", "sheets", "spreadsheets", "create", "--json", _json_arg(body),
              "--params", json.dumps({"fields": "spreadsheetId,sheets.properties(sheetId,title)"})])
    sid = r["spreadsheetId"]
    gids = {s["properties"]["title"]: s["properties"]["sheetId"] for s in r["sheets"]}
    open(SID_FILE, "w").write(sid)
    return sid, gids

def set_values(sid, value_ranges):
    """value_ranges: list of {'range': 'Tab!A1', 'values': [[...],...]} — USER_ENTERED."""
    # chunk to keep each request modest
    for i in range(0, len(value_ranges), 8):
        chunk = value_ranges[i:i+8]
        body = {"valueInputOption": "USER_ENTERED", "data": chunk}
        _run(["gws", "sheets", "spreadsheets", "values", "batchUpdate", "--json", _json_arg(body),
              "--params", json.dumps({"spreadsheetId": sid})])

def batch(sid, requests):
    """Send spreadsheets.batchUpdate requests, chunked."""
    for i in range(0, len(requests), 25):
        chunk = requests[i:i+25]
        body = {"requests": chunk}
        _run(["gws", "sheets", "spreadsheets", "batchUpdate", "--json", _json_arg(body),
              "--params", json.dumps({"spreadsheetId": sid})])

def col(n):
    """0-based column index -> A1 letter."""
    s = ""; n += 1
    while n:
        n, r = divmod(n - 1, 26); s = chr(65 + r) + s
    return s

# ---- colors ----
def rgb(r, g, b): return {"red": r, "green": g, "blue": b}
NAVY   = rgb(0.122, 0.204, 0.333)
BLUE   = rgb(0.259, 0.459, 0.710)
GREEN  = rgb(0.851, 0.918, 0.827)
GRAY   = rgb(0.921, 0.921, 0.921)
YELLOW = rgb(1.0, 0.949, 0.8)
WHITE  = rgb(1, 1, 1)
LTGRAY = rgb(0.965, 0.965, 0.965)

def gridrange(gid, r1, r2, c1, c2):
    return {"sheetId": gid, "startRowIndex": r1, "endRowIndex": r2,
            "startColumnIndex": c1, "endColumnIndex": c2}

def cellfmt(gid, r1, r2, c1, c2, *, bg=None, bold=None, fg=None, size=None,
            numfmt=None, halign=None, valign=None, wrap=None, italic=None):
    cell = {}; fields = []
    fmt = {}
    if bg is not None: fmt["backgroundColor"] = bg; fields.append("backgroundColor")
    tf = {}
    if bold is not None: tf["bold"] = bold
    if italic is not None: tf["italic"] = italic
    if fg is not None: tf["foregroundColor"] = fg
    if size is not None: tf["fontSize"] = size
    tf["fontFamily"] = "Calibri"
    fmt["textFormat"] = tf; fields.append("textFormat")
    if numfmt is not None:
        fmt["numberFormat"] = {"type": numfmt[0], "pattern": numfmt[1]}; fields.append("numberFormat")
    if halign is not None: fmt["horizontalAlignment"] = halign; fields.append("horizontalAlignment")
    if valign is not None: fmt["verticalAlignment"] = valign; fields.append("verticalAlignment")
    if wrap is not None: fmt["wrapStrategy"] = wrap; fields.append("wrapStrategy")
    return {"repeatCell": {"range": gridrange(gid, r1, r2, c1, c2),
            "cell": {"userEnteredFormat": fmt},
            "fields": "userEnteredFormat(" + ",".join(fields) + ")"}}

def colwidth(gid, c1, c2, px):
    return {"updateDimensionProperties": {"range": {"sheetId": gid, "dimension": "COLUMNS",
            "startIndex": c1, "endIndex": c2}, "properties": {"pixelSize": px}, "fields": "pixelSize"}}

def merge(gid, r1, r2, c1, c2):
    return {"mergeCells": {"range": gridrange(gid, r1, r2, c1, c2), "mergeType": "MERGE_ALL"}}

def freeze(gid, rows=0, cols=0):
    gp = {}; fields = []
    if rows: gp["frozenRowCount"] = rows; fields.append("gridProperties.frozenRowCount")
    if cols: gp["frozenColumnCount"] = cols; fields.append("gridProperties.frozenColumnCount")
    return {"updateSheetProperties": {"properties": {"sheetId": gid, "gridProperties": gp},
            "fields": ",".join(fields)}}

def hide_sheet(gid, hidden=True):
    return {"updateSheetProperties": {"properties": {"sheetId": gid, "hidden": hidden}, "fields": "hidden"}}

def hide_cols(gid, c1, c2):
    return {"updateDimensionProperties": {"range": {"sheetId": gid, "dimension": "COLUMNS",
            "startIndex": c1, "endIndex": c2}, "properties": {"hiddenByUser": True}, "fields": "hiddenByUser"}}

def tabcolor(gid, color):
    return {"updateSheetProperties": {"properties": {"sheetId": gid, "tabColor": color}, "fields": "tabColor"}}

# ---- month-add robustness: dynamic "latest / prior month" references ----
# The month grid lives in columns E.. (headers are real dates in row 1). These helpers
# build formula fragments that resolve the LATEST / PRIOR month column BY DATE, so every
# downstream formula keeps working when a new month column is added — no fixed "AT" pins.
# `tab` is the quoted sheet ref WITHOUT "!"  e.g.  CM = "'Customers — MRR'".
# Use these for any cross-tab "this month / last month" reference and for per-customer
# "current month" cells. Do NOT use them for column-aligned month mirrors (a cell in the
# month grid that references its own column, e.g. Customers — ARR) — those auto-adjust.
def latest(tab, row):
    """Value at `tab`,`row`, latest month column (by header date). Robust to added months."""
    return f"INDEX({tab}!$A:$BZ,{row},MATCH(MAX({tab}!$E$1:$BZ$1),{tab}!$1:$1,0))"
def prior(tab, row):
    """Value at `tab`,`row`, second-latest (prior) month column."""
    return f"INDEX({tab}!$A:$BZ,{row},MATCH(LARGE({tab}!$E$1:$BZ$1,2),{tab}!$1:$1,0))"
def latest_range(tab, r1, r2):
    """Whole latest-month column of `tab` for rows r1..r2 (array, for SUM/SUMPRODUCT/N)."""
    return f"INDEX({tab}!$A${r1}:$BZ${r2},0,MATCH(MAX({tab}!$E$1:$BZ$1),{tab}!$1:$1,0))"
def prior_range(tab, r1, r2):
    return f"INDEX({tab}!$A${r1}:$BZ${r2},0,MATCH(LARGE({tab}!$E$1:$BZ$1,2),{tab}!$1:$1,0))"
def colbyname(tab, row, header):
    """Value at `tab`,`row`, column whose row-1 header == `header` (e.g. 'Disc %','Bill Freq').
    Robust to structural columns shifting when a month is inserted."""
    return f'INDEX({tab}!$A:$BZ,{row},MATCH("{header}",{tab}!$1:$1,0))'
# Same-sheet variants (no tab prefix) — for MoM-Growth columns on the data tabs themselves.
def latest_self(row): return f"INDEX($A:$BZ,{row},MATCH(MAX($E$1:$BZ$1),$1:$1,0))"
def prior_self(row):  return f"INDEX($A:$BZ,{row},MATCH(LARGE($E$1:$BZ$1,2),$1:$1,0))"

# Rank-based refs for RECENT-FIRST tables (row 1 = latest, row 2 = 2nd latest, ...).
# k is the 1-based recency rank (k=1 latest). Robust to added months.
def nth(tab, row, k):
    return f"INDEX({tab}!$A:$BZ,{row},MATCH(LARGE({tab}!$E$1:$BZ$1,{k}),{tab}!$1:$1,0))"
def nth_date(tab, k):
    return f"LARGE({tab}!$E$1:$BZ$1,{k})"
def nth_range(tab, r1, r2, k):
    return f"INDEX({tab}!$A${r1}:$BZ${r2},0,MATCH(LARGE({tab}!$E$1:$BZ$1,{k}),{tab}!$1:$1,0))"

# number format tuples
CUR  = ("NUMBER", "$#,##0")
CUR2 = ("NUMBER", "$#,##0.00")
INT  = ("NUMBER", "#,##0")
PCT  = ("PERCENT", "0.0%")
PCTS = ("NUMBER", '+0.0%;\\-0.0%;"—"')
PPS  = ("NUMBER", '+0.0" pp";\\-0.0" pp";"—"')
DATEF= ("DATE", "mmm yyyy")
