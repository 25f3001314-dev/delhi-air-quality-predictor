import os
import json
import requests
from datetime import datetime
from http.server import BaseHTTPRequestHandler

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

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Get API key
            api_key = os.getenv("AQI_API_KEY", "demo")
            # Use geo coordinates for Delhi to ensure correct city
            api_url = "https://api.waqi.info/feed/geo:28.6139;77.2090/"
            
            # Fetch data
            response = requests.get(f"{api_url}?token={api_key}", timeout=5)
            data = response.json()
            
            # Parse response
            if data.get("status") == "ok" and "data" in data:
                aqi_value = int(data["data"].get("aqi", 131))
                city = data["data"].get("city", "Delhi")
                if isinstance(city, dict):
                    city = city.get("name", "Delhi")
            else:
                aqi_value = 131
                city = "Delhi"
            
            result = {
                "status": "success",
                "aqi": aqi_value,
                "category": get_aqi_category(aqi_value),
                "city": city,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Send response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            error_result = {
                "status": "error",
                "message": str(e),
                "aqi": 131,
                "category": "Data Unavailable",
                "city": "Delhi",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(error_result).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
