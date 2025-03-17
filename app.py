import json
import os
import sys
import threading
from contextlib import redirect_stdout
from os.path import expanduser

import uvicorn
import requests
import streamlit as st
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import pandas as pd
from astrodynamics.orbit_propagation import propagate_orbits
from astrodynamics.orbit_visualization import plot_orbits
from astrodynamics.collision_detection import detect_collisions
from data_collection.norad_gp_dataset import fetch_active_satellites_json

# ✅ Initialize FastAPI
api = FastAPI(title="Satellite Position API")

# ✅ Enable CORS (Allows Streamlit UI to talk to FastAPI)
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 **FastAPI Endpoints**
@api.get("/")
def home():
    return {"message": "Welcome to the Satellite Tracking API"}

@api.get("/satellites")
def get_active_satellites():
    """Return all active satellites."""
    return fetch_active_satellites_json()

@api.get("/predicted-positions")
def get_predicted_positions():
    """Return all future predicted positions."""
    return propagate_orbits()

@api.get("/visualization")
def get_visualization():
    """
    Generate and return the latest satellite orbit visualization.
    """
    VISUALIZATION_PATH = os.path.join(expanduser('~'), 'satellite_orbits.png')
    plot_orbits(VISUALIZATION_PATH)

    # ✅ Serve the image file as response
    if os.path.exists(VISUALIZATION_PATH):
        return FileResponse(VISUALIZATION_PATH, media_type="image/png", filename="satellite_orbits.png")

    return {"error": "Visualization could not be generated."}

@api.get("/collisions")
def get_collision_alerts():
    """
    Detect and return potential satellite collision warnings.
    """
    alerts = detect_collisions(threshold_km=50)  # Run with 50 km threshold

    if len(alerts) > 0:
        with open(os.path.join(expanduser('~'), 'collision_alerts.png'), "r") as file:
            return JSONResponse(content=json.load(file))

    return {"message": "No collision risks detected."}

# ✅ Run FastAPI in a background thread without logs
def run_fastapi():
    with open(os.devnull, "w") as f, redirect_stdout(f):  # Hide logs
        sys.stderr = f  # Redirect stderr to avoid clutter
        uvicorn.run(api, host="0.0.0.0", port=8000, log_level="critical")

threading.Thread(target=run_fastapi, daemon=True).start()

# 🔹 **Streamlit UI**
st.title("🛰️ Satellite Tracking Dashboard")

API_URL = "http://127.0.0.1:8000"

# # 📍 **1. Get Active Satellites**
# st.sidebar.header("📡 Active Satellites")
# satellites = requests.get(f"{API_URL}/satellites").json()
# satellite_names = [sat["name"] for sat in satellites]
# selected_satellite = st.sidebar.selectbox("Choose a Satellite", satellite_names)

# st.header(f"🔭 Orbit Prediction for {selected_satellite}")

# ✅ Fetch satellite positions
positions = requests.get(f"{API_URL}/satellites").json()

# ✅ Convert response to DataFrame
if isinstance(positions, dict):
    positions = [positions]  # Convert to list if it's a single dictionary

df_positions = pd.DataFrame(positions)

# ✅ Display DataFrame
st.subheader("📊 Processed Data")
st.dataframe(df_positions)

# 📍 **3. Display Satellite Visualization**
st.header("🌍 Satellite Orbits Visualization")
st.image(f"{API_URL}/visualization", caption="Satellite Orbit Plot")

# 📍 **4. Show Collision Alerts**
st.header("⚠️ Collision Warnings")
collision_data = requests.get(f"{API_URL}/collisions").json()

if "message" in collision_data:
    st.info("✅ No collision risks detected.")
else:
    st.warning("⚠️ Potential Collisions Detected!")
    df_collisions = pd.DataFrame(collision_data)
    st.dataframe(df_collisions)

# 📍 **5. Manually Update Data**
if st.button("🔄 Update Satellite Data"):
    requests.post(f"{API_URL}/trigger-update")
    st.success("✅ Data update started! Check back in a few minutes.")

