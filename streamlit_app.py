import streamlit as st
st.runtime.legacy_caching.disable_telemetry()
st.set_option("browser.gatherUsageStats", False)  # ✅ Inline telemetry disable

import pickle
import numpy as np
import os

# --- Safe Path Handling ---
BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "models", "model.pkl")
crop_encoder_path = os.path.join(BASE_DIR, "models", "encoder_crop.pkl")
district_encoder_path = os.path.join(BASE_DIR, "models", "encoder_district.pkl")

# --- Load Model and Encoders ---
try:
    model = pickle.load(open(model_path, "rb"))
    encoder_crop = pickle.load(open(crop_encoder_path, "rb"))
    encoder_district = pickle.load(open(district_encoder_path, "rb"))
except Exception as e:
    st.error(f"Failed to load model or encoders: {e}")
    st.stop()

# --- Dropdown Options ---
valid_crops = [c for c in encoder_crop.classes_ if c.lower() != "unknown"]
valid_districts = [d for d in encoder_district.classes_ if d.lower() != "unknown"]

# --- Streamlit UI ---
st.set_page_config(page_title="Crop Area Estimator", layout="centered")
st.header("🌾 Punjab Crop Area Estimator")
st.write("Estimate cultivation area using rainfall, crop type, and district.")

selected_crop = st.selectbox("Select Crop Type", valid_crops)
selected_district = st.selectbox("Select District", valid_districts)
rainfall = st.slider("Rainfall (mm)", min_value=0, max_value=500, value=100, step=10)

# --- Encode Inputs ---
encoded_crop = encoder_crop.transform([selected_crop])[0]
encoded_district = encoder_district.transform([selected_district])[0]
features = np.array([[encoded_crop, encoded_district, rainfall]])

# --- Predict Safely ---
try:
    predicted_area = model.predict(features)[0]
    st.success(
        f"Estimated cultivation area for **{selected_crop}** in **{selected_district}** "
        f"with **{rainfall} mm** rainfall is approximately **{predicted_area:.2f} acres**."
    )
except Exception as e:
    st.error(f"Prediction failed: {e}")
