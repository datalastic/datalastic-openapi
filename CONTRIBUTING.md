# Contributing

Thank you for helping improve this specification. Accurate API docs make
everyone's life easier.

## What to contribute

- **Bug fixes** — wrong parameter name, incorrect type, missing `nullable`,
  wrong endpoint path.
- **Missing fields** — a response field that exists in the real API but isn't
  in the schema.
- **New endpoints** — if Datalastic releases a new endpoint not yet covered.
- **Better descriptions** — clearer wording, additional context, corrected
  units.
- **New examples** — additional curl/Python/JavaScript examples.

## How to submit a change

1. **Fork** this repo and create a branch:
   ```bash
   git checkout -b fix/vessel-history-date-params
   ```

2. **Edit** `openapi.yaml` (or files in `examples/`).

3. **Validate** before opening a PR:
   ```bash
   npm install -g @redocly/cli
   redocly lint openapi.yaml
   ```
   The CI will also run this automatically.

4. **Open a PR** with a clear title and description explaining what was wrong
   and what the correct value is. If you have a link to the Datalastic docs
   that confirms the fix, include it.

## Style guide for the YAML

- Keep descriptions concise — one or two sentences max per field.
- Always mark fields `nullable: true` if the API can return `null`.
- Use `format: date` for `yyyy-mm-dd` strings, `format: date-time` for full
  ISO 8601 timestamps.
- Endpoint-level descriptions should include the credit cost and any important
  constraints (max radius, max window, etc.).
- Real example values are always preferred over placeholder strings.

## Reporting issues without a fix

Open a GitHub issue with:
- The endpoint path
- The parameter or field name
- What the spec currently says
- What the real API actually returns (paste the JSON if possible)

## Questions

Email [support@datalastic.com](mailto:support@datalastic.com) for questions
about the API itself. Open an issue here for anything spec-related.
