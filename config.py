import os

# ✅ Get the absolute path of the project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Root directory of the project
STORAGE_DIR = os.path.join(BASE_DIR, "storage")  # Ensure "storage/" is in project root

# ✅ Ensure storage directory exists
os.makedirs(STORAGE_DIR, exist_ok=True)

# ✅ Define paths for saved files
SATELLITE_PREDICTIONS_JSON_PATH = os.path.join(STORAGE_DIR, "satellite_predictions.json")
# ✅ Define path for collision alerts
COLLISION_ALERTS_PATH = os.path.join(STORAGE_DIR, "collision_alerts.json")
