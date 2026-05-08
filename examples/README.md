# Examples

Working code for the Datalastic Maritime API.

## Prerequisites

Set your API key as an environment variable:

```bash
export DATALASTIC_KEY=your_api_key
```

---

## curl

| File | What it covers |
|------|----------------|
| `curl/vessel-tracking.sh` | Real-time position (basic + pro + bulk), vessel finder, location radius, historical data |
| `curl/ports-and-usage.sh` | Port finder, terminal lookup, credit balance |
| `curl/addons.sh` | All 8 add-on endpoints: ownership, dry dock, casualties, inspections, SPD, classification, engines, companies |
| `curl/reports.sh` | Full async report workflow: submit → poll → download |

```bash
bash examples/curl/vessel-tracking.sh
bash examples/curl/ports-and-usage.sh
bash examples/curl/addons.sh
bash examples/curl/reports.sh
```

---

## Python

Requires Python 3.10+ and `requests`:

```bash
pip install requests
```

| File | What it covers |
|------|----------------|
| `python/vessel_tracking.py` | Live position, bulk, in-radius, historical, vessel finder, vessel info, credit usage |
| `python/addons.py` | All 8 add-on endpoints with typed wrapper functions |
| `python/reports.py` | `submit_report` + `poll_report` + `download_csv` helpers, end-to-end `run_report` |

```bash
python3 examples/python/vessel_tracking.py
python3 examples/python/addons.py
python3 examples/python/reports.py
```

---

## JavaScript (Node.js)

Requires Node.js 18+ (uses built-in `fetch`). No npm install needed.

| File | What it covers |
|------|----------------|
| `javascript/vessel-tracking.js` | Live position (basic + pro + bulk), in-radius, historical, vessel info, credit usage |
| `javascript/reports.js` | `submitReport` + `pollReport` helpers, end-to-end `runReport`, list all reports |

```bash
node examples/javascript/vessel-tracking.js
node examples/javascript/reports.js
```

---

## Example JSON responses

The `responses/` directory contains representative JSON responses for every endpoint — useful for building and testing client code without consuming API credits.

| File | Endpoint |
|------|----------|
| `vessel.json` | `GET /api/v0/vessel` |
| `vessel_pro.json` | `GET /api/v0/vessel_pro` |
| `vessel_pro_est.json` | `GET /api/v0/vessel_pro_est` (SAT-E, includes estimated_position) |
| `vessel_inradius.json` | `GET /api/v0/vessel_inradius` |
| `vessel_history.json` | `GET /api/v0/vessel_history` |
| `vessel_info.json` | `GET /api/v0/vessel_info` |
| `port_find.json` | `GET /api/v0/port_find` |
| `stat.json` | `GET /api/v0/stat` |
| `report_submitted.json` | `POST /api/v0/report` (202 response) |
| `report_done.json` | `GET /api/v0/report` (status DONE) |
| `dry_dock_dates.json` | `GET /api/maritime_reports/dry_dock_dates` |
| `ownership.json` | `GET /api/maritime_reports/ownership` |
| `casualty.json` | `GET /api/maritime_reports/casualty` |
| `inspections.json` | `GET /api/maritime_reports/inspections` |
| `spd.json` | `GET /api/maritime_reports/spd` |
| `class_society.json` | `GET /api/maritime_reports/class_society` |
| `engine.json` | `GET /api/maritime_reports/engine` |
| `error_401.json` | Invalid API key |
| `error_404.json` | Vessel / resource not found |
| `error_429.json` | Rate limit exceeded |
