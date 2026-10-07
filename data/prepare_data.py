import csv
import random
import os
from pathlib import Path

random.seed(42)

input_sample = r'C:\Users\mcr57\Downloads\crop_yield_prediction\crop_yield_prediction\data\sample_crop_yield.csv'
output_path = Path(__file__).resolve().parent / 'crop_yield.csv'

rows = []
if os.path.exists(input_sample):
    with open(input_sample, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                area = float(r['Area'])
                rainfall = float(r['Rainfall'])
                temp = float(r['Temperature'])
                fert = float(r['Fertilizer'])
                pest = float(r['Pesticide'])
                state = r['State'].strip()
                crop = r['Crop'].strip()
                season = r['Season'].strip()
                y = float(r['Yield'])
                # Fix negative or unrealistic yield values
                if y <= 0:
                    base_yields = {'Sugarcane': 65.0, 'Rice': 42.0, 'Wheat': 55.0, 'Cotton': 28.0}
                    y = base_yields.get(crop, 35.0) + random.uniform(-10, 15)
                rows.append({
                    'Area': round(area, 2),
                    'Rainfall': round(rainfall, 2),
                    'Temperature': round(temp, 2),
                    'Fertilizer': round(fert, 2),
                    'Pesticide': round(pest, 2),
                    'State': state,
                    'Crop': crop,
                    'Season': season,
                    'Yield': round(y, 2)
                })
            except Exception:
                continue

# Add enriched realistic records across major Indian agricultural zones
states_crops_seasons = [
    ('Punjab', 'Wheat', 'Rabi', (800, 3500), (550, 850), (14, 24), (110, 165), (10, 25), (60, 98)),
    ('Punjab', 'Rice', 'Kharif', (900, 4200), (700, 1100), (28, 36), (120, 175), (20, 40), (55, 88)),
    ('Punjab', 'Cotton', 'Kharif', (700, 2800), (600, 950), (28, 38), (85, 140), (25, 48), (25, 55)),
    ('Haryana', 'Wheat', 'Rabi', (750, 3200), (500, 800), (15, 25), (105, 160), (12, 26), (58, 92)),
    ('Haryana', 'Rice', 'Kharif', (800, 3600), (650, 1050), (27, 35), (115, 165), (18, 38), (50, 82)),
    ('Uttar Pradesh', 'Sugarcane', 'Whole Year', (1200, 4800), (950, 1400), (24, 36), (130, 195), (15, 38), (70, 115)),
    ('Uttar Pradesh', 'Wheat', 'Rabi', (900, 4000), (600, 950), (16, 26), (100, 150), (10, 24), (52, 85)),
    ('Uttar Pradesh', 'Potatoes', 'Rabi', (400, 2200), (450, 750), (15, 23), (120, 185), (20, 45), (65, 105)),
    ('Maharashtra', 'Cotton', 'Kharif', (1100, 4500), (650, 1150), (26, 35), (80, 135), (28, 52), (20, 52)),
    ('Maharashtra', 'Sugarcane', 'Whole Year', (1000, 4000), (800, 1300), (25, 37), (125, 190), (18, 42), (68, 110)),
    ('Maharashtra', 'Soybean', 'Kharif', (800, 3200), (700, 1200), (25, 33), (50, 95), (12, 28), (28, 58)),
    ('Gujarat', 'Cotton', 'Kharif', (1000, 4200), (600, 1050), (27, 37), (85, 140), (26, 50), (22, 58)),
    ('Gujarat', 'Groundnut', 'Kharif', (600, 2900), (550, 950), (26, 34), (45, 80), (10, 26), (28, 54)),
    ('Tamil Nadu', 'Rice', 'Kharif', (600, 3800), (900, 1450), (26, 34), (95, 155), (15, 35), (48, 85)),
    ('Tamil Nadu', 'Rice', 'Rabi', (600, 3500), (850, 1350), (24, 31), (90, 145), (14, 32), (52, 89)),
    ('Tamil Nadu', 'Sugarcane', 'Whole Year', (800, 3500), (950, 1500), (27, 36), (120, 185), (16, 38), (72, 118)),
    ('Kerala', 'Rice', 'Kharif', (400, 2400), (1200, 2200), (25, 32), (75, 125), (12, 30), (40, 75)),
    ('Kerala', 'Rice', 'Rabi', (400, 2200), (1100, 1800), (25, 31), (75, 120), (12, 28), (42, 78)),
    ('Kerala', 'Sugarcane', 'Whole Year', (500, 2800), (1300, 2400), (26, 34), (110, 175), (15, 35), (65, 105)),
    ('Andhra Pradesh', 'Rice', 'Kharif', (800, 3800), (850, 1350), (26, 35), (100, 160), (18, 38), (52, 88)),
    ('Andhra Pradesh', 'Cotton', 'Kharif', (900, 3600), (700, 1150), (27, 36), (85, 140), (25, 48), (22, 54)),
    ('Madhya Pradesh', 'Soybean', 'Kharif', (900, 4200), (750, 1250), (25, 34), (45, 90), (10, 25), (26, 56)),
    ('Madhya Pradesh', 'Wheat', 'Rabi', (900, 4000), (500, 850), (15, 26), (95, 145), (10, 22), (50, 82)),
    ('Karnataka', 'Maize', 'Kharif', (600, 3100), (600, 1050), (22, 32), (85, 145), (12, 30), (38, 76)),
    ('Karnataka', 'Sugarcane', 'Whole Year', (700, 3400), (850, 1400), (24, 35), (115, 180), (15, 38), (68, 112)),
    ('Bihar', 'Rice', 'Kharif', (700, 3600), (950, 1450), (26, 34), (90, 145), (14, 32), (44, 76)),
    ('Bihar', 'Maize', 'Rabi', (500, 2800), (500, 850), (16, 26), (90, 150), (12, 28), (42, 80)),
    ('West Bengal', 'Rice', 'Kharif', (800, 4000), (1100, 1850), (26, 33), (95, 150), (15, 34), (48, 82)),
    ('West Bengal', 'Potatoes', 'Rabi', (400, 2500), (450, 800), (16, 24), (115, 175), (18, 42), (68, 108)),
]

for item in states_crops_seasons:
    st_name, cr_name, sn_name, a_rng, r_rng, t_rng, f_rng, p_rng, y_rng = item
    count = 45  # 45 records per combination = ~1,300 additional records
    for _ in range(count):
        a = random.uniform(*a_rng)
        r_val = random.uniform(*r_rng)
        t_val = random.uniform(*t_rng)
        f_val = random.uniform(*f_rng)
        p_val = random.uniform(*p_rng)
        
        # Calculate yield based on agronomic relationship with subtle noise
        base = (y_rng[0] + y_rng[1]) / 2.0
        # Positive impact of optimal fertilizer and rainfall
        fert_factor = (f_val - f_rng[0]) / (f_rng[1] - f_rng[0] + 1e-5)
        rain_factor = (r_val - r_rng[0]) / (r_rng[1] - r_rng[0] + 1e-5)
        noise = random.gauss(0, (y_rng[1] - y_rng[0]) * 0.08)
        
        sim_yield = y_rng[0] + (fert_factor * 0.45 + rain_factor * 0.35) * (y_rng[1] - y_rng[0]) + noise
        sim_yield = max(5.0, min(140.0, sim_yield))
        
        rows.append({
            'Area': round(a, 2),
            'Rainfall': round(r_val, 2),
            'Temperature': round(t_val, 2),
            'Fertilizer': round(f_val, 2),
            'Pesticide': round(p_val, 2),
            'State': st_name,
            'Crop': cr_name,
            'Season': sn_name,
            'Yield': round(sim_yield, 2)
        })

fieldnames = ['Area', 'Rainfall', 'Temperature', 'Fertilizer', 'Pesticide', 'State', 'Crop', 'Season', 'Yield']
with open(output_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f'Successfully prepared dataset with {len(rows)} records at {output_path}')
