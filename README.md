# Datalastic Maritime API — OpenAPI Specification

[![Validate OpenAPI](https://github.com/datalastic/datalastic-openapi/actions/workflows/validate.yml/badge.svg)](https://github.com/datalastic/datalastic-openapi/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![OpenAPI 3.1](https://img.shields.io/badge/OpenAPI-3.1-green.svg)](openapi.yaml)

The official OpenAPI 3.1 specification for the [Datalastic Maritime API](https://datalastic.com/api-reference/) — covering all endpoints for real-time AIS vessel tracking, historical data, port information, and the full suite of add-on datasets.

---

## What's in this repo

```
datalastic-openapi/
├── openapi.yaml              # The spec — single source of truth
├── examples/
│   ├── curl/                 # Ready-to-run shell scripts
│   ├── python/               # Python 3 examples (requests library)
│   ├── javascript/           # Node.js / fetch examples
│   └── responses/            # Example JSON responses for every endpoint
├── .github/
│   └── workflows/
│       └── validate.yml      # CI: validates spec on every push/PR
├── CHANGELOG.md
├── CONTRIBUTING.md
└── LICENSE
```

---

## Quickstart

### Import into Postman

1. Open Postman → **Import**
2. Select **Link** and paste:
   ```
   https://raw.githubusercontent.com/datalastic/datalastic-openapi/main/openapi.yaml
   ```
3. All 19 endpoints are imported with parameters, response schemas, and example responses pre-filled.
4. Set the `api-key` collection variable to your key and start making requests.

### Import into Insomnia

1. **File → Import → From URL**
2. Paste the same raw URL above.
3. Insomnia will create a collection with all endpoints grouped by tag.

### Use with Mintlify

Add to your `mint.json`:
```json
{
  "api": {
    "openapi": "https://raw.githubusercontent.com/datalastic/datalastic-openapi/main/openapi.yaml"
  }
}
```

Mintlify reads the spec directly and generates the full API reference automatically, including try-it consoles, parameter tables, and code samples.

### Use with Swagger UI (local)

```bash
# Using Docker
docker run -p 8080:8080 \
  -e SWAGGER_JSON_URL=https://raw.githubusercontent.com/datalastic/datalastic-openapi/main/openapi.yaml \
  swaggerapi/swagger-ui

# Then open http://localhost:8080
```

---

## Generate client SDKs

The spec is ready for [openapi-generator](https://openapi-generator.tech/). One command produces a typed client in your language of choice.

```bash
# Install
npm install -g @openapitools/openapi-generator-cli

# TypeScript / Node.js
openapi-generator-cli generate \
  -i openapi.yaml \
  -g typescript-fetch \
  -o ./sdk/typescript

# Python
openapi-generator-cli generate \
  -i openapi.yaml \
  -g python \
  -o ./sdk/python \
  --additional-properties=packageName=datalastic

# Go
openapi-generator-cli generate \
  -i openapi.yaml \
  -g go \
  -o ./sdk/go \
  --additional-properties=packageName=datalastic

# Java
openapi-generator-cli generate \
  -i openapi.yaml \
  -g java \
  -o ./sdk/java
```

---

## API overview

All requests require your API key as the `api-key` query parameter.

```
https://api.datalastic.com/api/v0/vessel?api-key=YOUR_KEY&mmsi=566093000
```

A single key covers all endpoints across all plans. [Get your key →](https://datalastic.com/pricing/)

### Core endpoints (`/api/v0/`)

| Endpoint | Description | Credits |
|---|---|---|
| `GET /vessel` | Real-time AIS position (basic, ~5 ms) | 1 / vessel |
| `GET /vessel_pro` | Real-time AIS + ETA, ATD, draught (~900 ms) | 1 / vessel |
| `GET /vessel_pro_est` | SAT-E: vessel_pro + AI-estimated position when out of AIS range | 1 / vessel |
| `GET /vessel_bulk` | Up to 100 vessels in one request | 1 / vessel found |
| `GET /vessel_inradius` | All vessels in a radius or port area | 1 / vessel, max 500 |
| `GET /vessel_history` | Historical AIS positions by date range | 1 / vessel-day |
| `GET /vessel_info` | Static specs: dimensions, TEU, tonnage | 1 / vessel |
| `GET /vessel_find` | Search registry by name, flag, type | 1 / vessel returned |
| `GET /port_find` | Find ports by name, country, UNLOCODE | 1 / port returned |
| `GET /terminal_find` | Find terminals within a port | 1 credit per query |
| `GET /stat` | Credit usage and plan info | Free |
| `POST /report` | Submit async bulk export job | 1 to submit |
| `GET /report` | Poll job status / list all jobs | Free |

### Add-on endpoints (`/api/maritime_reports/`)

| Endpoint | Description |
|---|---|
| `GET /dry_dock_dates` | Planned and completed dry dock periods + IOPP dates |
| `GET /companies` | Maritime company profiles, contacts, parent company |
| `GET /casualty` | Incident records with full narrative |
| `GET /inspections` | Port State Control inspection and detention records |
| `GET /spd` | Ship sales, purchase, and demolition records |
| `GET /ownership` | Beneficial owner, operator, and manager chain |
| `GET /class_society` | Classification society, structural dims, engine details |
| `GET /engine` | Engine designation, MCO, builder, designer |

All add-on endpoints also support bulk CSV export via `POST /api/v0/report` — see [Async report pattern](#async-report-pattern).

### Credit limits

| Plan | Credits / month |
|---|---|
| Starter | 20 000 |
| Experimenter | 80 000 |
| Developer Pro+ | Unlimited |

Rate limit: **600 requests / minute**. Failed requests (vessel not found, bad identifier) do not consume credits.

### Async report pattern

Large datasets are exported asynchronously:

```bash
# 1. Submit
curl -X POST https://api.datalastic.com/api/v0/report \
  -H "Content-Type: application/json" \
  -d '{"api-key": "YOUR_KEY", "report_type": "ownership", "updated_from": "2024-01-01"}'

# Response: {"data": {"report_id": "rpt_7f3a9c12", "status": "PENDING", ...}}

# 2. Poll until DONE
curl "https://api.datalastic.com/api/v0/report?api-key=YOUR_KEY&report_id=rpt_7f3a9c12"

# 3. Download CSV from result_url when status == "DONE"
```

All add-on `report_type` values: `dry_dock_dates`, `companies`, `casualty`, `inspections`, `sales_purchase_demolitions`, `ownership`, `class_society`, `engine`, `vessel_list`, `port_list`, `request_usage`, `inradius_history`.

---

## Examples

See the [`examples/`](examples/) directory for working code in curl, Python, and JavaScript.

```bash
# Quick curl test
export DATALASTIC_KEY=your_api_key

# Real-time vessel position
curl "https://api.datalastic.com/api/v0/vessel?api-key=$DATALASTIC_KEY&mmsi=566093000"

# Port lookup
curl "https://api.datalastic.com/api/v0/port_find?api-key=$DATALASTIC_KEY&unlocode=NLRTM"

# Check credit balance
curl "https://api.datalastic.com/api/v0/stat?api-key=$DATALASTIC_KEY"
```

---

## Validate the spec locally

```bash
# Using Redocly CLI (recommended)
npm install -g @redocly/cli
redocly lint openapi.yaml

# Using Spectral
npm install -g @stoplight/spectral-cli
spectral lint openapi.yaml --ruleset @stoplight/spectral-oas

# Using swagger-parser
npm install -g @apidevtools/swagger-cli
swagger-cli validate openapi.yaml
```

---

## Versioning

This repo tracks the Datalastic API. The YAML `version` field matches the API version (`v0`). Breaking changes will be noted in [CHANGELOG.md](CHANGELOG.md).

---

## Contributing

Found a mistake in a parameter description, a wrong field type, or a missing endpoint? See [CONTRIBUTING.md](CONTRIBUTING.md) — PRs are welcome and reviewed promptly.

---

## Resources

- [Datalastic API Reference](https://datalastic.com/api-reference/)
- [Pricing & Plans](https://datalastic.com/pricing/)
- [Support](mailto:support@datalastic.com)

---

## License

[MIT](LICENSE) — free to use in personal and commercial projects, including generated SDKs.
