"""
TrailGemma & FloraCast - Touch Grass Outdoor Companion Backend
FastAPI server unifying:
1. Google Gemma 2 (Local Open-Weight Naturalist)
2. Prior Labs TabPFN (Tabular Foundation Model for Microclimates & Phenology)
3. ElevenLabs (Hands-Free Field Audio Guide)
"""

import os
import sys
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("trailgemma")

# Add backend directory to path
sys.path.append(os.path.dirname(__file__))

from tabpfn_engine import TabPFNOutdoorEngine
from gemma_client import GemmaLocalClient
from elevenlabs_engine import ElevenLabsAudioEngine
from trails_data import CURATED_TRAILS, COMMUNITY_GARDEN_PRESETS

app = FastAPI(
    title="TrailGemma & FloraCast",
    description="Offline Open-Source AI Trail Companion & Microclimate Predictor",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines
tabpfn_engine = TabPFNOutdoorEngine()
gemma_client = GemmaLocalClient()
audio_engine = ElevenLabsAudioEngine()

# --- Request Models ---

class FrostQuery(BaseModel):
    elevation_m: float = 250.0
    dist_water_km: float = 3.5
    slope_aspect_deg: float = 180.0
    canopy_cover_pct: float = 25.0
    avg_night_temp_c: float = 3.5
    soil_moisture_pct: float = 35.0
    day_of_autumn: int = 38

class FoliageQuery(BaseModel):
    elevation_m: float = 580.0
    latitude: float = 44.27
    sugar_maple_pct: float = 60.0
    red_oak_pct: float = 25.0
    aspen_birch_pct: float = 15.0
    chilling_hours: float = 180.0
    day_of_year: int = 282 # Early to mid October

class BirdQuery(BaseModel):
    hour_of_day: float = 7.5
    canopy_density_pct: float = 65.0
    elevation_m: float = 580.0
    ambient_temp_c: float = 9.0
    near_water: int = 1

class BriefingRequest(BaseModel):
    trail_id: str
    hour_of_day: float = 8.0
    day_of_year: int = 282

class NaturalistQuestion(BaseModel):
    question: str
    trail_id: Optional[str] = None
    context: Optional[str] = ""

# --- API Endpoints ---

@app.get("/api/status")
async def get_system_status():
    gemma_health = await gemma_client.check_health()
    return {
        "status": "online",
        "theme": "Touch Grass (Hacktoberfest Open-Source AI Challenge)",
        "gemma": gemma_health,
        "tabpfn": {
            "engine": "TabPFN Tabular Foundation Model (Prior Labs)",
            "version": "9.1.0",
            "device": tabpfn_engine.device,
            "trained_synthetic_contexts": ["frost_microclimate", "foliage_canopy", "bird_acoustics"]
        },
        "elevenlabs": {
            "configured": audio_engine.is_configured(),
            "default_voice": audio_engine.default_voice_id,
            "fallback": "Native Web Speech API (Local on-device audio)"
        },
        "offline_ready": True
    }

@app.get("/api/trails")
async def get_trails():
    return CURATED_TRAILS

@app.get("/api/garden-presets")
async def get_garden_presets():
    return COMMUNITY_GARDEN_PRESETS

@app.post("/api/predict/frost")
async def predict_frost(query: FrostQuery):
    result = tabpfn_engine.predict_frost(
        elevation_m=query.elevation_m,
        dist_water_km=query.dist_water_km,
        slope_aspect_deg=query.slope_aspect_deg,
        canopy_cover_pct=query.canopy_cover_pct,
        avg_night_temp_c=query.avg_night_temp_c,
        soil_moisture_pct=query.soil_moisture_pct,
        day_of_autumn=query.day_of_autumn
    )
    return result

@app.post("/api/predict/foliage")
async def predict_foliage(query: FoliageQuery):
    result = tabpfn_engine.predict_foliage(
        elevation_m=query.elevation_m,
        latitude=query.latitude,
        sugar_maple_pct=query.sugar_maple_pct,
        red_oak_pct=query.red_oak_pct,
        aspen_birch_pct=query.aspen_birch_pct,
        chilling_hours=query.chilling_hours,
        day_of_year=query.day_of_year
    )
    return result

@app.post("/api/predict/birds")
async def predict_birds(query: BirdQuery):
    result = tabpfn_engine.predict_birds(
        hour_of_day=query.hour_of_day,
        canopy_density_pct=query.canopy_density_pct,
        elevation_m=query.elevation_m,
        ambient_temp_c=query.ambient_temp_c,
        near_water=query.near_water
    )
    return result

@app.post("/api/briefing/generate")
async def generate_briefing(req: BriefingRequest):
    # Find trail
    trail = next((t for t in CURATED_TRAILS if t["id"] == req.trail_id), None)
    if not trail:
        raise HTTPException(status_code=404, detail="Trail not found")

    # 1. Run TabPFN Foliage prediction for trail
    foliage_res = tabpfn_engine.predict_foliage(
        elevation_m=trail["avg_elevation_m"],
        latitude=trail["lat"],
        sugar_maple_pct=trail["canopy_composition"]["sugar_maple"],
        red_oak_pct=trail["canopy_composition"]["red_oak"],
        aspen_birch_pct=trail["canopy_composition"]["aspen_birch"],
        chilling_hours=trail["chilling_hours_est"],
        day_of_year=req.day_of_year
    )

    # 2. Run TabPFN Bird occurrence prediction
    bird_res = tabpfn_engine.predict_birds(
        hour_of_day=req.hour_of_day,
        canopy_density_pct=75.0,
        elevation_m=trail["avg_elevation_m"],
        ambient_temp_c=8.5,
        near_water=1 if "cascade" in req.trail_id or "river" in req.trail_id else 0
    )

    # 3. Run TabPFN Frost prediction for trailhead microclimate
    frost_res = tabpfn_engine.predict_frost(
        elevation_m=trail["avg_elevation_m"],
        dist_water_km=1.5,
        slope_aspect_deg=170,
        canopy_cover_pct=60,
        avg_night_temp_c=2.8,
        soil_moisture_pct=42,
        day_of_autumn=req.day_of_year - 244 # approx days since Sept 1
    )

    # 4. Synthesize natural briefing script with Google Gemma 2
    script_text = await gemma_client.generate_trail_audio_script(
        trail_name=trail["name"],
        foliage_data=foliage_res,
        bird_data=bird_res,
        frost_data=frost_res
    )

    # 5. Synthesize audio with ElevenLabs (or fallback to local audio TTS)
    audio_res = await audio_engine.generate_speech(script_text)

    return {
        "trail": trail,
        "script": script_text,
        "audio": audio_res,
        "tabpfn_foliage": foliage_res,
        "tabpfn_birds": bird_res,
        "tabpfn_frost": frost_res
    }

@app.post("/api/naturalist/ask")
async def ask_naturalist(req: NaturalistQuestion):
    context = req.context
    if req.trail_id:
        trail = next((t for t in CURATED_TRAILS if t["id"] == req.trail_id), None)
        if trail:
            context += f" Trail: {trail['name']}, Elevation: {trail['avg_elevation_m']}m, Flora: {[f['name'] for f in trail.get('native_flora_markers', [])]}."

    response = await gemma_client.ask_field_naturalist(req.question, context)
    return {
        "model": "Gemma 2 (2B Open-Weight)",
        "question": req.question,
        "answer": response
    }

# Mount static frontend
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
