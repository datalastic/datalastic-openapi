"""
examples/python/addons.py

Add-on dataset endpoints: ownership, dry dock, casualties, inspections,
sales & demolitions, classification society, engines, and companies.

Requirements:
    pip install requests

Usage:
    DATALASTIC_KEY=your_api_key python3 examples/python/addons.py
"""

import os
import requests

API_KEY = os.environ.get("DATALASTIC_KEY")
if not API_KEY:
    raise ValueError("Set the DATALASTIC_KEY environment variable")

BASE_URL = "https://api.datalastic.com/api/maritime_reports"
SESSION = requests.Session()
SESSION.params = {"api-key": API_KEY}  # type: ignore[assignment]


def get_ownership(
    imo: str | None = None,
    name: str | None = None,
    beneficial_owner: str | None = None,
    operator: str | None = None,
    technical_manager: str | None = None,
    updated_from: str | None = None,
) -> dict:
    """Return beneficial owner, operator, and manager data for a vessel."""
    params = {}
    if imo:
        params["imo"] = imo
    if name:
        params["name"] = name
    if beneficial_owner:
        params["beneficial_owner"] = beneficial_owner
    if operator:
        params["operator"] = operator
    if technical_manager:
        params["technical_manager"] = technical_manager
    if updated_from:
        params["updated_from"] = updated_from

    r = SESSION.get(f"{BASE_URL}/ownership", params=params)
    r.raise_for_status()
    return r.json()


def get_dry_dock(
    imo: str | None = None,
    name: str | None = None,
    dry_dock_from: str | None = None,
    dry_dock_to: str | None = None,
) -> dict:
    """Return planned and completed dry dock dates for a vessel."""
    params = {}
    if imo:
        params["imo"] = imo
    if name:
        params["name"] = name
    if dry_dock_from:
        params["dry_dock_from"] = dry_dock_from
    if dry_dock_to:
        params["dry_dock_to"] = dry_dock_to

    r = SESSION.get(f"{BASE_URL}/dry_dock_dates", params=params)
    r.raise_for_status()
    return r.json()


def get_casualties(
    imo: str | None = None,
    name: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> dict:
    """Return incident records with type, date, and narrative."""
    params = {}
    if imo:
        params["imo"] = imo
    if name:
        params["name"] = name
    if date_from:
        params["from"] = date_from
    if date_to:
        params["to"] = date_to

    r = SESSION.get(f"{BASE_URL}/casualty", params=params)
    r.raise_for_status()
    return r.json()


def get_inspections(
    imo: str | None = None,
    name: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> dict:
    """Return Port State Control inspection and detention records."""
    params = {}
    if imo:
        params["imo"] = imo
    if name:
        params["name"] = name
    if date_from:
        params["from"] = date_from
    if date_to:
        params["to"] = date_to

    r = SESSION.get(f"{BASE_URL}/inspections", params=params)
    r.raise_for_status()
    return r.json()


def get_sales_and_demolitions(
    imo: str | None = None,
    name: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> dict:
    """Return ship sales, purchase, and demolition transaction records."""
    params = {}
    if imo:
        params["imo"] = imo
    if name:
        params["name"] = name
    if date_from:
        params["from"] = date_from
    if date_to:
        params["to"] = date_to

    r = SESSION.get(f"{BASE_URL}/spd", params=params)
    r.raise_for_status()
    return r.json()


def get_class_society(
    imo: str | None = None,
    name: str | None = None,
    fuzzy: bool = False,
    beneficial_owner: str | None = None,
    technical_manager: str | None = None,
    updated_from: str | None = None,
) -> dict:
    """
    Return classification society, survey dates, structural dimensions,
    and engine details for a vessel.

    Set fuzzy=True for approximate name matching.
    """
    params: dict = {"fuzzy": 1 if fuzzy else 0}
    if imo:
        params["imo"] = imo
    if name:
        params["name"] = name
    if beneficial_owner:
        params["beneficial_owner"] = beneficial_owner
    if technical_manager:
        params["technical_manager"] = technical_manager
    if updated_from:
        params["updated_from"] = updated_from

    r = SESSION.get(f"{BASE_URL}/class_society", params=params)
    r.raise_for_status()
    return r.json()


def get_engine(
    imo: str | None = None,
    name: str | None = None,
    fuzzy: bool = False,
    updated_from: str | None = None,
) -> dict:
    """Return engine designation, MCO, builder, and designer for a vessel."""
    params: dict = {"fuzzy": 1 if fuzzy else 0}
    if imo:
        params["imo"] = imo
    if name:
        params["name"] = name
    if updated_from:
        params["updated_from"] = updated_from

    r = SESSION.get(f"{BASE_URL}/engine", params=params)
    r.raise_for_status()
    return r.json()


def get_company(
    company_imo: str | None = None,
    name: str | None = None,
    updated_from: str | None = None,
) -> dict:
    """Return maritime company profile (type, status, contacts, parent)."""
    params = {}
    if company_imo:
        params["company_imo"] = company_imo
    if name:
        params["name"] = name
    if updated_from:
        params["updated_from"] = updated_from

    r = SESSION.get(f"{BASE_URL}/companies", params=params)
    r.raise_for_status()
    return r.json()


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("--- Vessel ownership: KARLOVASI ---")
    result = get_ownership(imo="9951783")
    for rec in result["data"]:
        print(f"  {rec['vessel_name']}")
        print(f"    Beneficial owner: {rec['beneficial_owner']} ({rec['beneficial_owner_country']})")
        print(f"    Commercial manager: {rec['commercial_manager']}")

    print("\n--- Dry dock dates: MSC ANNICK ---")
    result = get_dry_dock(imo="9169122")
    for rec in result["data"]:
        print(f"  {rec['vessel_name']}")
        print(f"    Next dry dock: {rec['dry_dock_date']}")
        print(f"    IOPP expires:  {rec['iopp_exp_date']}")
        print(f"    Tech manager:  {rec['technical_manager']}")

    print("\n--- Casualties: VENTO ---")
    result = get_casualties(imo="9319569")
    for rec in result["data"]:
        print(f"  [{rec['casualty_date']}] {rec['casualty_type']}")
        print(f"    {rec['casualty_details'][:120]}...")

    print("\n--- Inspections: ESVAGT CASSIOPEIA ---")
    result = get_inspections(imo="9362126")
    for rec in result["data"]:
        detained = "DETAINED" if rec["detention"] == "TRUE" else "ok"
        print(f"  [{rec['inspection_date']}] {rec['inspection_authority']} — {rec['ship_deficiencies']} deficiencies — {detained}")

    print("\n--- Classification: DARYA RASHMI ---")
    result = get_class_society(imo="9950404")
    for rec in result["data"]:
        print(f"  {rec['vessel_name']}  class: {rec['class1_code']}  LOA: {rec['loa']} m")
        print(f"    Engine: {rec['engine_designation']} by {rec['engine_builder']}")

    print("\n--- Engine specs (fuzzy name: DARYA) ---")
    result = get_engine(name="DARYA", fuzzy=True)
    for rec in result["data"]:
        print(f"  {rec['vessel_name']}  {rec['engine_designation']}  {rec['mco']} {rec['mco_unit']} @ {rec['mco_rpm']} rpm")
