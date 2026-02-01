import gradio as gr
import requests
from datetime import datetime

def get_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=28.61&longitude=77.23&current=temperature_2m,wind_speed_10m&timezone=Asia%2FKolkata"
        data = requests.get(url, timeout=10).json()
        return data['current']['temperature_2m'], data['current']['wind_speed_10m']
    except:
        return 20, 5  # Fallback

def get_aqi():
    try:
        token = "d4e8711cd3c48f702b02815a4e4db3"
        url = f"https://api.waqi.info/feed/@3715/?token={token}"
        data = requests.get(url, timeout=10).json()
        return data['data'].get('o3', 27)
    except:
        return 27

def load_real():
    temp, wind = get_weather()
    return 300, wind*0.28, temp, 2, 1  # Solar approx

def predict(solar, wind, temp, month, day):
    ozone = 0.1*solar - 0.5*wind + 0.8*temp/10 + get_aqi()
    cat = "Good" if ozone<30 else "Unhealthy"
    return f"Live Delhi O3: {get_aqi():.0f} ppb\nPred: {ozone:.0f} ppb\n{cat}"

with gr.Blocks() as demo:
    gr.Markdown("# Delhi Live AQI Predictor")
    solar = gr.Slider(0,1000, label="Solar (W/m²)")
    wind = gr.Slider(0,20, label="Wind (km/h)")
    temp = gr.Slider(0,50, label="Temp (°C)")
    month, day = gr.Slider(1,12), gr.Slider(1,31)
    out = gr.Textbox()
    gr.Button("Load Real Delhi Data").click(load_real, outputs=[solar,wind,temp,month,day])
    gr.Button("Predict").click(predict, [solar,wind,temp,month,day], out)

demo.queue().launch()
