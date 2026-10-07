import json
import os
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

from ml import config

def train_and_evaluate():
    print(f'Reading dataset from {config.DATA_PATH}...')
    df = pd.read_csv(config.DATA_PATH)
    print(f'Total records loaded: {len(df)}')

    # Clean missing values
    df = df.dropna(subset=[config.TARGET_COLUMN])
    df[config.TARGET_COLUMN] = df[config.TARGET_COLUMN].clip(lower=1.0)

    X = df[config.NUMERICAL_COLUMNS + config.CATEGORICAL_COLUMNS]
    y = df[config.TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, config.NUMERICAL_COLUMNS),
            ('cat', categorical_transformer, config.CATEGORICAL_COLUMNS)
        ]
    )

    print('Fitting preprocessor on training data...')
    X_train_trans = preprocessor.fit_transform(X_train)
    X_test_trans = preprocessor.transform(X_test)

    # Get transformed feature names for explainability
    cat_encoder = preprocessor.named_transformers_['cat'].named_steps['onehot']
    cat_feature_names = list(cat_encoder.get_feature_names_out(config.CATEGORICAL_COLUMNS))
    all_feature_names = config.NUMERICAL_COLUMNS + cat_feature_names

    models = {
        'Random Forest': RandomForestRegressor(n_estimators=150, max_depth=12, random_state=42, n_jobs=-1),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=150, max_depth=5, learning_rate=0.08, random_state=42),
        'Decision Tree': DecisionTreeRegressor(max_depth=8, random_state=42),
        'Ridge Regression': Ridge(alpha=1.0),
        'Linear Regression': LinearRegression()
    }

    comparison = []
    fitted_models = {}

    for name, model in models.items():
        print(f'Training {name}...')
        model.fit(X_train_trans, y_train)
        y_pred = model.predict(X_test_trans)
        
        r2 = float(r2_score(y_test, y_pred))
        rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
        mae = float(mean_absolute_error(y_test, y_pred))
        
        # 3-fold cross validation for reliability score
        cv_scores = cross_val_score(model, X_train_trans, y_train, cv=3, scoring='r2')
        cv_mean = float(np.mean(cv_scores))

        comparison.append({
            'name': name,
            'r2': round(r2, 4),
            'rmse': round(rmse, 3),
            'mae': round(mae, 3),
            'cv_r2': round(cv_mean, 4)
        })
        fitted_models[name] = model

    comparison.sort(key=lambda x: x['r2'], reverse=True)
    best_name = comparison[0]['name']
    best_model = fitted_models[best_name]

    print('\n' + '='*55)
    print('MODEL COMPARISON LEADERBOARD')
    for res in comparison:
        print(f"{res['name']:<20} | R2: {res['r2']:.4f} | RMSE: {res['rmse']:<6.2f} | MAE: {res['mae']:<6.2f} | CV-R2: {res['cv_r2']:.4f}")
    print('='*55)
    print(f'Champion Model Selected: {best_name}')

    # Calculate Feature Importances for explainability
    importances = []
    if hasattr(best_model, 'feature_importances_'):
        raw_imp = best_model.feature_importances_
        for feat, val in zip(all_feature_names, raw_imp):
            importances.append({'feature': feat, 'importance': round(float(val), 4)})
        importances.sort(key=lambda x: x['importance'], reverse=True)
    elif hasattr(best_model, 'coef_'):
        raw_imp = np.abs(best_model.coef_)
        total = np.sum(raw_imp) + 1e-6
        for feat, val in zip(all_feature_names, raw_imp / total):
            importances.append({'feature': feat, 'importance': round(float(val), 4)})
        importances.sort(key=lambda x: x['importance'], reverse=True)

    # Calculate Top Predictors aggregated by core features
    core_importance = {}
    for item in importances:
        feat = item['feature']
        core_name = feat.split('_')[0]
        core_importance[core_name] = core_importance.get(core_name, 0.0) + item['importance']
    
    aggregated_importances = [
        {'feature': k, 'importance': round(v, 4)} 
        for k, v in sorted(core_importance.items(), key=lambda x: x[1], reverse=True)
    ]

    # Save artifacts
    config.ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    
    bundle = {
        'model': best_model,
        'preprocessor': preprocessor,
        'model_name': best_name,
        'feature_names': all_feature_names,
        'metrics': comparison[0]
    }
    joblib.dump(bundle, config.MODEL_PATH)
    print(f'Model bundle saved to: {config.MODEL_PATH}')

    # Save Model Comparison & Explanations JSON
    unique_crops = sorted(df['Crop'].unique().tolist())
    unique_states = sorted(df['State'].unique().tolist())
    unique_seasons = sorted(df['Season'].unique().tolist())

    numerical_ranges = {}
    for col in config.NUMERICAL_COLUMNS:
        numerical_ranges[col] = {
            'min': float(df[col].min()),
            'max': float(df[col].max()),
            'mean': round(float(df[col].mean()), 2),
            'median': round(float(df[col].median()), 2)
        }

    comparison_payload = {
        'best_model': comparison[0],
        'models': comparison,
        'feature_importances': aggregated_importances,
        'detailed_importances': importances[:12],
        'crops': unique_crops,
        'states': unique_states,
        'seasons': unique_seasons,
        'ranges': numerical_ranges,
        'agronomic_profiles': config.AGRONOMIC_PROFILES,
        'crop_prices_inr': config.CROP_PRICES_INR,
        'usd_inr_rate': config.USD_INR_RATE
    }

    with open(config.METRICS_PATH, 'w', encoding='utf-8') as f:
        json.dump(comparison_payload, f, indent=2)

    # Compute Dataset Statistics
    avg_yield_by_crop = df.groupby('Crop')['Yield'].mean().round(2).to_dict()
    avg_yield_by_state = df.groupby('State')['Yield'].mean().round(2).to_dict()
    crop_counts = df['Crop'].value_counts().to_dict()
    state_counts = df['State'].value_counts().to_dict()
    season_counts = df['Season'].value_counts().to_dict()

    dataset_stats = {
        'total_records': len(df),
        'avg_yield': round(float(df['Yield'].mean()), 2),
        'max_yield': round(float(df['Yield'].max()), 2),
        'min_yield': round(float(df['Yield'].min()), 2),
        'avg_rainfall': round(float(df['Rainfall'].mean()), 1),
        'avg_fertilizer': round(float(df['Fertilizer'].mean()), 1),
        'avg_yield_by_crop': avg_yield_by_crop,
        'avg_yield_by_state': avg_yield_by_state,
        'crop_counts': crop_counts,
        'state_counts': state_counts,
        'season_counts': season_counts
    }

    with open(config.STATS_PATH, 'w', encoding='utf-8') as f:
        json.dump(dataset_stats, f, indent=2)

    # Save Presets
    presets = [
        {
            'id': 'punjab_wheat',
            'title': 'Punjab Wheat Belt (Rabi)',
            'desc': 'High-yield irrigated fertile plains with optimal nitrogen & winter temp.',
            'crop': 'Wheat',
            'state': 'Punjab',
            'season': 'Rabi',
            'area': 1850.0,
            'rainfall': 680.0,
            'temperature': 18.5,
            'fertilizer': 135.0,
            'pesticide': 18.0
        },
        {
            'id': 'maharashtra_cotton',
            'title': 'Maharashtra Black Soil (Cotton)',
            'desc': 'Major Kharif commercial cash-crop with moderate rainfall & warm climate.',
            'crop': 'Cotton',
            'state': 'Maharashtra',
            'season': 'Kharif',
            'area': 2400.0,
            'rainfall': 880.0,
            'temperature': 29.5,
            'fertilizer': 110.0,
            'pesticide': 38.0
        },
        {
            'id': 'up_sugarcane',
            'title': 'Uttar Pradesh Cane Basin (Annual)',
            'desc': 'Heavy biomass cash crop demanding high nutrient dosage and water.',
            'crop': 'Sugarcane',
            'state': 'Uttar Pradesh',
            'season': 'Whole Year',
            'area': 2100.0,
            'rainfall': 1180.0,
            'temperature': 28.0,
            'fertilizer': 165.0,
            'pesticide': 28.0
        },
        {
            'id': 'tn_paddy',
            'title': 'Tamil Nadu Cauvery Delta (Rice)',
            'desc': 'High rainfall tropical paddy cultivation with intensive management.',
            'crop': 'Rice',
            'state': 'Tamil Nadu',
            'season': 'Kharif',
            'area': 1600.0,
            'rainfall': 1250.0,
            'temperature': 30.0,
            'fertilizer': 125.0,
            'pesticide': 24.0
        },
        {
            'id': 'kerala_monsoon',
            'title': 'Kerala Coastal Strip (Rice)',
            'desc': 'Heavy monsoon precipitation, humid coastal temperature, organic rich soils.',
            'crop': 'Rice',
            'state': 'Kerala',
            'season': 'Kharif',
            'area': 950.0,
            'rainfall': 1650.0,
            'temperature': 28.5,
            'fertilizer': 105.0,
            'pesticide': 20.0
        }
    ]

    with open(config.PRESETS_PATH, 'w', encoding='utf-8') as f:
        json.dump(presets, f, indent=2)

    print('Training and artifact generation completed successfully!')

if __name__ == '__main__':
    train_and_evaluate()
