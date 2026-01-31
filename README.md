# Delhi Air Quality Predictor

Air quality (AQI proxy) prediction using machine learning models.

## Overview
This project predicts ozone concentration as an indicator of air quality using weather-based features. It is designed to support early air quality warnings and sustainability-focused decision making.

## Problem
Delhi faces frequent air quality degradation. Accurate short-term AQI prediction can help reduce health risks and support preventive action.

## Solution
Machine learning regression models are trained on historical air quality and meteorological data to forecast ozone levels.

## Models
- Random Forest Regressor (baseline)
- XGBoost Regressor (tuned using GridSearchCV)

## Dataset
NYC Air Quality Dataset (1973)  
Target: Ozone (ppb)  
Features: Solar Radiation, Wind, Temperature, Month, Day

## Performance
XGBoost achieved improved performance over the baseline:
- R² Score: 0.73
- MAE: 12.17  
(20% improvement compared to Random Forest)

## Key Insight
Temperature is the most influential feature, followed by wind speed and solar radiation.

## Usage
Example prediction:
```python
predict_aqi(200, 5, 80, 7, 200)
