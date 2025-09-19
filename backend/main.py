from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path
from typing import List, Dict, Any

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path("data")

def load_json_data(filename: str) -> Any:
    """Load JSON data from file"""
    file_path = DATA_DIR / filename
    if file_path.exists():
        with open(file_path, 'r') as file:
            return json.load(file)
    return {"error": "Data file not found"}

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI backend!"}

@app.get("/")
async def root():
    return {"message": "Dashboard API is running"}

@app.get("/dashboard/summary")
async def get_dashboard_summary():
    """Get dashboard summary data"""
    return load_json_data("dashboard_summary.json")

@app.get("/units")
async def get_units():
    """Get all units"""
    return load_json_data("units.json")

@app.get("/incidents")
async def get_incidents():
    """Get all incidents"""
    return load_json_data("incidents.json")

@app.get("/geofences")
async def get_geofences():
    """Get all geofences"""
    return load_json_data("geofences.json")

@app.get("/zones")
async def get_zones():
    """Get all zones"""
    return load_json_data("zones.json")

@app.get("/livemap")
async def get_livemap():
    """Get live map data"""
    return load_json_data("livemap.json")