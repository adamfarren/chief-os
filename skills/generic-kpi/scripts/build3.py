import os
WD=os.environ.get("GKPI_WORKDIR","/tmp/generic-kpi")
#!/usr/bin/env python3
"""Build remaining dashboard tabs: Revenue Dashboard, Compare, Churn, Autopay,
Revenue->Cash, Collections & A/R, Invoiced Volume, Usage Monthly History, Over-Min."""
import json
import wb
from wb import (col, NAVY, BLUE, GREEN, GRAY, YELLOW, WHITE, LTGRAY, rgb,
                CUR, CUR2, INT, PCT, PCTS, PPS, DATEF)

st = json.load(open(f"{WD}/state.json"))
SID=st["SID"]; G=st["G"]; SR=st["SR"]; R0=st["R0"]; RN=st["RN"]; NM=st["NM"]
LASTL=st["LASTL"]; PREVL=st["PREVL"]; MAU_TOT=st["MAU_TOMAU" ] if False else st["MAU_TOTAL"]
D=json.load(open(f"{WD}/data.json")); C=D["customers"]; COMPANY=D["company"]
FIRST_C=4
CM="'Customers — MRR'"; MAU="'Usage — MAU per Customer'"; SEATS="'Usage — Seats per Customer'"; USERS="'Usage — Active Users per Customer'"
def mcol(i): return col(FIRST_C+i)
def ML(rr): return col(FIRST_C+(NM-1)-rr)
LC=50  # lifecycle status col AY on MRR tab; churn col BA = LC+2
CHURN_COL = col(LC+2)   # BA
START_COL = "D"

vals=[]; reqs=[]
def V(t,a1,m): vals.append({"range":f"'{t}'!{a1}","values":m})
def title(g,c2,color=NAVY):
    reqs.append(wb.merge(g,0,1,0,c2)); reqs.append(wb.cellfmt(g,0,1,0,c2,bg=color,bold=True,fg=WHITE,size=14,valign="MIDDLE"))
def banner(g,r,c1,c2,color=BLUE):
    reqs.append(wb.merge(g,r-1,r,c1,c2)); reqs.append(wb.cellfmt(g,r-1,r,c1,c2,bg=color,bold=True,fg=WHITE,size=11,valign="MIDDLE"))

# =====================================================================
# 💳 Autopay Collections
# =====================================================================
T="💳 Autopay Collections"; g=G[T]
V(T,"A1",[[f"💳 {COMPANY} — Autopay Collections  (recurring, this month)"]])
V(T,"A3",[["Summary"]])
V(T,"A4",[["Autopay customers","=COUNTIF(F12:F200,TRUE)"]])
V(T,"A5",[["Gross MRR on autopay / mo","=SUMIF(F12:F200,TRUE,C12:C200)"]])
V(T,"A6",[["Discounts on autopay / mo","=SUMIF(F12:F200,TRUE,D12:D200)"]])
V(T,"A7",[["Net auto-collected / mo","=SUMIF(F12:F200,TRUE,E12:E200)"]])
V(T,"A8",[["% of total MRR via autopay",f"=IFERROR(B5/{wb.latest(CM,SR['GROSS'])},\"\")"]])
V(T,"A11",[["Customer","Bill Freq","Gross MRR","Discount","Net","Autopay?"]])
rows=[]
for idx,c in enumerate(C):
    r=R0+idx
    rows.append([f"={CM}!C{r}", c["billfreq"], "=" + wb.latest(CM, r),
                 f"=C{12+idx}*{c['disc_pct']}", f"=C{12+idx}-D{12+idx}",
                 True if c["autopay"] else False])
V(T,"A12",rows)
title(g,6); banner(g,3,0,5)
reqs+=[wb.colwidth(g,0,1,220),wb.colwidth(g,1,6,110),wb.freeze(g,rows=1),
       wb.cellfmt(g,3,8,0,1,bold=True), wb.cellfmt(g,3,7,1,2,numfmt=CUR),
       wb.cellfmt(g,3,4,1,2,numfmt=INT), wb.cellfmt(g,7,8,1,2,numfmt=PCT),
       wb.cellfmt(g,10,11,0,6,bg=GRAY,bold=True,halign="CENTER"),
       wb.cellfmt(g,11,11+len(C),2,5,numfmt=CUR),
       wb.tabcolor(g,BLUE)]
print("prepared Autopay")

# =====================================================================
# 📈 Usage Monthly History  (recent-first)
# =====================================================================
T="📈 Usage Monthly History"; g=G[T]
V(T,"A1",[[f"📈 {COMPANY} — Usage Monthly History"]])
V(T,"A2",[["Month","Total MAU","Total Seats","Total Active Users"]])
uh=[]
for rr in range(NM):
    k=rr+1
    uh.append(["="+wb.nth_date(CM,k), "="+wb.nth(MAU,MAU_TOT,k), "="+wb.nth(SEATS,MAU_TOT,k), "="+wb.nth(USERS,MAU_TOT,k)])
V(T,"A3",uh)
title(g,4)
reqs+=[wb.colwidth(g,0,1,100),wb.colwidth(g,1,4,130),wb.freeze(g,rows=2),
       wb.cellfmt(g,1,2,0,4,bg=BLUE,bold=True,fg=WHITE,halign="CENTER"),
       wb.cellfmt(g,2,NM+2,0,1,numfmt=DATEF,bold=True),
       wb.cellfmt(g,2,NM+2,1,4,numfmt=INT), wb.tabcolor(g,rgb(0.5,0.5,0.5))]
print("prepared Usage Monthly History")

# =====================================================================
# Over-Min History  (recent-first)
# =====================================================================
T="Over-Min History"; g=G[T]
V(T,"A1",[[f"📊 {COMPANY} — MAU Over-Minimum History"]])
V(T,"A2",[["Month","# Over Min","# Active","% Over Min"]])
om=[]
for rr in range(NM):
    k=rr+1; ar=rr+3
    mcur=wb.nth_range(MAU,R0,RN,k)
    om.append(["="+wb.nth_date(CM,k),
        f"=SUMPRODUCT((N({mcur})>=N({MAU}!$D${R0}:$D${RN}))*(N({mcur})>0))",
        f'=COUNTIF({mcur},">0")',
        f"=IFERROR(B{ar}/C{ar},\"\")"])
V(T,"A3",om)
title(g,4)
reqs+=[wb.colwidth(g,0,1,100),wb.colwidth(g,1,4,110),wb.freeze(g,rows=2),
       wb.cellfmt(g,1,2,0,4,bg=BLUE,bold=True,fg=WHITE,halign="CENTER"),
       wb.cellfmt(g,2,NM+2,0,1,numfmt=DATEF,bold=True),
       wb.cellfmt(g,2,NM+2,1,3,numfmt=INT), wb.cellfmt(g,2,NM+2,3,4,numfmt=PCT),
       wb.tabcolor(g,rgb(0.5,0.5,0.5))]
print("prepared Over-Min History")

# =====================================================================
# 📉 Churn & New Revenue  (MRR bridge, chronological)
# =====================================================================
T="📉 Churn & New Revenue"; g=G[T]
CURneg=("NUMBER","$#,##0;[Red]-$#,##0")
V(T,"A1",[[f"📉 {COMPANY} — Churn & New Revenue  (MRR bridge)"]])
V(T,"A2",[["How recurring revenue moved each month:   Starting  +  New  −  Churned  ±  Expansion  =  Ending MRR      ·      most recent month first"]])
V(T,"A3",[["Month","Starting MRR","New (new logos)","Churned","Expansion / Contraction","Ending MRR","Ending ARR"]])
# RECENT-FIRST: row 4 = latest month, row 45 = oldest
br=[]
for r in range(NM):
    R=4+r; k=r+1                          # recency rank (1 = latest), robust to added months
    dcur="="+wb.nth_date(CM,k)
    cur=wb.nth_range(CM,R0,RN,k)          # this month's per-customer MRR column
    prvcol=wb.nth_range(CM,R0,RN,k+1) if r < NM-1 else None   # one month older
    ending="="+wb.nth(CM,SR['GROSS'],k)
    new=f"=SUMPRODUCT((TEXT({CM}!${START_COL}${R0}:${START_COL}${RN},\"yyyymm\")=TEXT({wb.nth_date(CM,k)},\"yyyymm\"))*N({cur}))"
    churn=(f"=SUMPRODUCT((TEXT({CM}!${CHURN_COL}${R0}:${CHURN_COL}${RN},\"yyyymm\")=TEXT({wb.nth_date(CM,k)},\"yyyymm\"))*N({prvcol}))" if prvcol else "=0")
    start=f"=F{R+1}"                      # prior (older) month's Ending = row below
    exp=f"=F{R}-B{R}-C{R}+D{R}"
    br.append([dcur, start, new, churn, exp, ending, f"=F{R}*12"])
V(T,"A4",br)
# trailing-12-month summary = most-recent 12 rows (4..15)
V(T,"J3",[["Trailing-12-month summary"]])
V(T,"J4",[["New-logo MRR (T12M)","=SUM(C4:C15)"]])
V(T,"J5",[["Churned MRR (T12M)","=SUM(D4:D15)"]])
V(T,"J6",[["Net new MRR (T12M)","=K4-K5+SUM(E4:E15)"]])
V(T,"J7",[["Churned customers (all-time)",f'=COUNTIF({CM}!{col(LC)}{R0}:{col(LC)}{RN},"Churned")']])
title(g,7)
reqs+=[wb.colwidth(g,0,1,95),wb.colwidth(g,1,7,120),wb.colwidth(g,8,9,24),
       wb.colwidth(g,9,10,200),wb.colwidth(g,10,11,120),wb.freeze(g,rows=3),
       wb.merge(g,1,2,0,7), wb.cellfmt(g,1,2,0,7,italic=True,fg=rgb(0.4,0.4,0.4),size=10),
       wb.cellfmt(g,2,3,0,7,bg=BLUE,bold=True,fg=WHITE,halign="CENTER",wrap="WRAP"),  # per-column headers (no merge)
       wb.cellfmt(g,3,3+NM,0,1,numfmt=DATEF,bold=True),
       wb.cellfmt(g,3,3+NM,1,4,numfmt=CUR), wb.cellfmt(g,3,3+NM,4,5,numfmt=CURneg),
       wb.cellfmt(g,3,3+NM,5,7,numfmt=CUR),
       wb.cellfmt(g,2,3,9,11,bg=BLUE,bold=True,fg=WHITE),
       wb.cellfmt(g,3,7,9,10,bold=True), wb.cellfmt(g,3,6,10,11,numfmt=CUR,bold=True),
       wb.cellfmt(g,6,7,10,11,numfmt=INT,bold=True),
       wb.tabcolor(g,BLUE)]
print("prepared Churn & New Revenue")

# =====================================================================
# 🔍 Compare
# =====================================================================
T="🔍 Compare"; g=G[T]
def _bord(r1,r2,c1,c2):
    ln={"style":"SOLID","color":rgb(0.7,0.7,0.7)}
    return {"updateBorders":{"range":wb.gridrange(g,r1,r2,c1,c2),
        "top":ln,"bottom":ln,"left":ln,"right":ln,"innerHorizontal":ln,"innerVertical":ln}}
V(T,"A1",[[f"🔍 {COMPANY} — Compare any metric across two periods"]])
V(T,"A2",[["Pick a metric and two periods — the comparison updates automatically."]])
V(T,"A4",[["SELECT"]])
V(T,"A5",[["Metric","ARR"]])
V(T,"A6",[["Period A","=A66"]])
V(T,"A7",[["Period B","=A54"]])
V(T,"A9",[["RESULT"]])
V(T,"A10",[['=$B$5&"  —  "&TEXT($B$6,"mmm yyyy")',
   "=INDEX($B$25:$G$66,MATCH($B$6,$A$25:$A$66,0),MATCH($B$5,$B$24:$G$24,0))"]])
V(T,"A11",[['=$B$5&"  —  "&TEXT($B$7,"mmm yyyy")',
   "=INDEX($B$25:$G$66,MATCH($B$7,$A$25:$A$66,0),MATCH($B$5,$B$24:$G$24,0))"]])
V(T,"A12",[["Change (Δ)","=B10-B11"]])
V(T,"A13",[["Change (%)","=IFERROR(B10/B11-1,\"\")"]])
V(T,"A15",[["Metrics available: ARR · MRR · Net MRR · Discounts · Paying Customers · Total MAU"]])
V(T,"A17",[["↓ data model below powers the dropdowns — hidden on purpose; leave as-is."]])
# hidden model rows 24-66 (chronological)
V(T,"A24",[["Month","ARR","MRR","Net MRR","Discounts","Paying Customers","Total MAU"]])
model=[]
for r in range(NM):
    L=mcol(r)
    model.append([f"={CM}!{L}1",f"={CM}!{L}{SR['ARR']}",f"={CM}!{L}{SR['GROSS']}",
                  f"={CM}!{L}{SR['NET']}",f"={CM}!{L}{SR['DISC']}",f"={CM}!{L}{SR['PAY']}",
                  f"={MAU}!{L}{MAU_TOT}"])
V(T,"A25",model)
title(g,5)
metric_vals=[{"userEnteredValue":x} for x in ["ARR","MRR","Net MRR","Discounts","Paying Customers","Total MAU"]]
reqs+=[
  wb.colwidth(g,0,1,210),wb.colwidth(g,1,2,170),wb.colwidth(g,2,7,110),
  wb.merge(g,1,2,0,5), wb.cellfmt(g,1,2,0,5,italic=True,fg=rgb(0.4,0.4,0.4),size=10),
  # SELECT card
  wb.merge(g,3,4,0,2), wb.cellfmt(g,3,4,0,2,bg=BLUE,bold=True,fg=WHITE,halign="LEFT"),
  wb.cellfmt(g,4,7,0,1,bold=True,halign="RIGHT"),
  wb.cellfmt(g,4,7,1,2,bg=rgb(1,1,0.85),bold=True,halign="CENTER"),
  wb.cellfmt(g,5,7,1,2,numfmt=DATEF),
  _bord(4,7,0,2),
  # RESULT card
  wb.merge(g,8,9,0,2), wb.cellfmt(g,8,9,0,2,bg=BLUE,bold=True,fg=WHITE,halign="LEFT"),
  wb.cellfmt(g,9,11,0,1,bold=True), wb.cellfmt(g,9,11,1,2,numfmt=("NUMBER","#,##0"),bold=True,size=13,halign="CENTER"),
  wb.cellfmt(g,11,12,0,1,bold=True), wb.cellfmt(g,11,12,1,2,numfmt=("NUMBER","#,##0;[Red]-#,##0"),bold=True,size=12,halign="CENTER"),
  wb.cellfmt(g,12,13,0,1,bold=True), wb.cellfmt(g,12,13,1,2,numfmt=("NUMBER",'+0.0%;-0.0%;"—"'),bold=True,size=12,halign="CENTER"),
  # muted dark green / red for the Change % (avoids the bright [Green] token)
  {"addConditionalFormatRule":{"index":0,"rule":{"ranges":[wb.gridrange(g,12,13,1,2)],
    "booleanRule":{"condition":{"type":"NUMBER_GREATER","values":[{"userEnteredValue":"0"}]},
    "format":{"textFormat":{"foregroundColor":rgb(0.22,0.46,0.11),"bold":True}}}}}},
  {"addConditionalFormatRule":{"index":0,"rule":{"ranges":[wb.gridrange(g,12,13,1,2)],
    "booleanRule":{"condition":{"type":"NUMBER_LESS","values":[{"userEnteredValue":"0"}]},
    "format":{"textFormat":{"foregroundColor":rgb(0.80,0.0,0.0),"bold":True}}}}}},
  _bord(9,13,0,2),
  wb.cellfmt(g,14,15,0,5,italic=True,fg=rgb(0.4,0.4,0.4),size=9),
  wb.cellfmt(g,16,17,0,5,italic=True,fg=rgb(0.6,0.6,0.6),size=9),
  {"setDataValidation":{"range":wb.gridrange(g,4,5,1,2),"rule":{"condition":{"type":"ONE_OF_LIST","values":metric_vals},"showCustomUi":True,"strict":True}}},
  {"setDataValidation":{"range":wb.gridrange(g,5,7,1,2),"rule":{"condition":{"type":"ONE_OF_RANGE","values":[{"userEnteredValue":"='🔍 Compare'!$A$25:$A$66"}]},"showCustomUi":True,"strict":True}}},
  {"updateDimensionProperties":{"range":{"sheetId":g,"dimension":"ROWS","startIndex":22,"endIndex":66},"properties":{"hiddenByUser":True},"fields":"hiddenByUser"}},
  wb.tabcolor(g,BLUE),
]
print("prepared Compare")

# =====================================================================
# fake cash aggregates (Python) for Revenue->Cash + Collections
# =====================================================================
PRIOR_I = NM-2   # May 2026
def month_gross(i): return sum((c["mrr"][i] or 0) for c in C)
def month_disc(i):  return sum((c["mrr"][i] or 0)*c["disc_pct"] for c in C)
gp=month_gross(PRIOR_I); dp=month_disc(PRIOR_I)
net_mrr_prior=gp-dp

# =====================================================================
# 💵 Revenue → Cash
# =====================================================================
T="💵 Revenue → Cash"; g=G[T]; YEL=rgb(1,1,0.85)
V(T,"A1",[[f"💵 {COMPANY} — Revenue → Cash Cascade"]])
V(T,"A2",[["Accrual → cash. ‘Net MRR’ and ‘Net Invoiced’ are calculated from your data; the cash figures use simple assumptions you can replace with actuals (see notes at right and the how-to below)."]])
V(T,"A3",[["Latest closed month (cash lags one month)","="+wb.prior(CM,1)]])
V(T,"A4",[["Net MRR — accrual run-rate","="+wb.prior(CM,SR['NET'])]])
V(T,"A5",[["Net Invoiced this month (timing)","="+wb.prior(CM,SR['INV'])]])
V(T,"A6",[["Gross Invoiced (actual)","=B5"]])
V(T,"A7",[["Cash Collected","=ROUND(B6*0.88,0)"]])
V(T,"A8",[["Invoiced → Cash %","=IFERROR(B7/B6,\"\")"]])
V(T,"A9",[["On-time collection rate",0.55]])
# source notes (col C) — how to get each number
V(T,"C3",[["Where it comes from"]])
V(T,"C4",[["Auto — from your ‘Customers — MRR’ data"]])
V(T,"C5",[["Auto — quarterly billers counted only in their Q-start month"]])
V(T,"C6",[["✎ Enter your actual invoiced total (billing/invoicing report)"]])
V(T,"C7",[["✎ Enter actual cash, or link to ⏱ Collections & A/R (pasted payments)"]])
V(T,"C8",[["Cash ÷ Invoiced (auto)"]])
V(T,"C9",[["✎ From ⏱ Collections & A/R (pasted payments report)"]])
V(T,"A11",[["Trailing cash (modeled, last 6 closed months)"]])
V(T,"A12",[["Month","Net Invoiced","Cash Collected (≈88%)"]])
tc=[]
for rr in range(1,7):  # skip current (rr=0), take prior 6
    k=rr+1; arr=13+(rr-1)
    tc.append(["="+wb.nth_date(CM,k),"="+wb.nth(CM,SR['INV'],k),f"=ROUND(B{arr}*0.88,0)"])
V(T,"A13",tc)
V(T,"A20",[["HOW TO GET THESE NUMBERS"]])
V(T,"A21",[["•  Net MRR & Net Invoiced — calculated automatically from the ‘Customers — MRR’ tab; nothing to paste.\n"
 "•  Gross Invoiced (actual) — enter the real total you invoiced that month (from your billing/invoicing system).\n"
 "•  Cash Collected & On-time rate — come from your payments/collections report: paste it on the ⏱ Collections & A/R tab, then point these cells there.\n"
 "•  The trailing table below is a model (Net Invoiced × ~88%) — overwrite the Cash column with actuals if you track them.\n"
 "Yellow cells are the ones to replace with your real numbers."]])
title(g,3); banner(g,3,0,1,color=BLUE)
reqs+=[wb.colwidth(g,0,1,330),wb.colwidth(g,1,2,150),wb.colwidth(g,2,3,340),
       wb.cellfmt(g,2,3,0,1,bold=True,fg=WHITE), wb.cellfmt(g,2,3,1,2,numfmt=DATEF,bold=True,fg=WHITE),
       wb.cellfmt(g,3,7,1,2,numfmt=CUR), wb.cellfmt(g,7,9,1,2,numfmt=PCT),
       wb.merge(g,1,2,0,3), wb.cellfmt(g,1,2,0,3,italic=True,fg=rgb(0.4,0.4,0.4),size=10,wrap="WRAP"),
       wb.cellfmt(g,3,4,2,3,bold=True), wb.cellfmt(g,3,9,2,3,wrap="WRAP",size=9,fg=rgb(0.35,0.35,0.35)),
       wb.cellfmt(g,5,6,1,2,bg=YEL), wb.cellfmt(g,6,7,1,2,bg=YEL), wb.cellfmt(g,8,9,1,2,bg=YEL),
       wb.cellfmt(g,10,11,0,3,bg=GRAY,bold=True),
       wb.cellfmt(g,11,12,0,3,bold=True),
       wb.cellfmt(g,12,19,0,1,numfmt=DATEF), wb.cellfmt(g,12,19,1,3,numfmt=CUR),
       wb.merge(g,19,20,0,3), wb.cellfmt(g,19,20,0,3,bg=NAVY,bold=True,fg=WHITE,size=11),
       wb.merge(g,20,21,0,3), wb.cellfmt(g,20,21,0,3,wrap="WRAP",valign="TOP",size=10),
       {"updateDimensionProperties":{"range":{"sheetId":g,"dimension":"ROWS","startIndex":20,"endIndex":21},"properties":{"pixelSize":92},"fields":"pixelSize"}},
       wb.tabcolor(g,rgb(0.2,0.5,0.3))]
print("prepared Revenue -> Cash")

# =====================================================================
# ⏱ Collections & A/R
# =====================================================================
T="⏱ Collections & A/R"; g=G[T]
V(T,"A1",[[f"⏱ {COMPANY} — Collections & A/R Aging"]])
V(T,"A2",[["Paste your A/R Aging Summary in the table below (rows 20+). The summary and Combined Summary update automatically."]])
V(T,"A3",[["A/R Aging (period end)"]])
# aging buckets = SUM of the pasted table (cols B..F)
V(T,"A4",[["Current","=SUM(B20:B500)"]])
V(T,"A5",[["1–30 days","=SUM(C20:C500)"]])
V(T,"A6",[["31–60 days","=SUM(D20:D500)"]])
V(T,"A7",[["61–90 days","=SUM(E20:E500)"]])
V(T,"A8",[["91+ days","=SUM(F20:F500)"]])
V(T,"A9",[["Total A/R","=SUM(B4:B8)"]])
V(T,"A10",[["60+ day A/R","=B7+B8"]])
V(T,"A12",[["Collections timing (latest closed month)"]])
V(T,"A13",[["Cash collected","=SUM(J20:J500)"]])                          # from payments paste
V(T,"A14",[["   ⤷ On-time (≤ Net 30)","=SUMIFS(J20:J500,K20:K500,\"<=0\")"]])
V(T,"A15",[["   ⤷ Past-due caught up","=B13-B14"]])
V(T,"A16",[["On-time collection rate","=IFERROR(B14/B13,\"\")"]])
# paste area 1: A/R aging (cols A..G)
V(T,"A18",[["⬇  PASTE YOUR A/R AGING REPORT HERE  —  overwrite the sample rows (Customer + aging buckets)"]])
V(T,"A19",[["Customer","Current","1–30","31–60","61–90","91+","Total"]])
_prof=[[0.82,0.18,0,0,0],[0.55,0.25,0.12,0.08,0],[0.30,0.22,0.20,0.16,0.12]]
_live=sorted([c for c in C if c["churn_i"] is None], key=lambda c:-(c["mrr"][NM-1] or 0))[:20]
_sample=[]
for j,c in enumerate(_live):
    _mrr=c["mrr"][NM-1] or 0
    _billed=_mrr*(3 if c["billfreq"]=="Q" else 1)
    _total=max(200, round(_billed*(0.8+0.06*(j%10)),-1))
    _b=[round(_total*f,-1) for f in _prof[j%3]]
    _sample.append([c["name"]]+_b+[sum(_b)])
V(T,"A20",_sample)
# paste area 2: payments / collections (cols I..K) -> drives the timing block
V(T,"I17",[["(Days past due ≤ 0 = paid on time)"]])
V(T,"I18",[["⬇  PASTE YOUR PAYMENTS / COLLECTIONS REPORT HERE"]])
V(T,"I19",[["Customer","Amount collected","Days past due"]])
_pay=[]
for j,c in enumerate(_live[:22]):
    _m=c["mrr"][NM-1] or 0
    _pay.append([c["name"], max(100, round(_m*(0.35+0.03*(j%8)),-1)), 0 if (j%2==0) else 10+5*(j%11)])
V(T,"I20",_pay)
title(g,7)
_pend=19+max(len(_sample),60)
reqs+=[wb.colwidth(g,0,1,240),wb.colwidth(g,1,2,150),wb.colwidth(g,2,7,100),
       wb.colwidth(g,7,8,24),wb.colwidth(g,8,9,200),wb.colwidth(g,9,11,120),
       wb.merge(g,1,2,0,7), wb.cellfmt(g,1,2,0,7,italic=True,fg=rgb(0.4,0.4,0.4),size=10),
       wb.merge(g,2,3,0,2), wb.cellfmt(g,2,3,0,2,bg=BLUE,bold=True,fg=WHITE),
       wb.cellfmt(g,3,8,1,2,numfmt=CUR),
       wb.cellfmt(g,8,10,0,1,bold=True), wb.cellfmt(g,8,10,1,2,numfmt=CUR,bold=True),
       wb.cellfmt(g,11,12,0,1,bg=GRAY,bold=True),
       wb.cellfmt(g,12,16,1,2,numfmt=CUR), wb.cellfmt(g,15,16,1,2,numfmt=PCT),
       # aging paste
       wb.merge(g,17,18,0,7), wb.cellfmt(g,17,18,0,7,bg=NAVY,bold=True,fg=WHITE,size=11),
       wb.cellfmt(g,18,19,0,7,bg=GRAY,bold=True,halign="CENTER"),
       wb.cellfmt(g,19,_pend,0,7,bg=rgb(1,1,0.93)), wb.cellfmt(g,19,_pend,1,7,numfmt=CUR),
       # payments paste
       wb.cellfmt(g,16,17,8,11,italic=True,fg=rgb(0.5,0.5,0.5),size=9),
       wb.merge(g,17,18,8,11), wb.cellfmt(g,17,18,8,11,bg=NAVY,bold=True,fg=WHITE,size=11),
       wb.cellfmt(g,18,19,8,11,bg=GRAY,bold=True,halign="CENTER"),
       wb.cellfmt(g,19,_pend,8,11,bg=rgb(1,1,0.93)),
       wb.cellfmt(g,19,_pend,9,10,numfmt=CUR), wb.cellfmt(g,19,_pend,10,11,numfmt=("NUMBER","#,##0")),
       wb.freeze(g,rows=1),
       wb.tabcolor(g,rgb(0.2,0.5,0.3))]
print("prepared Collections & A/R")

# =====================================================================
# 💵 Invoiced Volume  (chronological)
# =====================================================================
T="💵 Invoiced Volume"; g=G[T]
V(T,"A1",[[f"💵 {COMPANY} — Invoiced Volume (cash-out schedule)"]])
V(T,"A2",[["Month","Recurring (monthly billers)","Quarterly billed (3× in Q-start)","Total Invoiced","Collected (≈88%)"]])
iv=[]
for i in range(NM):
    L=mcol(i); ar=i+3
    rec=f"={CM}!{L}{SR['GROSS']}-{CM}!{L}{SR['QMRR']}"
    qs=f"OR(MONTH({CM}!{L}1)=1,MONTH({CM}!{L}1)=4,MONTH({CM}!{L}1)=7,MONTH({CM}!{L}1)=10)"
    qb=f"=IF({qs},3*{CM}!{L}{SR['QMRR']},0)"
    iv.append([f"={CM}!{L}1",rec,qb,f"=B{ar}+C{ar}",f"=ROUND(D{ar}*0.88,0)"])
V(T,"A3",iv)
title(g,5)
reqs+=[wb.colwidth(g,0,1,100),wb.colwidth(g,1,5,175),wb.freeze(g,rows=2),
       wb.cellfmt(g,1,2,0,5,bg=BLUE,bold=True,fg=WHITE,halign="CENTER",wrap="WRAP"),
       wb.cellfmt(g,2,2+NM,0,1,numfmt=DATEF,bold=True),
       wb.cellfmt(g,2,2+NM,1,5,numfmt=CUR), wb.tabcolor(g,rgb(0.2,0.5,0.3))]
print("prepared Invoiced Volume")

# =====================================================================
# 📊 Revenue Dashboard
# =====================================================================
T="📊 Revenue Dashboard"; g=G[T]
S="'📊 MRR & ARR Summary'"; CA="'Customers — ARR'"
V(T,"A1",[[f"=\"📊 {COMPANY} — REVENUE SUMMARY   ·   \"&TEXT({S}!A3,\"mmmm yyyy\")"]])
V(T,"A2",[["📌 Key Metrics — this month"]]); V(T,"C2",[["MoM %"]])
V(T,"E2",[["📌 Retention & Efficiency"]]); V(T,"G2",[["MoM Δ"]])
V(T,"I2",[["💵 Gross MRR — invoiced per month (MRR − discounts)"]])
# left key metrics (A3:C6)
V(T,"A3",[["Total ARR (gross, list)",f"={S}!B3",f"=IFERROR({S}!B3/{S}!B4-1,\"\")"]])
V(T,"A4",[["Total MRR (gross)",f"={S}!C3",f"=IFERROR({S}!C3/{S}!C4-1,\"\")"]])
V(T,"A5",[["Net ARR (after discounts)",f"={S}!F3",f"=IFERROR({S}!F3/{S}!F4-1,\"\")"]])
V(T,"A6",[["New Customer ARR (this month)",f"={S}!H3","—"]])
# right block (E3:G6)  metric | value | MoM Δpp
V(T,"E3",[["Discounts as % of ARR",f"={S}!E3",f"=IFERROR(({S}!E3-{S}!E4)*100,\"\")"]])
V(T,"E4",[["Net ARR % of Gross ARR",f"={S}!G3",f"=IFERROR(({S}!G3-{S}!G4)*100,\"\")"]])
V(T,"E5",[["Net Retention — MoM (ex-new)",f"={S}!I3",f"=IFERROR(({S}!I3-{S}!I4)*100,\"\")"]])
V(T,"E6",[["Net Retention — T12M (ex-new)",f"={S}!J3",f"=IFERROR(({S}!J3-{S}!J4)*100,\"\")"]])
# trend table I3:L (13 months)
V(T,"I3",[["Month","Contracted MRR","Discounts (mo)","Gross MRR (invoiced)"]])
tr=[]
for k in range(13):
    ar=4+k; sr=3+k
    tr.append([f"=IFERROR({S}!A{sr},\"\")",f"=IF($I{ar}=\"\",\"\",{S}!C{sr})",
               f"=IF($I{ar}=\"\",\"\",{S}!D{sr}/12)",f"=IF($I{ar}=\"\",\"\",J{ar}-K{ar})"])
V(T,"I4",tr)
# movers (left A:B growth · right E:F decline)
V(T,"A9",[["🚀 Biggest ARR Growth — MoM"]]); V(T,"E9",[["📉 Biggest ARR Decline — MoM"]])
V(T,"A10",[["Customer","Δ ARR"]]); V(T,"E10",[["Customer","Δ ARR"]])
delta=f"(N({wb.latest_range(CA,R0,RN)})-N({wb.prior_range(CA,R0,RN)}))"
V(T,"A11",[[f"=IFERROR(ARRAY_CONSTRAIN(SORT(FILTER({{{CA}!C${R0}:C${RN},{delta}}},{delta}>1),2,FALSE),5,2),\"—\")"]])
V(T,"E11",[[f"=IFERROR(ARRAY_CONSTRAIN(SORT(FILTER({{{CA}!C${R0}:C${RN},{delta}}},{delta}<-1),2,TRUE),5,2),\"—\")"]])
# new logos (left A:B) / churned (right E:F) this month
V(T,"A18",[["🆕 New Logos — this month"]]); V(T,"E18",[["👋 Churned — this month"]])
V(T,"A19",[["Customer","ARR"]]); V(T,"E19",[["Customer","ARR lost"]])
newmask=f"(TEXT({CM}!${START_COL}${R0}:${START_COL}${RN},\"yyyymm\")=TEXT({wb.latest(CM,1)},\"yyyymm\"))"
V(T,"A20",[[f"=IFERROR(ARRAY_CONSTRAIN(SORT(FILTER({{{CM}!C${R0}:C${RN},N({wb.latest_range(CA,R0,RN)})}},{newmask}),2,FALSE),8,2),\"— none —\")"]])
chmask=f"(TEXT({CM}!${CHURN_COL}${R0}:${CHURN_COL}${RN},\"yyyymm\")=TEXT({wb.latest(CM,1)},\"yyyymm\"))"
V(T,"E20",[[f"=IFERROR(ARRAY_CONSTRAIN(SORT(FILTER({{{CM}!C${R0}:C${RN},N({wb.prior_range(CA,R0,RN)})}},{chmask}),2,FALSE),8,2),\"— none —\")"]])
title(g,12)   # full-width title
reqs+=[
 wb.colwidth(g,0,1,230),wb.colwidth(g,1,3,120),wb.colwidth(g,3,4,26),
 wb.colwidth(g,4,5,220),wb.colwidth(g,5,7,120),wb.colwidth(g,7,8,26),
 wb.colwidth(g,8,9,95),wb.colwidth(g,9,12,130),
 # aligned banner row
 wb.merge(g,1,2,0,2), wb.cellfmt(g,1,2,0,2,bg=BLUE,bold=True,fg=WHITE),
 wb.cellfmt(g,1,2,2,3,bg=BLUE,bold=True,fg=WHITE,halign="CENTER"),
 wb.merge(g,1,2,4,6), wb.cellfmt(g,1,2,4,6,bg=BLUE,bold=True,fg=WHITE),
 wb.cellfmt(g,1,2,6,7,bg=BLUE,bold=True,fg=WHITE,halign="CENTER"),
 wb.merge(g,1,2,8,12), wb.cellfmt(g,1,2,8,12,bg=BLUE,bold=True,fg=WHITE),
 wb.cellfmt(g,2,6,0,1,bold=True),wb.cellfmt(g,2,6,1,2,numfmt=CUR,bold=True),wb.cellfmt(g,2,6,2,3,numfmt=PCTS),
 wb.cellfmt(g,2,6,4,5,bold=True),wb.cellfmt(g,2,6,5,6,numfmt=PCT,bold=True),wb.cellfmt(g,2,6,6,7,numfmt=PPS),
 wb.cellfmt(g,2,3,8,12,bg=GRAY,bold=True,halign="CENTER"),wb.cellfmt(g,3,16,8,9,numfmt=DATEF),
 wb.cellfmt(g,3,16,9,12,numfmt=CUR),
 # movers
 wb.merge(g,8,9,0,2), wb.cellfmt(g,8,9,0,2,bg=GRAY,bold=True),
 wb.merge(g,8,9,4,6), wb.cellfmt(g,8,9,4,6,bg=GRAY,bold=True),
 wb.cellfmt(g,9,10,0,2,bold=True), wb.cellfmt(g,9,10,4,6,bold=True),
 wb.cellfmt(g,10,16,1,2,numfmt=CUR),wb.cellfmt(g,10,16,5,6,numfmt=CUR),
 # new logos / churned
 wb.merge(g,17,18,0,2), wb.cellfmt(g,17,18,0,2,bg=GRAY,bold=True),
 wb.merge(g,17,18,4,6), wb.cellfmt(g,17,18,4,6,bg=GRAY,bold=True),
 wb.cellfmt(g,18,19,0,2,bold=True), wb.cellfmt(g,18,19,4,6,bold=True),
 wb.cellfmt(g,19,28,1,2,numfmt=CUR),wb.cellfmt(g,19,28,5,6,numfmt=CUR),
 wb.freeze(g,rows=2),wb.tabcolor(g,NAVY),
]
print("prepared Revenue Dashboard")

print("Writing values (dash part B)...")
wb.set_values(SID, vals)
print("Applying formats (dash part B)...")
wb.batch(SID, reqs)
print("DONE dash part B")
