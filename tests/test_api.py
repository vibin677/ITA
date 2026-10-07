"""
Automated Integration and Unit Tests for AgroPredict AI
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model_name" in data
    assert data["total_dataset_records"] > 0

def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "AgroPredict" in response.text
    assert "Predictor Studio" in response.text

def test_presets():
    response = client.get("/api/presets")
    assert response.status_code == 200
    presets = response.json()
    assert len(presets) >= 4
    first = presets[0]
    assert "crop" in first
    assert "rainfall" in first
    assert "temperature" in first

def test_models_comparison():
    response = client.get("/api/models/comparison")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert "best_model" in data
    assert "feature_importances" in data
    assert len(data["models"]) >= 5
    assert data["best_model"]["r2"] > 0.75

def test_dataset_stats():
    response = client.get("/api/dataset/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_records"] > 1000
    assert "avg_yield" in data
    assert "crop_counts" in data

def test_dataset_records():
    response = client.get("/api/dataset/records?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert len(data["records"]) == 10
    assert "Crop" in data["records"][0]
    assert "Yield" in data["records"][0]

def test_prediction_single():
    payload = {
        "crop": "Wheat",
        "state": "Punjab",
        "season": "Rabi",
        "area": 1200.0,
        "rainfall": 680.0,
        "temperature": 18.5,
        "fertilizer": 135.0,
        "pesticide": 18.0
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_yield_tonnes_per_ha" in data
    assert data["predicted_yield_tonnes_per_ha"] > 0
    assert data["total_production_tonnes"] > 0
    assert "economics" in data
    assert data["economics"]["gross_revenue_inr"] > 0
    assert "advisory" in data
    assert len(data["advisory"]["recommendations"]) >= 3

def test_sensitivity():
    payload = {
        "base_request": {
            "crop": "Wheat",
            "state": "Punjab",
            "season": "Rabi",
            "area": 1000.0,
            "rainfall": 700.0,
            "temperature": 20.0,
            "fertilizer": 120.0,
            "pesticide": 15.0
        },
        "parameter": "rainfall"
    }
    response = client.post("/api/predict/sensitivity", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["parameter"] == "rainfall"
    assert len(data["curve"]) == 7
    assert data["curve"][3]["delta_pct"] == "0%"

def test_batch_prediction():
    csv_content = (
        "Area,Rainfall,Temperature,Fertilizer,Pesticide,State,Crop,Season\n"
        "1000,750,22.0,110,15,Punjab,Wheat,Rabi\n"
        "1500,900,28.0,120,25,Tamil Nadu,Rice,Kharif\n"
    )
    files = {"file": ("test.csv", csv_content, "text/csv")}
    response = client.post("/api/predict/batch", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["total_rows_processed"] == 2
    assert "Predicted_Yield_Tonnes_Ha" in data["preview_rows"][0]
    assert "Total_Production_Tonnes" in data["preview_rows"][0]
    assert len(data["csv_data"]) > 0

if __name__ == "__main__":
    pytest.main(["-v", __file__])

