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

def build_current_payload(aqi, category, color, iaqi, timestamp, station, *, fallback=False):
    payload = {
        'status': 'success',
        'aqi': aqi,
        'category': category,
        'color': color,
        'pm25': iaqi.get("pm25", {}).get("v", "N/A"),
        'pm10': iaqi.get("pm10", {}).get("v", "N/A"),
        'co': iaqi.get("co", {}).get("v", "N/A"),
        'no2': iaqi.get("no2", {}).get("v", "N/A"),
        'o3': iaqi.get("o3", {}).get("v", "N/A"),
        'so2': iaqi.get("so2", {}).get("v", "N/A"),
        'temperature': iaqi.get("t", {}).get("v", "N/A"),
        'humidity': iaqi.get("h", {}).get("v", "N/A"),
        'wind_speed': iaqi.get("w", {}).get("v", "N/A"),
        'timestamp': timestamp,
        'station': station,
    }

    if fallback:
        payload['fallback'] = True

    return payload

def build_error_payload(message):
    return {
        'status': 'error',
        'message': message,
        'timestamp': datetime.now().isoformat(),
    }

def build_legacy_payload(current_data):
    if current_data.get('status') != 'success':
        return current_data

    base_aqi = current_data.get('aqi', 131)
    weather = {
        'temperature': current_data.get('temperature', 'N/A'),
        'humidity': current_data.get('humidity', 'N/A'),
        'wind_speed': current_data.get('wind_speed', 'N/A'),
        'wind_direction': 'N/A',
    }

    stations = [
        {"name": "Anand Vihar", "multiplier": 1.2},
        {"name": "Punjabi Bagh", "multiplier": 0.9},
        {"name": "RK Puram", "multiplier": 1.0},
        {"name": "Dwarka", "multiplier": 0.85},
        {"name": "ITO", "multiplier": 1.1},
    ]

    stations_data = []
    for station in stations:
        aqi_adjusted = int(base_aqi * station['multiplier'])
        pm25_value = current_data.get('pm25', 'N/A')
        pm10_value = current_data.get('pm10', 'N/A')

        stations_data.append({
            'name': station['name'],
            'aqi': aqi_adjusted,
            'category': get_aqi_category(aqi_adjusted),
            'color': get_aqi_color(aqi_adjusted),
            'pm25': pm25_value if pm25_value == 'N/A' else round(float(pm25_value) * station['multiplier'], 1),
            'pm10': pm10_value if pm10_value == 'N/A' else round(float(pm10_value) * station['multiplier'], 1),
            'o3': current_data.get('o3', 'N/A'),
            'no2': current_data.get('no2', 'N/A'),
            'co': current_data.get('co', 'N/A'),
        })

    return {
        'status': 'success',
        'stations': stations_data,
        'weather': weather,
        'prediction_method': 'waqi_api',
        'model_loaded': False,
        'timestamp': current_data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    }

def fetch_aqi_data():
    api_key = os.getenv("AQI_API_KEY")
    if not api_key:
        return build_error_payload(
            "AQI_API_KEY is not configured. Set the environment variable before requesting WAQI data."
        )

    try:
        url = f"https://api.waqi.info/feed/delhi/?token={api_key}"
        resp = requests.get(url, timeout=5)
        data = resp.json()

        if data.get("status") == "ok":
            aqi_data = data["data"]
            iaqi = aqi_data.get("iaqi", {})
            aqi = aqi_data.get("aqi", 131)
            return build_current_payload(
                aqi,
                get_aqi_category(aqi),
                get_aqi_color(aqi),
                iaqi,
                aqi_data.get("time", {}).get("s", datetime.now().isoformat()),
                aqi_data.get("city", {}).get("name", "Delhi"),
            )
    except Exception as e:
        print(f"API Error: {e}")

    aqi = 131
    return build_current_payload(
        aqi,
        get_aqi_category(aqi),
        get_aqi_color(aqi),
        {},
        datetime.now().isoformat(),
        "Delhi",
        fallback=True,
    )

def generate_historical_data():
    """Generate last 24 hours of sample AQI data for the chart"""
    data = []
    current_data = fetch_aqi_data()
    base_aqi = current_data.get('aqi', 131) if current_data.get('status') == 'success' else 131
    now = datetime.now()
    for i in range(24, 0, -3):
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
    def write_json(self, payload, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_GET(self):
        path = self.path.split('?')[0]

        if path == '/api/current':
            self.write_json(fetch_aqi_data())
            return

        if path == '/api/aqi':
            self.write_json(build_legacy_payload(fetch_aqi_data()))
            return

        if path == '/api/historical':
            self.write_json(generate_historical_data())
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
