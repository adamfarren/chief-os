import os
WD=os.environ.get("GKPI_WORKDIR","/tmp/generic-kpi")
#!/usr/bin/env python3
"""Final, isolated number-format pass — applied LAST so nothing overrides it.
(Percent/pp formats on the summary tabs don't survive the big accumulated batches;
re-pinning them here as the final operation is reliable.)"""
import json, wb
from wb import CUR, INT, PCT, PCTS, PPS, DATEF
st=json.load(open(f"{WD}/state.json"))
SID=st["SID"]; G=st["G"]; NM=st["NM"]
R=2+NM  # end row index for data rows 3..(2+NM)
r=[]
# force Calibri across every cell of every tab (covers cells never explicitly formatted)
for _gid in G.values():
    r.append({"repeatCell":{"range":{"sheetId":_gid},
        "cell":{"userEnteredFormat":{"textFormat":{"fontFamily":"Calibri"}}},
        "fields":"userEnteredFormat.textFormat.fontFamily"}})
def f(tab,r1,r2,c1,c2,nf): r.append(wb.cellfmt(G[tab],r1,r2,c1,c2,numfmt=nf))

# 📊 MRR & ARR Summary
t="📊 MRR & ARR Summary"
f(t,2,R,0,1,DATEF); f(t,2,R,1,4,CUR); f(t,2,R,4,5,PCT); f(t,2,R,5,6,CUR)
f(t,2,R,6,7,PCT); f(t,2,R,7,8,CUR); f(t,2,R,8,10,PCT)
# 📊 Usage Summary
t="📊 Usage Summary"
for cell,nf in [(2,INT),(3,INT),(4,PCTS),(5,INT),(6,INT)]:  # B3..B7
    f(t,cell,cell+1,1,2,nf)
for cell,nf in [(2,INT),(3,PCT),(4,INT),(5,INT),(6,INT)]:   # E3..E7
    f(t,cell,cell+1,4,5,nf)
# 📊 Revenue Dashboard
t="📊 Revenue Dashboard"
f(t,2,6,1,2,CUR); f(t,2,5,2,3,PCTS)          # B3:B6 $, C3:C5 %
f(t,2,4,5,6,PCT); f(t,4,6,5,6,PCT); f(t,2,6,6,7,PPS)  # F disc/net %, F NRR %, G pp
f(t,3,16,8,9,DATEF); f(t,3,16,9,12,CUR)      # trend
f(t,10,16,1,2,CUR); f(t,10,16,4,6,CUR)       # movers
f(t,19,28,1,2,CUR); f(t,19,28,4,6,CUR)       # new/churn lists
# Over-Min History
t="Over-Min History"; f(t,2,R,0,1,DATEF); f(t,2,R,1,3,INT); f(t,2,R,3,4,PCT)
# 📈 Usage Monthly History
t="📈 Usage Monthly History"; f(t,2,R,0,1,DATEF); f(t,2,R,1,4,INT)
# 📉 Churn & New Revenue
t="📉 Churn & New Revenue"; f(t,3,3+NM,0,1,DATEF); f(t,3,3+NM,1,7,CUR)
# 💵 Invoiced Volume
t="💵 Invoiced Volume"; f(t,2,2+NM,0,1,DATEF); f(t,2,2+NM,1,5,CUR)
# 🔍 Compare
t="🔍 Compare"; f(t,8,9,1,4,("NUMBER","#,##0")); f(t,8,9,4,5,PCTS)
# 💳 Autopay Collections (list $)
t="💳 Autopay Collections"; f(t,11,11+35+3,2,5,CUR)

wb.batch(SID, r)
print(f"format pass applied ({len(r)} requests)")
