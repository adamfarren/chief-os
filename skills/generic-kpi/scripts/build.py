import os
WD=os.environ.get("GKPI_WORKDIR","/tmp/generic-kpi")
#!/usr/bin/env python3
import json, datetime as dt
import wb
from wb import (col, NAVY, BLUE, GREEN, GRAY, YELLOW, WHITE, LTGRAY, rgb,
                CUR, CUR2, INT, PCT, PCTS, PPS, DATEF)

D = json.load(open(f"{WD}/data.json"))
C = D["customers"]
NC = len(C)
NM = D["n_months"]                     # 42
COMPANY = D["company"]
FIRST_C = 4                            # col E (0-based) = first month
LAST_C = FIRST_C + NM - 1             # col AT
PREV_C = LAST_C - 1
LASTL = col(LAST_C); PREVL = col(PREV_C); FIRSTL = col(FIRST_C)
R0 = 2                                 # first customer row (1-based)
RN = R0 + NC - 1                       # last customer row
def mcol(i):                          # 0-based month index -> col letter
    return col(FIRST_C + i)

# summary rows on Customers — MRR
INPUT_HDR="Customer      ⬇  INPUT — paste / edit your data in the rows below (one row per customer)"
GREEN_TAB=rgb(0.20,0.66,0.33)
SR = dict(MON=RN+5, PAY=RN+6, GROSS=RN+7, DISC=RN+8, NET=RN+9, INV=RN+10, ARR=RN+11, GROW=RN+12, QMRR=RN+13, NETG=RN+14, OMIN=RN+15)

# ============ TAB LIST ============
TABS = [
    "📕 How to Use", "📖 Definitions & Sources", "📊 Combined Summary", "🔍 Compare",
    "📊 Revenue Dashboard", "📊 MRR & ARR Summary", "📊 Usage Summary", "📉 Churn & New Revenue",
    "💳 Autopay Collections", "💵 Revenue → Cash", "⏱ Collections & A/R", "💵 Invoiced Volume",
    "📈 Usage Monthly History", "Over-Min History",
    "Customers — MRR", "Customers — ARR",
    "Usage — MAU per Customer", "Usage — Seats per Customer", "Usage — Active Users per Customer",
    "Minimum MAU", "Pricing Engine",
]
TITLE = f"{COMPANY} — SaaS KPI Dashboard (Sample · Fictional Data)"

print("Creating spreadsheet...")
SID, G = wb.create(TITLE, TABS)
print("SID:", SID)
print("URL: https://docs.google.com/spreadsheets/d/%s/edit" % SID)

vals = []   # value ranges
reqs = []   # format requests
def V(tab, a1, matrix): vals.append({"range": f"'{tab}'!{a1}", "values": matrix})

# ==================================================================
# DATA LAYER — Customers — MRR
# ==================================================================
T = "Customers — MRR"; g = G[T]
# header row
hdr = ["", "Include?", INPUT_HDR, "Rev Start"]
row1 = hdr[:]
row1 += ["" ] * (NM)   # month cells set via formula below
# month header formulas
mrow = [None]*4
for i in range(NM):
    if i == 0: mrow.append("=DATE(2023,1,1)")
    else: mrow.append(f"=EDATE({mcol(i-1)}1,1)")
# lifecycle headers at AY.. (col 50..)
LC = 50  # AY
V(T, "A1", [row1])
V(T, f"E1", [mrow[4:]])
V(T, f"{col(LC)}1", [["Status", "Go-Live", "Churn", "Bill Freq", "Disc %"]])

# customer rows
body = []
for c in C:
    y, m, _ = map(int, c["start_iso"].split("-"))
    r = ["", "Y", c["name"], f"=DATE({y},{m},1)"]
    for i in range(NM):
        v = c["mrr"][i]
        r.append("" if v is None else v)
    body.append(r)
V(T, f"A{R0}", body)
# lifecycle per customer
lc = []
for c in C:
    status = "Churned" if c["churn_i"] is not None else "Live"
    y, m, _ = map(int, c["start_iso"].split("-"))
    golive = f"=DATE({y},{m},1)"
    if c["churn_i"] is not None:
        cy, cm, _ = map(int, c["churn_iso"].split("-"))
        churn = f"=DATE({cy},{cm},1)"
    else:
        churn = ""
    lc.append([status, golive, churn, c["billfreq"], c["disc_pct"]])
V(T, f"{col(LC)}{R0}", lc)

# summary block
def summ_formula_rows():
    rows = {k: [] for k in SR}
    labels = {"PAY":"Paying Customers","GROSS":"Gross MRR (list)","DISC":"Discounts (this month)",
              "NET":"Net MRR (after discounts)","INV":"Net Invoiced this month (timing)",
              "ARR":"Total ARR (gross ×12)","GROW":"NRR Growth %","QMRR":"Quarterly MRR (helper)",
              "MON":"Month","NETG":"NRR Growth","OMIN":"% Customers over MAU Min"}
    # build per-month formula lists
    data = {k: [] for k in SR}
    for i in range(NM):
        X = mcol(i)
        data["MON"].append(f"={X}1")
        data["PAY"].append(f'=COUNTIF({X}{R0}:{X}{RN},">0")')
        data["GROSS"].append(f"=SUM({X}{R0}:{X}{RN})")
        data["DISC"].append(f"=SUMPRODUCT(N({X}{R0}:{X}{RN}),$BC${R0}:$BC${RN})")
        data["QMRR"].append(f'=SUMPRODUCT(N({X}{R0}:{X}{RN}),($BB${R0}:$BB${RN}="Q"))')
        data["NET"].append(f"={X}{SR['GROSS']}-{X}{SR['DISC']}")
        qs = f"OR(MONTH({X}{SR['MON']})=1,MONTH({X}{SR['MON']})=4,MONTH({X}{SR['MON']})=7,MONTH({X}{SR['MON']})=10)"
        data["INV"].append(f"={X}{SR['NET']}-{X}{SR['QMRR']}+IF({qs},3*{X}{SR['QMRR']},0)")
        data["ARR"].append(f"={X}{SR['GROSS']}*12")
        if i == 0:
            data["GROW"].append(""); data["NETG"].append("")
        else:
            data["GROW"].append(f"=IFERROR({X}{SR['ARR']}/{mcol(i-1)}{SR['ARR']}-1,\"\")")
            data["NETG"].append(f"={X}{SR['ARR']}-{mcol(i-1)}{SR['ARR']}")
        data["OMIN"].append(f"=IFERROR(INDEX('Over-Min History'!$D:$D,MATCH({X}1,'Over-Min History'!$A:$A,0)),\"\")")
    return labels, data
labels, sdata = summ_formula_rows()
# write labels in col C and formulas E..AT for each summary row
for k, rownum in SR.items():
    V(T, f"C{rownum}", [[labels[k]]])
    V(T, f"E{rownum}", [sdata[k]])

# ---------- formatting: Customers — MRR ----------
reqs += [
    wb.colwidth(g, 0, 1, 24), wb.colwidth(g, 1, 2, 70), wb.colwidth(g, 2, 3, 220),
    wb.colwidth(g, 3, 4, 90), wb.colwidth(g, 4, LAST_C+1, 82),
    wb.colwidth(g, LC, LC+5, 84),
    wb.freeze(g, rows=1, cols=3),
    wb.cellfmt(g, 0, 1, 0, LC+5, bg=NAVY, bold=True, fg=WHITE, size=10, halign="CENTER"),
    wb.cellfmt(g, 0, 1, 4, LAST_C+1, bg=NAVY, bold=True, fg=WHITE, numfmt=DATEF, halign="CENTER"),
    wb.cellfmt(g, R0-1, RN, 4, LAST_C+1, numfmt=CUR),
    wb.cellfmt(g, R0-1, RN, 3, 4, numfmt=DATEF),
    wb.cellfmt(g, R0-1, RN, LC+1, LC+3, numfmt=DATEF),   # go-live, churn
    wb.cellfmt(g, R0-1, RN, LC+4, LC+5, numfmt=PCT),      # disc %
    # --- monthly totals block ---
    # navy separator bar one row above the totals (C frozen + D:AT merged, no freeze conflict)
    wb.merge(g, SR["MON"]-2, SR["MON"]-1, 3, LAST_C+1),
    wb.cellfmt(g, SR["MON"]-2, SR["MON"]-1, 2, LAST_C+1, bg=NAVY, bold=True, fg=WHITE, size=11, valign="MIDDLE"),
    # label-column band + bold; separator line above the block
    wb.cellfmt(g, SR["MON"]-1, SR["OMIN"], 2, 3, bg=rgb(0.94,0.94,0.94), bold=True),
    wb.cellfmt(g, SR["NETG"]-1, SR["NETG"], 4, LAST_C+1, numfmt=("NUMBER","$#,##0;[Red]-$#,##0")),
    wb.cellfmt(g, SR["OMIN"]-1, SR["OMIN"], 4, LAST_C+1, numfmt=PCT),
    {"updateBorders": {"range": wb.gridrange(g, SR["MON"]-1, SR["MON"], 2, LAST_C+1),
        "top": {"style": "SOLID_MEDIUM", "color": rgb(0.4,0.4,0.4)}}},
    wb.cellfmt(g, SR["GROSS"]-1, SR["GROSS"], 4, LAST_C+1, numfmt=CUR),
    wb.cellfmt(g, SR["DISC"]-1, SR["INV"], 4, LAST_C+1, numfmt=CUR),
    wb.cellfmt(g, SR["ARR"]-1, SR["ARR"], 4, LAST_C+1, numfmt=CUR),
    wb.cellfmt(g, SR["NET"]-1, SR["NET"], 4, LAST_C+1, numfmt=CUR, bold=True),  # values clean
    wb.cellfmt(g, SR["NET"]-1, SR["NET"], 2, 3, bg=GREEN, bold=True),           # green flag on label only
    wb.cellfmt(g, SR["GROW"]-1, SR["GROW"], 4, LAST_C+1, numfmt=PCTS),
    wb.cellfmt(g, SR["PAY"]-1, SR["PAY"], 4, LAST_C+1, numfmt=INT),
    wb.tabcolor(g, GREEN_TAB),
    wb.cellfmt(g, 0, 1, 2, 3, wrap="WRAP", valign="MIDDLE"),  # wrap the input-header instruction
    {"updateDimensionProperties":{"range":{"sheetId":g,"dimension":"ROWS","startIndex":0,"endIndex":1},"properties":{"pixelSize":46},"fields":"pixelSize"}},
]
# a friendly label in the separator bar
V(T, f"C{SR['MON']-1}", [["▼  MONTHLY TOTALS  (all customers)"]])
# gray out churned rows
for idx, c in enumerate(C):
    if c["churn_i"] is not None:
        rr = R0 + idx
        reqs.append(wb.cellfmt(g, rr-1, rr, 1, LC+5, bg=rgb(0.87,0.87,0.87)))
# hide disc-% helper col + the Quarterly-MRR helper row
reqs.append(wb.hide_cols(g, LC+4, LC+5))
reqs.append({"updateDimensionProperties": {"range": {"sheetId": g, "dimension": "ROWS",
    "startIndex": SR["QMRR"]-1, "endIndex": SR["QMRR"]}, "properties": {"hiddenByUser": True}, "fields": "hiddenByUser"}})

print("Prepared Customers — MRR")

# ==================================================================
# DATA LAYER — Customers — ARR (×12 mirror)
# ==================================================================
T = "Customers — ARR"; g = G[T]
V(T, "A1", [["", "Include?", "Customer", "Rev Start"]])
V(T, "E1", [mrow[4:]])
arr_body = []
for idx, c in enumerate(C):
    r = ["", "Y", f"='Customers — MRR'!C{R0+idx}", f"='Customers — MRR'!D{R0+idx}"]
    for i in range(NM):
        X = mcol(i)
        r.append(f'=IF(\'Customers — MRR\'!{X}{R0+idx}="","",\'Customers — MRR\'!{X}{R0+idx}*12)')
    arr_body.append(r)
V(T, f"A{R0}", arr_body)
# summary ARR row
arr_tot = [f"='Customers — MRR'!{mcol(i)}{SR['ARR']}" for i in range(NM)]
V(T, f"C{RN+7}", [["Total ARR (gross)"]])
V(T, f"E{RN+7}", [arr_tot])
reqs += [
    wb.colwidth(g, 0,1,24), wb.colwidth(g,1,2,70), wb.colwidth(g,2,3,220),
    wb.colwidth(g,3,4,90), wb.colwidth(g,4,LAST_C+1,90), wb.freeze(g,rows=1,cols=3),
    wb.cellfmt(g,0,1,0,LAST_C+1,bg=NAVY,bold=True,fg=WHITE,size=10,halign="CENTER"),
    wb.cellfmt(g,0,1,4,LAST_C+1,bg=NAVY,bold=True,fg=WHITE,numfmt=DATEF,halign="CENTER"),
    wb.cellfmt(g,R0-1,RN,4,LAST_C+1,numfmt=CUR),
    wb.cellfmt(g,RN+6,RN+7,4,LAST_C+1,numfmt=CUR),
    wb.cellfmt(g,RN+6,RN+7,2,3,bold=True),
    wb.tabcolor(g, rgb(0.4,0.4,0.4)),
]
print("Prepared Customers — ARR")

# ==================================================================
# DATA LAYER — Usage per-customer tabs (MAU / Seats / Active Users)
# ==================================================================
def usage_tab(T, key, unit, with_min=False):
    g = G[T]
    V(T, "A1", [["", INPUT_HDR, "", "Min " + unit if with_min else ""]])
    V(T, "E1", [mrow[4:]])
    b = []
    for c in C:
        r = ["", c["name"], "", (c["min_mau"] if with_min else "")]
        for i in range(NM):
            v = c[key][i]
            r.append("" if v is None else v)
        b.append(r)
    V(T, f"A{R0}", b)
    # TOTAL row
    tr = RN + 3
    V(T, f"B{tr}", [["TOTAL"]])
    V(T, f"E{tr}", [[f"=SUM({mcol(i)}{R0}:{mcol(i)}{RN})" for i in range(NM)]])
    reqs.extend([
        wb.colwidth(g,0,1,24), wb.colwidth(g,1,2,220), wb.colwidth(g,2,3,20),
        wb.colwidth(g,3,4,90), wb.colwidth(g,4,LAST_C+1,80), wb.freeze(g,rows=1,cols=2),
        wb.cellfmt(g,0,1,0,LAST_C+1,bg=NAVY,bold=True,fg=WHITE,size=10,halign="CENTER"),
        wb.cellfmt(g,0,1,4,LAST_C+1,bg=NAVY,bold=True,fg=WHITE,numfmt=DATEF,halign="CENTER"),
        wb.cellfmt(g,R0-1,RN,4,LAST_C+1,numfmt=INT),
        wb.cellfmt(g,R0-1,RN,3,4,numfmt=INT),
        wb.cellfmt(g,tr-1,tr,1,LAST_C+1,bold=True,numfmt=INT),
        wb.tabcolor(g, GREEN_TAB), wb.colwidth(g,1,2,250),
        wb.cellfmt(g,0,1,1,2,wrap="WRAP",valign="MIDDLE"),
        {"updateDimensionProperties":{"range":{"sheetId":g,"dimension":"ROWS","startIndex":0,"endIndex":1},"properties":{"pixelSize":46},"fields":"pixelSize"}},
    ])
    for idx, c in enumerate(C):
        if c["churn_i"] is not None:
            rr = R0+idx; reqs.append(wb.cellfmt(g,rr-1,rr,1,LAST_C+1,bg=rgb(0.87,0.87,0.87)))
    return tr

MAU_TOTAL = usage_tab("Usage — MAU per Customer", "mau", "MAU", with_min=True)
usage_tab("Usage — Seats per Customer", "seats", "Seats")
usage_tab("Usage — Active Users per Customer", "users", "Users")
print("Prepared Usage tabs")

# ==================================================================
# DATA LAYER — Minimum MAU + Pricing Engine
# ==================================================================
T = "Minimum MAU"; g = G[T]
V(T, "A1", [[INPUT_HDR, "Min MAU", "Current MAU", "Over Min?", "Headroom"]])
mb = []
for idx, c in enumerate(C):
    r = c["name"]; row = R0+idx
    mb.append([c["name"], c["min_mau"],
               "=" + wb.latest("'Usage — MAU per Customer'", row),
               f"=IF(N(C{R0+idx})>=B{R0+idx},TRUE,FALSE)",
               f"=IFERROR(C{R0+idx}-B{R0+idx},\"\")"])
V(T, f"A{R0}", mb)
reqs += [wb.colwidth(g,0,1,220), wb.colwidth(g,1,5,110), wb.freeze(g,rows=1),
         wb.cellfmt(g,0,1,0,5,bg=NAVY,bold=True,fg=WHITE,size=10,halign="CENTER"),
         wb.cellfmt(g,R0-1,RN,1,3,numfmt=INT), wb.cellfmt(g,R0-1,RN,4,5,numfmt=INT),
         wb.colwidth(g,0,1,250), wb.cellfmt(g,0,1,0,1,wrap="WRAP",valign="MIDDLE"),
         {"updateDimensionProperties":{"range":{"sheetId":g,"dimension":"ROWS","startIndex":0,"endIndex":1},"properties":{"pixelSize":46},"fields":"pixelSize"}},
         wb.tabcolor(g, GREEN_TAB)]
print("Prepared Minimum MAU")

T = "Pricing Engine"; g = G[T]
V(T, "A1", [["Customer","Model","Monthly Base","Included MAU","Overage Rate ($/MAU)","Min MAU","Bill Freq","Current MRR (from Customers)"]])
pb = []
for idx, c in enumerate(C):
    row = R0+idx
    model = "Tiered" if c["tier"]!="Enterprise" else "Committed"
    base = round((c["mrr"][c["start_i"]] or 0)*0.6, -1)
    inc = c["min_mau"]
    rate = round(( (c["mrr"][c["start_i"]] or 1) *0.4)/max(1,c["min_mau"]),3)
    pb.append([c["name"], model, base, inc, rate, c["min_mau"], c["billfreq"],
               "=" + wb.latest("'Customers — MRR'", row)])
V(T, f"A{R0}", pb)
reqs += [wb.colwidth(g,0,1,220), wb.colwidth(g,1,8,120), wb.freeze(g,rows=1),
         wb.cellfmt(g,0,1,0,8,bg=NAVY,bold=True,fg=WHITE,size=10,halign="CENTER",wrap="WRAP"),
         wb.cellfmt(g,R0-1,RN,2,3,numfmt=CUR), wb.cellfmt(g,R0-1,RN,3,4,numfmt=INT),
         wb.cellfmt(g,R0-1,RN,4,5,numfmt=CUR2), wb.cellfmt(g,R0-1,RN,5,6,numfmt=INT),
         wb.cellfmt(g,R0-1,RN,7,8,numfmt=CUR), wb.tabcolor(g, rgb(0.6,0.6,0.6))]
print("Prepared Pricing Engine")

# save state so later sections can extend
json.dump({"SID": SID, "G": G, "SR": SR, "R0": R0, "RN": RN, "NM": NM,
           "LASTL": LASTL, "PREVL": PREVL, "MAU_TOTAL": MAU_TOTAL},
          open(f"{WD}/state.json","w"))

print("Writing values (data layer)...")
wb.set_values(SID, vals)
print("Applying formats (data layer)...")
wb.batch(SID, reqs)
print("DONE data layer.")
