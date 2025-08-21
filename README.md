# Daegu-Groundwater-Quality-Analysis

\<p align="center"\>
\<img src="[https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge\&logo=python](https://www.google.com/search?q=https://img.shields.io/badge/Python-3.9%252B-blue%3Fstyle%3Dfor-the-badge%26logo%3Dpython)" alt="Python Version"\>
\<img src="[https://img.shields.io/badge/TensorFlow-2.x-FF6F00?style=for-the-badge\&logo=tensorflow](https://www.google.com/search?q=https://img.shields.io/badge/TensorFlow-2.x-FF6F00%3Fstyle%3Dfor-the-badge%26logo%3Dtensorflow)" alt="TensorFlow"\>
\<img src="[https://img.shields.io/badge/Pandas-2.0-blue?style=for-the-badge\&logo=pandas](https://www.google.com/search?q=https://img.shields.io/badge/Pandas-2.0-blue%3Fstyle%3Dfor-the-badge%26logo%3Dpandas)" alt="Pandas"\>
\<img src="[https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge](https://www.google.com/search?q=https://img.shields.io/badge/License-MIT-yellow.svg%3Fstyle%3Dfor-the-badge)" alt="License: MIT"\>
\</p\>

> Spatiotemporal analysis and forecasting of groundwater quality for the Daegu National Industrial Complex using AI models.

This project aims to analyze and predict the groundwater quality within the Daegu National Industrial Complex by leveraging spatiotemporal data from a strategically selected sensor network. Various deep learning models are implemented and compared to build a robust forecasting system.

\<br\>

## Table of Contents

  - [Methodology](https://www.google.com/search?q=%23-methodology)
  - [Sensor Network](https://www.google.com/search?q=%23-sensor-network)
  - [Installation](https://www.google.com/search?q=%23-installation)
  - [Usage](https://www.google.com/search?q=%23-usage)
  - [Results](https://www.google.com/search?q=%23-results)

\<br\>

## Methodology

The core of this research lies in establishing a scientifically sound monitoring network to ensure the quality and representativeness of the data used for AI modeling. The selection process was guided by two primary principles:

#### 1\. General Rationale

  - **Data Homogeneity:** To ensure data comparability, all selected wells monitor the same **deep bedrock aquifer**. This minimizes potential errors from mixing data from different hydrogeological units.
  - **Relevance to Objective:** The wells are located within and around the industrial complex, maximizing sensitivity to changes caused by industrial activities.
  - **Data Availability:** Wells with sufficient and reliable historical data were chosen to facilitate robust time-series analysis and model training.

#### 2\. Triangulation Configuration

  - **Spatial Representativeness:** A triangular formation was used to effectively encompass the target area, reducing spatial bias and enabling a more generalized analysis.
  - **Groundwater Flow Estimation:** The network provides the necessary data to estimate groundwater flow direction, which is critical for tracking contaminant movement.
  - **Enhanced Model Input:** Spatially distributed data enriches the input for AI models, allowing them to learn complex spatial patterns and improving predictive performance.

\<br\>

## Sensor Network

The following three monitoring wells were selected to form the triangulation network for this study.

| No. | Sensor Name | Location (Relative to Target) | Aquifer Type | Role in Network |
|:---:|:---|:---|:---|:---|
| 1 | `Daegu Nongong_Sin` | North | Bedrock | Northern boundary monitoring |
| 2 | `Daegu Hyeonpung` | Northeast | Bedrock | Inflow/outflow monitoring |
| 3 | `Daegu Guji 2-ri` | Internal | Deep Layer | Direct impact measurement |

### Triangulation Network Visualization

The image below illustrates the final configuration of the sensor network relative to the Daegu National Industrial Complex.

\<br\>

## Installation

*(Provide instructions on how to set up the project environment. Example below)*

```bash
# Clone the repository
git clone https://github.com/your-username/Daegu-Groundwater-Quality-Analysis.git
cd Daegu-Groundwater-Quality-Analysis

# Create a virtual environment and install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

\<br\>

## Usage

*(Provide instructions on how to run the code. Example below)*

```bash
# To run the data preprocessing script
python src/preprocess_data.py

# To train a model
python src/train_model.py --model N-BEATSx --epochs 100
```

\<br\>

## Results

*(Summarize the key findings or link to a more detailed report.)*

The comparative analysis demonstrates that the `[Best Model Name]` achieved the highest performance with an RMSE of `[value]` and an R² of `[value]`. Detailed results and visualizations can be found in the `reports/` directory.
