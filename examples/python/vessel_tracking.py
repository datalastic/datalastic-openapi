"""
examples/python/vessel_tracking.py

Real-time and historical AIS vessel tracking with the Datalastic API.

Requirements:
    pip install requests

Usage:
    DATALASTIC_KEY=your_api_key python3 examples/python/vessel_tracking.py
"""

import os
import time
import requests
from datetime import date, timedelta

API_KEY = os.environ.get("DATALASTIC_KEY")
if not API_KEY:
    raise ValueError("Set the DATALASTIC_KEY environment variable")

BASE_URL = "https://api.datalastic.com/api/v0"
SESSION = requests.Session()
SESSION.params = {"api-key": API_KEY}  # type: ignore[assignment]


def get_vessel(mmsi: str | None = None, imo: str | None = None, uuid: str | None = None) -> dict:
    """Fetch real-time AIS position (basic) for a single vessel."""
    params = {}
    if mmsi:
        params["mmsi"] = mmsi
    if imo:
        params["imo"] = imo
    if uuid:
        params["uuid"] = uuid

    r = SESSION.get(f"{BASE_URL}/vessel", params=params)
    r.raise_for_status()
    return r.json()


def get_vessel_pro(mmsi: str | None = None, imo: str | None = None) -> dict:
    """Fetch real-time AIS position (pro) — includes ETA, ATD, draught."""
    params = {}
    if mmsi:
        params["mmsi"] = mmsi
    if imo:
        params["imo"] = imo

    r = SESSION.get(f"{BASE_URL}/vessel_pro", params=params)
    r.raise_for_status()
    return r.json()


def get_vessel_pro_est(mmsi: str | None = None, imo: str | None = None, uuid: str | None = None) -> dict:
    """
    SAT-E: fetch vessel_pro data plus an AI-estimated position.

    The `estimated_position` field is populated when the vessel has been out of
    terrestrial AIS range for 3+ hours. The estimate is calculated from the
    vessel's last known position, destination port, and ETA.

    **Credit cost:** 1 per vessel queried.
    """
    params = {}
    if mmsi:
        params["mmsi"] = mmsi
    if imo:
        params["imo"] = imo
    if uuid:
        params["uuid"] = uuid

    r = SESSION.get(f"{BASE_URL}/vessel_pro_est", params=params)
    r.raise_for_status()
    return r.json()


def get_vessel_bulk(mmsi_list: list[str]) -> dict:
    """Fetch real-time positions for up to 100 vessels in one request."""
    r = SESSION.get(f"{BASE_URL}/vessel_bulk", params={"mmsi": ",".join(mmsi_list)})
    r.raise_for_status()
    return r.json()


def get_vessel_history(
    mmsi: str,
    days: int | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> dict:
    """
    Fetch historical AIS positions for a vessel.

    Use `days` for a relative window (e.g. days=7 = last 7 days), or
    `from`/`to` (yyyy-mm-dd) for an explicit range.

    Credit cost: 1 per vessel-day.
    """
    params: dict = {"mmsi": mmsi}
    if days:
        params["days"] = days
    if date_from:
        params["from"] = date_from
    if date_to:
        params["to"] = date_to

    r = SESSION.get(f"{BASE_URL}/vessel_history", params=params)
    r.raise_for_status()
    return r.json()


def get_vessels_in_radius(
    lat: float | None = None,
    lon: float | None = None,
    radius: int = 10,
    port_unlocode: str | None = None,
    vessel_type: str | None = None,
    type_specific: str | None = None,
) -> dict:
    """
    Fetch all vessels currently within a radius of a point or port.

    Credit cost: 1 per vessel found, capped at 500.
    """
    params: dict = {"radius": radius}
    if lat is not None:
        params["lat"] = lat
    if lon is not None:
        params["lon"] = lon
    if port_unlocode:
        params["port_unlocode"] = port_unlocode
    if vessel_type:
        params["type"] = vessel_type
    if type_specific:
        params["type_specific"] = type_specific

    r = SESSION.get(f"{BASE_URL}/vessel_inradius", params=params)
    r.raise_for_status()
    return r.json()


def get_vessel_info(mmsi: str | None = None, imo: str | None = None) -> dict:
    """Fetch static vessel specifications (dimensions, tonnage, TEU, etc.)."""
    params = {}
    if mmsi:
        params["mmsi"] = mmsi
    if imo:
        params["imo"] = imo

    r = SESSION.get(f"{BASE_URL}/vessel_info", params=params)
    r.raise_for_status()
    return r.json()


def find_vessels(
    name: str | None = None,
    country_iso: str | None = None,
    vessel_type: str | None = None,
    type_specific: str | None = None,
) -> dict:
    """Search the vessel registry by name, flag, type, or subtype."""
    params = {}
    if name:
        params["name"] = name
    if country_iso:
        params["country_iso"] = country_iso
    if vessel_type:
        params["type"] = vessel_type
    if type_specific:
        params["type_specific"] = type_specific

    r = SESSION.get(f"{BASE_URL}/vessel_find", params=params)
    r.raise_for_status()
    return r.json()


def get_credit_usage() -> dict:
    """Return current API credit usage. Free — does not consume credits."""
    r = SESSION.get(f"{BASE_URL}/stat")
    r.raise_for_status()
    return r.json()


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import json

    print("--- Credit balance ---")
    stat = get_credit_usage()
    d = stat["data"]
    print(f"  Plan: {d['plan']}")
    print(f"  Credits used: {d['credits_used']} / {d['credits_total']}")
    print(f"  Resets: {d['reset_date']}")

    print("\n--- Real-time position for MAERSK CHENNAI ---")
    result = get_vessel(mmsi="566093000")
    if result["meta"]["success"]:
        v = result["data"]
        print(f"  {v['name']}  {v['lat']:.4f}°N {v['lon']:.4f}°E  speed {v['speed']} kt  → {v['destination']}")
    else:
        print("  Not found.")

    print("\n--- Static specs (IMO lookup) ---")
    result = get_vessel_info(imo="9525338")
    if result["meta"]["success"]:
        v = result["data"]
        print(f"  {v['name']}  {v['year_built']}  {v['deadweight']} DWT  TEU: {v['teu']}")

    print("\n--- All cargo vessels in Rotterdam (5 NM) ---")
    result = get_vessels_in_radius(port_unlocode="NLRTM", radius=5, vessel_type="Cargo")
    vessels = result["data"]
    print(f"  Found {len(vessels)} cargo vessels")
    for v in vessels[:3]:
        print(f"    {v['name']} ({v['type_specific']})  {v['speed']} kt")

    print("\n--- Historical data: last 7 days ---")
    result = get_vessel_history(mmsi="566093000", days=7)
    positions = result["data"]
    print(f"  {len(positions)} position records")
    if positions:
        first = positions[0]
        last = positions[-1]
        print(f"  Earliest: {first['timestamp_UTC']}  {first['lat']:.4f}°N {first['lon']:.4f}°E")
        print(f"  Latest:   {last['timestamp_UTC']}  {last['lat']:.4f}°N {last['lon']:.4f}°E")

    print("\n--- SAT-E estimated position ---")
    result = get_vessel_pro_est(mmsi="566093000")
    if result["meta"]["success"]:
        v = result["data"]
        est = v.get("estimated_position")
        if est:
            print(f"  Last known: {v['lat']:.4f}°N {v['lon']:.4f}°E")
            print(f"  Estimated:  {est['lat']:.4f}°N {est['lon']:.4f}°E  (vessel out of AIS range)")
        else:
            print(f"  {v['name']} is within AIS range — no estimate needed")

    print("\n--- Bulk request: 3 vessels ---")
    mmsi_list = ["566093000", "636016785", "477305700"]
    result = get_vessel_bulk(mmsi_list)
    print(f"  Returned {len(result['data'])} vessels")
    for v in result["data"]:
        if v:
            print(f"    {v['name']}  {v['navigational_status']}")
