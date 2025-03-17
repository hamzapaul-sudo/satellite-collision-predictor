import json
import os
from os.path import expanduser

import numpy as np


# ✅ Load satellite predictions
def load_predictions():
    """Load satellite predictions from the stored JSON file."""
    predictions_path = os.path.join(expanduser('~'), "satellite_predictions.json")

    if not os.path.exists(predictions_path):
        print("❌ No predictions file found. Run orbit_propagation.py first.")
        return None

    with open(predictions_path, "r") as file:
        return json.load(file)


# ✅ Function to calculate the Euclidean distance between two points in space
def calculate_distance(pos1, pos2):
    """Compute the distance between two satellites in 3D space."""
    return np.linalg.norm(np.array(pos1) - np.array(pos2))


# ✅ Detect collisions
def detect_collisions(threshold_km=50):
    """
    Detect satellites that come closer than `threshold_km` and save collision alerts.

    Args:
        threshold_km (float): Distance threshold in km for a collision alert.

    Returns:
        List of detected close approaches.
    """
    predictions = load_predictions()
    if not predictions:
        return []

    collision_alerts = []

    # ✅ Extract satellite list from dictionary
    satellite_list = list(predictions.values())

    # ✅ Get number of time steps (assume all satellites have the same count)
    time_steps = len(satellite_list[0]["predictions"]) if satellite_list else 0

    for i in range(time_steps):
        time = satellite_list[0]["predictions"][i]["time"]  # ✅ Extract timestamp

        # ✅ Compare every satellite pair
        for idx1 in range(len(satellite_list)):
            for idx2 in range(idx1 + 1, len(satellite_list)):  # Avoid duplicate checks
                sat1 = satellite_list[idx1]
                sat2 = satellite_list[idx2]

                if "predictions" not in sat1 or "predictions" not in sat2:
                    continue  # ✅ Skip satellites with missing data

                if i >= len(sat1["predictions"]) or i >= len(sat2["predictions"]):
                    continue  # ✅ Avoid out-of-range errors

                pos1 = [
                    sat1["predictions"][i]["x"],
                    sat1["predictions"][i]["y"],
                    sat1["predictions"][i]["z"],
                ]
                pos2 = [
                    sat2["predictions"][i]["x"],
                    sat2["predictions"][i]["y"],
                    sat2["predictions"][i]["z"],
                ]

                # ✅ Compute distance
                distance = calculate_distance(pos1, pos2)

                # ✅ If below threshold, record a collision warning
                if distance < threshold_km:
                    alert = {
                        "time": time,
                        "satellite_1": sat1["satellite_name"],
                        "satellite_2": sat2["satellite_name"],
                        "distance_km": round(distance, 2),
                        "status": "WARNING: Possible Close Approach!",
                    }
                    print(
                        f"⚠️ Collision Alert: {sat1['satellite_name']} & {sat2['satellite_name']} at {distance:.2f} km")
                    collision_alerts.append(alert)

    # ✅ Save alerts to a file
    COLLISION_ALERTS_PATH = os.path.join(expanduser('~'), "collision_alerts.json")
    with open(COLLISION_ALERTS_PATH, "w") as file:
        json.dump(collision_alerts, file, indent=4)

    print(f"✅ Collision alerts saved to {COLLISION_ALERTS_PATH}")
    return collision_alerts

