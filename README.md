---
title: Delhi Air Quality Predictor
emoji: 🌍
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "4.0.2"
python_version: "3.10"
app_file: app.py
pinned: false
---

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

## 🌐 Web Interface

Try the interactive web app to predict air quality in real-time!

### Running Locally
```bash
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:7860` in your browser.

### Deployment
This app can be deployed on:
- **Hugging Face Spaces** (recommended for Gradio)
- **Google Colab**
- **Railway**
- **Render**

### Using the App
1. Adjust the input sliders for weather conditions
2. Click "Predict Air Quality" to get the predicted ozone level
3. View the air quality category and health advisory

## 🚀 Deployment

### Live Demo
🌐 **Try it live:** https://huggingface.co/spaces/25f3001314/Bachao

### Auto-Deploy
This repository automatically syncs to Hugging Face Spaces on every push to main branch using GitHub Actions.

## Usage

### Web Interface (Recommended)
Use the interactive Gradio app by running `python app.py` and visit http://localhost:7860

### Programmatic Usage
Once a trained model is integrated, you can use it programmatically:
```python
# Example with future trained model
from app import predict_air_quality
result = predict_air_quality(solar_radiation=200, wind_speed=10, temperature=80, month=7, day=15)
```