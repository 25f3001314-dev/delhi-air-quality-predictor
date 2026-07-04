from flask import Flask, render_template, jsonify
import requests
from datetime import datetime, timedelta
import random
import os

app = Flask(__name__)

# AQI API configuration
AQI_API_KEY = os.getenv("AQI_API_KEY")
AQI_API_URL = "https://api.waqi.info/feed/delhi/"

def get_aqi_category(aqi):
    if aqi <= 50:
        return {"category": "Good", "color": "#00e400"}
    elif aqi <= 100:
        return {"category": "Moderate", "color": "#ffff00"}
    elif aqi <= 150:
        return {"category": "Unhealthy for Sensitive Groups", "color": "#ff7e00"}
    elif aqi <= 200:
        return {"category": "Unhealthy", "color": "#ff0000"}
    elif aqi <= 300:
        return {"category": "Very Unhealthy", "color": "#8f3f97"}
    else:
        return {"category": "Hazardous", "color": "#7e0023"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/current')
def get_current_aqi():
    if not AQI_API_KEY:
        return jsonify({
            'error': 'AQI_API_KEY environment variable is required',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 500

    try:
        # Fetch real data from API
        response = requests.get(f"{AQI_API_URL}?token={AQI_API_KEY}", timeout=5)
        data = response.json()
        
        if data['status'] == 'ok':
            aqi_data = data['data']
            aqi_value = aqi_data['aqi']
            category_info = get_aqi_category(aqi_value)
            
            return jsonify({
                'aqi': aqi_value,
                'category': category_info['category'],
                'color': category_info['color'],
                'pm25': aqi_data['iaqi'].get('pm25', {}).get('v', 'N/A'),
                'pm10': aqi_data['iaqi'].get('pm10', {}).get('v', 'N/A'),
                'temperature': aqi_data['iaqi'].get('t', {}).get('v', 'N/A'),
                'humidity': aqi_data['iaqi'].get('h', {}).get('v', 'N/A'),
                'wind_speed': aqi_data['iaqi'].get('w', {}).get('v', 'N/A'),
                'timestamp': aqi_data['time']['s']
            })
    except Exception as e:
        print(f"API Error: {e}")
        pass
    
    # Demo data
    aqi = 131
    category_info = get_aqi_category(aqi)
    return jsonify({
        'aqi': aqi,
        'category': category_info['category'],
        'color': category_info['color'],
        'pm25': 50,
        'pm10': 65,
        'temperature': 22,
        'humidity': 50,
        'wind_speed': 7,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/api/historical')
def get_historical_data():
    # Generate demo historical data
    data = []
    now = datetime.now()
    
    for i in range(48):  # 48 hours of data
        timestamp = now - timedelta(hours=48-i)
        # Simulate AQI variation
        base_aqi = 250
        variation = random.randint(-100, 100)
        aqi = max(50, min(400, base_aqi + variation - (i * 2)))
        
        data.append({
            'timestamp': timestamp.strftime('%I:%M %p'),
            'aqi': aqi,
            'date': timestamp.strftime('%d-%m-%Y')
        })
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860, debug=True)
