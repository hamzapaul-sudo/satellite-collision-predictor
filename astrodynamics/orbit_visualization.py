import matplotlib.pyplot as plt
import numpy as np
import json
import os
from configs.config import SATELLITE_PREDICTIONS_JSON_PATH

# Earth radius in km
EARTH_RADIUS = 6371

def load_predictions():
    """Load satellite predictions from a file if available."""
    if not os.path.exists(SATELLITE_PREDICTIONS_JSON_PATH):
        print("❌ No saved predictions found! Run orbit_propagation.py first.")
        return None

    with open(SATELLITE_PREDICTIONS_JSON_PATH, "r") as file:
        predictions = json.load(file)
        return predictions

def plot_orbits(path):
    """Load saved orbit predictions and plot them in 3D."""
    predictions = load_predictions()
    if not predictions:
        return

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_title("Satellite Orbits")

    # ✅ Generate Earth sphere coordinates
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = EARTH_RADIUS * np.outer(np.cos(u), np.sin(v))
    y = EARTH_RADIUS * np.outer(np.sin(u), np.sin(v))
    z = EARTH_RADIUS * np.outer(np.ones(np.size(u)), np.cos(v))

    # ✅ Ensure Earth is visible (set alpha for transparency)
    ax.plot_surface(x, y, z, color="blue", alpha=0.5, edgecolor="black")

    # Plot each satellite orbit
    for norad_id, data in predictions.items():
        sat_name = data["satellite_name"]
        positions = np.array([[p["x"], p["y"], p["z"]] for p in data["predictions"]])

        print(f"📊 Plotting {sat_name} (NORAD ID: {norad_id})")
        ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], label=sat_name)

    ax.set_xlabel("X (km)")
    ax.set_ylabel("Y (km)")
    ax.set_zlabel("Z (km)")

    ax.legend()
    plt.savefig(path)
    print("✅ Orbit plot saved as 'satellite_orbits.png'")
