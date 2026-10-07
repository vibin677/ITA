# 🚀 AgroPredict AI — Deployment & Setup Guide

## System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: Minimum 2GB (4GB recommended)
- **Disk**: 500MB free space

---

## ✅ Quick Start (Windows PowerShell)

### Step 1: Create Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Launch the Application
```powershell
.\.venv\Scripts\python.exe run.py
```

The application will:
1. ✅ Verify the dataset (`data/crop_yield.csv`)
2. ✅ Train/load the ML model (`ml/artifacts/best_crop_model.joblib`)
3. ✅ Start the FastAPI web server

### Step 4: Access the Website
Open your browser and navigate to:
```
http://127.0.0.1:8000
```

### API Documentation
Interactive API docs available at:
```
http://127.0.0.1:8000/docs
```

---

## 🧪 Running Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -v tests/test_api.py
```

---

## 📁 Project Structure

```
ita/
├── backend/              # FastAPI REST API backend
│   └── app.py           # Main FastAPI application with all endpoints
├── data/                # Dataset & data preparation
│   ├── crop_yield.csv   # 1,805+ agricultural records
│   └── prepare_data.py  # Data curation script
├── frontend/            # Web UI (Single Page Application)
│   ├── static/
│   │   ├── css/style.css        # Glassmorphic design system
│   │   └── js/app.js            # Interactive frontend logic
│   └── templates/
│       └── index.html           # Main HTML template
├── ml/                  # Machine Learning components
│   ├── config.py        # Agronomic parameters & configurations
│   ├── model_trainer.py # Multi-model training & benchmarking
│   └── artifacts/       # Serialized models & metadata
│       ├── best_crop_model.joblib    # Champion model
│       ├── model_comparison.json     # Benchmark metrics
│       ├── dataset_stats.json        # Data statistics
│       └── presets.json              # Predefined agricultural scenarios
├── tests/               # Automated test suite
│   └── test_api.py      # Pytest integration tests
├── reports/             # Project documentation & reports
├── requirements.txt     # Python dependencies
├── run.py              # Single-command launcher
├── README.md           # Main documentation
└── DEPLOYMENT.md       # This file
```

---

## 🌟 Key Features Overview

### 1. 🌾 **Predictor Studio**
- Input agricultural parameters (area, rainfall, temperature, fertilizer, pesticide)
- Select crop and region
- Get instant production forecasts with:
  - Total production in tonnes
  - Yield rate (tonnes/hectare)
  - Agro-climatic suitability score (0-100)
  - Radar chart breakdown
  - Farm economics & revenue calculator
  - Smart agronomist advisory

### 2. 📈 **Sensitivity ("What-If") Simulator**
- Simulate production changes with varying inputs (-30% to +30%)
- Interactive response curves for:
  - Rainfall impact
  - Fertilizer impact
  - Temperature impact
- Step-by-step impact breakdown table

### 3. 🏆 **Model Leaderboard & Explainable AI**
- Compare 5 regression algorithms:
  - Gradient Boosting Regressor (Champion: R² ≈ 0.813)
  - Random Forest Regressor
  - Linear Regression
  - Ridge Regression
  - Decision Tree Regressor
- Feature importance visualization
- Detailed performance metrics

### 4. 📊 **Dataset Explorer**
- Browse 1,805+ agricultural records
- Search by crop, state, or keyword
- Paginated table view
- Statistical summary metrics
- Export-ready data

### 5. 📁 **Batch CSV Predictor**
- Upload multiple farm records at once
- Drag-and-drop CSV interface
- Instant bulk processing
- Download results with predictions
- Sample CSV template included

---

## 🔌 API Endpoints

All endpoints return JSON responses with standardized error handling.

### Prediction Endpoints

**POST /predict**
```json
{
  "cultivated_area_ha": 10,
  "rainfall_mm": 800,
  "temperature_c": 25,
  "fertilizer_kg_ha": 100,
  "pesticide_kg_ha": 5,
  "crop": "Wheat",
  "state": "Punjab",
  "season": "Rabi"
}
```

Response:
```json
{
  "total_production_tonnes": 45.2,
  "yield_tonnes_ha": 4.52,
  "rating": "Outstanding",
  "suitability_score": 88.5,
  "radar_dimensions": {...},
  "economics": {...},
  "advisory": "..."
}
```

**POST /analyze-sensitivity**
- Simulate production changes with varying inputs
- Returns impact analysis and response curves

**POST /batch-predict**
- Upload CSV file for bulk predictions
- Returns enhanced CSV with predictions

**GET /presets**
- Retrieve predefined agricultural scenarios

**GET /model-comparison**
- Get benchmark metrics for all 5 models

**GET /dataset**
- Fetch paginated dataset records

---

## ⚙️ Configuration

All agricultural parameters and market prices are configured in `ml/config.py`:

```python
# Crop-specific water requirements
CROP_WATER_REQUIREMENTS = {
    "Wheat": 600,
    "Rice": 1200,
    ...
}

# Market prices (Minimum Support Prices - MSP)
MARKET_PRICES = {
    "Wheat": 2500,  # ₹ per tonne
    "Rice": 4000,
    ...
}

# NPK Ratios for optimal fertilizer balance
NPK_RATIOS = {
    "Wheat": {"N": 10, "P": 2.6, "K": 0.5},
    ...
}
```

---

## 🐛 Troubleshooting

### Issue: "Module not found" error
**Solution**: Ensure you've activated the virtual environment:
```powershell
.\.venv\Scripts\Activate.ps1
```

### Issue: Port 8000 already in use
**Solution**: Change the port in `run.py` or kill the process using port 8000:
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue: Model artifacts missing
**Solution**: The model will be trained automatically on first run. This may take 1-2 minutes.

### Issue: Dataset not found
**Solution**: Run the data preparation script:
```powershell
.\.venv\Scripts\python.exe data/prepare_data.py
```

---

## 📊 Performance Metrics

The champion **Gradient Boosting Regressor** model achieves:
- **R² Score**: 0.813 (explains 81.3% of variance)
- **RMSE**: 9.71 tonnes
- **MAE**: 7.24 tonnes
- **Training Time**: ~30 seconds (first run)

---

## 🔐 Production Deployment

For production deployment, consider:

1. **Use a production ASGI server**:
   ```powershell
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.app:app
   ```

2. **Enable HTTPS**:
   - Use a reverse proxy (Nginx, Apache)
   - Configure SSL certificates

3. **Environment Variables**:
   - Set `ENVIRONMENT=production`
   - Configure logging to files

4. **Docker Deployment**:
   Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "run.py"]
   ```

---

## 📝 License

This project is open-source. See repository for details.

---

## 👨‍💻 Support & Contribution

For issues, feature requests, or contributions:
1. Check existing GitHub issues
2. Create a detailed bug report
3. Submit pull requests with clear descriptions

---

## 🎯 Next Steps

1. ✅ Run the application: `python run.py`
2. ✅ Explore all features in the web interface
3. ✅ Review API documentation at `/docs`
4. ✅ Run test suite: `pytest -v tests/`
5. ✅ Deploy to production using provided guidelines

---

**Happy Farming with AgroPredict AI! 🌾**
