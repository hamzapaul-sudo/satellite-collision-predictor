import streamlit as st
import requests
import pandas as pd

# ✅ FastAPI Backend URL
API_URL = "http://127.0.0.1:8000"

# ✅ Page Title
st.title("🛰️ Satellite Tracking Dashboard")

# 📍 **1. Get Active Satellites**
# st.sidebar.header("📡 Active Satellites")
# satellites = requests.get(f"{API_URL}/satellites").json()
# satellite_names = [sat["name"] for sat in satellites]
# selected_satellite = st.sidebar.selectbox("Choose a Satellite", satellite_names)

# st.header(f"🔭 Orbit Prediction for {selected_satellite}")

# ✅ Fetch satellite positions
positions = requests.get(f"{API_URL}/satellites").json()

# ✅ Convert response to DataFrame
if isinstance(positions, dict):
    positions = [positions]  # Convert to list if it's a single dictionary

df_positions = pd.DataFrame(positions)

# ✅ Display DataFrame
st.subheader("📊 Processed Data")
st.dataframe(df_positions)

# 📍 **3. Display Satellite Visualization**
st.header("🌍 Satellite Orbits Visualization")
st.image(f"{API_URL}/visualization", caption="Satellite Orbit Plot")

# 📍 **4. Show Collision Alerts**
st.header("⚠️ Collision Warnings")
collision_data = requests.get(f"{API_URL}/collisions").json()

if "message" in collision_data:
    st.info("✅ No collision risks detected.")
else:
    st.warning("⚠️ Potential Collisions Detected!")
    df_collisions = pd.DataFrame(collision_data)
    st.dataframe(df_collisions)

# 📍 **5. Manually Update Data**
if st.button("🔄 Update Satellite Data"):
    requests.post(f"{API_URL}/trigger-update")
    st.success("✅ Data update started! Check back in a few minutes.")