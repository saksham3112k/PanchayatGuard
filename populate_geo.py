from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random

engine = create_engine("sqlite:///./backend/panchayatguard.db")
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Add latitude and longitude manually using raw SQL
panchayats = session.execute("SELECT id, name FROM panchayats").fetchall()

# UP roughly between lat 24.5 to 29.5, long 77.0 to 84.0
for p in panchayats:
    lat = round(random.uniform(25.0, 29.0), 4)
    lng = round(random.uniform(77.5, 83.5), 4)
    session.execute(f"UPDATE panchayats SET latitude = {lat}, longitude = {lng} WHERE id = {p.id}")

session.commit()
session.close()
print("Populated geographic data.")
