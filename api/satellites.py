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

# ✅ Set JAVA_HOME directory
JAVA_HOME = "/opt/render/.jdk"

# ✅ If Java is missing, install OpenJDK 23
if not os.path.exists(JAVA_HOME):
    print("⚠️ Java not found, installing OpenJDK 23...")
    subprocess.run(["mkdir", "-p", JAVA_HOME])
    subprocess.run([
        "curl", "-fsSL",
        "https://download.java.net/java/GA/jdk23.0.2/6da2a6609d6e406f85c491fcb119101b/7/GPL/openjdk-23.0.2_linux-aarch64_bin.tar.gz",
        "-o", "/tmp/openjdk.tar.gz"
    ])
    subprocess.run(["tar", "-xzf", "/tmp/openjdk.tar.gz", "-C", JAVA_HOME, "--strip-components=1"])

# ✅ Set JAVA_HOME environment variable so Orekit can find it
os.environ["JAVA_HOME"] = JAVA_HOME
os.environ["PATH"] += f":{JAVA_HOME}/bin"

print(f"✅ JAVA_HOME is set to: {os.environ['JAVA_HOME']}")

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
    uvicorn.run(app, host="0.0.0.0", port=8000)
