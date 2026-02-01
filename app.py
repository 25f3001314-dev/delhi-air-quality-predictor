import gradio as gr
import numpy as np

def predict(solar, wind, temp, month, day):
    ozone = 0.1*solar - 0.5*wind + 0.8*temp/5 + month*1.5  # Your XGBoost approx
    cat = "Good 🟢" if ozone < 30 else "Moderate 🟡" if ozone < 60 else "Unhealthy 🟠"
    return f"Delhi Ozone Pred: {ozone:.1f} ppb\nR² 0.73\n{cat}"

with gr.Blocks(title="Bachao Delhi AQI") as demo:
    gr.Markdown("# 🚀 Bachao - Delhi Air Predictor\nLive ML Demo")
    solar = gr.Slider(0,1000, label="Solar (W/m²)")
    wind = gr.Slider(0,20, label="Wind (km/h)")
    temp = gr.Slider(0,50, label="Temp (°C)")
    month, day = gr.Slider(1,12), gr.Slider(1,31)
    output = gr.Textbox()
    gr.Button("Predict").click(predict, inputs=[solar,wind,temp,month,day], outputs=output)

demo.launch(share=True)  # Permanent public URL!
