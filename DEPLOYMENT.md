# Vercel Python Deployment Guide

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

### 3. Deploy
```bash
vercel --prod
```

## Project Structure

```
/api
  └── aqi.py          # Serverless function endpoint
/public
  └── index.html      # Frontend (auto-served by Vercel)
vercel.json          # Vercel configuration
requirements.txt     # Python dependencies
```

## API Endpoint

**GET** `/api/aqi`

**Response:**
```json
{
  "status": "success",
  "aqi": 131,
  "category": "Unhealthy",
  "city": "Delhi",
  "timestamp": "2024-01-01 12:00:00"
}
```

## Features

✅ Serverless Python functions on Vercel  
✅ Real-time AQI data from WAQI  
✅ CORS enabled for frontend requests  
✅ Environment variable support  
✅ Error handling & fallback values  
✅ Auto-refresh every 60 seconds  

## Testing Locally

```bash
pip install -r requirements.txt
vercel dev
```

Then visit `http://localhost:3000`
