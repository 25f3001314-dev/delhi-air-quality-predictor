import os
import json
import requests
from datetime import datetime

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

def handler(request):
    """Serverless function to fetch AQI data"""
    
    # CORS headers
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }
    
    # Handle CORS preflight
    if request.method == "OPTIONS":
        return ("", 204, headers)
    
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
        
        return (json.dumps(result), 200, headers)
    
    except Exception as e:
        error_result = {
            "status": "error",
            "message": str(e),
            "aqi": 131,
            "category": "Data Unavailable",
            "city": "Delhi",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return (json.dumps(error_result), 500, headers)
