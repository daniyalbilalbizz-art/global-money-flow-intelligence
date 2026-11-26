"""Free/public data adapters. All adapters return normalized, provenance-aware records."""
from datetime import datetime, timezone
import hashlib
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "GMF-OS/0.1 (open-source research tool)", "Accept": "application/json"})
retry = Retry(total=3, connect=3, read=3, backoff_factor=0.5,
              status_forcelist=(429, 500, 502, 503, 504), allowed_methods=frozenset(["GET"]))
SESSION.mount("https://", HTTPAdapter(max_retries=retry))

def _utc_now():
    return datetime.now(timezone.utc).isoformat()

def _record(series_id, source_id, value, unit, observed_at, frequency, source_record_id=None, metadata=None):
    retrieved = _utc_now()
    stable = "|".join([source_id, series_id, str(observed_at), str(value)])
    return {
        "observation_id": hashlib.sha256(stable.encode()).hexdigest(),
        "series_id": series_id, "source_id": source_id, "value": float(value), "unit": unit,
        "observed_at": observed_at, "published_at": None, "retrieved_at": retrieved,
        "frequency": frequency, "evidence_class": "REPORTED", "quality_status": "VALID",
        "source_record_id": source_record_id, "metadata": metadata or {}
    }

def _get_json(url, params=None, timeout=20):
    response = SESSION.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()

def fetch_fred_series(series_id, api_key=None, observation_start=None):
    """Fetch a FRED series. Requires a free FRED API key."""
    key = api_key or os.getenv("FRED_API_KEY")
    if not key:
        raise RuntimeError("FRED_API_KEY is missing. Add a free FRED API key to the app's secrets.")
    params = {"series_id": series_id, "api_key": key, "file_type": "json"}
    if observation_start:
        params["observation_start"] = observation_start
    data = _get_json("https://api.stlouisfed.org/fred/series/observations", params)
    observations = []
    for item in data.get("observations", []):
        raw = item.get("value")
        if raw in (None, ".", ""):
            continue
        observations.append(_record(series_id, "fred", float(raw), "source_defined",
            item["date"] + "T00:00:00+00:00", "series_defined", item.get("realtime_start"),
            {"realtime_start": item.get("realtime_start"), "realtime_end": item.get("realtime_end")}))
    return observations

def fetch_treasury_dataset(endpoint, page_size=100):
    """Fetch a documented Treasury Fiscal Data API endpoint supplied by config."""
    if not endpoint.startswith("https://api.fiscaldata.treasury.gov/services/api/fiscal_service/"):
        raise ValueError("Use a verified api.fiscaldata.treasury.gov fiscal_service endpoint.")
    payload = _get_json(endpoint, {"page[size]": min(int(page_size), 1000), "sort": "-record_date"})
    rows = payload.get("data", [])
    return rows, payload.get("meta", {})

def fetch_defillama_stablecoins():
    """Fetch public stablecoin overview; returns raw provider payload with retrieval time."""
    payload = _get_json("https://stablecoins.llama.fi/stablecoins")
    return {"source_id": "defillama", "retrieved_at": _utc_now(), "data": payload}

def fetch_sec_company_submissions(cik):
    """Fetch public SEC submissions metadata for a 10-digit zero-padded CIK."""
    cik10 = str(cik).zfill(10)
    payload = _get_json(f"https://data.sec.gov/submissions/CIK{cik10}.json")
    return {"source_id": "sec_edgar", "retrieved_at": _utc_now(), "data": payload}

def fetch_cftc_socrata(dataset_id, limit=1000):
    """Fetch a CFTC public Socrata dataset using its documented dataset identifier."""
    if not dataset_id or not str(dataset_id).strip():
        raise ValueError("Provide the official CFTC Socrata dataset identifier after verifying the chosen report.")
    url = f"https://publicreporting.cftc.gov/resource/{dataset_id}.json"
    return _get_json(url, {"$limit": min(int(limit), 50000), "$order": "report_date_as_yyyy_mm_dd DESC"})

