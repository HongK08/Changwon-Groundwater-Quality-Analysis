# dem_to_depth_changwon_windows.py
# 1) NGII DEM(.img)에서 각 관정 위치의 지표 표고(m AMSL) 샘플링
# 2) 병합 CSV(el.m)와 결합해 Depth to water (m bgs) 계산
#    depth = ground_elev_m_AMSL - Water_Level(el.m)

import os
from pathlib import Path
import pandas as pd
import rasterio
from rasterio.warp import transform

# --------------------------------------------------------------------
# USER CONFIG (Windows absolute paths)
# --------------------------------------------------------------------
# DEM 파일 절대경로(각 관정별 .img 파일을 직접 지정)
DEM_PATHS = {
    "Seongsan_Alluvial":  r"C:\Users\HongKi_LT\Desktop\신나는 지하수 그래프 크롤러\EDM\창원성산.img",
    "Sinchon_Alluvial":   r"C:\Users\HongKi_LT\Desktop\신나는 지하수 그래프 크롤러\EDM\창원신촌.img",
    "Cheonseon_Alluvial": r"C:\Users\HongKi_LT\Desktop\신나는 지하수 그래프 크롤러\EDM\창원천선.img",
}

# 제공한 좌표 (lat, lon)
SITE_COORDS = {
    "Seongsan_Alluvial":  (35.202756, 128.671303),  # 성산동 522 (central)
    "Sinchon_Alluvial":   (35.211574, 128.622809),  # 신촌동 67-5
    "Cheonseon_Alluvial": (35.184898, 128.696354),  # 천선동 1296-101
}

# Optional: merged CSV to add depth columns (el.m)
MERGED_CSV   = r"C:\Users\HongKi_LT\Desktop\신나는 지하수 그래프 크롤러\Changwon_Alluvial_3sites_inner_merge.csv"
OUT_ELEV_CSV = r"C:\Users\HongKi_LT\Desktop\신나는 지하수 그래프 크롤러\Changwon_site_elevations.csv"
OUT_DEPTH_CSV= r"C:\Users\HongKi_LT\Desktop\신나는 지하수 그래프 크롤러\Changwon_Alluvial_with_depth.csv"

# 한글/공백 경로 대응
os.environ["GDAL_FILENAME_IS_UTF8"] = "YES"

# --------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------
def sample_elevation(img_path: str, lat: float, lon: float) -> float:
    """DEM(.img)에서 주어진 WGS84(lat, lon)의 표고(m AMSL) 샘플."""
    img_p = Path(img_path)
    if not img_p.exists():
        raise FileNotFoundError(f"DEM not found: {img_p}")
    with rasterio.open(img_p) as src:
        # 위경도(EPSG:4326) -> DEM의 CRS로 변환 후 샘플링
        x, y = transform("EPSG:4326", src.crs, [lon], [lat])
        value = next(src.sample([(x[0], y[0])]))[0]
        return float(value)

# --------------------------------------------------------------------
# 1) 각 관정 표고 샘플링
# --------------------------------------------------------------------
rows = []
for site, (lat, lon) in SITE_COORDS.items():
    img_path = DEM_PATHS[site]
    elev = sample_elevation(img_path, lat, lon)
    rows.append({
        "site_id": site,
        "lat": lat,
        "lon": lon,
        "dem_path": img_path,
        "ground_elev_m_AMSL": elev,
    })
    print(f"{site:18s} | elev = {elev:.3f} m | {img_path}")

elev_df = pd.DataFrame(rows)
Path(OUT_ELEV_CSV).parent.mkdir(parents=True, exist_ok=True)
elev_df.to_csv(OUT_ELEV_CSV, index=False, encoding="utf-8-sig")
print(f"\nSaved site elevations -> {OUT_ELEV_CSV}")

# --------------------------------------------------------------------
# 2) 병합 CSV에 깊이(m bgs) 컬럼 추가: depth = ground_elev - el.m
# --------------------------------------------------------------------
if Path(MERGED_CSV).exists():
    merged = pd.read_csv(MERGED_CSV)

    # 필요한 수위 컬럼 확인
    need_cols = [
        "Water_Level_Seongsan",
        "Water_Level_Sinchon",
        "Water_Level_Cheonseon",
    ]
    missing = [c for c in need_cols if c not in merged.columns]
    if missing:
        raise ValueError(f"Missing columns in merged CSV: {missing}")

    # 표고 매핑
    elev_map = dict(zip(elev_df["site_id"], elev_df["ground_elev_m_AMSL"]))

    merged["Depth_Seongsan_m"]  = elev_map["Seongsan_Alluvial"]  - merged["Water_Level_Seongsan"]
    merged["Depth_Sinchon_m"]   = elev_map["Sinchon_Alluvial"]   - merged["Water_Level_Sinchon"]
    merged["Depth_Cheonseon_m"] = elev_map["Cheonseon_Alluvial"] - merged["Water_Level_Cheonseon"]

    merged.to_csv(OUT_DEPTH_CSV, index=False, encoding="utf-8-sig")
    print(f"Saved merged with depths -> {OUT_DEPTH_CSV}")
else:
    print(f"MERGED_CSV not found, skipped depth export: {MERGED_CSV}")
