import json

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
import os
import uvicorn
from astrodynamics.orbit_propagation import propagate_orbits
from config import STORAGE_DIR, COLLISION_ALERTS_PATH
from astrodynamics.orbit_visualization import plot_orbits
from astrodynamics.collision_detection import detect_collisions
from data_collection.norad_gp_dataset import fetch_active_satellites_json
import subprocess

app = FastAPI(title="Satellite Position API")

@app.get("/")
def home():
    return {"message": "Welcome to the Satellite Tracking API"}

@app.get("/satellites")
def get_active_satellites():
    """Return all active satellites."""
    return fetch_active_satellites_json()

@app.get("/predicted-positions")
def get_predicted_positions():
    """Return all future predicted positions."""
    return propagate_orbits()


@app.get("/visualization")
def get_visualization():
    """
    Generate and return the latest satellite orbit visualization.
    """
    VISUALIZATION_PATH = os.path.join(STORAGE_DIR, 'satellite_orbits.png')
    plot_orbits(VISUALIZATION_PATH)

    # ✅ Serve the image file as response
    if os.path.exists(VISUALIZATION_PATH):
        return FileResponse(VISUALIZATION_PATH, media_type="image/png", filename="satellite_orbits.png")

    return {"error": "Visualization could not be generated."}

@app.get("/collisions")
def get_collision_alerts():
    """
    Detect and return potential satellite collision warnings.
    """
    # ✅ Run the collision detection function
    alerts = detect_collisions(threshold_km=50)  # Run with 50 km threshold

    # ✅ Serve the alerts as a JSON response
    if len(alerts) > 0:
        with open(COLLISION_ALERTS_PATH, "r") as file:
            return JSONResponse(content=json.load(file))

    return {"message": "No collision risks detected."}

if __name__ == "__main__":
    # ✅ Ensure Java (JVM) is installed before running Orekit
    if not os.path.exists("/usr/lib/jvm/java-11-openjdk-amd64"):
        print("⚠️ Java not found, installing OpenJDK 11...")
        subprocess.run(["apt-get", "update"])
        subprocess.run(["apt-get", "install", "-y", "openjdk-11-jdk"])

    # ✅ Set JAVA_HOME so Orekit can find it
    os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64"
    os.environ["PATH"] += ":/usr/lib/jvm/java-11-openjdk-amd64/bin"
    uvicorn.run(app, host="0.0.0.0", port=8000)
