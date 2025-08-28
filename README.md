# Changwon-Groundwater-Quality-Analysis

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/Status-In%20Progress-green?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/License-Private-lightgrey?style=for-the-badge" alt="License: Private">
</p>

> Spatiotemporal analysis of groundwater quality in **Changwon Alluvial Aquifer**  
> Focused on water level, temperature, and electrical conductivity (EC / EC25).

This project investigates groundwater dynamics in the Changwon region using hourly monitoring data.  
We preprocess, audit, and merge multiple well datasets, incorporating DEM-derived depth and temperature-corrected EC (EC25), to enable comparative analysis and AI-based modeling.

---

## Table of Contents
- [Dataset](#dataset)
- [Methodology](#methodology)
- [Monitoring-Wells](#monitoring-wells)
- [Preprocessing--Merge](#preprocessing--merge)
- [Feature Engineering](#feature-engineering)
- [File Organization](#file-organization)

---

## Dataset

The dataset is obtained from the **National Groundwater Information Center (GIMS)**.  
It includes **hourly time-series data** of:

- Water Level (m)
- Water Temperature (°C)
- Electrical Conductivity (µS/cm, raw sensor value)
- Depth (m, derived from DEM `.img` files)
- EC25 (µS/cm, normalized to 25 °C)

Period covered: **2021–2025** (continuous monitoring).  
Total merged records: **32,592 hourly observations**.

---

## Methodology

The analysis emphasizes **data integrity and transparency**:

1. **No Interpolation**  
   - All analyses are based on observed values only.  
   - Missing timestamps are dropped rather than filled.

2. **Inner Join Merge**  
   - Datasets from multiple wells are merged only on **common timestamps**.  
   - This ensures that every record represents simultaneous observations across wells.

3. **Audit Logging**  
   - Any timestamps dropped during merging are logged for reproducibility.  
   - Drop counts and sample timestamps are recorded per well.

4. **Depth Extraction (DEM)**  
   - Groundwater depth values (`Depth_Seongsan_m`, `Depth_Sinchon_m`, `Depth_Cheonseon_m`) are derived from DEM `.img` rasters.  

5. **Temperature Correction (EC → EC25)**  
   - Raw EC is corrected to 25 °C using the standard EC-25 formula.  
   - Both raw EC and EC25 are preserved in the dataset for modeling and comparison.

---

## Monitoring Wells

Three alluvial wells in Changwon were selected:

| No. | Well Name   | Aquifer Type | Role in Analysis              |
|:---:|:------------|:-------------|:------------------------------|
| 1   | Seongsan    | Alluvial     | Regional representative well  |
| 2   | Sinchon     | Alluvial     | Boundary monitoring           |
| 3   | Cheonseon   | Alluvial     | Event-sensitive observation   |

---

## Preprocessing & Merge

The merge and audit log generation were performed using:

- `scripts/merge_alluvial.py`

This script loads the three raw CSV files from `data/raw/`, performs an inner join on `timestamp`,  
applies DEM-based depth extraction and EC25 correction, and saves both the merged dataset and an audit log into `data/processed/`.

### Merge Results
- **Original Rows**  
  - Seongsan: 32,603  
  - Sinchon: 32,606  
  - Cheonseon: 32,623  

- **Final Common Timestamps (inner join):** **32,592**

- **Dropped Records**  
  - Seongsan → 11 (0.03%)  
  - Sinchon → 14 (0.04%)  
  - Cheonseon → 31 (0.09%)

### Example of Dropped Timestamps
- Seongsan: `2022-08-22 10:00`, `2023-08-24 11:00` …  
- Sinchon: `2023-05-24 12:00`, `2024-01-01 13:00` …  
- Cheonseon: `2021-12-07 16:00`, `2024-08-01 11:00` …

### Output Files
- `Changwon_Alluvial_with_depth_ec25.csv` — Merged dataset (**32,592 rows × 16 cols**)  
- `Changwon_Alluvial_merge_audit.csv` — Audit log (drop counts + timestamp samples)  

---

## Feature Engineering

For modeling and interpretation, we include:

- **Raw values**: EC, Water Temperature, Water Level  
- **Corrected values**: EC25 (temperature normalized)  
- **DEM-derived values**: Depth (per well)  
- **Derived features** (optional):  
  - ΔEC = EC25 – EC (magnitude of correction)  
  - Ratios such as EC25/Temp, EC/Level for correlation studies  

This ensures both physical interpretability and robust predictive modeling.

---

## File Organization

```bash
~/Desktop/UML_Changwon
├── CODE
│   ├── Crawler.py
│   ├── DEM_Import.py
│   ├── merge_alluvial.py
│   └── merge_Dep_and_EC25.py
│
├── DATA_SET
│   ├── FINAL_DATA
│   │   └── Changwon_Alluvial_with_depth_ec25.csv
│   │
│   ├── Original_Merged
│   │   ├── Changwon_Alluvial_3sites_inner_merge.csv
│   │   └── Changwon_Alluvial_merge_audit.csv
│   │
│   ├── RAW_DATA
│   │   ├── Changwon_Cheonseon_Alluvial.csv
│   │   ├── Changwon_Seongsan_Alluvial.csv
│   │   └── Changwon_Sinchon_Alluvial.csv
│   │
│   └── SITE_ELEVATIONS
│       └── Changwon_site_elevations.csv
│
└── EDM
    ├── 창원성산.img
    ├── 창원신촌.img
    └── 창원천선.img

