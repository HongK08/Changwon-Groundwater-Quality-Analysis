# scripts/merge_alluvial.py
"""
Merge groundwater monitoring datasets from Changwon (Seongsan, Sinchon, Cheonseon)
using inner join on timestamps. No interpolation is applied.
An audit log of dropped timestamps is also saved.
"""

import pandas as pd
from pathlib import Path

# ----------------------------
# User config (edit if needed)
# ----------------------------
BASE_DIR = Path("/home/hai/Desktop/UML/data")
RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = BASE_DIR / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

FILES = {
    "Seongsan": RAW_DIR / "Changwon_Seongsan_Alluvial.csv",
    "Sinchon": RAW_DIR / "Changwon_Sinchon_Alluvial.csv",
    "Cheonseon": RAW_DIR / "Changwon_Cheonseon_Alluvial.csv",
}

# ----------------------------
# Load and clean datasets
# ----------------------------
dfs = {}
audit = {}

for site, path in FILES.items():
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    # duplicates check
    dup_mask = df["timestamp"].duplicated(keep=False)
    dup_count = dup_mask.sum()
    dup_samples = df.loc[dup_mask, "timestamp"].astype(str).head(10).tolist()

    dfs[site] = df
    audit[site] = {
        "rows_original": len(df),
        "duplicates_by_timestamp": int(dup_count),
        "duplicate_timestamps_samples": dup_samples,
        "unique_ts_count": df["timestamp"].nunique(),
    }

# ----------------------------
# Find intersection of timestamps
# ----------------------------
ts_sets = {site: set(df["timestamp"]) for site, df in dfs.items()}
intersection_ts = set.intersection(*ts_sets.values())
intersection_count = len(intersection_ts)

# For each site, log dropped timestamps
for site, ts_set in ts_sets.items():
    dropped = sorted(list(ts_set - intersection_ts))
    audit[site].update({
        "dropped_count_for_inner": len(dropped),
        "dropped_pct_of_unique": round(100 * len(dropped) / audit[site]["unique_ts_count"], 4),
        "dropped_examples": [str(t) for t in dropped[:10]]
    })

# ----------------------------
# Merge datasets (inner join)
# ----------------------------
common_ts_sorted = pd.DataFrame({"timestamp": sorted(intersection_ts)})

def rename_vars(df, site):
    cols = ["timestamp", "Water_Level", "Water_Temp", "EC"]
    sub = df[cols].copy()
    return sub.rename(columns={
        "Water_Level": f"Water_Level_{site}",
        "Water_Temp": f"Water_Temp_{site}",
        "EC": f"EC_{site}",
    })

merged = common_ts_sorted.copy()
for site, df in dfs.items():
    merged = merged.merge(rename_vars(df, site), on="timestamp", how="left")

# ----------------------------
# Save outputs
# ----------------------------
merged_path = PROCESSED_DIR / "Changwon_Alluvial_3sites_inner_merge.csv"
audit_path = PROCESSED_DIR / "Changwon_Alluvial_merge_audit.csv"

merged.to_csv(merged_path, index=False, encoding="utf-8-sig")

audit_df = pd.DataFrame([
    {"site": site, **info, "intersection_count": intersection_count}
    for site, info in audit.items()
])
audit_df.to_csv(audit_path, index=False, encoding="utf-8-sig")

print("Merge complete.")
print(f" - Common timestamps: {intersection_count}")
print(f" - Merged file saved to: {merged_path}")
print(f" - Audit log saved to:   {audit_path}")
