# Changwon-Groundwater-Quality-Analysis

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/Status-In%20Progress-green?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/License-Private-lightgrey?style=for-the-badge" alt="License: Private">
</p>

> Spatiotemporal analysis of groundwater quality in **Changwon Alluvial Aquifer**  
> Focused on water level, temperature, and electrical conductivity (EC).

This project investigates groundwater dynamics in the Changwon region using hourly monitoring data.  
We preprocess, audit, and merge multiple well datasets to enable comparative analysis and AI-based modeling.

---

## Table of Contents
- [Dataset](#dataset)
- [Methodology](#methodology)
- [Monitoring-Wells](#monitoring-wells)
- [Preprocessing--Merge](#preprocessing--merge)

---

## Dataset

The dataset is obtained from the **National Groundwater Information Center (GIMS)**.  
It includes **hourly time-series data** of:

- Water Level (m)
- Water Temperature (°C)
- Electrical Conductivity (µS/cm)

Period covered: **2021–2025** (continuous monitoring).

---

## Methodology

The analysis emphasizes **data integrity and transparency**:

1. **No Interpolation**  
   - All analyses are based on observed values only.  
   - Missing timestamps are removed rather than filled.

2. **Inner Join Merge**  
   - Datasets from multiple wells are merged only on **common timestamps**.  
   - This ensures that every record represents simultaneous observations across wells.

3. **Audit Logging**  
   - Any timestamps dropped during merging are logged for reproducibility.  
   - Drop counts and examples are provided per well.

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
- `Changwon_Alluvial_3sites_inner_merge.csv` — Merged dataset (32,592 rows × 10 cols)  
- `Changwon_Alluvial_merge_audit.csv` — Audit log (drop counts + timestamp samples)  

### File Organization
