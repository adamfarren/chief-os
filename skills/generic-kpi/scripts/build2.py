import os
WD=os.environ.get("GKPI_WORKDIR","/tmp/generic-kpi")
#!/usr/bin/env python3
"""Build the dashboard/presentation tabs on top of the data layer."""
import json
import wb
from wb import (col, NAVY, BLUE, GREEN, GRAY, YELLOW, WHITE, LTGRAY, rgb,
                CUR, CUR2, INT, PCT, PCTS, PPS, DATEF)

st = json.load(open(f"{WD}/state.json"))
SID = st["SID"]; G = st["G"]; SR = st["SR"]; R0 = st["R0"]; RN = st["RN"]; NM = st["NM"]
LASTL = st["LASTL"]; PREVL = st["PREVL"]
D = json.load(open(f"{WD}/data.json")); C = D["customers"]; COMPANY = D["company"]
FIRST_C = 4
CM = "'Customers — MRR'"; MAU = "'Usage — MAU per Customer'"; SEATS = "'Usage — Seats per Customer'"; USERS = "'Usage — Active Users per Customer'"
MAU_TOT = st["MAU_TOTAL"]  # 39
SEAT_TOT = MAU_TOT; USER_TOT = MAU_TOT  # same TOTAL row layout in each usage tab
def mcol(i): return col(FIRST_C + i)         # 0-based month -> letter
def ML(rr):  return col(FIRST_C + (NM-1) - rr)  # recent-first row -> col letter

vals = []; reqs = []
def V(tab, a1, m): vals.append({"range": f"'{tab}'!{a1}", "values": m})
def banner(g, r, c1, c2, text, color=BLUE):
    reqs.append(wb.merge(g, r-1, r, c1, c2))
    reqs.append(wb.cellfmt(g, r-1, r, c1, c2, bg=color, bold=True, fg=WHITE, size=11, halign="LEFT", valign="MIDDLE"))
def title(g, text_c2):
    reqs.append(wb.merge(g, 0, 1, 0, text_c2))
    reqs.append(wb.cellfmt(g, 0, 1, 0, text_c2, bg=NAVY, bold=True, fg=WHITE, size=14, valign="MIDDLE"))

# =====================================================================
# 📊 MRR & ARR Summary  (months as rows, recent-first)
# =====================================================================
T = "📊 MRR & ARR Summary"; g = G[T]
V(T, "A1", [[f"📊 {COMPANY} — MRR & ARR Summary  (recurring revenue cascade)"]])
hdrs = ["Month","Total ARR (gross)","Total MRR (gross)","Discounts (annual)","Discounts % of ARR",
        "Net ARR (after disc)","Net ARR % of Gross","New Customer ARR","Net Retention MoM","Net Retention T12M"]
V(T, "A2", [hdrs])
rows = []
for rr in range(NM):
    k = rr + 1                                    # recency rank (1 = latest) — robust to added months
    ar = rr + 3
    cur = wb.nth_range(CM, R0, RN, k)             # this month's per-customer MRR column (array)
    prv = wb.nth_range(CM, R0, RN, k+1)           # prior month
    y12 = wb.nth_range(CM, R0, RN, k+12)          # 12 months ago
    row = [
        "=" + wb.nth_date(CM, k),
        "=" + wb.nth(CM, SR['ARR'], k),
        "=" + wb.nth(CM, SR['GROSS'], k),
        "=" + wb.nth(CM, SR['DISC'], k) + "*12",
        f"=IFERROR(D{ar}/B{ar},\"\")",
        f"=B{ar}-D{ar}",
        f"=IFERROR(F{ar}/B{ar},\"\")",
        f"=12*SUMPRODUCT((TEXT({CM}!$D${R0}:$D${RN},\"yyyymm\")=TEXT($A{ar},\"yyyymm\"))*N({cur}))",
    ]
    if rr+1 < NM:
        row.append(f"=IFERROR(SUMPRODUCT(N({cur})*(N({prv})>0))/SUMPRODUCT(N({prv})*(N({prv})>0)),\"\")")
    else: row.append("")
    if rr+12 < NM:
        row.append(f"=IFERROR(SUMPRODUCT(N({cur})*(N({y12})>0))/SUMPRODUCT(N({y12})*(N({y12})>0)),\"\")")
    else: row.append("")
    rows.append(row)
V(T, "A3", rows)
title(g, 10)
reqs += [
    wb.freeze(g, rows=2), wb.colwidth(g,0,1,95), wb.colwidth(g,1,10,120),
    wb.cellfmt(g,1,2,0,10,bg=BLUE,bold=True,fg=WHITE,size=10,halign="CENTER",wrap="WRAP"),
    wb.cellfmt(g,2,NM+2,0,1,numfmt=DATEF,bold=True),
    wb.cellfmt(g,2,NM+2,1,4,numfmt=CUR),
    wb.cellfmt(g,2,NM+2,4,5,numfmt=PCT),
    wb.cellfmt(g,2,NM+2,5,6,numfmt=CUR),
    wb.cellfmt(g,2,NM+2,6,7,numfmt=PCT),
    wb.cellfmt(g,2,NM+2,7,8,numfmt=CUR),
    wb.cellfmt(g,2,NM+2,8,10,numfmt=PCT),
    wb.tabcolor(g, BLUE),
]
S = "📊 MRR & ARR Summary"   # ref name; row 3 = latest, row 4 = prior
print("prepared MRR & ARR Summary")

# =====================================================================
# 📊 Usage Summary
# =====================================================================
T = "📊 Usage Summary"; g = G[T]
V(T,"A1",[[f"👥 {COMPANY} — Usage Summary  (this month: ={CM}!{LASTL}1)".replace(f"={CM}!{LASTL}1","")]])
V(T,"A1",[[f"=\"👥 {COMPANY} — Usage Summary  —  \"&TEXT({wb.latest(CM,1)},\"mmmm yyyy\")"]])
# rows: header=2, data 3..7
usage_block = [
    ["📌 Headline", "", "", "📌 MAU vs Minimum", ""],
    ["Total MAU (this month)", "=" + wb.latest(MAU, MAU_TOT), "", "Customers over MAU min",
        f"=COUNTIF('Minimum MAU'!D{R0}:D{RN},TRUE)"],
    ["Total MAU (prior month)", "=" + wb.prior(MAU, MAU_TOT), "", "% of customers over min",
        f"=IFERROR(E3/B6,\"\")"],
    ["MoM MAU Growth %", "=IFERROR(B3/B4-1,\"\")", "", "Go-Lives this month",
        f"=SUMPRODUCT((TEXT({CM}!$D${R0}:$D${RN},\"yyyymm\")=TEXT({wb.latest(CM,1)},\"yyyymm\"))*1)"],
    ["Active Customers (paying)", "=" + wb.latest(CM, SR['PAY']), "", "Total Seats",
        "=" + wb.latest(SEATS, SEAT_TOT)],
    ["Total Active Users", "=" + wb.latest(USERS, USER_TOT), "", "Avg MAU / customer",
        f"=IFERROR(B3/B6,\"\")"],
]
V(T,"A2",usage_block)
# over-min list
V(T,"A9",[["✅ Customers over MAU minimum (this month)"]])
V(T,"A10",[["Customer","MAU","Min","Headroom"]])
V(T,"A11",[[f"=IFERROR(ARRAY_CONSTRAIN(SORT(FILTER({{'Minimum MAU'!A{R0}:A{RN},'Minimum MAU'!C{R0}:C{RN},'Minimum MAU'!B{R0}:B{RN},'Minimum MAU'!E{R0}:E{RN}}},'Minimum MAU'!D{R0}:D{RN}=TRUE),4,FALSE),25,4),\"—\")"]])
title(g, 5)
# section banners span label + value; over-min list header is its own banner
banner(g,2,0,2,"📌 Headline"); banner(g,2,3,5,"📌 MAU vs Minimum")
banner(g,9,0,4,"✅ over-min")
reqs += [
    wb.colwidth(g,0,1,240), wb.colwidth(g,1,2,120), wb.colwidth(g,2,3,100),
    wb.colwidth(g,3,4,200), wb.colwidth(g,4,5,120), wb.freeze(g,rows=1),
    wb.cellfmt(g,2,7,1,2,numfmt=INT,bold=True), wb.cellfmt(g,4,5,1,2,numfmt=PCTS,bold=True),
    wb.cellfmt(g,2,7,4,5,numfmt=INT,bold=True), wb.cellfmt(g,3,4,4,5,numfmt=PCT,bold=True),
    wb.cellfmt(g,9,10,0,4,bg=GRAY,bold=True),        # list column header
    wb.cellfmt(g,10,36,1,4,numfmt=INT,halign="RIGHT"),
    wb.tabcolor(g, BLUE),
    # explicit pins (these two were not inheriting the range formats reliably)
    wb.cellfmt(g,3,4,4,5,numfmt=PCT,bold=True),   # E4 % over min
    wb.cellfmt(g,6,7,4,5,numfmt=INT,bold=True),   # E7 avg MAU/customer
    wb.cellfmt(g,4,5,1,2,numfmt=PCTS,bold=True),  # B5 MoM MAU %
]
print("prepared Usage Summary")

# =====================================================================
# 📊 Combined Summary
# =====================================================================
T = "📊 Combined Summary"; g = G[T]
def cs(a1, m): V(T, a1, m)
cs("A1",[[f"📊 {COMPANY} — Combined KPI Summary"]])
cs("A2",[["Latest month:", "=" + wb.latest(CM, 1)]])
cs("A4",[["📊  ACCRUAL REVENUE — ARR Financial Model  (recurring run-rate)"]])
cs("A5",[["Gross MRR  (list price, all customers counted monthly)", "=" + wb.latest(CM, SR['GROSS'])]])
cs("A6",[["   less: Discounts (this month)", "=-" + wb.latest(CM, SR['DISC'])]])
cs("A7",[["Net MRR — net of discounts (every customer at monthly run-rate, incl. quarterly billers)", "=" + wb.latest(CM, SR['NET'])]])
cs("A8",[["Total ARR  —  gross  (list × 12)", "=" + wb.latest(CM, SR['ARR'])]])
cs("A9",[["Net ARR  —  after discounts  (× 12)", "=" + wb.latest(CM, SR['NET']) + "*12"]])
cs("A10",[["MoM ARR Growth %", "=" + wb.latest(CM, SR['GROW'])]])
cs("A11",[["Paying Customers", "=" + wb.latest(CM, SR['PAY'])]])
cs("A13",[["💵  CASH-BASIS REVENUE — What We Actually Invoice & Collect  (≠ the accrual model)"]])
cs("A14",[["Net Invoiced this month (MODELED — timing: quarterly billers only in Q-start month)", "=" + wb.latest(CM, SR['INV'])]])
cs("A15",[["   ⤷ difference vs Net MRR  (quarterly billing timing)", "=" + wb.latest(CM, SR['INV']) + "-" + wb.latest(CM, SR['NET'])]])
cs("A16",[["Cash actually collected (from pasted payments report)", "='⏱ Collections & A/R'!B13"]])
cs("A17",[["A/R still outstanding (period end)", "='⏱ Collections & A/R'!B9"]])
cs("A19",[["👥  USAGE"]])
cs("A20",[["Total MAU (this month)", "='📊 Usage Summary'!B3"]])
cs("A21",[["MoM MAU Growth %", "='📊 Usage Summary'!B5"]])
cs("A22",[["Total Seats", "='📊 Usage Summary'!E6"]])
cs("A23",[["Total Active Users", "='📊 Usage Summary'!B7"]])
cs("A24",[["Active Customers (excl. churned)", "='📊 Usage Summary'!B6"]])
cs("A25",[["Customers over MAU Min", "='📊 Usage Summary'!E3"]])
cs("A26",[["% of Customers over MAU Min", "='📊 Usage Summary'!E4"]])
cs("A28",[["💳  AUTOPAY  (recurring, this month)"]])
cs("A29",[["Autopay customers", "='💳 Autopay Collections'!B4"]])
cs("A30",[["Gross MRR on autopay / mo", "='💳 Autopay Collections'!B5"]])
cs("A31",[["Net auto-collected / mo (after discounts)", "='💳 Autopay Collections'!B7"]])
cs("A32",[["% of total MRR via autopay", "='💳 Autopay Collections'!B8"]])
cs("A34",[["💡 TWO VIEWS OF REVENUE.  (A) ACCRUAL / ARR model = recurring revenue at list price, every customer counted monthly regardless of billing cadence — the board number (Net = after discounts; ARR = ×12).  (B) CASH-BASIS = what we actually invoice & can collect: quarterly customers bill 3× only in their Q-start month (Jan/Apr/Jul/Oct), so they're excluded until billed — that gap is billing timing, not lost revenue. Cash collected lags invoicing. All figures are FICTIONAL sample data."]])
title(g, 8)
for r in (4,13,19,28): banner(g,r,0,7,"")  # colored below
for r,txt in [(4,"A"),(13,"B"),(19,"C"),(28,"D")]:
    pass
reqs += [
    wb.colwidth(g,0,1,560), wb.colwidth(g,1,2,150), wb.freeze(g,rows=2),
    wb.cellfmt(g,3,4,0,8,bg=BLUE,bold=True,fg=WHITE,size=11),
    wb.cellfmt(g,12,13,0,8,bg=BLUE,bold=True,fg=WHITE,size=11),
    wb.cellfmt(g,18,19,0,8,bg=BLUE,bold=True,fg=WHITE,size=11),
    wb.cellfmt(g,27,28,0,8,bg=BLUE,bold=True,fg=WHITE,size=11),
    wb.cellfmt(g,1,2,0,1,bold=True), wb.cellfmt(g,1,2,1,2,numfmt=DATEF,bold=True),
    wb.cellfmt(g,4,9,1,2,numfmt=CUR),            # rows 5-9 currency
    wb.cellfmt(g,9,10,1,2,numfmt=PCTS),          # row 10 MoM ARR growth %
    wb.cellfmt(g,10,11,1,2,numfmt=INT),          # row 11 paying customers
    wb.cellfmt(g,6,7,0,2,bg=GREEN,bold=True),    # Net MRR row highlight
    wb.cellfmt(g,13,17,1,2,numfmt=CUR),          # rows 14-17 cash-basis $
    wb.cellfmt(g,19,26,1,2,numfmt=INT),          # rows 20-26 usage counts
    wb.cellfmt(g,20,21,1,2,numfmt=PCTS),         # row 21 MoM MAU %
    wb.cellfmt(g,25,26,1,2,numfmt=PCT),          # row 26 % over min
    wb.cellfmt(g,28,32,1,2,numfmt=CUR),          # rows 29-32 autopay $
    wb.cellfmt(g,28,29,1,2,numfmt=INT),          # row 29 autopay count
    wb.cellfmt(g,31,32,1,2,numfmt=PCT),          # row 32 % via autopay
    wb.cellfmt(g,33,34,0,8,wrap="WRAP",italic=True,size=9),
    wb.merge(g,33,34,0,8),
    wb.tabcolor(g, NAVY),
]
print("prepared Combined Summary")

json.dump({"done":"part2a"}, open(f"{WD}/state2.json","w"))
print("Writing values (dash part A)...")
wb.set_values(SID, vals)
print("Applying formats (dash part A)...")
wb.batch(SID, reqs)
print("DONE dash part A")
