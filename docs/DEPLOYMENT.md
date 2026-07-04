# Vercel Deployment Guide

## Setup for Vercel Deployment

### 1. Create Vercel Project
```bash
npm install -g vercel
vercel
```

### 2. Set Environment Variables

Go to Vercel Dashboard → Project Settings → Environment Variables

Add:
- **AQI_API_KEY** = Your WAQI API key from https://aqicn.org/api/

If this variable is missing, the app returns a clear error payload instead of silently falling back to WAQI.

### 3. Deploy
```bash
vercel --prod
```

## Project Structure

```
/api
  └── index.py        # Canonical serverless function entrypoint
/templates
  └── index.html      # Canonical dashboard HTML
/static
  ├── css/style.css
  └── js/app.js
/public
  └── index.html      # Legacy dashboard kept for compatibility
/legacy
  ├── app.py
  ├── flask_app.py
  ├── aqi.py
  ├── train_model.py
  ├── Procfile
  └── render.yaml
vercel.json           # Vercel configuration
requirements.txt      # Python dependencies for Vercel runtime
```

## API Endpoint

**GET** `/api/current`

**Response:**
```json
{
  "status": "success",
  "aqi": 131,
  "category": "Unhealthy",
  "color": "#ff0000",
  "station": "Delhi",
  "timestamp": "2024-01-01 12:00:00"
}
```

Legacy compatibility is still available at **GET** `/api/aqi` for the archived public dashboard.

## Features

✅ Serverless Python functions on Vercel
✅ Real-time AQI data from WAQI
✅ CORS enabled for frontend requests
✅ Environment variable support
✅ Explicit error handling when AQI_API_KEY is missing
✅ Auto-refresh every 5 minutes

## Testing Locally

```bash
pip install -r requirements.txt
vercel dev
```

Then visit `http://localhost:3000`

If you need the archived Render/Flask path, it now lives under `legacy/` and is not part of the Vercel deployment.
