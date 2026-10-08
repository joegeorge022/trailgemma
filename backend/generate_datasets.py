"""
Generate realistic, ecologically grounded synthetic datasets for:
1. Microclimate Frost Date & Backyard Soil Prediction
2. Fall Foliage Peak Coloration & Trail Canopy Phenology
3. Trailhead Bird Bio-Acoustic Occurrence Likelihood
"""

import os
import numpy as np
import pandas as pd

np.random.seed(42)

def generate_frost_dataset(n_samples=180):
    elev = np.random.uniform(100, 950, n_samples)
    dist_water = np.random.uniform(0.1, 12.0, n_samples)
    slope_aspect = np.random.uniform(0, 360, n_samples) # South = 180 gets most solar radiation
    canopy = np.random.uniform(5, 85, n_samples)
    soil_moist = np.random.uniform(15, 60, n_samples)
    day_autumn = np.random.uniform(15, 65, n_samples) # days since Sept 1st
    
    # Physics-based environmental heuristic
    solar_mod = np.cos(np.radians(slope_aspect - 180)) * 2.0
    water_thermal_buffer = np.clip(3.0 - (dist_water * 0.35), 0, 3.5)
    elev_lapse = (elev / 100.0) * -0.65
    canopy_insulation = canopy * 0.04
    
    latent_night_temp = 14.0 - (day_autumn * 0.22) + elev_lapse + solar_mod + water_thermal_buffer + canopy_insulation + np.random.normal(0, 1.2, n_samples)
    
    frost_cat = []
    days_to_kill_frost = []
    
    for t, day in zip(latent_night_temp, day_autumn):
        if t <= 0.0:
            frost_cat.append(2) # Hard Freeze
            days = max(0, int(np.random.uniform(0, 3)))
        elif t <= 3.5:
            frost_cat.append(1) # Light Frost
            days = int(np.random.uniform(2, 8))
        else:
            frost_cat.append(0) # Safe
            days = int(np.random.uniform(9, 30))
        days_to_kill_frost.append(days)
        
    df = pd.DataFrame({
        'elevation_m': np.round(elev, 1),
        'dist_water_km': np.round(dist_water, 2),
        'slope_aspect_deg': np.round(slope_aspect, 1),
        'canopy_cover_pct': np.round(canopy, 1),
        'avg_night_temp_c': np.round(latent_night_temp, 1),
        'soil_moisture_pct': np.round(soil_moist, 1),
        'day_of_autumn': np.round(day_autumn, 0).astype(int),
        'frost_risk_cat': frost_cat,
        'days_until_frost': days_to_kill_frost
    })
    return df

def generate_foliage_dataset(n_samples=180):
    elev = np.random.uniform(150, 1100, n_samples)
    lat = np.random.uniform(41.0, 45.5, n_samples)
    sugar_maple = np.random.uniform(10, 60, n_samples)
    red_oak = np.random.uniform(5, 50, n_samples)
    aspen_birch = np.random.uniform(5, 40, n_samples)
    day_of_year = np.random.uniform(262, 302, n_samples) # Sept 19 to Oct 29
    
    # Chilling degrees accumulation
    chilling_hours = (day_of_year - 255) * 8.5 + (elev / 100.0) * 12.0 + (lat - 41.0) * 25.0 + np.random.normal(0, 15, n_samples)
    chilling_hours = np.clip(chilling_hours, 10, 450)
    
    # Phenology score: peak anthocyanin & carotenoid unmasking
    peak_score = (chilling_hours / 3.0) + (sugar_maple * 0.4) - np.abs(day_of_year - 282) * 2.5 + np.random.normal(0, 6, n_samples)
    peak_score = np.clip(peak_score, 5, 100)
    
    stages = []
    for s in peak_score:
        if s < 35:
            stages.append(0) # Early Green
        elif s < 65:
            stages.append(1) # Turning / Moderate Color
        elif s < 88:
            stages.append(2) # Peak Vibrant Foliage
        else:
            stages.append(3) # Past Peak / Golden Carpet
            
    df = pd.DataFrame({
        'elevation_m': np.round(elev, 1),
        'latitude': np.round(lat, 2),
        'sugar_maple_pct': np.round(sugar_maple, 1),
        'red_oak_pct': np.round(red_oak, 1),
        'aspen_birch_pct': np.round(aspen_birch, 1),
        'chilling_hours': np.round(chilling_hours, 1),
        'day_of_year': np.round(day_of_year, 0).astype(int),
        'foliage_stage': stages,
        'vibrancy_index': np.round(peak_score, 1)
    })
    return df

def generate_bird_dataset(n_samples=180):
    hour = np.random.uniform(5.5, 18.5, n_samples)
    canopy = np.random.uniform(15, 95, n_samples)
    elev = np.random.uniform(150, 1000, n_samples)
    temp = np.random.uniform(4, 24, n_samples)
    near_water = np.random.choice([0, 1], n_samples, p=[0.45, 0.55])
    
    # Species affinity:
    # 0 = Hermit Thrush (high elevation, deep canopy, dawn/dusk)
    # 1 = Black-capped Chickadee (ubiquitous, dense shrubs/canopy)
    # 2 = Red-tailed Hawk (midday, thermal soaring, open canopy)
    # 3 = Pileated Woodpecker (mature hardwood, morning, deep forest)
    # 4 = Belted Kingfisher / Waterfowl (near water)
    # 5 = White-throated Sparrow (cool autumn mornings, brushy edge)
    species = []
    for h, c, el, t, nw in zip(hour, canopy, elev, temp, near_water):
        if nw == 1 and np.random.rand() > 0.4:
            species.append(4) # Water affinity
        elif c < 35 and (10 <= h <= 15):
            species.append(2) # Hawk
        elif el > 600 and (h < 9 or h > 16):
            species.append(0) # Hermit Thrush
        elif c > 70 and h < 11:
            species.append(3) # Pileated Woodpecker
        elif t < 12 and h < 10:
            species.append(5) # White-throated Sparrow
        else:
            species.append(1) # Chickadee
            
    df = pd.DataFrame({
        'hour_of_day': np.round(hour, 1),
        'canopy_density_pct': np.round(canopy, 1),
        'elevation_m': np.round(elev, 1),
        'ambient_temp_c': np.round(temp, 1),
        'near_water': near_water,
        'species_id': species
    })
    return df

if __name__ == '__main__':
    data_dir = os.path.join(os.path.dirname(__file__), 'datasets')
    os.makedirs(data_dir, exist_ok=True)
    
    frost_df = generate_frost_dataset()
    frost_df.to_csv(os.path.join(data_dir, 'frost_microclimate_train.csv'), index=False)
    print(f"Saved frost_microclimate_train.csv ({len(frost_df)} rows)")
    
    foliage_df = generate_foliage_dataset()
    foliage_df.to_csv(os.path.join(data_dir, 'foliage_canopy_train.csv'), index=False)
    print(f"Saved foliage_canopy_train.csv ({len(foliage_df)} rows)")
    
    bird_df = generate_bird_dataset()
    bird_df.to_csv(os.path.join(data_dir, 'bird_acoustics_train.csv'), index=False)
    print(f"Saved bird_acoustics_train.csv ({len(bird_df)} rows)")
