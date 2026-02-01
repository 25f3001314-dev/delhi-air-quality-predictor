"""
Generate synthetic Delhi AQI dataset for model training.
This script creates a dataset matching the structure expected by train_model.py
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("🔄 Generating synthetic Delhi AQI dataset...")

# Set random seed for reproducibility
np.random.seed(42)

# Generate date range: Nov 2020 to Jan 2023 (hourly data)
start_date = datetime(2020, 11, 25, 0, 0, 0)
end_date = datetime(2023, 1, 24, 23, 0, 0)
date_range = pd.date_range(start=start_date, end=end_date, freq='H')

# Initialize data dictionary
data = {
    'date': date_range,
}

# Generate realistic pollutant values based on Delhi's typical patterns
n_samples = len(date_range)

# PM2.5 - varies by season and time of day (higher in winter, early morning)
base_pm25 = np.random.normal(150, 50, n_samples)
seasonal_factor = np.sin(np.arange(n_samples) * 2 * np.pi / (365 * 24)) * 30
hourly_factor = np.sin(np.arange(n_samples) * 2 * np.pi / 24) * 20
data['pm2_5'] = np.maximum(10, base_pm25 + seasonal_factor - hourly_factor)

# PM10 - typically 1.5-2x PM2.5
data['pm10'] = data['pm2_5'] * np.random.uniform(1.5, 2.0, n_samples)

# CO (Carbon Monoxide) - correlated with PM2.5
data['co'] = data['pm2_5'] * np.random.uniform(0.05, 0.15, n_samples) + np.random.normal(0, 2, n_samples)

# NO (Nitric Oxide) - traffic related
base_no = np.random.normal(30, 15, n_samples)
data['no'] = np.maximum(0, base_no + np.sin(np.arange(n_samples) * 2 * np.pi / 24 - 8) * 10)

# NO2 (Nitrogen Dioxide) - traffic and industrial
base_no2 = np.random.normal(50, 20, n_samples)
data['no2'] = np.maximum(0, base_no2 + np.sin(np.arange(n_samples) * 2 * np.pi / 24 - 8) * 15)

# O3 (Ozone) - higher during day, photochemical reactions
base_o3 = np.random.normal(40, 15, n_samples)
daytime_o3 = np.maximum(0, np.sin(np.arange(n_samples) * 2 * np.pi / 24 - 6) * 20)
data['o3'] = np.maximum(0, base_o3 + daytime_o3)

# SO2 (Sulfur Dioxide) - industrial emissions
data['so2'] = np.maximum(0, np.random.normal(15, 8, n_samples))

# NH3 (Ammonia) - agricultural and industrial
data['nh3'] = np.maximum(0, np.random.normal(25, 12, n_samples))

# Create DataFrame
df = pd.DataFrame(data)

# Add some realistic correlations and noise
# Winter months (Nov-Feb) have higher pollution
winter_months = df['date'].dt.month.isin([11, 12, 1, 2])
df.loc[winter_months, 'pm2_5'] *= 1.3
df.loc[winter_months, 'pm10'] *= 1.3
df.loc[winter_months, 'no2'] *= 1.2

# Rush hours (7-9 AM, 6-8 PM) have higher traffic-related pollutants
rush_hours = df['date'].dt.hour.isin([7, 8, 18, 19])
df.loc[rush_hours, 'no'] *= 1.4
df.loc[rush_hours, 'no2'] *= 1.3
df.loc[rush_hours, 'co'] *= 1.2

# Ensure all values are positive and reasonable
for col in ['pm2_5', 'pm10', 'co', 'no', 'no2', 'o3', 'so2', 'nh3']:
    df[col] = np.maximum(0, df[col])
    
# Round to 2 decimal places
for col in df.columns:
    if col != 'date':
        df[col] = df[col].round(2)

# Save to CSV
output_file = 'delhi_aqi.csv'
df.to_csv(output_file, index=False)

print(f"✅ Successfully generated {output_file}")
print(f"📊 Total records: {len(df):,}")
print(f"📅 Date range: {df['date'].min()} to {df['date'].max()}")
print(f"\n📈 Sample statistics:")
print(f"   PM2.5 - Mean: {df['pm2_5'].mean():.2f}, Std: {df['pm2_5'].std():.2f}, Range: [{df['pm2_5'].min():.2f}, {df['pm2_5'].max():.2f}]")
print(f"   PM10  - Mean: {df['pm10'].mean():.2f}, Std: {df['pm10'].std():.2f}, Range: [{df['pm10'].min():.2f}, {df['pm10'].max():.2f}]")
print(f"\n✅ Ready to run: python train_model.py")
