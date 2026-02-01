import os
import gradio as gr
import requests
from datetime import datetime

# AQI API configuration (you'll need to get API key from aqicn.org)
AQI_API_KEY = "demo"  # Replace with your actual API key
AQI_API_URL = "https://api.waqi.info/feed/delhi/"

def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"

def get_current_aqi():
    try:
        r = requests.get(f"{AQI_API_URL}?token={AQI_API_KEY}")
        data = r.json()
        if data.get("status") == "ok":
            aqi = data["data"]["aqi"]
        else:
            aqi = 131
    except Exception:
        aqi = 131

    category = get_aqi_category(aqi)
    return aqi, category, datetime.now().strftime("%Y-%m-%d %H:%M:%S")

demo = gr.Interface(
    fn=get_current_aqi,
    inputs=[],
    outputs=[
        gr.Number(label="AQI"),
        gr.Text(label="Category"),
        gr.Text(label="Last Updated"),
    ],
    title="Delhi AQI Monitor",
    description="Live AQI data using WAQI API (demo fallback)",
)

demo.launch()
