Daegu-Groundwater-Quality-Analysis
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/Status-In%20Progress-green?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/License-Private-lightgrey?style=for-the-badge" alt="License: Private">
</p>

Spatiotemporal analysis and forecasting of groundwater quality for the Daegu National Industrial Complex using AI models.

This project aims to analyze and predict the groundwater quality within the Daegu National Industrial Complex by leveraging spatiotemporal data from a strategically selected sensor network. Various deep learning models are implemented and compared to build a robust forecasting system.

<br>

Table of Contents
Dataset

Methodology

Sensor-Network

<br>

Dataset
The dataset used in this study is confidential and not publicly available. It is comprised of time-series data from monitoring wells managed by the National Groundwater Information Center (GIMS).

<br>

Methodology
The core of this research lies in establishing a scientifically sound monitoring network to ensure the quality and representativeness of the data used for AI modeling. The selection process was guided by two primary principles:

1. General Rationale
Data Homogeneity: To ensure data comparability, all selected wells monitor the same deep bedrock aquifer. This minimizes potential errors from mixing data from different hydrogeological units.

Relevance to Objective: The wells are located within and around the industrial complex, maximizing sensitivity to changes caused by industrial activities.

Data Availability: Wells with sufficient and reliable historical data were chosen to facilitate robust time-series analysis and model training.

2. Triangulation Configuration
Spatial Representativeness: A triangular formation was used to effectively encompass the target area, reducing spatial bias and enabling a more generalized analysis.

Groundwater Flow Estimation: The network provides the necessary data to estimate groundwater flow direction, which is critical for tracking contaminant movement.

Enhanced Model Input: Spatially distributed data enriches the input for AI models, allowing them to learn complex spatial patterns and improving predictive performance.

<br>

Sensor Network
The following three monitoring wells were selected to form the triangulation network for this study.

No.	Sensor Name	Location (Relative to Target)	Aquifer Type	Role in Network
1	Daegu Nongong_Sin	North	Bedrock	Northern boundary monitoring
2	Daegu Hyeonpung	Northeast	Bedrock	Inflow/outflow monitoring
3	Daegu Guji 2-ri	Internal	Deep Layer	Direct impact measurement

Sheets로 내보내기
Triangulation Network Visualization
The image below illustrates the final configuration of the sensor network relative to the Daegu National Industrial Complex.
