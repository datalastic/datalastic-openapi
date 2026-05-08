/**
 * examples/javascript/reports.js
 *
 * Async bulk export: submit → poll → get download URL.
 * Works with Node.js 18+ (built-in fetch). No dependencies.
 *
 * Usage:
 *   DATALASTIC_KEY=your_api_key node examples/javascript/reports.js
 */

const API_KEY = process.env.DATALASTIC_KEY;
if (!API_KEY) throw new Error("Set the DATALASTIC_KEY environment variable");

const BASE_URL = "https://api.datalastic.com/api/v0";

async function apiPost(endpoint, body) {
  const res = await fetch(`${BASE_URL}${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ "api-key": API_KEY, ...body }),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

async function apiGet(endpoint, params = {}) {
  const url = new URL(`${BASE_URL}${endpoint}`);
  url.searchParams.set("api-key", API_KEY);
  for (const [k, v] of Object.entries(params)) {
    url.searchParams.set(k, String(v));
  }
  const res = await fetch(url.toString());
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

/**
 * Submit a report job and return the report_id.
 * @param {string} reportType
 * @param {Record<string, any>} options  Additional payload fields.
 */
async function submitReport(reportType, options = {}) {
  const result = await apiPost("/report", { report_type: reportType, ...options });
  const { report_id, status } = result.data;
  console.log(`  Submitted: ${reportType} → ${report_id} (${status})`);
  return report_id;
}

/**
 * Poll a report until DONE. Returns the completed job object.
 * @param {string} reportId
 * @param {number} intervalMs  Polling interval in milliseconds.
 * @param {number} timeoutMs   Give up after this many milliseconds.
 */
async function pollReport(reportId, intervalMs = 5000, timeoutMs = 300_000) {
  const deadline = Date.now() + timeoutMs;

  while (Date.now() < deadline) {
    const result = await apiGet("/report", { report_id: reportId });
    const job = result.data;
    console.log(`  [${new Date().toISOString()}] ${reportId} — ${job.status}`);

    if (job.status === "DONE") return job;
    if (job.status === "FAILED") throw new Error(`Report ${reportId} failed`);

    await new Promise((r) => setTimeout(r, intervalMs));
  }

  throw new Error(`Report ${reportId} timed out after ${timeoutMs / 1000}s`);
}

/**
 * Full pipeline: submit → poll → return download URL.
 */
async function runReport(reportType, options = {}) {
  const reportId = await submitReport(reportType, options);
  const job = await pollReport(reportId);
  console.log(`  Done! Download URL: ${job.result_url}`);
  return job.result_url;
}

/** List all reports generated with this API key. */
async function listAllReports() {
  const result = await apiGet("/report", { report_id: "_all" });
  return result.data;
}

// ---------------------------------------------------------------------------
// Demo
// ---------------------------------------------------------------------------

async function main() {
  console.log("=== All previous reports ===");
  const reports = await listAllReports();
  reports.slice(0, 5).forEach((job) => {
    console.log(`  ${job.report_id}  ${job.report_type}  ${job.status}`);
  });

  console.log("\n=== API usage report — April 2026 ===");
  await runReport("request_usage", { from: "2026-04-01", to: "2026-04-30" });

  console.log("\n=== Historical location — Rotterdam, 1-3 Jan 2026 ===");
  await runReport("inradius_history", {
    lat: 51.8951,
    lon: 4.3973,
    radius: 10,
    from: "2026-01-01",
    to: "2026-01-03",
  });

  console.log("\n=== Ownership bulk export (updated since 2024) ===");
  await runReport("ownership", { updated_from: "2024-01-01" });
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
