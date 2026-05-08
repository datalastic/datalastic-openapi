# Changelog

All notable changes to this specification are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] — 2026-05-07

### Added
- Initial release of the Datalastic OpenAPI 3.1 specification.
- Full coverage of all 19 endpoints across two base paths:
  - Core AIS & ports: `/api/v0/`
  - Add-on datasets: `/api/maritime_reports/`
- Complete request parameter definitions for all endpoints.
- Response schemas for all 18 data types with field-level descriptions and examples.
- Inline response examples on all key endpoints (compatible with Postman, Insomnia, Mintlify).
- Async report pattern documented: `POST /report` → poll `GET /report` → download CSV.
- All 12 `report_type` enum values documented with credit costs.
- Credit cost documented per endpoint.
- Rate limit (600 req/min) documented at spec and endpoint level.
- Working examples in curl, Python, and JavaScript.
- Example JSON responses for every endpoint.
- GitHub Actions workflow to validate spec on every push and PR.

---

## Upcoming

- `x-codeSamples` extensions for Mintlify/Redocly inline code tabs.
- Webhook documentation (if Datalastic adds webhook support).
- SDK packages for Python and TypeScript (auto-generated from this spec).
