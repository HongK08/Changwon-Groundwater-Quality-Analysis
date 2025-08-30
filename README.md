# Changwon Groundwater Quality Analysis & Forecasting

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/Status-Completed-blue?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/License-Private-lightgrey?style=for-the-badge" alt="License: Private">
</p>

> Spatiotemporal analysis and AI-driven forecasting of groundwater quality in the **Changwon Alluvial Aquifer**. This project systematically evaluates multiple deep learning architectures and feature sets to build the most accurate predictive model for groundwater dynamics.

This repository contains a complete, iterative pipeline for analyzing and forecasting groundwater quality in the Changwon region. We process raw hourly monitoring data, correct sensor errors, handle data gaps via interpolation, and conduct a series of controlled experiments to identify the optimal model and feature combination.

---

## Table of Contents
- [Dataset](#dataset)
- [Methodology](#methodology)
- [Experimental Results](#experimental-results)
- [Key Findings & Conclusion](#key-findings--conclusion)
- [Final Model Recommendation](#final-model-recommendation)
- [File Organization](#file-organization)

---

## Dataset

The dataset is sourced from the **National Groundwater Information Center (GIMS)** and consists of hourly time-series data from three alluvial wells in Changwon (Seongsan, Sinchon, Cheonseon) for the period **2021–2025**. After preprocessing, the final dataset contains **32,673 continuous hourly observations**.

---

## Methodology

Our analysis follows a rigorous, multi-stage experimental design to ensure robust and reproducible results.

1.  **Preprocessing**: Raw data from three wells was merged using an `outer join` to create a complete time index. Identified sensor errors (`EC=0`) and gaps were filled using **Linear Interpolation**, creating a continuous, high-integrity dataset suitable for time-series modeling.

2.  **Feature Engineering**: A rich set of features was engineered to provide the models with comprehensive information:
    - **Core Features**: Water Level, Water Temperature.
    - **Target-related Features**: Raw `EC` and temperature-corrected `EC25`.
    - **Static Features**: DEM-derived ground `Elevation` for each well.
    - **Volatility Features**: Rate of Change (`EC_RoC`) and 6-hour Rolling Standard Deviation (`EC_Std6H`).
    - **Lag Features**: Past `EC25` values from 24h, 168h (weekly), and 720h (monthly) ago.

3.  **Model Architectures**: Two primary architectures were evaluated:
    - **Vanilla LSTM**: A standard LSTM network serving as a strong baseline.
    - **LSTM with Attention**: An enhanced architecture designed to focus on the most relevant past time steps, especially for long-term forecasting.
    - Both models were trained with regularization (Dropout, Weight Decay) and Early Stopping to prevent overfitting.

4.  **Controlled Experiments**: We conducted three main experiments by training the models on different feature sets to determine the optimal combination:
    - **`all_features`**: Uses all engineered features.
    - **`ec25_only`**: Uses a minimal set of core features + `EC25` and its LAGs.
    - **`ec_only`**: Uses a minimal set of core features + raw `EC` and its LAGs.

---

## Experimental Results

The following table summarizes the performance (R² score) of the best model architecture (**LSTM with Attention + LAGs**) across the three feature set experiments for the 90-day forecast horizon (t+90).

| Monitoring Well | `all_features` (R²) | **`ec25_only` (R²) 🏆** | `ec_only` (R²) |
|:---:|:---:|:---:|:---:|
| **Cheonseon** | 0.941 | **0.942** | 0.941 |
| **Sinchon** | 0.670 | **0.705** | 0.664 |
| **Seongsan** | -0.409 | -0.836 | **-0.381** |

---

## Key Findings & Conclusion

Our systematic experiments led to several critical insights:

1.  **The "Less is More" Principle for Features**: The **`ec25_only`** feature set consistently outperformed the `all_features` set, especially for the Attention model. This indicates that additional features like water level and volatility acted as noise, confusing the model. The most effective approach was to provide the model with only the most crucial, high-signal information: temperature-corrected `EC25` and its past (`LAG`) values.

2.  **Attention + LAG is the Winning Combination**: The **LSTM with Attention** model, when combined with **LAG features**, proved to be the most powerful architecture. While the base Attention model struggled with overfitting, providing it with explicit LAG features allowed its "focusing" ability to shine, resulting in the highest accuracy for predictable sites (Sinchon and Cheonseon).

3.  **The Seongsan Anomaly - A Data Limitation Problem**: Across all experiments, **no model was able to successfully predict the long-term water quality for the Seongsan site**. The consistent failure, regardless of model complexity or feature set, strongly suggests this is a **data limitation problem**, not a modeling failure. The dynamics at Seongsan are likely driven by complex, external factors (e.g., irregular rainfall events, undocumented pumping, land-use changes) that are not present in the current dataset. This finding itself is a significant outcome of the research.

---

## Final Model Recommendation

-   For **Sinchon and Cheonseon**, the **`LSTMAttentionModel`** trained on the **`ec25_only` feature set with LAGs** is the definitive choice, delivering highly accurate and reliable forecasts (R² > 0.70).

-   For **Seongsan**, a different approach is required. Future work should focus on **incorporating external data** (especially rainfall data) or shifting the problem from forecasting to **anomaly detection** to identify when external events are impacting the system.

---

## File Organization

```bash
.
├── Model_Res
│   └── LSTM
│       ├── all_features
│       │   ├── lstm_lag/
│       │   └── attention_lag/
│       ├── ec25_only
│       │   ├── lstm_lag/
│       │   └── attention_lag/
│       └── ec_only
│           ├── lstm_lag/
│           └── attention_lag/
│
├── UQML_Changwon
│   ├── CODE
│   │   ├── Get_Data
│   │   │   └── FIN_DATA_IMP.py           (Final Preprocessing Script)
│   │   └── Models
│   │       └── run_all_models_final.py   (Final Training/Experiment Script)
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
