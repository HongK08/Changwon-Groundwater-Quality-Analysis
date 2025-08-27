# -*- coding: utf-8 -*-
"""
GIMS 다중 센서 크롤러 (2021-12-14 ~ 어제까지, 365일 단위 쪼개기)
"""

import os, time, requests, pandas as pd
from functools import reduce
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Dict, List, Optional

# ===== 센서 정의 =====
SENSORS = [
    {"name": "창원신촌", "gennum": "777748", "address": "경상남도 창원시 성산구 신촌동 67-5",   "type": "충적", "role": "외부충적"},
    {"name": "창원팔용", "gennum": "777752", "address": "경상남도 창원시 의창구 팔용동 10-1",   "type": "충적", "role": "외부충적"},
    {"name": "창원천선", "gennum": "777750", "address": "경상남도 창원시 성산구 천선동 1296-101","type": "충적", "role": "외부충적"},
    {"name": "창원성산", "gennum": "777746", "address": "경상남도 창원시 성산구 성산동 522",     "type": "충적", "role": "중앙"},
    {"name": "창원화양", "gennum": "771698", "address": "경상남도 창원시 의창구 동읍 화양리 1241","type": "암반", "role": "외부암반"},
]

# ===== feature ↔ endpoint =====
FEATURES: Dict[str, List[str]] = {
    "Water_Level": ["selectRealTimeChart1.do"],  # 수위
    "Water_Temp":  ["selectRealTimeChart2.do"],  # 수온
    "EC":          ["selectRealTimeChart3.do"],  # EC
    "pH":          ["selectWtbobscd.do", "selectWobsbcd.do"],  # pH 후보
}

BASE_URL  = "https://www.gims.go.kr/"
OUTPUT_DIR = "./gims_outputs"
SESSION = requests.Session()
SESSION.headers.update({"User-Agent":"Mozilla/5.0 (data-collection)"})

def _get_json(url, params, retries=3, sleep_sec=0.6):
    for i in range(retries):
        try:
            r = SESSION.get(url, params=params, timeout=20)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            if i == retries-1:
                print(f"[ERR] {url} {params} -> {e}")
                return None
            time.sleep(sleep_sec)

def fetch_feature(feature, endpoints, sensor_code, start, end) -> Optional[pd.DataFrame]:
    for ep in endpoints:
        data = _get_json(BASE_URL + ep, {"gennum": sensor_code, "fdate": start, "edate": end})
        if not data: 
            continue
        try:
            df = pd.DataFrame(data)
            if "n" in df.columns and "c" in df.columns:
                df = df[["n","c"]].rename(columns={"n":"timestamp","c":feature})
                df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
                df[feature] = pd.to_numeric(df[feature], errors="coerce")
                df = df.dropna(subset=["timestamp"]).sort_values("timestamp")
                print(f"[OK] {feature}:{sensor_code} {start}~{end} via {ep} rows={len(df)}")
                return df
        except Exception:
            pass
    print(f"[MISS] {feature}:{sensor_code} {start}~{end}")
    return None

def fetch_sensor_all(sensor_code, start, end) -> Optional[pd.DataFrame]:
    frames = []
    for feat, eps in FEATURES.items():
        df = fetch_feature(feat, eps, sensor_code, start, end)
        if df is not None and len(df):
            frames.append(df)
        time.sleep(0.2)
    if not frames:
        return None
    if len(frames) == 1:
        return frames[0].sort_values("timestamp").reset_index(drop=True)
    merged = reduce(lambda l,r: pd.merge(l,r,on="timestamp", how="outer"), frames)
    return merged.sort_values("timestamp").reset_index(drop=True)

def split_fetch(sensor, start_date, end_date):
    """365일 단위로 쪼개서 전체 데이터프레임 병합"""
    all_chunks = []
    start_dt = datetime.strptime(start_date, "%Y%m%d")
    end_dt   = datetime.strptime(end_date, "%Y%m%d")

    cur = start_dt
    while cur < end_dt:
        next_dt = min(cur + timedelta(days=365), end_dt)
        s_str = cur.strftime("%Y%m%d")
        e_str = next_dt.strftime("%Y%m%d")
        df = fetch_sensor_all(sensor["gennum"], s_str, e_str)
        if df is not None and not df.empty:
            all_chunks.append(df)
        cur = next_dt + timedelta(days=1)

    if all_chunks:
        return pd.concat(all_chunks).drop_duplicates("timestamp").sort_values("timestamp")
    return None

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # === 날짜: 20211214 ~ 어제(KST) ===
    kst_now = datetime.now(ZoneInfo("Asia/Seoul"))
    END   = (kst_now - timedelta(days=1)).strftime("%Y%m%d")
    START = "20211214"
    print(f"[RANGE] {START} ~ {END} (KST)")

    for s in SENSORS:
        name, code, role, stype = s["name"], s["gennum"], s["role"], s["type"]
        print(f"\n===== {name} ({code}) {role}/{stype} =====")
        df = split_fetch(s, START, END)
        if df is None or df.empty:
            print(f"[SKIP] {name} 데이터 없음")
            continue

        out = os.path.join(OUTPUT_DIR, f"gw_{name}_{role}_{code}_{START}_{END}.csv")
        df.to_csv(out, index=False, encoding="utf-8-sig")
        print(f"[SAVE] {out} rows={len(df)}")
