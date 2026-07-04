# Delhi Air Quality Predictor 🌍

Real-time Air Quality Index dashboard for Delhi, deployed on Vercel.

## 🚀 Features

- **Vercel-First Deployment**: Canonical entry point is `api/index.py`
- **Real-time Weather Integration**: Temperature, humidity, wind speed data
- **Multi-Station Monitoring**: Track AQI across 5 Delhi locations
- **Beautiful Dashboard**: Interactive charts and visualizations
- **Auto-Refresh**: Updates every 5 minutes

## 📁 Project Structure

```text
api/index.py            # Canonical Vercel serverless entrypoint
templates/index.html    # Canonical dashboard HTML
static/css/style.css    # Dashboard styling
static/js/app.js        # Frontend data loading and rendering
public/index.html       # Legacy dashboard kept for compatibility
legacy/                 # Archived Render/Flask entrypoints and training script
docs/                   # Deployment and implementation notes
notebooks/              # Archived notebook exports
scripts/                # Archived helper scripts
```

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/25f3001314-dev/delhi-air-quality-predictor.git
cd delhi-air-quality-predictor

# Install dependencies
pip install -r requirements.txt

# Run locally
vercel dev
```

## 🔧 Configuration

Set environment variable for real-time data access:
```bash
export AQI_API_KEY=your_waqi_api_key
```

Get your API key from: https://aqicn.org/api/

## 🌐 API Endpoints

- `GET /api/current` returns the current AQI payload for the canonical dashboard.
- `GET /api/historical` returns the chart data used by the canonical dashboard.
- `GET /api/aqi` is preserved for the legacy dashboard under `public/index.html`.

## 🌐 Deployment

Deploy to Vercel:
```bash
vercel --prod
```

For local testing, use:
```bash
vercel dev
```

If you need the archived Render/Flask stack, it is now under `legacy/` and is not part of the active deployment.

## 📄 License

MIT License - See LICENSE file
