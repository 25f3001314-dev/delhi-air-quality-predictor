# Delhi Air Quality Predictor 🌍

Real-time Air Quality Index prediction for Delhi using Machine Learning.

## 🚀 Features

- **ML-Powered Predictions**: Trained Random Forest model on 18,776+ historical data points
- **Real-time Weather Integration**: Temperature, humidity, wind speed data
- **Multi-Station Monitoring**: Track AQI across 5 Delhi locations
- **Beautiful Dashboard**: Interactive charts and visualizations
- **Auto-Refresh**: Updates every 5 minutes

## 🤖 Machine Learning Model

- **Algorithm**: Random Forest Regressor
- **Training Data**: Delhi AQI dataset (Nov 2020 - Jan 2023)
- **Features**: 15 features including pollutants (CO, NO, NO2, O3, SO2, PM10, NH3) and temporal patterns
- **Performance**: 
  - Test R² Score: ~0.66
  - Test MAE: ~19 µg/m³

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/25f3001314-dev/delhi-air-quality-predictor.git
cd delhi-air-quality-predictor

# Install dependencies
pip install -r requirements.txt

# Train model (first time only)
python train_model.py

# Run locally
vercel dev
```

## 🔧 Configuration

Set environment variable for real-time data enhancement:
```bash
export AQI_API_KEY=your_waqi_api_key
```

Get your API key from: https://aqicn.org/api/

## 📊 Model Training

To retrain the model with new data:

```bash
# Place your delhi_aqi.csv in the root directory
python train_model.py
```

This will:
1. Train a new Random Forest model
2. Save model to `models/aqi_model.pkl`
3. Generate performance metrics
4. Save model metadata

## 🌐 Deployment

Deploy to Vercel:
```bash
vercel --prod
```

## 📄 License

MIT License - See LICENSE file
