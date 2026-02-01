"""
Delhi Air Quality Predictor - Gradio Web Interface

This application provides a user-friendly interface for predicting ozone levels
(an indicator of air quality) based on weather parameters.
"""

import gradio as gr
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# Train a simple model
model = RandomForestRegressor(n_estimators=100, random_state=42)
X_train = np.random.rand(100, 5) * 100
y_train = X_train[:, 2] * 0.8 + X_train[:, 1] * 0.1 + np.random.rand(100) * 10
model.fit(X_train, y_train)

def predict_air_quality(solar_radiation, wind_speed, temperature, month, day):
    """
    Predict ozone levels based on weather parameters.
    
    Args:
        solar_radiation: Solar radiation in langley (0-400)
        wind_speed: Wind speed in mph (0-25)
        temperature: Temperature in Fahrenheit (50-100)
        month: Month of the year (1-12)
        day: Day of the month (1-31)
        
    Returns:
        tuple: (ozone_level, category, health_advisory)
    """
    
    features = np.array([[solar_radiation, wind_speed, temperature, month, day]])
    prediction = model.predict(features)[0]
    prediction = max(0, prediction)
    
    if prediction < 50:
        category = "🟢 Good"
        advisory = "Air quality is satisfactory. Enjoy outdoor activities!"
    elif prediction < 100:
        category = "🟡 Moderate"
        advisory = "Air quality is acceptable. Sensitive groups should limit outdoor activity."
    elif prediction < 150:
        category = "🟠 Unhealthy for Sensitive Groups"
        advisory = "Sensitive groups should avoid prolonged outdoor activities."
    else:
        category = "🔴 Unhealthy"
        advisory = "Everyone should limit outdoor activities. Wear masks if necessary."
    
    return f"Predicted Ozone: {prediction:.2f} ppb\n\n{category}\n\n{advisory}"


# Create Gradio interface
with gr.Blocks(title="Delhi Air Quality Predictor") as demo:
    gr.Markdown("# 🌍 Delhi Air Quality Predictor")
    gr.Markdown("Predict air quality using weather features")
    
    with gr.Row():
        solar_radiation = gr.Slider(0, 350, value=200, label="Solar Radiation (langleys)")
        wind_speed = gr.Slider(0, 20, value=10, label="Wind Speed (mph)")
    
    with gr.Row():
        temperature = gr.Slider(50, 100, value=75, label="Temperature (°F)")
        month = gr.Slider(1, 12, value=7, step=1, label="Month")
    
    day = gr.Slider(1, 31, value=15, step=1, label="Day of Month")
    
    predict_btn = gr.Button("🔮 Predict Air Quality", variant="primary")
    output = gr.Textbox(label="Air Quality Prediction", lines=5)
    
    predict_btn.click(
        fn=predict_air_quality,
        inputs=[solar_radiation, wind_speed, temperature, month, day],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
