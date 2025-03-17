from sqlalchemy import Column, Integer, String, Float, DateTime
from database.connection import Base


class Satellite(Base):
    __tablename__ = "satellites"
    __table_args__ = {"schema": "public"}  # Explicitly use 'public' schema

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    norad_cat_id = Column(Integer, unique=True, index=True)
    object_id = Column(String, index=True)
    epoch = Column(DateTime)
    mean_motion = Column(Float)
    eccentricity = Column(Float)
    inclination = Column(Float)
    ra_of_asc_node = Column(Float)
    arg_of_pericenter = Column(Float)
    mean_anomaly = Column(Float)
    classification_type = Column(String)
    element_set_no = Column(Integer)
    rev_at_epoch = Column(Integer)
    bstar = Column(Float)
    mean_motion_dot = Column(Float)
    ephemeris_type = Column(Integer)
    timestamp = Column(DateTime)
