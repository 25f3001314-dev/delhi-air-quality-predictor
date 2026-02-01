import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import json
from datetime import datetime

# Load and prepare data
# NOTE: If delhi_aqi.csv is missing, run: python extract_data_from_notebook.py
print("Loading Delhi AQI dataset...")
df = pd.read_csv('delhi_aqi.csv')

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Feature Engineering - Extract temporal features
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['hour'] = df['date'].dt.hour
df['dayofweek'] = df['date'].dt.dayofweek

# Create lag features for better predictions
# Lag features capture temporal dependencies in air quality:
# - pm2_5_lag1: Previous hour's PM2.5 (immediate history)
# - pm2_5_lag24: PM2.5 from 24 hours ago (daily pattern)
# - pm10_lag1: Previous hour's PM10 (correlated with PM2.5)
df['pm2_5_lag1'] = df['pm2_5'].shift(1)
df['pm2_5_lag24'] = df['pm2_5'].shift(24)
df['pm10_lag1'] = df['pm10'].shift(1)

# Drop rows with NaN due to lag features
df = df.dropna()

# Define features and target
feature_columns = ['co', 'no', 'no2', 'o3', 'so2', 'pm10', 'nh3', 
                   'year', 'month', 'day', 'hour', 'dayofweek',
                   'pm2_5_lag1', 'pm2_5_lag24', 'pm10_lag1']

X = df[feature_columns]
y = df['pm2_5']

# Train-test split (80-20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")

# Train Random Forest Model
print("\nTraining Random Forest Regressor...")
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=30,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1,
    verbose=1
)

model.fit(X_train, y_train)

# Make predictions
print("\nEvaluating model...")
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# Calculate metrics
train_mae = mean_absolute_error(y_train, y_pred_train)
train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
train_r2 = r2_score(y_train, y_pred_train)

test_mae = mean_absolute_error(y_test, y_pred_test)
test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
test_r2 = r2_score(y_test, y_pred_test)

# Print results
print("\n" + "="*50)
print("MODEL PERFORMANCE METRICS")
print("="*50)
print("\nTraining Set:")
print(f"  MAE:  {train_mae:.2f}")
print(f"  RMSE: {train_rmse:.2f}")
print(f"  R²:   {train_r2:.4f}")

print("\nTest Set:")
print(f"  MAE:  {test_mae:.2f}")
print(f"  RMSE: {test_rmse:.2f}")
print(f"  R²:   {test_r2:.4f}")
print("="*50)

# Feature importance
feature_importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 10 Most Important Features:")
print(feature_importance.head(10).to_string(index=False))

# Save the model
print("\nSaving trained model...")
joblib.dump(model, 'models/aqi_model.pkl')

# Save feature columns list
with open('models/feature_columns.json', 'w') as f:
    json.dump(feature_columns, f)

# Save model metadata
metadata = {
    'model_type': 'RandomForestRegressor',
    'trained_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'features': feature_columns,
    'train_samples': int(X_train.shape[0]),
    'test_samples': int(X_test.shape[0]),
    'metrics': {
        'train_mae': float(train_mae),
        'train_rmse': float(train_rmse),
        'train_r2': float(train_r2),
        'test_mae': float(test_mae),
        'test_rmse': float(test_rmse),
        'test_r2': float(test_r2)
    }
}

with open('models/model_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print("\n✅ Model training complete!")
print(f"Model saved to: models/aqi_model.pkl")
print(f"Metadata saved to: models/model_metadata.json")
