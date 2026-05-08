/**
 * examples/javascript/vessel-tracking.js
 *
 * Real-time AIS vessel tracking with the Datalastic API.
 * Uses the built-in Node.js fetch (Node 18+). No dependencies.
 *
 * Usage:
 *   DATALASTIC_KEY=your_api_key node examples/javascript/vessel-tracking.js
 */

const API_KEY = process.env.DATALASTIC_KEY;
if (!API_KEY) throw new Error("Set the DATALASTIC_KEY environment variable");

const BASE_URL = "https://api.datalastic.com/api/v0";

/**
 * Low-level GET helper. Merges api-key into every request.
 * @param {string} endpoint
 * @param {Record<string, string | number>} params
 * @returns {Promise<any>}
 */
async function apiGet(endpoint, params = {}) {
  const url = new URL(`${BASE_URL}${endpoint}`);
  url.searchParams.set("api-key", API_KEY);
  for (const [k, v] of Object.entries(params)) {
    url.searchParams.set(k, String(v));
  }

  const res = await fetch(url.toString());
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`HTTP ${res.status} from ${endpoint}: ${body}`);
  }
  return res.json();
}

// ---------------------------------------------------------------------------
// Public functions
// ---------------------------------------------------------------------------

/** Real-time AIS position (basic). ~5 ms response. */
async function getVessel({ mmsi, imo, uuid } = {}) {
  return apiGet("/vessel", { ...(mmsi && { mmsi }), ...(imo && { imo }), ...(uuid && { uuid }) });
}

/** Real-time AIS position (pro) — includes ETA, ATD, draught. ~900 ms. */
async function getVesselPro({ mmsi, imo } = {}) {
  return apiGet("/vessel_pro", { ...(mmsi && { mmsi }), ...(imo && { imo }) });
}

/**
 * SAT-E: vessel_pro data plus an AI-estimated position.
 * The `estimated_position` field is populated when the vessel has been out of
 * terrestrial AIS range for 3+ hours.
 * Credit cost: 1 per vessel queried.
 */
async function getVesselProEst({ mmsi, imo, uuid } = {}) {
  return apiGet("/vessel_pro_est", {
    ...(mmsi && { mmsi }),
    ...(imo && { imo }),
    ...(uuid && { uuid }),
  });
}

/** Up to 100 vessels in a single request. */
async function getVesselBulk(mmsiList) {
  return apiGet("/vessel_bulk", { mmsi: mmsiList.join(",") });
}

/**
 * All vessels currently within a radius of a point or port.
 * Credit cost: 1 per vessel found, capped at 500.
 */
async function getVesselsInRadius({ lat, lon, radius = 10, portUnlocode, type, typeSpecific } = {}) {
  return apiGet("/vessel_inradius", {
    ...(lat !== undefined && { lat }),
    ...(lon !== undefined && { lon }),
    radius,
    ...(portUnlocode && { port_unlocode: portUnlocode }),
    ...(type && { type }),
    ...(typeSpecific && { type_specific: typeSpecific }),
  });
}

/**
 * Historical AIS positions for a vessel.
 * Credit cost: 1 per vessel-day.
 */
async function getVesselHistory({ mmsi, imo, days, dateFrom, dateTo } = {}) {
  return apiGet("/vessel_history", {
    ...(mmsi && { mmsi }),
    ...(imo && { imo }),
    ...(days && { days }),
    ...(dateFrom && { from: dateFrom }),
    ...(dateTo && { to: dateTo }),
  });
}

/** Static vessel specifications: dimensions, TEU, tonnage, etc. */
async function getVesselInfo({ mmsi, imo, uuid } = {}) {
  return apiGet("/vessel_info", {
    ...(mmsi && { mmsi }),
    ...(imo && { imo }),
    ...(uuid && { uuid }),
  });
}

/** Current API credit usage. Free — no credits consumed. */
async function getCreditUsage() {
  return apiGet("/stat");
}

// ---------------------------------------------------------------------------
// Demo
// ---------------------------------------------------------------------------

async function main() {
  console.log("--- Credit balance ---");
  const stat = await getCreditUsage();
  const { plan, credits_used, credits_total, reset_date } = stat.data;
  console.log(`  Plan: ${plan}`);
  console.log(`  Credits: ${credits_used} / ${credits_total}`);
  console.log(`  Resets: ${reset_date}`);

  console.log("\n--- Real-time position: MAERSK CHENNAI ---");
  const vessel = await getVessel({ mmsi: "566093000" });
  if (vessel.meta.success) {
    const v = vessel.data;
    console.log(`  ${v.name}  ${v.lat.toFixed(4)}°N ${v.lon.toFixed(4)}°E  ${v.speed} kt  → ${v.destination}`);
    console.log(`  Status: ${v.navigational_status}`);
  }

  console.log("\n--- Pro data (ETA, ATD, draught) ---");
  const pro = await getVesselPro({ mmsi: "566093000" });
  if (pro.meta.success) {
    const v = pro.data;
    console.log(`  ETA: ${v.eta_UTC ?? "unknown"}`);
    console.log(`  Draught: ${v.draught_avg} m avg`);
  }

  console.log("\n--- Static specs ---");
  const info = await getVesselInfo({ imo: "9525338" });
  if (info.meta.success) {
    const v = info.data;
    console.log(`  ${v.name}  built ${v.year_built}  ${v.deadweight} DWT  TEU: ${v.teu}`);
    console.log(`  ${v.length} m × ${v.breadth} m  GT: ${v.gross_tonnage}`);
  }

  console.log("\n--- All cargo vessels in Rotterdam (5 NM) ---");
  const inRadius = await getVesselsInRadius({ portUnlocode: "NLRTM", radius: 5, type: "Cargo" });
  console.log(`  Found ${inRadius.data.length} cargo vessels`);
  inRadius.data.slice(0, 3).forEach((v) => {
    console.log(`    ${v.name} (${v.type_specific})  ${v.speed} kt`);
  });

  console.log("\n--- SAT-E estimated position ---");
  const est = await getVesselProEst({ mmsi: "566093000" });
  if (est.meta.success) {
    const v = est.data;
    const ep = v.estimated_position;
    if (ep) {
      console.log(`  Last known: ${v.lat.toFixed(4)}°N ${v.lon.toFixed(4)}°E`);
      console.log(`  Estimated:  ${ep.lat.toFixed(4)}°N ${ep.lon.toFixed(4)}°E  (vessel out of AIS range)`);
    } else {
      console.log(`  ${v.name} is within AIS range — no estimate needed`);
    }
  }

  console.log("\n--- Historical: last 3 days ---");
  const history = await getVesselHistory({ mmsi: "566093000", days: 3 });
  const positions = history.data;
  console.log(`  ${positions.length} position records`);
  if (positions.length > 0) {
    const last = positions[positions.length - 1];
    console.log(`  Latest: ${last.timestamp_UTC}  ${last.lat.toFixed(4)}°N ${last.lon.toFixed(4)}°E`);
  }

  console.log("\n--- Bulk request: 3 vessels ---");
  const bulk = await getVesselBulk(["566093000", "636016785", "477305700"]);
  bulk.data.forEach((v) => {
    if (v) console.log(`  ${v.name}  ${v.navigational_status}`);
  });
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
