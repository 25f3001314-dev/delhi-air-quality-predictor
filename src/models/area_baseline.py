# Simple Delhi Area-wise AQI Prediction Model
# Based on historical patterns and area characteristics

import random
from datetime import datetime

# Delhi area coordinates with typical AQI ranges
DELHI_AREAS = {
    "Connaught Place": {
        "lat": 28.6315, "lng": 77.2167,
        "base_aqi": 180, "variance": 40,
        "factors": {"traffic": 1.2, "commercial": 1.1}
    },
    "Dwarka": {
        "lat": 28.5921, "lng": 77.0460,
        "base_aqi": 160, "variance": 35,
        "factors": {"residential": 1.0, "industrial": 0.9}
    },
    "Rohini": {
        "lat": 28.7496, "lng": 77.0674,
        "base_aqi": 190, "variance": 45,
        "factors": {"residential": 1.1, "traffic": 1.15}
    },
    "Noida": {
        "lat": 28.5355, "lng": 77.3910,
        "base_aqi": 210, "variance": 50,
        "factors": {"industrial": 1.3, "construction": 1.2}
    },
    "Gurgaon": {
        "lat": 28.4595, "lng": 77.0266,
        "base_aqi": 200, "variance": 45,
        "factors": {"industrial": 1.2, "traffic": 1.25}
    },
    "Karol Bagh": {
        "lat": 28.6519, "lng": 77.1909,
        "base_aqi": 195, "variance": 40,
        "factors": {"commercial": 1.15, "traffic": 1.2}
    },
    "Vasant Vihar": {
        "lat": 28.5677, "lng": 77.1615,
        "base_aqi": 150, "variance": 30,
        "factors": {"residential": 0.9, "green": 0.85}
    },
    "Mayur Vihar": {
        "lat": 28.6089, "lng": 77.2983,
        "base_aqi": 185, "variance": 40,
        "factors": {"residential": 1.05, "traffic": 1.1}
    },
    "Punjabi Bagh": {
        "lat": 28.6692, "lng": 77.1311,
        "base_aqi": 175, "variance": 38,
        "factors": {"residential": 1.0, "traffic": 1.05}
    },
    "Chandni Chowk": {
        "lat": 28.6507, "lng": 77.2302,
        "base_aqi": 220, "variance": 55,
        "factors": {"commercial": 1.3, "traffic": 1.35, "congestion": 1.4}
    }
}

def get_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in km"""
    from math import radians, sin, cos, sqrt, atan2
    
    R = 6371  # Earth's radius in km
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c

def predict_aqi_for_location(lat, lng):
    """
    Predict AQI based on coordinates
    Uses nearest area's base AQI with time-based adjustments
    """
    # Find nearest area
    nearest_area = None
    min_distance = float('inf')
    
    for area_name, area_data in DELHI_AREAS.items():
        distance = get_distance(lat, lng, area_data["lat"], area_data["lng"])
        if distance < min_distance:
            min_distance = distance
            nearest_area = area_name
    
    if not nearest_area:
        return {"area": "Unknown", "aqi": 180, "category": "Unhealthy"}
    
    area_data = DELHI_AREAS[nearest_area]
    
    # Time-based adjustment
    hour = datetime.now().hour
    time_factor = 1.0
    
    # Peak pollution hours (morning and evening rush)
    if 7 <= hour <= 10 or 17 <= hour <= 21:
        time_factor = 1.2
    # Night hours (lower pollution)
    elif 0 <= hour <= 5:
        time_factor = 0.8
    
    # Calculate predicted AQI
    base_aqi = area_data["base_aqi"]
    variance = area_data["variance"]
    
    # Add some randomness for realistic variation
    random_factor = random.uniform(-0.15, 0.15)
    
    predicted_aqi = int(base_aqi * time_factor * (1 + random_factor))
    predicted_aqi = max(50, min(500, predicted_aqi))  # Clamp between 50-500
    
    # Get category
    category = get_aqi_category(predicted_aqi)
    
    return {
        "area": nearest_area,
        "aqi": predicted_aqi,
        "category": category,
        "distance_km": round(min_distance, 2),
        "time_factor": round(time_factor, 2)
    }

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

def get_all_areas_prediction():
    """Get predicted AQI for all Delhi areas"""
    predictions = []
    
    for area_name, area_data in DELHI_AREAS.items():
        result = predict_aqi_for_location(area_data["lat"], area_data["lng"])
        predictions.append(result)
    
    # Sort by AQI (worst first)
    predictions.sort(key=lambda x: x["aqi"], reverse=True)
    
    return predictions
