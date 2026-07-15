#!/bin/bash
# Generate a fresh, self-contained generic SaaS KPI dashboard (fictional data)
# as a NEW Google Sheet, make it link-shareable, and print the URL.
# Usage: run.sh [seed] [n_customers]
set -e
SEED="${1:-$RANDOM}"
NCUST="${2:-35}"
DIR="$(cd "$(dirname "$0")" && pwd)"
WD="$(mktemp -d /tmp/generic-kpi-XXXXXX)"
export GKPI_WORKDIR="$WD"
cp "$DIR"/*.py "$WD"/
cd "$WD"
echo "▶ Generating fictional data (seed=$SEED, customers=$NCUST)..."
python3 gen_data.py "$SEED" "$NCUST"
echo "▶ Building workbook (data layer → dashboards → docs → formats)..."
python3 build.py  >/dev/null
python3 build2.py >/dev/null
python3 build3.py >/dev/null
python3 build4.py >/dev/null
python3 fmt_pass.py
SID="$(cat "$WD/spreadsheet_id.txt")"
echo "▶ Enabling link sharing (anyone with link can view)..."
gws drive permissions create --params "{\"fileId\":\"$SID\"}" \
    --json '{"type":"anyone","role":"reader"}' >/dev/null 2>&1 || echo "  (sharing step skipped)"
echo ""
echo "✅ Done. Shareable URL:"
echo "https://docs.google.com/spreadsheets/d/$SID/edit"
