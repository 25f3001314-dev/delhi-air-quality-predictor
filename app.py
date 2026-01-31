"""
Delhi Air Quality Predictor - Gradio Web Interface

This application provides a user-friendly interface for predicting ozone levels
(an indicator of air quality) based on weather parameters.
"""

import gradio as gr
import numpy as np


def interpret_ozone(ozone_ppb):
    """
    Interpret ozone levels according to AQI categories.
    
    Args:
        ozone_ppb: Ozone concentration in parts per billion
        
    Returns:
        tuple: (category, health_advisory)
    """
    if ozone_ppb < 50:
        return "Good", "🟢 Air quality is satisfactory"
    elif ozone_ppb < 100:
        return "Moderate", "🟡 Acceptable for most, sensitive groups may experience issues"
    elif ozone_ppb < 150:
        return "Unhealthy for Sensitive Groups", "🟠 Sensitive groups should limit outdoor exposure"
    else:
        return "Unhealthy", "🔴 Everyone may experience health effects"


def predict_air_quality(solar_radiation, wind_speed, temperature, month, day):
    """
    Predict ozone levels based on weather parameters.
    
    Currently uses a placeholder prediction formula based on insights from the README:
    - Temperature is the most influential feature
    - Wind speed and solar radiation also play important roles
    
    Args:
        solar_radiation: Solar radiation in langley (0-400)
        wind_speed: Wind speed in mph (0-25)
        temperature: Temperature in Fahrenheit (50-100)
        month: Month of the year (1-12)
        day: Day of the month (1-31)
        
    Returns:
        tuple: (ozone_level, category, health_advisory)
    """
    
    # TODO: Replace this placeholder with your trained XGBoost model
    # Example integration:
    # import joblib
    # model = joblib.load('xgboost_model.pkl')
    # features = np.array([[solar_radiation, wind_speed, temperature, month, day]])
    # ozone_level = model.predict(features)[0]
    
    # Placeholder prediction logic based on README insights
    # Temperature is most influential, followed by wind and solar radiation
    # Formula creates realistic ozone predictions (30-150 ppb range)
    
    # Validate inputs
    if not (0 <= solar_radiation <= 400):
        return "Error: Solar radiation must be between 0 and 400", "", ""
    if not (0 <= wind_speed <= 25):
        return "Error: Wind speed must be between 0 and 25 mph", "", ""
    if not (50 <= temperature <= 100):
        return "Error: Temperature must be between 50 and 100°F", "", ""
    if not (1 <= month <= 12):
        return "Error: Month must be between 1 and 12", "", ""
    if not (1 <= day <= 31):
        return "Error: Day must be between 1 and 31", "", ""
    
    # Realistic placeholder formula based on domain knowledge:
    # - Higher temperature increases ozone (most influential)
    # - Higher solar radiation increases ozone
    # - Higher wind speed decreases ozone (disperses pollutants)
    # - Summer months tend to have higher ozone
    
    # Base ozone from temperature (most influential factor)
    base_ozone = (temperature - 50) * 1.5
    
    # Solar radiation contribution (positive correlation)
    solar_contribution = solar_radiation * 0.15
    
    # Wind speed effect (negative correlation - wind disperses ozone)
    wind_effect = -wind_speed * 2.0
    
    # Seasonal effect (higher in summer months)
    if month in [5, 6, 7, 8]:  # Peak summer months
        seasonal_factor = 15
    elif month in [4, 9]:  # Shoulder months
        seasonal_factor = 8
    else:
        seasonal_factor = 0
    
    # Calculate predicted ozone level
    ozone_level = base_ozone + solar_contribution + wind_effect + seasonal_factor
    
    # Add some realistic variation based on day
    day_variation = np.sin(day / 31 * np.pi) * 5
    ozone_level += day_variation
    
    # Ensure realistic bounds (typical range 30-150 ppb)
    ozone_level = np.clip(ozone_level, 30, 150)
    
    # Round to 1 decimal place
    ozone_level = round(ozone_level, 1)
    
    # Get interpretation
    category, health_advisory = interpret_ozone(ozone_level)
    
    # Format output
    result = f"**Predicted Ozone Level:** {ozone_level} ppb"
    
    return result, category, health_advisory


# Create Gradio interface
with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue", secondary_hue="green")) as demo:
    gr.Markdown(
        """
        # 🌍 Delhi Air Quality Predictor
        
        Predict ozone concentration (an indicator of air quality) based on weather parameters.
        
        This tool uses machine learning insights to estimate air quality. Adjust the weather 
        conditions below to see how they affect predicted ozone levels.
        
        ⚠️ *Note: Currently using a demonstration model. Real predictions will be available once the XGBoost model is integrated.*
        """
    )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Input Weather Parameters")
            
            solar_radiation = gr.Slider(
                minimum=0,
                maximum=400,
                value=200,
                step=10,
                label="Solar Radiation (langley)",
                info="Amount of solar radiation - higher values increase ozone formation"
            )
            
            wind_speed = gr.Slider(
                minimum=0,
                maximum=25,
                value=10,
                step=0.5,
                label="Wind Speed (mph)",
                info="Wind speed - higher winds help disperse pollutants"
            )
            
            temperature = gr.Slider(
                minimum=50,
                maximum=100,
                value=80,
                step=1,
                label="Temperature (°F)",
                info="Air temperature - most influential factor for ozone formation"
            )
            
            month = gr.Slider(
                minimum=1,
                maximum=12,
                value=7,
                step=1,
                label="Month",
                info="Month of the year (1=Jan, 12=Dec)"
            )
            
            day = gr.Slider(
                minimum=1,
                maximum=31,
                value=15,
                step=1,
                label="Day",
                info="Day of the month"
            )
            
            predict_btn = gr.Button("Predict Air Quality", variant="primary", size="lg")
        
        with gr.Column():
            gr.Markdown("### Prediction Results")
            
            ozone_output = gr.Markdown(label="Ozone Level")
            category_output = gr.Textbox(label="Air Quality Category", interactive=False)
            advisory_output = gr.Textbox(label="Health Advisory", interactive=False)
    
    # Examples section
    gr.Markdown("### Example Scenarios")
    gr.Examples(
        examples=[
            [200, 10, 80, 7, 15],  # Typical summer day
            [300, 5, 95, 8, 20],   # Hot summer day, low wind - higher ozone
            [150, 15, 70, 4, 10],  # Spring day, high wind - lower ozone
            [100, 8, 60, 12, 5],   # Winter day - low ozone
            [350, 3, 90, 6, 25],   # High solar radiation, low wind - high ozone
        ],
        inputs=[solar_radiation, wind_speed, temperature, month, day],
        label="Click an example to try it out"
    )
    
    # Connect the prediction function
    predict_btn.click(
        fn=predict_air_quality,
        inputs=[solar_radiation, wind_speed, temperature, month, day],
        outputs=[ozone_output, category_output, advisory_output]
    )
    
    gr.Markdown(
        """
        ---
        
        ### About the Model
        
        This predictor is based on analysis showing that:
        - **Temperature** is the most influential factor (higher temps → more ozone)
        - **Wind Speed** helps disperse pollutants (higher wind → less ozone)
        - **Solar Radiation** contributes to ozone formation (higher solar → more ozone)
        - **Season** affects baseline ozone levels (summer → higher ozone)
        
        ### Data Source
        Based on NYC Air Quality Dataset (1973) with features: Solar Radiation, Wind, Temperature, Month, Day
        
        ### Performance (Target with Real Model)
        - R² Score: 0.73
        - MAE: 12.17 ppb
        """
    )

# Launch the app
if __name__ == "__main__":
    demo.launch()
