"""
explain.py -- AgroPredict AI: Mentor Walkthrough
=================================================
Run this script to get a complete, guided explanation of how
the AgroPredict project is built, the ML pipeline, and results.

Usage:
    python explain.py
"""

import sys

# Fix Windows terminal encoding (cp1252 -> utf-8)
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import json
from pathlib import Path

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def section(title: str):
    print()
    print("=" * 65)
    print(f"  {title}")
    print("=" * 65)

def step(label: str, text: str):
    print(f"\n  [{label}]  {text}")

def bullet(items: list):
    for item in items:
        if item == "":
            print()
        else:
            print(f"      *  {item}")

def bar(label: str, value: float, total: float = 1.0, width: int = 28):
    filled = int((value / total) * width)
    b = "#" * filled + "." * (width - filled)
    print(f"      {label:<24} [{b}]  {value:.4f}")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT         = Path(__file__).resolve().parent
METRICS_PATH = ROOT / "ml" / "artifacts" / "model_comparison.json"
STATS_PATH   = ROOT / "ml" / "artifacts" / "dataset_stats.json"

# ===========================================================================
# TITLE CARD
# ===========================================================================

print()
print("+" + "-" * 63 + "+")
print("|       AGROPREDICT AI  -- MENTOR WALKTHROUGH                  |")
print("|       Crop Production & Yield Intelligence Platform           |")
print("+" + "-" * 63 + "+")
print()
print("  This walkthrough covers:")
print("    1. What problem this project solves")
print("    2. Project architecture overview")
print("    3. The ML pipeline (data -> training -> deployment)")
print("    4. Actual model results and feature importance")
print("    5. Live prediction demo")
print("    6. API endpoints")
print("    7. Honest limitations and next steps")

# ===========================================================================
# SECTION 1 -- Problem statement
# ===========================================================================

section("1. WHAT PROBLEM DOES THIS PROJECT SOLVE?")

print("""
  Indian agriculture supports ~600 million people but farmers still
  rely on guesswork for yield estimation. A small mismatch between
  expected and actual yield leads to:

      * Over-purchasing fertilizer / pesticide  ->  wasted cost
      * Under-irrigating during critical stages ->  crop loss
      * Poor market timing                      ->  low revenue

  AgroPredict addresses this with a data-driven crop yield prediction
  system. A farmer (or agri officer) enters simple field parameters
  and receives an instant, ML-powered prediction + actionable advice.

  Key outputs per prediction:
      * Yield forecast     (tonnes/ha + total production)
      * Agronomic advisory (what input is deficient / excessive)
      * Economics          (revenue, cost, net profit, ROI)
      * Suitability radar  (soil, moisture, thermal, pest scores)
      * What-if analysis   (how yield changes if rainfall drops 20%)
      * Batch prediction   (upload CSV for 100s of plots at once)
""")

# ===========================================================================
# SECTION 2 -- Architecture
# ===========================================================================

section("2. PROJECT ARCHITECTURE")

print("""
  d:/GitHub/ITA/
  |
  +-- data/
  |   +-- crop_yield.csv          1,805 agronomic records (dataset)
  |   +-- prepare_data.py         dataset generation script
  |
  +-- ml/
  |   +-- config.py               paths, crop profiles, MSP prices
  |   +-- model_trainer.py        full ML training pipeline
  |   +-- artifacts/
  |       +-- best_crop_model.joblib      champion model (~632 KB)
  |       +-- suitability_models.joblib   4 radar sub-models (~10 MB)
  |       +-- model_comparison.json       benchmarks for all models
  |       +-- dataset_stats.json          dataset summary
  |       +-- presets.json                quick-preset scenarios
  |
  +-- backend/
  |   +-- app.py                  FastAPI web server (9 REST endpoints)
  |
  +-- frontend/
  |   +-- templates/index.html    single-page UI
  |   +-- static/                 JS, CSS, assets
  |
  +-- run.py                      one-click launcher
  +-- explain.py                  this file (you are here)

  Tech Stack:
      Backend   ->  Python 3.11 + FastAPI + Uvicorn
      ML        ->  scikit-learn  (GradientBoosting, RandomForest, etc.)
      Storage   ->  joblib model serialisation, lazy-load caching
      Frontend  ->  Vanilla HTML / CSS / JavaScript  (no framework)
      CI/CD     ->  GitHub Actions  (.github/workflows/ci.yml)
      Container ->  Docker + docker-compose
""")

# ===========================================================================
# SECTION 3 -- ML Pipeline
# ===========================================================================

section("3. ML PIPELINE  (ml/model_trainer.py)")

step("STEP 1", "Load dataset: data/crop_yield.csv")
print("             Features: Area, Rainfall, Temperature, Fertilizer,")
print("                       Pesticide, State, Crop, Season")
print("             Target  : Yield (tonnes per hectare)")

step("STEP 2", "Preprocessing via scikit-learn ColumnTransformer")
bullet([
    "Numerical columns (5 features):",
    "   SimpleImputer(strategy=median)  ->  StandardScaler",
    "Categorical columns (3 features):",
    "   SimpleImputer(strategy=most_frequent)  ->  OneHotEncoder",
])

step("STEP 3", "80 / 20 train-test split  (random_state=42 for reproducibility)")

step("STEP 4", "Train 5 models and benchmark each:")
bullet([
    "Gradient Boosting   (n_estimators=150, max_depth=5, lr=0.08)",
    "Random Forest       (n_estimators=150, max_depth=12, n_jobs=-1)",
    "Decision Tree       (max_depth=8)",
    "Ridge Regression    (alpha=1.0)",
    "Linear Regression",
    "",
    "Metrics per model:  R2, RMSE, MAE, 3-fold cross-validated R2",
])

step("STEP 5", "Champion model selected automatically -> highest R2 on test set")

step("STEP 6", "Train 4 suitability sub-models (each a RandomForestRegressor):")
bullet([
    "soil_nutrition      -- fertilizer suitability per crop profile",
    "moisture_level      -- rainfall suitability",
    "thermal_fit         -- temperature suitability",
    "protection_balance  -- pesticide suitability",
    "",
    "Labels (0-100 scores) are derived from per-crop agronomic rules.",
    "The sub-models learn crop-specific context from the full dataset.",
])

step("STEP 7", "All artifacts serialized to ml/artifacts/ via joblib")

# ===========================================================================
# SECTION 4 -- Real model results
# ===========================================================================

section("4. ACTUAL MODEL RESULTS")

if METRICS_PATH.exists() and STATS_PATH.exists():
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        metrics = json.load(f)
    with open(STATS_PATH, "r", encoding="utf-8") as f:
        stats = json.load(f)

    best = metrics["best_model"]
    print(f"\n  Champion Model   :  {best['name']}")
    print(f"  R2  (accuracy)   :  {best['r2']}  "
          f"(explains {int(best['r2']*100)}% of yield variance)")
    print(f"  RMSE             :  {best['rmse']} tonnes/ha")
    print(f"  MAE              :  {best['mae']}  tonnes/ha")
    print(f"  CV-R2  (3-fold)  :  {best['cv_r2']}  (stable across folds)")

    print("\n  -- All 5 Models Compared (more # = better R2) --------")
    for m in metrics["models"]:
        bar(m["name"], m["r2"])

    print("\n  -- Feature Importance (what drives yield the most?) ---")
    fi = metrics["feature_importances"]
    total_imp = sum(x["importance"] for x in fi)
    for item in fi:
        bar(item["feature"], item["importance"], total=total_imp)

    print("\n  -- Dataset Summary ------------------------------------")
    print(f"      Total records   :  {stats['total_records']:,}")
    print(f"      Crops covered   :  {', '.join(metrics['crops'])}")
    print(f"      States covered  :  {len(metrics['states'])} Indian states")
    print(f"      Seasons         :  Kharif, Rabi, Whole Year")
    print(f"      Avg yield       :  {stats['avg_yield']} tonnes/ha")
    print(f"      Yield range     :  {stats['min_yield']} - "
          f"{stats['max_yield']} tonnes/ha")
else:
    print("\n  [!] Artifact files not found.")
    print("      Run `python run.py` first to train the models.")

# ===========================================================================
# SECTION 5 -- Live prediction demo
# ===========================================================================

section("5. LIVE PREDICTION DEMO")

print("""
  Scenario: Punjab Wheat farm, Rabi season
      Area        = 1,850 ha
      Rainfall    = 680 mm
      Temperature = 18.5 degC
      Fertilizer  = 135 kg/ha
      Pesticide   = 18 kg/ha
""")

try:
    sys.path.insert(0, str(ROOT))
    import joblib
    import pandas as pd
    from ml import config

    bundle       = joblib.load(config.MODEL_PATH)
    model        = bundle["model"]
    preprocessor = bundle["preprocessor"]

    sample = pd.DataFrame([{
        "Area":        1850.0,
        "Rainfall":    680.0,
        "Temperature": 18.5,
        "Fertilizer":  135.0,
        "Pesticide":   18.0,
        "State":       "Punjab",
        "Crop":        "Wheat",
        "Season":      "Rabi",
    }])

    X          = preprocessor.transform(sample)
    pred_yield = max(1.0, round(float(model.predict(X)[0]), 2))
    total_prod = round(pred_yield * 1850.0, 2)
    msp        = config.CROP_PRICES_INR.get("Wheat", 22750)
    revenue    = round(total_prod * msp, 2)
    cost       = round((22000 + 135 * 24 + 18 * 450) * 1850, 2)
    profit     = round(revenue - cost, 2)
    roi        = round((profit / max(1, cost)) * 100, 1)

    print(f"  [OK] Predicted Yield      :  {pred_yield} tonnes / ha")
    print(f"  [OK] Total Production     :  {total_prod:,.1f} tonnes")
    print(f"  [OK] Estimated Revenue    :  Rs {revenue:,.0f}"
          f"  (${revenue/86.5:,.0f} USD)")
    print(f"  [OK] Estimated Cost       :  Rs {cost:,.0f}")
    print(f"  [OK] Net Profit           :  Rs {profit:,.0f}")
    print(f"  [OK] ROI                  :  {roi}%")
    print(f"\n  Model used : {bundle['model_name']}")
    print(f"  Model R2   : {bundle['metrics']['r2']}")

except Exception as e:
    print(f"  [!] Could not run live demo: {e}")
    print("      Run `python run.py` first to train & start the server.")

# ===========================================================================
# SECTION 6 -- API endpoints
# ===========================================================================

section("6. REST API ENDPOINTS  (backend/app.py)")

endpoints = [
    ("GET",  "/",                        "Serves the web UI (index.html)"),
    ("GET",  "/api/health",              "Model status + champion R2"),
    ("GET",  "/api/presets",             "Load preset farm scenarios"),
    ("GET",  "/api/models/comparison",   "Model leaderboard + feature importance"),
    ("GET",  "/api/dataset/stats",       "Dataset summary statistics"),
    ("GET",  "/api/dataset/records",     "Paginated, filterable dataset browser"),
    ("POST", "/api/predict",             "Yield prediction + advisory + economics"),
    ("POST", "/api/predict/sensitivity", "What-if curve (rainfall/fertilizer/temp)"),
    ("POST", "/api/predict/batch",       "Bulk CSV prediction"),
]

print()
for method, path, desc in endpoints:
    tag = f"[{method}]"
    print(f"    {tag:<7}  {path:<36} {desc}")

print()
print("  Interactive API docs:  http://127.0.0.1:8000/docs  (Swagger UI)")

# ===========================================================================
# SECTION 7 -- Honest limitations
# ===========================================================================

section("7. HONEST LIMITATIONS & NEXT STEPS")

bullet([
    "DATASET: Training data is SYNTHETIC (generated by prepare_data.py).",
    "  Real field survey data (ICAR/ICMR) would improve accuracy significantly.",
    "",
    "WEATHER: Rainfall and temperature are user-entered, not auto-fetched",
    "  from a live weather API (e.g., OpenWeatherMap, IMD).",
    "",
    "PRICES: MSP crop prices are hardcoded constants, not live market rates",
    "  from NAFED or eNAM.",
    "",
    "AUTH: No user authentication or prediction history persistence.",
    "",
    "SUITABILITY LABELS: Rule-derived, not validated by agronomists.",
    "",
    "NEXT STEPS:",
    "  1. Replace synthetic data with real ICAR district-level records",
    "  2. Integrate IMD weather API for auto-filled climate inputs",
    "  3. Add live MSP price feed from eNAM API",
    "  4. Deploy to cloud (Docker + GCP Cloud Run / AWS ECS)",
    "  5. Add user login + prediction history dashboard",
])

# ===========================================================================
# HOW TO RUN
# ===========================================================================

section("HOW TO RUN THE PROJECT")

print("""
  One-command launch (recommended):
  -----------------------------------------------
    python run.py
  -----------------------------------------------
  This will:
    [1/3]  Verify dataset exists
    [2/3]  Train models if artifacts are missing
    [3/3]  Start web server at http://127.0.0.1:8000

  Then open:
    Web App   ->  http://127.0.0.1:8000
    API Docs  ->  http://127.0.0.1:8000/docs

  To retrain models from scratch:
    python ml/model_trainer.py

  To run tests:
    pytest tests/
""")

print("=" * 65)
print("  WALKTHROUGH COMPLETE")
print("  Questions? See README.md or ask the developer.")
print("=" * 65)
print()
