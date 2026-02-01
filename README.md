---
title: Bachao
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "4.44.0"
python_version: "3.10"
app_file: app.py
pinned: false
---

# Bachao - Delhi Air Quality Predictor

Predict air quality using machine learning models.

## Overview
This project predicts ozone concentration as an indicator of air quality using weather-based features.

## Models
- Random Forest Regressor (baseline)
- XGBoost Regressor (tuned)

## Features
- Solar Radiation (langleys)
- Wind Speed (mph)
- Temperature (°F)
- Month
- Day

## Running Locally
```bash
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:7860`

## Live Demo
🌐 https://huggingface.co/spaces/25f3001314/Bachao
