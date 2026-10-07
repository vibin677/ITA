import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_PATH = DATA_DIR / "crop_yield.csv"
ARTIFACTS_DIR = BASE_DIR / "ml" / "artifacts"
MODEL_PATH = ARTIFACTS_DIR / "best_crop_model.joblib"
METRICS_PATH = ARTIFACTS_DIR / "model_comparison.json"
STATS_PATH = ARTIFACTS_DIR / "dataset_stats.json"
PRESETS_PATH = ARTIFACTS_DIR / "presets.json"

TARGET_COLUMN = "Yield"
NUMERICAL_COLUMNS = ["Area", "Rainfall", "Temperature", "Fertilizer", "Pesticide"]
CATEGORICAL_COLUMNS = ["State", "Crop", "Season"]

# Indicative MSP / Market benchmark rate per tonne (in INR)
CROP_PRICES_INR = {
    "Rice": 23000,
    "Wheat": 22750,
    "Cotton": 71200,
    "Sugarcane": 3400,
    "Maize": 20900,
    "Potatoes": 12000,
    "Groundnut": 67800,
    "Soybean": 48920,
}

USD_INR_RATE = 86.5

AGRONOMIC_PROFILES = {
    "Rice": {
        "opt_rainfall": (1000, 1600),
        "opt_temp": (20, 32),
        "opt_fertilizer": (80, 140),
        "opt_pesticide": (15, 35),
        "typical_yield_range": (30, 80),
        "irrigation_advice": "Maintain 2-5 cm standing water during vegetative stage. Implement Alternate Wetting and Drying (AWD) to conserve water.",
        "nutrient_advice": "Apply split Nitrogen application (50% basal, 25% tillering, 25% panicle initiation) with balanced Zinc Sulfate.",
    },
    "Wheat": {
        "opt_rainfall": (600, 1100),
        "opt_temp": (15, 25),
        "opt_fertilizer": (90, 150),
        "opt_pesticide": (10, 30),
        "typical_yield_range": (35, 95),
        "irrigation_advice": "Crucial irrigation at Crown Root Initiation (CRI) stage (21 days after sowing) and flowering stage.",
        "nutrient_advice": "Apply Phosphorus and Potash as basal dose; top-dress Urea before 1st and 2nd irrigations.",
    },
    "Cotton": {
        "opt_rainfall": (600, 1200),
        "opt_temp": (21, 35),
        "opt_fertilizer": (70, 130),
        "opt_pesticide": (20, 50),
        "typical_yield_range": (15, 65),
        "irrigation_advice": "Avoid waterlogging; cotton requires well-drained loamy soil. Drip irrigation improves boll retention.",
        "nutrient_advice": "Supplement with Boron and Magnesium sulfate to avoid leaf reddening and square dropping.",
    },
    "Sugarcane": {
        "opt_rainfall": (1100, 1800),
        "opt_temp": (24, 38),
        "opt_fertilizer": (120, 200),
        "opt_pesticide": (15, 40),
        "typical_yield_range": (50, 120),
        "irrigation_advice": "Requires 1500-2500 mm total water across season. Trash mulching helps conserve root zone moisture.",
        "nutrient_advice": "Heavy feeder of Potassium for sucrose synthesis; apply organic press-mud compost if available.",
    },
    "Maize": {
        "opt_rainfall": (500, 900),
        "opt_temp": (18, 30),
        "opt_fertilizer": (80, 140),
        "opt_pesticide": (10, 30),
        "typical_yield_range": (25, 75),
        "irrigation_advice": "Critical stages for water are knee-high, tasseling, and grain filling.",
        "nutrient_advice": "Balanced NPK 120:60:40 kg/ha with micronutrient Zinc application.",
    },
    "Potatoes": {
        "opt_rainfall": (400, 700),
        "opt_temp": (15, 24),
        "opt_fertilizer": (110, 180),
        "opt_pesticide": (15, 45),
        "typical_yield_range": (40, 110),
        "irrigation_advice": "Maintain uniform soil moisture; tuber cracking occurs if soil cycles between dry and wet.",
        "nutrient_advice": "High Potash demand for tuber sizing; avoid excess Nitrogen late in season.",
    },
    "Groundnut": {
        "opt_rainfall": (500, 850),
        "opt_temp": (22, 32),
        "opt_fertilizer": (30, 70),
        "opt_pesticide": (10, 25),
        "typical_yield_range": (20, 55),
        "irrigation_advice": "Flowering and peg penetration stages require adequate moisture; avoid water stress during pod development.",
        "nutrient_advice": "Apply Gypsum (200-400 kg/ha) at pegging to supply Calcium and Sulfur for robust pod filling.",
    },
}
