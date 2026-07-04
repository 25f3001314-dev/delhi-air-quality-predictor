import os
import json
import random
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler
import requests

def get_aqi_category(aqi):
    if aqi <= 50: return "Good"
    elif aqi <= 100: return "Moderate"
    elif aqi <= 150: return "Unhealthy for Sensitive Groups"
    elif aqi <= 200: return "Unhealthy"
    elif aqi <= 300: return "Very Unhealthy"
    else: return "Hazardous"

def get_aqi_color(aqi):
    if aqi <= 50: return "#00e400"
    elif aqi <= 100: return "#ffff00"
    elif aqi <= 150: return "#ff7e00"
    elif aqi <= 200: return "#ff0000"
    elif aqi <= 300: return "#8f3f97"
    else: return "#7e0023"

def fetch_aqi_data():
    try:
        api_key = os.getenv("AQI_API_KEY")
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

    aqi = 131
    return {
        'aqi': aqi, 'category': get_aqi_category(aqi), 'color': get_aqi_color(aqi),
        'pm25': 50, 'pm10': 65, 'co': 'N/A', 'no2': 'N/A', 'o3': 'N/A', 'so2': 'N/A',
        'temperature': 22, 'humidity': 50, 'wind_speed': 7,
        'timestamp': datetime.now().isoformat(), 'station': 'Delhi'
    }

def generate_historical_data():
    """Generate last 24 hours of sample AQI data for the chart"""
    data = []
    base_aqi = fetch_aqi_data()['aqi']
    now = datetime.now()
    for i in range(24, 0, -1):
        t = now - timedelta(hours=i)
        variation = random.randint(-20, 20)
        aqi = max(20, base_aqi + variation)
        data.append({
            'timestamp': t.strftime('%H:%M'),
            'aqi': aqi
        })
    return data

def render_html():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(base_dir, 'templates', 'index.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split('?')[0]

        if path == '/api/current':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(fetch_aqi_data()).encode())
            return

        if path == '/api/historical':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(generate_historical_data()).encode())
            return

        # Default: serve the HTML dashboard
        try:
            html = render_html()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Error loading page: {e}".encode())
        return
