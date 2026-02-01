import os
import json
import requests
from datetime import datetime
from http.server import BaseHTTPRequestHandler

def get_aqi_from_pm25(pm25):
    """Convert PM2.5 to AQI using US EPA standard"""
    if pm25 <= 12.0:
        return int((50 - 0) / (12.0 - 0.0) * (pm25 - 0.0) + 0)
    elif pm25 <= 35.4:
        return int((100 - 51) / (35.4 - 12.1) * (pm25 - 12.1) + 51)
    elif pm25 <= 55.4:
        return int((150 - 101) / (55.4 - 35.5) * (pm25 - 35.5) + 101)
    elif pm25 <= 150.4:
        return int((200 - 151) / (150.4 - 55.5) * (pm25 - 55.5) + 151)
    elif pm25 <= 250.4:
        return int((300 - 201) / (250.4 - 150.5) * (pm25 - 150.5) + 201)
    else:
        return int((500 - 301) / (500.4 - 250.5) * (pm25 - 250.5) + 301)

def get_aqi_category(aqi):
    """Determine AQI category"""
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

def get_aqi_color(aqi):
    """Get color based on AQI"""
    if aqi <= 50:
        return "#00e400"
    elif aqi <= 100:
        return "#ffff00"
    elif aqi <= 150:
        return "#ff7e00"
    elif aqi <= 200:
        return "#ff0000"
    elif aqi <= 300:
        return "#8f3f97"
    else:
        return "#7e0023"

def fetch_aqi_data():
    """Fetch real-time AQI data from WAQI API"""
    try:
        api_key = os.getenv("AQI_API_KEY", "4e84e711ecd384cb72016b0238185ae0a443dbe3")
        url = f"https://api.waqi.info/feed/delhi/?token={api_key}"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        
        if data.get("status") == "ok":
            aqi_data = data["data"]
            iaqi = aqi_data.get("iaqi", {})
            aqi = aqi_data.get("aqi", 131)
            
            return {
                'aqi': aqi,
                'category': get_aqi_category(aqi),
                'color': get_aqi_color(aqi),
                'pm25': iaqi.get("pm25", {}).get("v", "N/A"),
                'pm10': iaqi.get("pm10", {}).get("v", "N/A"),
                'co': iaqi.get("co", {}).get("v", "N/A"),
                'no2': iaqi.get("no2", {}).get("v", "N/A"),
                'o3': iaqi.get("o3", {}).get("v", "N/A"),
                'so2': iaqi.get("so2", {}).get("v", "N/A"),
                'temperature': iaqi.get("t", {}).get("v", "N/A"),
                'humidity': iaqi.get("h", {}).get("v", "N/A"),
                'wind_speed': iaqi.get("w", {}).get("v", "N/A"),
                'timestamp': aqi_data.get("time", {}).get("s", datetime.now().isoformat()),
                'station': aqi_data.get("city", {}).get("name", "Delhi")
            }
    except Exception as e:
        print(f"API Error: {e}")
    
    # Fallback demo data
    aqi = 131
    return {
        'aqi': aqi,
        'category': get_aqi_category(aqi),
        'color': get_aqi_color(aqi),
        'pm25': 50,
        'pm10': 65,
        'co': 'N/A',
        'no2': 'N/A',
        'o3': 'N/A',
        'so2': 'N/A',
        'temperature': 22,
        'humidity': 50,
        'wind_speed': 7,
        'timestamp': datetime.now().isoformat(),
        'station': 'Delhi'
    }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Enable CORS
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Fetch and return AQI data
        aqi_data = fetch_aqi_data()
        self.wfile.write(json.dumps(aqi_data).encode())
        return
