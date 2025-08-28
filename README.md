# Daegu-Groundwater-Quality-Analysis

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/Status-In%20Progress-green?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/License-Private-lightgrey?style=for-the-badge" alt="License: Private">
</p>

> Spatiotemporal analysis and forecasting of groundwater quality for the Daegu National Industrial Complex using AI models.

This project aims to analyze and predict the groundwater quality within the Daegu National Industrial Complex by leveraging spatiotemporal data from a strategically selected sensor network. Various deep learning models are implemented and compared to build a robust forecasting system.

---

## Table of Contents
- [Dataset](#dataset)
- [Methodology](#methodology)
- [Sensor-Network](#sensor-network)
- [Preprocessing & Merge](#preprocessing--merge)

---

## Dataset

The dataset used in this study is confidential and not publicly available.  
It is comprised of time-series data from monitoring wells managed by the **National Groundwater Information Center (GIMS)**.

- **Sampling frequency**: hourly  
- **Variables**: Water Level, Water Temperature, EC  
- **Period**: 2021–2025 (continuous monitoring)  

---

## Methodology

The core of this research lies in establishing a scientifically sound monitoring network to ensure the quality and representativeness of the data used for AI modeling. The selection process was guided by two primary principles:

### 1. General Rationale
- **Data Homogeneity:** All selected wells monitor the same **deep bedrock aquifer** to ensure comparability.  
- **Relevance to Objective:** Wells are located inside/around the industrial complex for sensitivity to industrial impacts.  
- **Data Availability:** Sufficient historical data for time-series modeling.  

### 2. Triangulation Configuration
- **Spatial Representativeness:** A triangular formation reduces spatial bias.  
- **Groundwater Flow Estimation:** Provides flow direction estimates for tracking contaminants.  
- **Enhanced Model Input:** Spatially distributed data improves AI learning.  

---

## Sensor Network

The following three monitoring wells were selected to form the triangulation network for this study.

| No. | Sensor Name       | Location (Relative) | Aquifer Type | Role in Network             |
|:---:|:------------------|:--------------------|:-------------|:----------------------------|
| 1   | `Daegu Nongong_Sin` | North              | Bedrock      | Northern boundary monitoring |
| 2   | `Daegu Hyeonpung`   | Northeast          | Bedrock      | Inflow/outflow monitoring   |
| 3   | `Daegu Guji 2-ri`   | Internal           | Deep Layer   | Direct impact measurement   |

### Triangulation Network Visualization
<img width="800" height="800" alt="image" src="https://github.com/user-attachments/assets/67fdfb2b-491c-4681-98bc-deec8f5a7db8" />

---

## Preprocessing & Merge

Raw data from GIMS often contains:
- Slightly mismatched timestamp counts across wells  
- Occasional missing records (sensor downtime, maintenance, etc.)  

### Merge Strategy
- **Method:** Inner join on `timestamp` across all wells  
- **No interpolation:** To preserve scientific integrity of the raw record  
- **Dropped timestamps:** Logged and audited for transparency  

### Results
- **Original rows:**  
  - Seongsan: 32,603  
  - Sinchon: 32,606  
  - Cheonseon: 32,623  
- **Common timestamps after merge:** **32,592**  
- **Dropped counts:**  
  - Seongsan → 11 (0.03%)  
  - Sinchon → 14 (0.04%)  
  - Cheonseon → 31 (0.09%)  

All dropped timestamps are recorded in [`Changwon_Alluvial_merge_audit.csv`](data/processed/Changwon_Alluvial_merge_audit.csv).

### File Organization
