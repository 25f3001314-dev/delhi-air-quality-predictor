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

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            api_key = os.getenv("AQI_API_KEY", "demo")
            
            # Multiple Delhi monitoring stations
            stations = [
                {"name": "Anand Vihar", "coords": "28.6469,77.3155"},
                {"name": "Punjabi Bagh", "coords": "28.6742,77.1310"},
                {"name": "RK Puram", "coords": "28.5677,77.1803"},
                {"name": "Dwarka", "coords": "28.5921,77.0460"},
                {"name": "ITO", "coords": "28.6281,77.2419"},
            ]
            
            stations_data = []
            
            for station in stations:
                try:
                    lat, lon = station["coords"].split(",")
                    url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={api_key}"
                    resp = requests.get(url, timeout=3)
                    data = resp.json()
                    
                    if data.get("status") == "ok":
                        aqi_val = int(data["data"].get("aqi", 0))
                        iaqi = data["data"].get("iaqi", {})
                        
                        stations_data.append({
                            "name": station["name"],
                            "aqi": aqi_val,
                            "category": get_aqi_category(aqi_val),
                            "color": get_aqi_color(aqi_val),
                            "pm25": iaqi.get("pm25", {}).get("v", "N/A"),
                            "pm10": iaqi.get("pm10", {}).get("v", "N/A"),
                            "o3": iaqi.get("o3", {}).get("v", "N/A"),
                            "no2": iaqi.get("no2", {}).get("v", "N/A"),
                            "co": iaqi.get("co", {}).get("v", "N/A"),
                        })
                except:
                    continue
            
            # Get weather data for Delhi
            weather_url = "https://api.open-meteo.com/v1/forecast?latitude=28.6139&longitude=77.2090&current=temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m&timezone=Asia/Kolkata"
            weather_resp = requests.get(weather_url, timeout=3)
            weather_data = weather_resp.json().get("current", {})
            
            result = {
                "status": "success",
                "stations": stations_data,
                "weather": {
                    "temperature": weather_data.get("temperature_2m", "N/A"),
                    "humidity": weather_data.get("relative_humidity_2m", "N/A"),
                    "wind_speed": weather_data.get("wind_speed_10m", "N/A"),
                    "wind_direction": weather_data.get("wind_direction_10m", "N/A"),
                },
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            error_result = {
                "status": "error",
                "message": str(e),
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
