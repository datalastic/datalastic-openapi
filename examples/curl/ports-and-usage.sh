#!/usr/bin/env bash
# examples/curl/ports-and-usage.sh
# Port finder, terminal lookup, and credit usage monitoring.
#
# Usage:
#   export DATALASTIC_KEY=your_api_key
#   bash examples/curl/ports-and-usage.sh

set -euo pipefail

BASE="https://api.datalastic.com/api/v0"
KEY="${DATALASTIC_KEY:?Set DATALASTIC_KEY environment variable}"

echo "=== Port lookup by UNLOCODE ==="
curl -s "${BASE}/port_find?api-key=${KEY}&unlocode=NLRTM" | python3 -m json.tool

echo ""
echo "=== Port lookup by name ==="
curl -s "${BASE}/port_find?api-key=${KEY}&name=rotterdam" | python3 -m json.tool

echo ""
echo "=== All ports in the Netherlands ==="
curl -s "${BASE}/port_find?api-key=${KEY}&country_iso=NL" | python3 -m json.tool

echo ""
echo "=== Terminals in Rotterdam ==="
curl -s "${BASE}/terminal_find?api-key=${KEY}&port_unlocode=NLRTM" | python3 -m json.tool

echo ""
echo "=== Filter terminals by name ==="
curl -s "${BASE}/terminal_find?api-key=${KEY}&port_unlocode=NLRTM&name=ECT" | python3 -m json.tool

echo ""
echo "=== Check credit balance ==="
curl -s "${BASE}/stat?api-key=${KEY}" | python3 -m json.tool
