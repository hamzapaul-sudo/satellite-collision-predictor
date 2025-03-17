import os

import orekit_jpype as orekit
orekit.initVM()

from orekit_jpype.pyhelpers import setup_orekit_data
setup_orekit_data()

import json
from datetime import datetime
from org.orekit.time import AbsoluteDate, TimeScalesFactory
from org.orekit.propagation.analytical.tle import TLEPropagator, TLE
from data_collection.norad_gp_dataset import fetch_active_satellites_tle
from config import SATELLITE_PREDICTIONS_JSON_PATH

def propagate_orbits(days=1):
    """Fetch latest TLEs, propagate orbits, and save results to a file."""
    tle_dict = fetch_active_satellites_tle()

    if not tle_dict:
        print("❌ No valid TLEs found!")
        return

    utc = TimeScalesFactory.getUTC()
    predictions_data = {}

    for norad_id, (sat_name, tle_line1, tle_line2) in list(tle_dict.items())[:10]:  # Limit to 10 satellites for speed
        try:
            print(f"\n🔍 Propagating orbit for {sat_name} (NORAD ID: {norad_id})")
            tle = TLE(tle_line1, tle_line2)
            propagator = TLEPropagator.selectExtrapolator(tle)

            # Predict positions for the next `days`
            positions = []
            for i in range(days * 24 * 6):  # Every hour
                future_date = AbsoluteDate(datetime.utcnow().year, datetime.utcnow().month, datetime.utcnow().day,
                                           utc).shiftedBy(i * 600)  # 600s = 10 min
                state = propagator.propagate(future_date)
                position = state.getPVCoordinates().getPosition()
                positions.append({
                    "time": future_date.toString(),
                    "x": position.getX(),
                    "y": position.getY(),
                    "z": position.getZ()
                })

            predictions_data[norad_id] = {
                "satellite_name": sat_name,
                "tle": [tle_line1, tle_line2],
                "predictions": positions
            }

        except Exception as e:
            print(f"⚠️ Error propagating {sat_name} (NORAD ID: {norad_id}): {e}")

    # ✅ Save to JSON file
    with open(SATELLITE_PREDICTIONS_JSON_PATH, "w") as file:
        json.dump(predictions_data, file, indent=4)

    print(f"\n✅ Predictions saved to {SATELLITE_PREDICTIONS_JSON_PATH}")

    """Load satellite predictions from JSON file."""
    if not os.path.exists(SATELLITE_PREDICTIONS_JSON_PATH):
        return []
    with open(SATELLITE_PREDICTIONS_JSON_PATH, "r") as file:
        return json.load(file)



