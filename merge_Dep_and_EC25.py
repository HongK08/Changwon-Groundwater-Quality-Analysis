# merge_depth_and_ec25_paths.py
# - Load merged dataset (inner-merged 3 sites) from Original_Merged
# - Load site elevations (DEM-derived) from SITE_ELEVATIONS
# - Add Depth (m bgs) and EC-25 columns, save to FINAL_DATA

import pandas as pd
from pathlib import Path
import glob

# -----------------------------
# Base paths (Windows)
# -----------------------------
BASE = Path(r"C:\Users\HongKi_LT\Desktop\UML_Changwon\DATA_SET")
DIR_ORIG   = BASE / "Original_Merged"
DIR_ELEV   = BASE / "SITE_ELEVATIONS"
DIR_FINAL  = BASE / "FINAL_DATA"
DIR_FINAL.mkdir(parents=True, exist_ok=True)

# If you use fixed filenames, set them here. Otherwise we will auto-detect.
MERGED_CSV = DIR_ORIG / "Changwon_Alluvial_3sites_inner_merge.csv"
ELEV_CSV   = DIR_ELEV / "Changwon_site_elevations.csv"

# Auto-detect if the fixed names are not found
if not MERGED_CSV.exists():
    cand = glob.glob(str(DIR_ORIG / "*.csv"))
    if not cand:
        raise FileNotFoundError(f"No CSV found in {DIR_ORIG}")
    MERGED_CSV = Path(sorted(cand)[0])

if not ELEV_CSV.exists():
    cand = glob.glob(str(DIR_ELEV / "*.csv"))
    if not cand:
        raise FileNotFoundError(f"No CSV found in {DIR_ELEV}")
    ELEV_CSV = Path(sorted(cand)[0])

OUT_CSV = DIR_FINAL / "Changwon_Alluvial_with_depth_ec25.csv"

# EC temperature compensation coefficient (per °C)
ALPHA = 0.019  # 0.019~0.020 commonly used

# Column mappings
SITE_TO_LEVEL_COL = {
    "Seongsan_Alluvial":  "Water_Level_Seongsan",
    "Sinchon_Alluvial":   "Water_Level_Sinchon",
    "Cheonseon_Alluvial": "Water_Level_Cheonseon",
}
SITE_TO_TEMP_COL = {
    "Seongsan_Alluvial":  "Water_Temp_Seongsan",
    "Sinchon_Alluvial":   "Water_Temp_Sinchon",
    "Cheonseon_Alluvial": "Water_Temp_Cheonseon",
}
SITE_TO_EC_COL = {
    "Seongsan_Alluvial":  "EC_Seongsan",
    "Sinchon_Alluvial":   "EC_Sinchon",
    "Cheonseon_Alluvial": "EC_Cheonseon",
}

if __name__ == "__main__":
    print(f"Reading merged: {MERGED_CSV}")
    print(f"Reading elevations: {ELEV_CSV}")

    merged = pd.read_csv(MERGED_CSV)
    elev   = pd.read_csv(ELEV_CSV)

    # Elevation lookup
    if "site_id" not in elev.columns or "ground_elev_m_AMSL" not in elev.columns:
        raise ValueError("Elevation CSV must contain columns: site_id, ground_elev_m_AMSL")
    elev_map = dict(zip(elev["site_id"], elev["ground_elev_m_AMSL"]))

    # Add Depth columns: depth = ground_elev - el.m
    for site, wl_col in SITE_TO_LEVEL_COL.items():
        if wl_col not in merged.columns:
            raise ValueError(f"Missing column in merged CSV: {wl_col}")
        if site not in elev_map:
            raise ValueError(f"Missing site in elevations CSV: {site}")
        out_col = f"Depth_{site.split('_')[0]}_m"  # e.g., Depth_Seongsan_m
        merged[out_col] = elev_map[site] - merged[wl_col]

    # Add EC-25 columns: EC25 = EC / (1 + ALPHA*(T-25))
    for site, ec_col in SITE_TO_EC_COL.items():
        t_col = SITE_TO_TEMP_COL[site]
        if ec_col not in merged.columns or t_col not in merged.columns:
            raise ValueError(f"Missing EC/Temp columns for site {site}: {ec_col}, {t_col}")
        out_col = f"EC25_{site.split('_')[0]}"
        merged[out_col] = merged[ec_col] / (1.0 + ALPHA * (merged[t_col] - 25.0))

    merged.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    print(f"Saved -> {OUT_CSV}")
