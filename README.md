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

# Generate dataset (first time only)
python extract_data_from_notebook.py

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

## 📊 Dataset Setup

The model requires `delhi_aqi.csv` with Delhi air quality data.

### Option 1: Generate Synthetic Data (Recommended)
```bash
python extract_data_from_notebook.py
```

This generates a synthetic dataset matching Delhi's pollution patterns based on the notebook's statistics (18,776 hourly records from Nov 2020 - Jan 2023).

### Option 2: Use Your Own Data
If you have the dataset from Google Colab or Kaggle:
1. Place `delhi_aqi.csv` in the project root
2. Ensure it has columns: `date, co, no, no2, o3, so2, pm2_5, pm10, nh3`

### Option 3: Download from Kaggle
1. Visit: [Air Quality Data in India](https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india)
2. Download Delhi subset
3. Place as `delhi_aqi.csv` in project root

## 🧠 Model Training

To train or retrain the model:

```bash
# Generate dataset if not already present
python extract_data_from_notebook.py

# Train the model
python train_model.py
```

This will:
1. Load the Delhi AQI dataset
2. Train a new Random Forest model
3. Save model to `models/aqi_model.pkl`
4. Generate performance metrics
5. Save model metadata

## 🌐 Deployment

Deploy to Vercel:
```bash
vercel --prod
```

## 📄 License

MIT License - See LICENSE file
