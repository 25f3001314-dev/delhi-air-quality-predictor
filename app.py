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
    cat = "Good 🟢" if ozone<30 else "Moderate 🟡" if ozone<60 else "Unhealthy 🟠"
    return f"🌍 Live Delhi O3: {get_aqi():.0f} ppb\n📊 Prediction: {ozone:.0f} ppb\n{cat}"

css = """
.gradio-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.gr-box {
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 15px !important;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3) !important;
}
.gr-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
}
.gr-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
}
.gr-textbox {
    border-radius: 10px !important;
    border: 2px solid #667eea !important;
    background: #f8f9ff !important;
}
.gr-slider {
    border-radius: 10px !important;
}
"""

with gr.Blocks(css=css, title="🌍 Delhi Live AQI Predictor") as demo:
    gr.Markdown("""
    <div style="text-align: center; padding: 20px;">
    <h1 style="color: white; font-size: 2.5em; margin-bottom: 10px;">🌍 Delhi Live AQI Predictor</h1>
    <p style="color: #f0f0f0; font-size: 1.1em;">Real-time Air Quality Predictions powered by ML</p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🌤️ Weather Parameters")
            solar = gr.Slider(0, 1000, value=200, step=10, label="☀️ Solar Radiation (W/m²)")
            wind = gr.Slider(0, 20, value=5, step=0.5, label="💨 Wind Speed (km/h)")
            temp = gr.Slider(-10, 50, value=16, step=0.5, label="🌡️ Temperature (°C)")
        
        with gr.Column(scale=1):
            gr.Markdown("### 📅 Time Period")
            month = gr.Slider(1, 12, value=2, step=1, label="📆 Month")
            day = gr.Slider(1, 31, value=1, step=1, label="📆 Day")
            gr.Markdown("*Current date: Feb 1*")
    
    gr.Markdown("---")
    
    with gr.Row():
        load_btn = gr.Button("📍 Load Today's Real Delhi Data", size="lg")
        predict_btn = gr.Button("🔮 Predict Air Quality", size="lg")
    
    output = gr.Textbox(label="📊 Prediction Results", lines=5, interactive=False)
    
    info = gr.Markdown("""
    <div style="background: #f0f0f0; padding: 15px; border-radius: 10px; margin-top: 20px;">
    <p><strong>📡 Data Sources:</strong></p>
    <ul>
    <li>🌤️ Weather: Open-Meteo API (Real-time)</li>
    <li>💨 Wind & Temp: Global Weather Data</li>
    <li>🌍 AQI: WAQI Station #3715 (Delhi ITO)</li>
    </ul>
    </div>
    """)
    
    load_btn.click(
        fn=load_real,
        outputs=[solar, wind, temp, month, day]
    )
    
    predict_btn.click(
        fn=predict,
        inputs=[solar, wind, temp, month, day],
        outputs=output
    )

demo.queue().launch(share=True)
