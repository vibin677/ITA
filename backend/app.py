import io
import json
import os
from pathlib import Path
from typing import Optional, List

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, File, UploadFile, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from ml import config

app = FastAPI(
    title='AgroPredict — Crop Production & Yield AI Platform',
    description='Intelligent Crop Yield & Production Forecasting Engine using Machine Learning',
    version='2.0.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Mount static files and templates
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / 'frontend' / 'static'
TEMPLATES_DIR = BASE_DIR / 'frontend' / 'templates'

if STATIC_DIR.exists():
    app.mount('/static', StaticFiles(directory=str(STATIC_DIR)), name='static')

# Cache model and metadata in memory
_model_bundle = None
_metadata = None
_stats = None
_presets = None
_df_cache = None

def get_model_bundle():
    global _model_bundle
    if _model_bundle is None:
        if not config.MODEL_PATH.exists():
            from ml.model_trainer import train_and_evaluate
            train_and_evaluate()
        _model_bundle = joblib.load(config.MODEL_PATH)
    return _model_bundle

def get_metadata():
    global _metadata
    if _metadata is None:
        if config.METRICS_PATH.exists():
            with open(config.METRICS_PATH, 'r', encoding='utf-8') as f:
                _metadata = json.load(f)
        else:
            _metadata = {}
    return _metadata

def get_stats():
    global _stats
    if _stats is None:
        if config.STATS_PATH.exists():
            with open(config.STATS_PATH, 'r', encoding='utf-8') as f:
                _stats = json.load(f)
        else:
            _stats = {}
    return _stats

def get_presets():
    global _presets
    if _presets is None:
        if config.PRESETS_PATH.exists():
            with open(config.PRESETS_PATH, 'r', encoding='utf-8') as f:
                _presets = json.load(f)
        else:
            _presets = []
    return _presets

def get_dataframe():
    global _df_cache
    if _df_cache is None:
        if config.DATA_PATH.exists():
            _df_cache = pd.read_csv(config.DATA_PATH)
        else:
            _df_cache = pd.DataFrame()
    return _df_cache


# Pydantic Schemas
class PredictionRequest(BaseModel):
    crop: str = Field(..., json_schema_extra={'example': 'Wheat'})
    state: str = Field(..., json_schema_extra={'example': 'Punjab'})
    season: str = Field(..., json_schema_extra={'example': 'Rabi'})
    area: float = Field(..., ge=1.0, description='Cultivated area in hectares', json_schema_extra={'example': 1200.0})
    rainfall: float = Field(..., ge=0.0, description='Annual/seasonal rainfall in mm', json_schema_extra={'example': 650.0})
    temperature: float = Field(..., description='Average temperature in Celsius', json_schema_extra={'example': 20.5})
    fertilizer: float = Field(..., ge=0.0, description='Fertilizer usage in kg/ha', json_schema_extra={'example': 120.0})
    pesticide: float = Field(..., ge=0.0, description='Pesticide usage in kg/ha', json_schema_extra={'example': 15.0})

class SensitivityRequest(BaseModel):
    base_request: PredictionRequest
    parameter: str = Field(..., description='Parameter to vary: rainfall, fertilizer, or temperature', json_schema_extra={'example': 'rainfall'})


def generate_agronomic_advisory(req: PredictionRequest, yield_val: float):
    crop = req.crop
    profiles = config.AGRONOMIC_PROFILES
    profile = profiles.get(crop, {
        'opt_rainfall': (600, 1200),
        'opt_temp': (18, 32),
        'opt_fertilizer': (70, 140),
        'opt_pesticide': (10, 35),
        'typical_yield_range': (25, 75),
        'irrigation_advice': 'Maintain regular soil moisture monitoring and avoid stress during flowering stage.',
        'nutrient_advice': 'Follow standard soil health card recommendations for balanced NPK.'
    })

    # Rainfall assessment
    r_min, r_max = profile['opt_rainfall']
    if req.rainfall < r_min:
        r_status = 'Deficient Moisture'
        r_note = f'{round(r_min - req.rainfall, 1)} mm below optimum. Supplementary irrigation recommended.'
    elif req.rainfall > r_max:
        r_status = 'Excess Precipitation'
        r_note = f'{round(req.rainfall - r_max, 1)} mm above optimum. Ensure surface drainage to prevent waterlogging.'
    else:
        r_status = 'Optimal Moisture'
        r_note = 'Rainfall is within the ideal growth envelope.'

    # Temperature assessment
    t_min, t_max = profile['opt_temp']
    if req.temperature < t_min:
        t_status = 'Cool / Sub-optimal'
        t_note = f'Temperature is {round(t_min - req.temperature, 1)}°C below standard germination/grain filling range.'
    elif req.temperature > t_max:
        t_status = 'Heat Stress Risk'
        t_note = f'Temperature is {round(req.temperature - t_max, 1)}°C above optimal threshold. May cause early senescence.'
    else:
        t_status = 'Ideal Thermal Zone'
        t_note = 'Thermal conditions support peak photosynthetic efficiency.'

    # Fertilizer assessment
    f_min, f_max = profile['opt_fertilizer']
    if req.fertilizer < f_min:
        f_status = 'Sub-optimal Nutrition'
        f_note = f'Fertilizer rate is {round(f_min - req.fertilizer, 1)} kg/ha lower than recommended dosage.'
    elif req.fertilizer > f_max:
        f_status = 'Elevated Nutrient Level'
        f_note = f'Fertilizer rate exceeds {f_max} kg/ha. Avoid excessive urea to prevent lodging and groundwater leaching.'
    else:
        f_status = 'Balanced Nutrition'
        f_note = 'Fertilizer rate aligns well with standard agronomic nutrient management.'

    # Pesticide assessment
    p_min, p_max = profile['opt_pesticide']
    if req.pesticide > p_max:
        p_status = 'High Chemical Intensity'
        p_note = 'Pesticide load is elevated. Transition towards Integrated Pest Management (IPM) and biocontrol agents.'
    else:
        p_status = 'Moderate / Controlled'
        p_note = 'Pesticide dosage is within sustainable crop protection limits.'

    # Yield category
    y_min, y_max = profile['typical_yield_range']
    if yield_val >= y_max * 0.9:
        category = 'Outstanding (Bumper Yield)'
        category_badge = 'emerald'
    elif yield_val >= (y_min + y_max) / 2:
        category = 'Above Average'
        category_badge = 'blue'
    elif yield_val >= y_min:
        category = 'Moderate Yield'
        category_badge = 'amber'
    else:
        category = 'Sub-optimal / Vulnerable'
        category_badge = 'rose'

    recommendations = [
        profile.get('irrigation_advice', 'Adopt drip or sprinkler irrigation to maximize water use efficiency.'),
        profile.get('nutrient_advice', 'Conduct pre-season soil testing to calibrate Nitrogen, Phosphorus, and Potassium.'),
        r_note,
        f_note
    ]

    return {
        'category': category,
        'category_badge': category_badge,
        'rainfall_eval': {'status': r_status, 'note': r_note},
        'temperature_eval': {'status': t_status, 'note': t_note},
        'fertilizer_eval': {'status': f_status, 'note': f_note},
        'pesticide_eval': {'status': p_status, 'note': p_note},
        'recommendations': recommendations
    }


def compute_economics(crop: str, total_tonnes: float, area_ha: float, fertilizer_kg_ha: float, pesticide_kg_ha: float):
    rate_inr = config.CROP_PRICES_INR.get(crop, 22000)
    gross_revenue_inr = round(total_tonnes * rate_inr, 2)
    gross_revenue_usd = round(gross_revenue_inr / config.USD_INR_RATE, 2)

    # Approximated production cost per hectare
    fert_cost = fertilizer_kg_ha * 24.0  # ~Rs. 24/kg subsidized average
    pest_cost = pesticide_kg_ha * 450.0  # ~Rs. 450/kg pesticide cost
    base_operational_cost_ha = 22000.0   # Land prep, seeds, labor, machinery
    cost_per_ha = base_operational_cost_ha + fert_cost + pest_cost
    total_cost_inr = round(cost_per_ha * area_ha, 2)
    total_cost_usd = round(total_cost_inr / config.USD_INR_RATE, 2)

    net_profit_inr = round(gross_revenue_inr - total_cost_inr, 2)
    net_profit_usd = round(net_profit_inr / config.USD_INR_RATE, 2)
    roi_pct = round((net_profit_inr / max(1.0, total_cost_inr)) * 100, 1)

    return {
        'msp_rate_per_tonne_inr': rate_inr,
        'msp_rate_per_tonne_usd': round(rate_inr / config.USD_INR_RATE, 2),
        'gross_revenue_inr': gross_revenue_inr,
        'gross_revenue_usd': gross_revenue_usd,
        'total_cost_inr': total_cost_inr,
        'total_cost_usd': total_cost_usd,
        'net_profit_inr': net_profit_inr,
        'net_profit_usd': net_profit_usd,
        'roi_percentage': roi_pct
    }


@app.get('/', response_class=HTMLResponse)
def index_page():
    index_file = TEMPLATES_DIR / 'index.html'
    if not index_file.exists():
        return HTMLResponse('<h2>AgroPredict frontend is initializing... please check back shortly.</h2>')
    with open(index_file, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())


@app.get('/api/health')
def health_check():
    bundle = get_model_bundle()
    stats = get_stats()
    return {
        'status': 'healthy',
        'model_name': bundle.get('model_name', 'Unknown'),
        'total_dataset_records': stats.get('total_records', 0),
        'champion_r2': bundle.get('metrics', {}).get('r2', None)
    }


@app.get('/api/presets')
def fetch_presets():
    return get_presets()


@app.get('/api/models/comparison')
def fetch_model_comparison():
    return get_metadata()


@app.get('/api/dataset/stats')
def fetch_dataset_stats():
    return get_stats()


@app.get('/api/dataset/records')
def fetch_dataset_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(15, ge=5, le=100),
    crop: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    df = get_dataframe()
    if df.empty:
        return {'total': 0, 'page': page, 'page_size': page_size, 'records': []}

    filtered = df.copy()
    if crop:
        filtered = filtered[filtered['Crop'].str.lower() == crop.lower()]
    if state:
        filtered = filtered[filtered['State'].str.lower() == state.lower()]
    if search:
        s = search.lower()
        filtered = filtered[
            filtered['Crop'].str.lower().str.contains(s) |
            filtered['State'].str.lower().str.contains(s) |
            filtered['Season'].str.lower().str.contains(s)
        ]

    total = len(filtered)
    start = (page - 1) * page_size
    end = start + page_size
    records = filtered.iloc[start:end].to_dict(orient='records')

    return {
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': max(1, int(np.ceil(total / page_size))),
        'records': records
    }


@app.post('/api/predict')
def predict_crop_yield(req: PredictionRequest):
    bundle = get_model_bundle()
    model = bundle['model']
    preprocessor = bundle['preprocessor']

    row_data = {
        'Area': [req.area],
        'Rainfall': [req.rainfall],
        'Temperature': [req.temperature],
        'Fertilizer': [req.fertilizer],
        'Pesticide': [req.pesticide],
        'State': [req.state],
        'Crop': [req.crop],
        'Season': [req.season]
    }
    input_df = pd.DataFrame(row_data)

    try:
        X_trans = preprocessor.transform(input_df)
        pred_yield = float(model.predict(X_trans)[0])
        pred_yield = max(1.0, round(pred_yield, 2))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Prediction failed: {str(e)}')

    total_production = round(pred_yield * req.area, 2)
    advisory = generate_agronomic_advisory(req, pred_yield)
    economics = compute_economics(req.crop, total_production, req.area, req.fertilizer, req.pesticide)

    # Suitability index score (0 - 100)
    soil_score = min(100, max(20, int(70 + (req.fertilizer / 200.0) * 30)))
    moisture_score = min(100, max(30, int(100 - abs(req.rainfall - 1000) * 0.05)))
    temp_score = min(100, max(25, int(100 - abs(req.temperature - 25) * 4)))
    protection_score = min(100, max(30, int(85 - (req.pesticide / 60.0) * 20)))
    overall_suitability = int(np.mean([soil_score, moisture_score, temp_score, protection_score]))

    return {
        'crop': req.crop,
        'state': req.state,
        'season': req.season,
        'area_hectares': req.area,
        'predicted_yield_tonnes_per_ha': pred_yield,
        'total_production_tonnes': total_production,
        'model_used': bundle.get('model_name', 'Gradient Boosting'),
        'model_r2': bundle.get('metrics', {}).get('r2', 0.81),
        'suitability_score': overall_suitability,
        'radar_metrics': {
            'Soil Nutrition': soil_score,
            'Moisture Level': moisture_score,
            'Thermal Fit': temp_score,
            'Protection Balance': protection_score,
            'Overall Index': overall_suitability
        },
        'advisory': advisory,
        'economics': economics
    }


@app.post('/api/predict/sensitivity')
def analyze_sensitivity(req: SensitivityRequest):
    bundle = get_model_bundle()
    model = bundle['model']
    preprocessor = bundle['preprocessor']

    base = req.base_request
    param = req.parameter.lower()

    if param not in ['rainfall', 'fertilizer', 'temperature']:
        raise HTTPException(status_code=400, detail='Parameter must be rainfall, fertilizer, or temperature')

    percentages = [-30, -20, -10, 0, 10, 20, 30]
    data_points = []

    base_val = getattr(base, param)

    for pct in percentages:
        val = max(1.0, round(base_val * (1.0 + pct / 100.0), 2))
        
        row_dict = {
            'Area': [base.area],
            'Rainfall': [val if param == 'rainfall' else base.rainfall],
            'Temperature': [val if param == 'temperature' else base.temperature],
            'Fertilizer': [val if param == 'fertilizer' else base.fertilizer],
            'Pesticide': [base.pesticide],
            'State': [base.state],
            'Crop': [base.crop],
            'Season': [base.season]
        }
        df_step = pd.DataFrame(row_dict)
        X_trans = preprocessor.transform(df_step)
        pred = max(1.0, round(float(model.predict(X_trans)[0]), 2))
        prod = round(pred * base.area, 2)

        data_points.append({
            'delta_pct': f'{"+" if pct > 0 else ""}{pct}%',
            'value': val,
            'predicted_yield': pred,
            'total_production': prod
        })

    return {
        'parameter': param,
        'base_value': base_val,
        'crop': base.crop,
        'curve': data_points
    }


@app.post('/api/predict/batch')
async def batch_predict(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail='Only CSV files are supported for batch prediction.')

    content = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Invalid CSV format: {str(e)}')

    req_cols = ['Area', 'Rainfall', 'Temperature', 'Fertilizer', 'Pesticide', 'State', 'Crop', 'Season']
    missing = [c for c in req_cols if c not in df.columns]
    if missing:
        raise HTTPException(status_code=400, detail=f'Missing required columns in CSV: {missing}')

    bundle = get_model_bundle()
    model = bundle['model']
    preprocessor = bundle['preprocessor']

    X_trans = preprocessor.transform(df[req_cols])
    preds = model.predict(X_trans)
    df['Predicted_Yield_Tonnes_Ha'] = [max(1.0, round(float(p), 2)) for p in preds]
    df['Total_Production_Tonnes'] = (df['Predicted_Yield_Tonnes_Ha'] * df['Area']).round(2)

    # Return summary + records
    records = df.head(100).to_dict(orient='records')
    avg_yield = round(float(df['Predicted_Yield_Tonnes_Ha'].mean()), 2)
    total_prod = round(float(df['Total_Production_Tonnes'].sum()), 2)

    # Generate downloadable CSV string
    output_stream = io.StringIO()
    df.to_csv(output_stream, index=False)
    csv_str = output_stream.getvalue()

    return {
        'total_rows_processed': len(df),
        'preview_rows': records,
        'summary': {
            'average_predicted_yield_tonnes_ha': avg_yield,
            'total_batch_production_tonnes': total_prod
        },
        'csv_data': csv_str
    }
