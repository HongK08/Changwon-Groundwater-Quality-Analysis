# Changwon Groundwater Quality Analysis & Forecasting

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/Status-Completed-blue?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/License-Private-lightgrey?style=for-the-badge" alt="License: Private">
</p>

> Spatiotemporal analysis and AI-driven forecasting of groundwater quality in the **Changwon Alluvial Aquifer**. This project focuses on modeling water level, temperature, and electrical conductivity (EC) to understand and predict groundwater dynamics.

This repository contains the complete pipeline for analyzing groundwater dynamics in the Changwon region. We process raw hourly monitoring data, correct sensor errors, handle data gaps through interpolation, and enrich the dataset with geospatial (DEM) and engineered features. The final, cleaned dataset serves as the foundation for building predictive AI models.

---

## Table of Contents
- [Dataset](#dataset)
- [Methodology](#methodology)
- [Monitoring Wells](#monitoring-wells)
- [Preprocessing & Feature Engineering](#preprocessing--feature-engineering)
- [AI Modeling](#ai-modeling)
- [File Organization](#file-organization)

---

## Dataset

The dataset is sourced from the **National Groundwater Information Center (GIMS)** and consists of hourly time-series data from three alluvial wells in Changwon.

- **Primary Variables**:
    - Water Level (m)
    - Water Temperature (°C)
    - Electrical Conductivity (EC, µS/cm)
- **Data Period**: **2021–2025** (continuous monitoring)
- **Final Dataset**: **32,673 hourly observations** after cleaning and interpolation.

---

## Methodology

The core of this project is the creation of a **continuous, high-integrity dataset** suitable for time-series modeling. The methodology was evolved from a simple `inner join` to a more robust `outer join` and interpolation approach.

1.  **Data Integration via `Outer Join`**: Datasets from the three wells are merged using an `outer join` on the `timestamp`. This creates a complete time index that preserves every observation from all wells, preventing data loss.

2.  **Error Correction & Linear Interpolation**:
    - **Error Identification**: Non-physical values (e.g., `EC = 0`) are identified as sensor errors and explicitly marked as missing data (`NaN`).
    - **Interpolation**: All missing data points—both from the outer join and the identified errors—are filled using **Linear Interpolation**. This method is chosen for its scientific validity in representing the gradual changes typical of groundwater systems.

3.  **Reproducibility**: The entire preprocessing pipeline is codified in `UQML_Changwon/CODE/Get_Data/FIN_DATA_IMP.py`, ensuring a fully reproducible workflow from raw data to the final model-ready dataset.

---

## Monitoring Wells

Three key alluvial wells in Changwon provide the data for this study:

| No. | Well Name | Aquifer Type | Role in Analysis | Ground Elevation (m) |
|:---:|:---|:---|:---|:---:|
| 1 | **Seongsan** | Alluvial | Regional representative well | 20.57 |
| 2 | **Sinchon** | Alluvial | Boundary monitoring | 7.84 |
| 3 | **Cheonseon** | Alluvial | Event-sensitive observation | 48.03 |

---

## Preprocessing & Feature Engineering

The raw data is transformed into a feature-rich dataset ready for advanced modeling.

### Preprocessing Pipeline
The `FIN_DATA_IMP.py` script automates the following:
1.  **Loads** raw CSV files from `UQML_Changwon/DATA_SET/RAW_DATA/`.
2.  **Merges** the data using an outer join and converts `0` values to `NaN`.
3.  **Reindexes** the data to a perfect hourly frequency.
4.  **Applies linear interpolation** to fill all gaps.
5.  **Executes feature engineering** steps and saves the final dataset.

### Engineered Features
To enhance the model's predictive power, several key features were engineered:

- **Temperature-Corrected EC (EC25)**: Raw EC is normalized to 25°C to remove temperature bias, providing a more stable indicator of water quality.
- **DEM-Derived Elevation**: The ground elevation for each well is added as a **static feature**, allowing the model to learn location-specific patterns.
- **Volatility Metrics**: To capture sudden changes—a key indicator of external events—the following are calculated:
    - **Rate of Change (EC\_RoC)**: The difference in EC from the previous hour.
    - **Rolling Standard Deviation (EC\_Std6H)**: The EC's standard deviation over a 6-hour window.

### Final Output File
- **`Changwon_Preprocessed_with_Features.csv`**: The final, model-ready dataset (**32,673 rows × 22 cols**).

---

## AI Modeling
The cleaned and feature-engineered dataset is used to train a predictive LSTM model.

- **Model Code**: `UQML_Changwon/CODE/Models/LSTM.py`
- **Key Capabilities**:
    - **Feature-Mode Switching**: Allows training with different feature sets (e.g., `ec25_only`, `all_features`).
    - **Early Stopping**: Prevents model overfitting by monitoring validation loss and saving the best-performing model.
    - **Automated Reporting**: Automatically generates performance metrics, heatmaps, and plots for each training run.
- **Results**: All model outputs, including predictions and reports, are saved under `Model_Res/LSTM/<feature_mode>/`.

---

## File Organization
.
├── Model_Res
│   └── LSTM
│       └── ... (AI model results are saved here)
│
├── UQML_Changwon
│   ├── CODE
│   │   ├── Get_Data
│   │   │   └── FIN_DATA_IMP.py  (Final Preprocessing Script)
│   │   └── Models
│   │       └── LSTM.py          (LSTM Model Training Script)
│   │
│   └── DATA_SET
│       ├── FINAL_DATA
│       │   └── Changwon_Preprocessed_with_Features.csv (MODEL-READY DATA)
│       │
│       ├── RAW_DATA
│       │   ├── Changwon_Cheonseon_Alluvial.csv
│       │   ├── Changwon_Seongsan_Alluvial.csv
│       │   └── Changwon_Sinchon_Alluvial.csv
│       │
│       └── SITE_ELEVATIONS
│           └── Changwon_site_elevations.csv
│
└── ... (Other project folders)
