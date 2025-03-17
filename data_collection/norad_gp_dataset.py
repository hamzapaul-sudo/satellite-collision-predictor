import requests
from database.connection import SessionLocal
from database.models import Satellite
from datetime import datetime

def fetch_active_satellites_json():
    url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=json"
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors
    tle_json = response.json()
    return parse_satellite_data(tle_json)


def fetch_active_satellites_tle():
    """
        Fetch the latest TLEs for all active satellites from Celestrak.

        :return: A dictionary {NORAD_ID: (tle_line1, tle_line2)}
        """
    url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error if the request fails

    tle_data = response.text.strip().split("\n")
    tle_dict = {}

    for i in range(0, len(tle_data), 3):
        if i + 2 < len(tle_data):
            sat_name = tle_data[i].strip()
            tle_line1 = tle_data[i + 1].strip()
            tle_line2 = tle_data[i + 2].strip()
            norad_id = tle_line1.split()[1]  # Extract NORAD ID from TLE line 1

            tle_dict[norad_id] = (sat_name, tle_line1, tle_line2)

    return tle_dict

def parse_satellite_data(tle_json):
    satellites = []
    for sat in tle_json:
        satellite = {
            "name": sat.get("OBJECT_NAME"),
            "norad_cat_id": sat.get("NORAD_CAT_ID"),
            "object_id": sat.get("OBJECT_ID"),
            "epoch": sat.get("EPOCH"),
            "mean_motion": sat.get("MEAN_MOTION"),
            "eccentricity": sat.get("ECCENTRICITY"),
            "inclination": sat.get("INCLINATION"),
            "ra_of_asc_node": sat.get("RA_OF_ASC_NODE"),
            "arg_of_pericenter": sat.get("ARG_OF_PERICENTER"),
            "mean_anomaly": sat.get("MEAN_ANOMALY"),
            "classification_type": sat.get("CLASSIFICATION_TYPE"),
            "element_set_no": sat.get("ELEMENT_SET_NO"),
            "rev_at_epoch": sat.get("REV_AT_EPOCH"),
            "bstar": sat.get("BSTAR"),
            "mean_motion_dot": sat.get("MEAN_MOTION_DOT"),
            "ephemeris_type": sat.get("EPHEMERIS_TYPE"),
            "timestamp": datetime.utcnow().isoformat()
        }
        satellites.append(satellite)
    return satellites

def save_satellites(satellites_data):
    db = SessionLocal()
    for sat in satellites_data:
        satellite = Satellite(
            name=sat["name"],
            norad_cat_id=int(sat["norad_cat_id"]),
            object_id=sat["object_id"],
            epoch=datetime.fromisoformat(sat["epoch"]),
            mean_motion=float(sat["mean_motion"]),
            eccentricity=float(sat["eccentricity"]),
            inclination=float(sat["inclination"]),
            ra_of_asc_node=float(sat["ra_of_asc_node"]),
            arg_of_pericenter=float(sat["arg_of_pericenter"]),
            mean_anomaly=float(sat["mean_anomaly"]),
            classification_type=sat["classification_type"],
            element_set_no=int(sat["element_set_no"]),
            rev_at_epoch=int(sat["rev_at_epoch"]),
            bstar=float(sat["bstar"]),
            mean_motion_dot=float(sat["mean_motion_dot"]),
            ephemeris_type=int(sat["ephemeris_type"]),
            timestamp=datetime.utcnow()
        )
        db.merge(satellite)
    db.commit()
    db.close()
    print(f"✅ Saved {len(satellites_data)} satellites to database.")


if __name__ == "__main__":
    fetch_active_satellites_tle()





