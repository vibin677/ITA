# 🌾 AgroPredict AI — Intelligent Crop Yield & Production Forecasting Engine

An end-to-end, production-grade Machine Learning web application designed to forecast agricultural crop yield (Tonnes/Ha) and aggregate production volume (Tonnes) across key crops, agro-climatic zones, and seasonal conditions.

---

## 🌟 Key Features

### 1. 🌾 AI Yield & Production Predictor Studio
- **Input Parameters**: Cultivated Area, Annual/Seasonal Rainfall, Mean Temperature, Fertilizer Application Rate, Pesticide Dosage, Target Crop, Region/State, and Agricultural Season.
- **One-Click Real-World Presets**:
  - *Punjab Wheat Belt (Rabi)*
  - *Maharashtra Black Soil (Cotton - Kharif)*
  - *Uttar Pradesh Cane Basin (Sugarcane - Annual)*
  - *Tamil Nadu Cauvery Delta (Rice - Kharif)*
  - *Kerala Coastal Strip (Rice - Kharif)*
- **Multi-Faceted Output**:
  - **Estimated Total Production (Tonnes)** and **Normalized Yield Rate (Tonnes/Hectare)**.
  - **Yield Performance Rating**: Outstanding (Bumper Yield), Above Average, Moderate Yield, Sub-optimal / Vulnerable.
  - **Agro-climatic Suitability Score (0-100)** with interactive radar dimension breakdown (Soil Nutrition, Moisture Availability, Thermal Fit, Protection Balance).
  - **Farm Economics & Revenue Calculator**: Project gross revenue, operational production costs, net farm profit, and estimated ROI percentage based on benchmark Minimum Support Prices (MSP) / market rates.
  - **Smart Agronomist Advisory**: Actionable guidance tailored to specific crop water requirements, NPK balance, and pest management.

### 2. 📈 What-If Sensitivity Simulator
- Dynamically simulate how production responds when weather or chemical inputs fluctuate (-30% to +30%).
- Interactive Chart.js response curves for **Rainfall**, **Fertilizer**, or **Temperature**.
- Step-by-step impact breakdown table showing exact numerical changes.

### 3. 🏆 Comparative Model Leaderboard & Explainable AI (XAI)
- Benchmarks 5 regression algorithms on the same train/test split:
  1. **Gradient Boosting Regressor** (Champion: $R^2 \approx 0.813$, $\text{RMSE} \approx 9.71$)
  2. **Random Forest Regressor** ($R^2 \approx 0.786$, $\text{RMSE} \approx 10.41$)
  3. **Linear Regression** ($R^2 \approx 0.745$, $\text{RMSE} \approx 11.36$)
  4. **Ridge Regression** ($R^2 \approx 0.744$, $\text{RMSE} \approx 11.37$)
  5. **Decision Tree Regressor** ($R^2 \approx 0.656$, $\text{RMSE} \approx 13.18$)
- **Feature Importance Chart**: Visualizes the relative predictive influence of Fertilizer, Area, Rainfall, Temperature, Pesticides, and Crop.

### 4. 📊 Interactive Dataset Explorer
- Full search and filtering capabilities (by Crop, State, keyword) over 1,800+ curated agricultural records.
- Paginated table with statistical summary metrics.

### 5. 📁 Enterprise Batch CSV Predictor
- Drag-and-drop CSV upload for multi-farm bulk inference.
- Instant processing with summary metrics, preview table, and 1-click download of the enriched CSV with predictions.
- Downloadable sample CSV template included.

---

## 🚀 Quickstart Guide

### 1. Launch the Website
Run the all-in-one runner script:
```powershell
.\.venv\Scripts\python.exe run.py
```

Open your browser and navigate to:
```
http://127.0.0.1:8000
```

Interactive API documentation is also available at:
```
http://127.0.0.1:8000/docs
```

---

## 📁 Project Architecture

```
ita/
├── backend/
│   └── app.py                     # FastAPI backend REST API + Static/HTML mounting
├── data/
│   ├── crop_yield.csv             # Curated crop agricultural dataset (1,805 records)
│   └── prepare_data.py            # Data curation and cleansing script
├── frontend/
│   ├── static/
│   │   ├── css/style.css          # Glassmorphic AgroTech design & animations
│   │   └── js/app.js              # Client-side UI logic, charts, and API integration
│   └── templates/
│       └── index.html             # Main responsive single-page web dashboard
├── ml/
│   ├── config.py                  # Agronomic profiles, market prices, and paths
│   ├── model_trainer.py           # Multi-model training, evaluation & artifact export
│   └── artifacts/
│       ├── best_crop_model.joblib # Serialized champion model + preprocessor
│       ├── model_comparison.json  # Benchmark metrics & feature importances
│       ├── dataset_stats.json     # Precomputed distribution statistics
│       └── presets.json           # Quick-load agricultural scenarios
├── tests/
│   └── test_api.py                # Automated pytest test suite
├── requirements.txt               # Python package dependencies
├── run.py                         # Single-command launcher
└── README.md                      # Project documentation
```

---

## 🧪 Running Automated Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -v tests/test_api.py
```

