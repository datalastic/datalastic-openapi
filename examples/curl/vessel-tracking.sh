#!/usr/bin/env bash
# examples/curl/vessel-tracking.sh
# Real-time and historical AIS vessel tracking examples.
#
# Usage:
#   export DATALASTIC_KEY=your_api_key
#   bash examples/curl/vessel-tracking.sh

set -euo pipefail

BASE="https://api.datalastic.com/api/v0"
KEY="${DATALASTIC_KEY:?Set DATALASTIC_KEY environment variable}"

echo "=== Real-time position (basic) ==="
curl -s "${BASE}/vessel?api-key=${KEY}&mmsi=566093000" | python3 -m json.tool

echo ""
echo "=== Real-time position (pro — includes ETA, ATD, draught) ==="
curl -s "${BASE}/vessel_pro?api-key=${KEY}&mmsi=566093000" | python3 -m json.tool

echo ""
echo "=== Bulk request — 3 vessels at once ==="
curl -s "${BASE}/vessel_bulk?api-key=${KEY}&mmsi=566093000,636016785,477305700" | python3 -m json.tool

echo ""
echo "=== SAT-E: estimated position for vessel out of AIS range ==="
curl -s "${BASE}/vessel_pro_est?api-key=${KEY}&mmsi=566093000" | python3 -m json.tool

echo ""
echo "=== Look up by IMO instead of MMSI ==="
curl -s "${BASE}/vessel?api-key=${KEY}&imo=9525338" | python3 -m json.tool

echo ""
echo "=== Historical positions — last 7 days ==="
curl -s "${BASE}/vessel_history?api-key=${KEY}&mmsi=566093000&days=7" | python3 -m json.tool

echo ""
echo "=== Historical positions — specific date range (from/to) ==="
curl -s "${BASE}/vessel_history?api-key=${KEY}&mmsi=566093000&from=2026-01-01&to=2026-01-07" | python3 -m json.tool

echo ""
echo "=== Static vessel specs ==="
curl -s "${BASE}/vessel_info?api-key=${KEY}&imo=9525338" | python3 -m json.tool

echo ""
echo "=== Vessel finder — all Container Ships flagged Netherlands ==="
curl -s "${BASE}/vessel_find?api-key=${KEY}&type_specific=Container+Ship&country_iso=NL" | python3 -m json.tool

echo ""
echo "=== All vessels in Rotterdam port (5 NM radius) ==="
curl -s "${BASE}/vessel_inradius?api-key=${KEY}&port_unlocode=NLRTM&radius=5" | python3 -m json.tool

echo ""
echo "=== Only Cargo vessels in Rotterdam ==="
curl -s "${BASE}/vessel_inradius?api-key=${KEY}&port_unlocode=NLRTM&radius=5&type=Cargo" | python3 -m json.tool

echo ""
echo "=== Vessels by lat/lon coordinate ==="
curl -s "${BASE}/vessel_inradius?api-key=${KEY}&lat=51.9433&lon=4.1418&radius=10" | python3 -m json.tool
