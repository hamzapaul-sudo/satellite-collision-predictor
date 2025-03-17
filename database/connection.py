from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://satellite_user:tmp4Team@localhost/satellite_db"

engine = create_engine(DATABASE_URL,  echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
