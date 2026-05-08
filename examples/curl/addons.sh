#!/usr/bin/env bash
# examples/curl/addons.sh
# Add-on dataset endpoints: ownership, dry dock, casualties, inspections,
# sales & demolitions, classification society, engines, and companies.
#
# Usage:
#   export DATALASTIC_KEY=your_api_key
#   bash examples/curl/addons.sh

set -euo pipefail

BASE_REPORTS="https://api.datalastic.com/api/maritime_reports"
KEY="${DATALASTIC_KEY:?Set DATALASTIC_KEY environment variable}"

echo "=== Vessel ownership ==="
curl -s "${BASE_REPORTS}/ownership?api-key=${KEY}&imo=9951783" | python3 -m json.tool

echo ""
echo "=== Ownership — search by beneficial owner name ==="
curl -s "${BASE_REPORTS}/ownership?api-key=${KEY}&beneficial_owner=Steamship" | python3 -m json.tool

echo ""
echo "=== Dry dock dates ==="
curl -s "${BASE_REPORTS}/dry_dock_dates?api-key=${KEY}&imo=9169122" | python3 -m json.tool

echo ""
echo "=== Dry dock dates — filter by date range ==="
curl -s "${BASE_REPORTS}/dry_dock_dates?api-key=${KEY}&dry_dock_from=2024-01-01&dry_dock_to=2025-12-31" | python3 -m json.tool

echo ""
echo "=== Ship casualties ==="
curl -s "${BASE_REPORTS}/casualty?api-key=${KEY}&imo=9319569" | python3 -m json.tool

echo ""
echo "=== Casualties in a date range ==="
curl -s "${BASE_REPORTS}/casualty?api-key=${KEY}&from=2023-09-01&to=2023-09-30" | python3 -m json.tool

echo ""
echo "=== PSC inspections ==="
curl -s "${BASE_REPORTS}/inspections?api-key=${KEY}&imo=9362126" | python3 -m json.tool

echo ""
echo "=== Detentions only (filter by date) ==="
curl -s "${BASE_REPORTS}/inspections?api-key=${KEY}&from=2023-01-01" | python3 -m json.tool

echo ""
echo "=== Sales, purchases, and demolitions ==="
curl -s "${BASE_REPORTS}/spd?api-key=${KEY}&imo=9104586" | python3 -m json.tool

echo ""
echo "=== Classification society ==="
curl -s "${BASE_REPORTS}/class_society?api-key=${KEY}&imo=9950404" | python3 -m json.tool

echo ""
echo "=== Class society — fuzzy name search ==="
curl -s "${BASE_REPORTS}/class_society?api-key=${KEY}&name=DARYA&fuzzy=1" | python3 -m json.tool

echo ""
echo "=== Vessel engine specs ==="
curl -s "${BASE_REPORTS}/engine?api-key=${KEY}&imo=9575149" | python3 -m json.tool

echo ""
echo "=== Engine — fuzzy name search ==="
curl -s "${BASE_REPORTS}/engine?api-key=${KEY}&name=DARYA&fuzzy=1" | python3 -m json.tool

echo ""
echo "=== Maritime companies ==="
curl -s "${BASE_REPORTS}/companies?api-key=${KEY}&name=Maersk" | python3 -m json.tool
