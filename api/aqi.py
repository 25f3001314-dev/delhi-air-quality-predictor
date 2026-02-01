import os
import json
import requests
import joblib
import numpy as np
from datetime import datetime
from http.server import BaseHTTPRequestHandler

# Load the trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'aqi_model.pkl')
FEATURES_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'feature_columns.json')

try:
    model = joblib.load(MODEL_PATH)
    with open(FEATURES_PATH, 'r') as f:
        feature_columns = json.load(f)
    MODEL_LOADED = True
except Exception as e:
    MODEL_LOADED = False
    print(f"Warning: Could not load model: {e}")

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

def fetch_realtime_pollutants():
    """Fetch real-time pollutant data from WAQI API for feature engineering"""
    try:
        api_key = os.getenv("AQI_API_KEY", "demo")
        url = f"https://api.waqi.info/feed/delhi/?token={api_key}"
        resp = requests.get(url, timeout=3)
        data = resp.json()
        
        if data.get("status") == "ok":
            iaqi = data["data"].get("iaqi", {})
            return {
                'co': iaqi.get("co", {}).get("v", 2000),
                'no': iaqi.get("no", {}).get("v", 30),
                'no2': iaqi.get("no2", {}).get("v", 60),
                'o3': iaqi.get("o3", {}).get("v", 50),
                'so2': iaqi.get("so2", {}).get("v", 60),
                'pm10': iaqi.get("pm10", {}).get("v", 250),
                'nh3': iaqi.get("nh3", {}).get("v", 25),
                'pm2_5_current': iaqi.get("pm25", {}).get("v", 200)
            }
    except:
        pass
    
    # Default fallback values (typical Delhi pollution levels)
    return {
        'co': 2000, 'no': 30, 'no2': 60, 'o3': 50,
        'so2': 60, 'pm10': 250, 'nh3': 25, 'pm2_5_current': 200
    }

def predict_aqi_ml():
    """Predict AQI using ML model"""
    if not MODEL_LOADED:
        return None
    
    try:
        # Get current datetime features
        now = datetime.now()
        
        # Fetch real-time pollutant data
        pollutants = fetch_realtime_pollutants()
        
        # Prepare features for prediction
        features = {
            'co': pollutants['co'],
            'no': pollutants['no'],
            'no2': pollutants['no2'],
            'o3': pollutants['o3'],
            'so2': pollutants['so2'],
            'pm10': pollutants['pm10'],
            'nh3': pollutants['nh3'],
            'year': now.year,
            'month': now.month,
            'day': now.day,
            'hour': now.hour,
            'dayofweek': now.weekday(),
            'pm2_5_lag1': pollutants['pm2_5_current'],
            'pm2_5_lag24': pollutants['pm2_5_current'] * 0.9,
            'pm10_lag1': pollutants['pm10'] * 0.95
        }
        
        # Create feature array in correct order
        X = np.array([[features[col] for col in feature_columns]])
        
        # Predict PM2.5
        pm25_pred = model.predict(X)[0]
        pm25_pred = max(0, pm25_pred)  # Ensure non-negative
        
        # Convert to AQI
        aqi = get_aqi_from_pm25(pm25_pred)
        
        return {
            'aqi': int(aqi),
            'pm25': round(pm25_pred, 2),
            'pm10': pollutants['pm10'],
            'category': get_aqi_category(aqi),
            'color': get_aqi_color(aqi),
            'prediction_type': 'ml_model',
            'model_loaded': True
        }
    except Exception as e:
        print(f"ML Prediction error: {e}")
        return None

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Try ML prediction first
            ml_result = predict_aqi_ml()
            
            if ml_result:
                # ML prediction successful
                stations_data = []
                
                # Create multiple station predictions (simulate different areas)
                stations = [
                    {"name": "Anand Vihar", "multiplier": 1.2},
                    {"name": "Punjabi Bagh", "multiplier": 0.9},
                    {"name": "RK Puram", "multiplier": 1.0},
                    {"name": "Dwarka", "multiplier": 0.85},
                    {"name": "ITO", "multiplier": 1.1},
                ]
                
                for station in stations:
                    aqi_adjusted = int(ml_result['aqi'] * station['multiplier'])
                    pm25_adjusted = ml_result['pm25'] * station['multiplier']
                    pm10_adjusted = ml_result['pm10'] * station['multiplier']
                    
                    stations_data.append({
                        "name": station["name"],
                        "aqi": aqi_adjusted,
                        "category": get_aqi_category(aqi_adjusted),
                        "color": get_aqi_color(aqi_adjusted),
                        "pm25": round(pm25_adjusted, 1),
                        "pm10": round(pm10_adjusted, 1),
                        "o3": "N/A",
                        "no2": "N/A",
                        "co": "N/A",
                    })
            else:
                # Fallback to WAQI API
                api_key = os.getenv("AQI_API_KEY", "demo")
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
                "prediction_method": "ml_model" if ml_result else "waqi_api",
                "model_loaded": MODEL_LOADED,
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
