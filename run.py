"""
AgroPredict AI — One-Click Application Runner
Automatically verifies ML models, datasets, and launches the web application.
"""

import sys
import os
from pathlib import Path
import uvicorn

# Reconfigure stdout for UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from ml import config

def main():
    print("=" * 65)
    print("       AGROPREDICT AI - CROP PRODUCTION & YIELD SYSTEM          ")
    print("=" * 65)

    # 1. Check dataset
    if not config.DATA_PATH.exists():
        print("[1/3] Curated dataset not found. Generating data/crop_yield.csv...")
        from data import prepare_data
        print("  [OK] Dataset ready.")
    else:
        print("[1/3] Dataset verified: data/crop_yield.csv exists.")

    # 2. Check trained model
    if not config.MODEL_PATH.exists():
        print("[2/3] Model artifacts not found. Training & benchmarking models...")
        from ml.model_trainer import train_and_evaluate
        train_and_evaluate()
        print("  [OK] Model trained and saved.")
    else:
        print("[2/3] Trained ML Model bundle verified: ml/artifacts/best_crop_model.joblib.")

    # 3. Launch Web Server
    print("[3/3] Starting AgroPredict Web Application...")
    print("  -> Access the website at: http://127.0.0.1:8000")
    print("  -> API Documentation at:  http://127.0.0.1:8000/docs")
    print("=" * 65)
    print("Press CTRL+C in this terminal to stop the server.\n")

    uvicorn.run(
        "backend.app:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()

