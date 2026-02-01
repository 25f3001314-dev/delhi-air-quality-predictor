---
title: Delhi Air Quality Predictor
emoji: 🌍
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "4.0"
python_version: "3.12"
app_file: app.py
pinned: false
---

# Delhi Air Quality Predictor

This is a Gradio Space. Ensure `app.py` defines `demo` and calls `demo.launch()`.

## Features

- Real-time weather data from Open-Meteo API
- Live AQI data from AQICN
- Air quality predictions based on weather parameters
- Interactive Gradio interface

## Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open in browser:
```
http://localhost:7860
```

## Configuration

This application uses:
- **Weather Data**: Open-Meteo API (https://open-meteo.com/)
- **AQI Data**: AQICN API (https://aqicn.org/api/)

## Deploy

Push this repo to a Hugging Face Space (SDK: Gradio). The Space will install `requirements.txt` automatically and stay running.

## Reference

Check out the Hugging Face Spaces configuration reference: https://huggingface.co/docs/hub/spaces-config-reference
