#!/usr/bin/env bash
# examples/curl/reports.sh
# Async bulk export: submit a job, poll until done, download the CSV.
#
# Usage:
#   export DATALASTIC_KEY=your_api_key
#   bash examples/curl/reports.sh

set -euo pipefail

BASE="https://api.datalastic.com/api/v0"
KEY="${DATALASTIC_KEY:?Set DATALASTIC_KEY environment variable}"

# ---------------------------------------------------------------------------
# Helper: poll a report until DONE, then print the download URL
# ---------------------------------------------------------------------------
poll_report() {
  local report_id="$1"
  local max_attempts=20
  local attempt=0

  echo "Polling report ${report_id}..."
  while [ $attempt -lt $max_attempts ]; do
    response=$(curl -s "${BASE}/report?api-key=${KEY}&report_id=${report_id}")
    status=$(echo "$response" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['status'])")

    echo "  Status: ${status}"

    if [ "$status" = "DONE" ]; then
      result_url=$(echo "$response" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['result_url'])")
      echo "  Download URL: ${result_url}"
      return 0
    elif [ "$status" = "FAILED" ]; then
      echo "  Report failed."
      echo "$response" | python3 -m json.tool
      return 1
    fi

    attempt=$((attempt + 1))
    sleep 5
  done

  echo "Timed out waiting for report ${report_id}"
  return 1
}

# ---------------------------------------------------------------------------
# 1. Historical location traffic (Rotterdam, 1–5 Jan 2026)
# ---------------------------------------------------------------------------
echo "=== Submit: Historical location traffic (inradius_history) ==="
response=$(curl -s -X POST "${BASE}/report" \
  -H "Content-Type: application/json" \
  -d "{
    \"api-key\": \"${KEY}\",
    \"report_type\": \"inradius_history\",
    \"lat\": 51.8951,
    \"lon\": 4.3973,
    \"radius\": 10,
    \"from\": \"2026-01-01\",
    \"to\": \"2026-01-05\"
  }")
echo "$response" | python3 -m json.tool
report_id=$(echo "$response" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['report_id'])")
poll_report "$report_id"

echo ""
echo "=== Submit: Ownership bulk export (updated since 2024) ==="
response=$(curl -s -X POST "${BASE}/report" \
  -H "Content-Type: application/json" \
  -d "{
    \"api-key\": \"${KEY}\",
    \"report_type\": \"ownership\",
    \"updated_from\": \"2024-01-01\"
  }")
echo "$response" | python3 -m json.tool
report_id=$(echo "$response" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['report_id'])")
poll_report "$report_id"

echo ""
echo "=== Submit: API usage report for last month ==="
response=$(curl -s -X POST "${BASE}/report" \
  -H "Content-Type: application/json" \
  -d "{
    \"api-key\": \"${KEY}\",
    \"report_type\": \"request_usage\",
    \"from\": \"2026-04-01\",
    \"to\": \"2026-04-30\"
  }")
echo "$response" | python3 -m json.tool
report_id=$(echo "$response" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['report_id'])")
poll_report "$report_id"

echo ""
echo "=== List all previously generated reports ==="
curl -s "${BASE}/report?api-key=${KEY}&report_id=_all" | python3 -m json.tool
