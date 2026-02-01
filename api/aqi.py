import os
import json
import requests
from datetime import datetime
from http.server import BaseHTTPRequestHandler

def get_aqi_category(aqi):
    """Determine AQI category based on value"""
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
        """Handle GET requests"""
        
        # Set CORS headers
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        
        try:
            # Get API key from environment
            api_key = os.getenv("AQI_API_KEY", "demo")
            api_url = "https://api.waqi.info/feed/delhi/"
            
            # Fetch AQI data
            response = requests.get(f"{api_url}?token={api_key}", timeout=5)
            data = response.json()
            
            if data.get("status") == "ok":
                aqi_value = int(data["data"]["aqi"])
                city = data["data"].get("city", {}).get("name", "Delhi")
            else:
                aqi_value = 131
                city = "Delhi"
            
            category = get_aqi_category(aqi_value)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            result = {
                "status": "success",
                "aqi": aqi_value,
                "category": category,
                "city": city,
                "timestamp": timestamp
            }
            
            self.wfile.write(json.dumps(result).encode())
        
        except Exception as e:
            self.send_response(500)
            error_result = {
                "status": "error",
                "message": str(e),
                "aqi": 131,
                "category": "Data Unavailable",
                "city": "Delhi",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.wfile.write(json.dumps(error_result).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
