from database.connection import SessionLocal
from database.models import Satellite


def get_latest_tle():
    """Fetch the most recent TLE data from the database."""
    session = SessionLocal()
    satellite = session.query(Satellite).order_by(Satellite.epoch.desc()).first()
    session.close()

    if not satellite:
        print("❌ No TLE data found in the database!")
        return None

    return satellite


def get_all_satellites():
    """Retrieve all satellites stored in the database."""
    session = SessionLocal()
    satellites = session.query(Satellite).all()
    session.close()

    return satellites
