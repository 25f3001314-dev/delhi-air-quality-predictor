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
    """Vercel serverless function handler"""
    
    # Handle preflight CORS
    if request.method == "OPTIONS":
        return {
            "statusCode": 204,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            },
        }
    
    try:
        # Get API key from environment
        api_key = os.getenv("AQI_API_KEY", "demo")
        api_url = "https://api.waqi.info/feed/delhi/"
        
        # Fetch AQI data from WAQI API
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
        
        category = get_aqi_category(aqi_value)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        result = {
            "status": "success",
            "aqi": aqi_value,
            "category": category,
            "city": city,
            "timestamp": timestamp
        }
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            },
            "body": json.dumps(result),
        }
    
    except requests.exceptions.RequestException as e:
        error_result = {
            "status": "error",
            "message": f"API Error: {str(e)}",
            "aqi": 131,
            "category": "Data Unavailable",
            "city": "Delhi",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(error_result),
        }
    
    except Exception as e:
        error_result = {
            "status": "error",
            "message": f"Server Error: {str(e)}",
            "aqi": 131,
            "category": "Data Unavailable",
            "city": "Delhi",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(error_result),
        }
