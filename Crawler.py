# gims_fetch_30d.py

import requests
import pandas as pd
from functools import reduce
from datetime import datetime, timedelta
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# ---------------------------
# Hyperparameters (user config)
# ---------------------------
SENSOR_CODE = "777748"       # Observation well code (gennum)
START_DATE  = "20210101"     # Start date (YYYYMMDD)
END_DATE    = "20250828"     # End date   (YYYYMMDD)
CHUNK_DAYS  = 30             # Interval split (default 30 days)
OUTPUT_ENCODING = "utf-8-sig"

FEATURES_TO_SCRAPE = {
    "Water_Level": "selectRealTimeChart1.do",  # Water level
    "Water_Temp":  "selectRealTimeChart2.do",  # Water temperature
    "EC":          "selectRealTimeChart3.do",  # Electrical conductivity
}

BASE_URL = "https://www.gims.go.kr/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; gims-fetch/1.0)",
    "Referer": "https://www.gims.go.kr/natnPollutnObsvStts.do",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json, text/javascript, */*; q=0.01",
}

# ---------------------------
# Utility functions
# ---------------------------
def make_session():
    """Create a requests session with retry policy."""
    s = requests.Session()
    s.headers.update(HEADERS)
    retry = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    s.mount("https://", HTTPAdapter(max_retries=retry))
    return s

def date_chunks(start, end, days=30):
    """Split a date range into smaller chunks (default: 30 days)."""
    cur = datetime.strptime(start, "%Y%m%d")
    end_dt = datetime.strptime(end, "%Y%m%d")
    while cur <= end_dt:
        seg_end = min(cur + timedelta(days=days), end_dt)
        yield cur.strftime("%Y%m%d"), seg_end.strftime("%Y%m%d")
        cur = seg_end + timedelta(days=1)

def parse_series_json(records, feature_name):
    """Convert JSON response records into a pandas DataFrame."""
    if not records:
        return None
    if isinstance(records, dict):
        for v in records.values():
            if isinstance(v, list) and v:
                records = v
                break
    if not isinstance(records, list) or not records:
        return None

    ts_keys = ["n", "date", "dt", "timestamp"]
    val_keys = ["c", "value", "val", "v"]
    sample = records[0]
    tsk = next((k for k in ts_keys if k in sample), None)
    vak = next((k for k in val_keys if k in sample), None)
    if tsk is None or vak is None:
        print(f"[WARN] {feature_name}: unexpected keys {list(sample.keys())}")
        return None

    df = pd.DataFrame(records).rename(columns={tsk: "timestamp", vak: feature_name})
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df[feature_name] = pd.to_numeric(df[feature_name], errors="coerce")
    df = df.dropna(subset=["timestamp"]).drop_duplicates(subset=["timestamp"])
    return df[["timestamp", feature_name]]

def fetch_feature_data(feature_name, api_endpoint, sensor_code, start_date, end_date, session=None):
    """Fetch time series data for a given feature and observation well."""
    ses = session or make_session()
    url = BASE_URL + api_endpoint
    parts = []

    for fdate, edate in date_chunks(start_date, end_date, days=CHUNK_DAYS):
        params = {"gennum": sensor_code, "fdate": fdate, "edate": edate, "type": "json"}
        try:
            r = ses.get(url, params=params, timeout=20)
            try:
                data = r.json()
            except Exception:
                ct = r.headers.get("Content-Type", "")
                print(f"[{feature_name}] {fdate}~{edate}: invalid JSON (Content-Type={ct})")
                continue

            df = parse_series_json(data, feature_name)
            if df is None or df.empty:
                print(f"[{feature_name}] {fdate}~{edate}: no data")
                continue
            parts.append(df)

        except requests.RequestException as e:
            print(f"[{feature_name}] {fdate}~{edate}: request failed: {e}")
            continue

    if not parts:
        return None
    out = pd.concat(parts, ignore_index=True).sort_values("timestamp").drop_duplicates("timestamp")
    print(f"{feature_name}: {len(out)} rows collected")
    return out

# ---------------------------
# Main execution
# ---------------------------
if __name__ == "__main__":
    ses = make_session()
    dfs = []
    for feat, ep in FEATURES_TO_SCRAPE.items():
        df = fetch_feature_data(feat, ep, SENSOR_CODE, START_DATE, END_DATE, session=ses)
        if df is not None and not df.empty:
            dfs.append(df)

    if len(dfs) > 1:
        merged = reduce(lambda l, r: pd.merge(l, r, on="timestamp", how="outer"), dfs)
        merged = merged.sort_values("timestamp").drop_duplicates("timestamp")
        print("\n--- Data preview ---")
        print(merged.head())
        out = f"gims_30d_{SENSOR_CODE}_{START_DATE}_{END_DATE}.csv"
        merged.to_csv(out, index=False, encoding=OUTPUT_ENCODING)
        print(f"\nSaved to {out}")
    elif len(dfs) == 1:
        out = f"gims_30d_single_{SENSOR_CODE}_{START_DATE}_{END_DATE}.csv"
        dfs[0].to_csv(out, index=False, encoding=OUTPUT_ENCODING)
        print(f"\nSaved single feature to {out}")
    else:
        print("\nNo data collected")
