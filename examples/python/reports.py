"""
examples/python/reports.py

Async bulk data export: submit a report job, poll until complete,
then download the CSV.

Requirements:
    pip install requests

Usage:
    DATALASTIC_KEY=your_api_key python3 examples/python/reports.py
"""

import os
import time
import urllib.request
from pathlib import Path

import requests

API_KEY = os.environ.get("DATALASTIC_KEY")
if not API_KEY:
    raise ValueError("Set the DATALASTIC_KEY environment variable")

BASE_URL = "https://api.datalastic.com/api/v0"
SESSION = requests.Session()


def submit_report(report_type: str, **kwargs) -> str:
    """
    Submit an async report job. Returns the report_id.

    report_type values:
        vessel_list, port_list, request_usage, inradius_history,
        dry_dock_dates, companies, casualty, inspections,
        sales_purchase_demolitions, ownership, class_society, engine

    Additional kwargs are passed as JSON payload fields (e.g. lat, lon,
    radius, from, to, updated_from).
    """
    payload = {"api-key": API_KEY, "report_type": report_type, **kwargs}
    r = SESSION.post(f"{BASE_URL}/report", json=payload)
    r.raise_for_status()
    data = r.json()

    if not data["meta"]["success"]:
        raise RuntimeError(f"Report submission failed: {data}")

    report_id = data["data"]["report_id"]
    print(f"Submitted {report_type} report — ID: {report_id}")
    return report_id


def poll_report(report_id: str, interval: int = 5, timeout: int = 300) -> dict:
    """
    Poll a report job until status is DONE or FAILED.

    Returns the completed report job object (including result_url).
    Raises TimeoutError if the job doesn't complete within `timeout` seconds.
    """
    elapsed = 0
    while elapsed < timeout:
        r = SESSION.get(f"{BASE_URL}/report", params={"api-key": API_KEY, "report_id": report_id})
        r.raise_for_status()
        job = r.json()["data"]

        status = job["status"]
        print(f"  [{elapsed:>4}s] {report_id} — {status}")

        if status == "DONE":
            return job
        if status == "FAILED":
            raise RuntimeError(f"Report {report_id} failed.")

        time.sleep(interval)
        elapsed += interval

    raise TimeoutError(f"Report {report_id} did not complete within {timeout}s")


def download_csv(result_url: str, output_path: str) -> Path:
    """Download the completed report CSV to a local file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(result_url, path)
    size_kb = path.stat().st_size / 1024
    print(f"  Downloaded to {path} ({size_kb:.1f} KB)")
    return path


def run_report(report_type: str, output_path: str, **kwargs) -> Path:
    """End-to-end: submit → poll → download. Returns the local CSV path."""
    report_id = submit_report(report_type, **kwargs)
    job = poll_report(report_id)
    return download_csv(job["result_url"], output_path)


def list_all_reports() -> list[dict]:
    """Return all previously generated reports for this API key."""
    r = SESSION.get(f"{BASE_URL}/report", params={"api-key": API_KEY, "report_id": "_all"})
    r.raise_for_status()
    return r.json()["data"]


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== All previous reports ===")
    reports = list_all_reports()
    for job in reports[:5]:
        print(f"  {job['report_id']}  {job['report_type']}  {job['status']}")

    print("\n=== API usage report for April 2026 ===")
    run_report(
        "request_usage",
        output_dir="/tmp/datalastic-exports/usage_april_2026.csv",
        **{"from": "2026-04-01", "to": "2026-04-30"},
    )

    print("\n=== Historical location traffic — Rotterdam, 1-3 Jan 2026 ===")
    run_report(
        "inradius_history",
        "/tmp/datalastic-exports/rotterdam_jan2026.csv",
        lat=51.8951,
        lon=4.3973,
        radius=10,
        **{"from": "2026-01-01", "to": "2026-01-03"},
    )

    print("\n=== Ownership bulk export (updated since 2024) ===")
    run_report(
        "ownership",
        "/tmp/datalastic-exports/ownership_2024_onwards.csv",
        updated_from="2024-01-01",
    )

    print("\nAll done.")
