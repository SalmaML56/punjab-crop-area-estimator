import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from catboost import CatBoostRegressor
from math import sqrt
import pickle
import os

# --- Step 1: Load Dataset ---
DATA_PATH = os.path.join("data", "crop_yield_data.csv")
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"CSV file not found at {DATA_PATH}")

df = pd.read_csv(DATA_PATH)

# --- Step 2: Select Crop Columns ---
crop_columns = ['Citrus ( ACRE)', 'Rabi Fruits (ACRE)', 'Fodder (ACRE)']
df_long = df.melt(value_vars=crop_columns, var_name='Crop_Type', value_name='Area')
df_long['Area'] = pd.to_numeric(df_long['Area'], errors='coerce')
df_long.dropna(subset=['Area'], inplace=True)
df_long = df_long[df_long['Area'] < 100000]

# --- Step 3: Clean Crop Names & Encode ---
df_long['Crop_Type'] = df_long['Crop_Type'].str.strip().str.lower()
common_crops = df_long['Crop_Type'].value_counts()[df_long['Crop_Type'].value_counts() > 30].index
df_long['Crop_Group'] = df_long['Crop_Type'].apply(lambda x: x if x in common_crops else 'other')
encoder_crop = LabelEncoder()
df_long['Crop_Code'] = encoder_crop.fit_transform(df_long['Crop_Group'])

# --- Step 4: Extract & Encode District ---
district_col = None
for col in df.columns:
    if col.strip().lower() == 'district' or col == '-':
        district_col = col
        break

if district_col:
    df.rename(columns={district_col: 'District'}, inplace=True)
else:
    raise ValueError("No 'District' column found in dataset")

df['District'] = df['District'].astype(str).str.strip().str.title()
encoder_district = LabelEncoder()
df['District_Code'] = encoder_district.fit_transform(df['District'])

# Match District_Code to long format
df_long['District_Code'] = df['District_Code'].values[:len(df_long)]

# --- Step 5: Handle Rainfall ---
if 'Rainfall' in df.columns:
    df_long['Rainfall'] = pd.to_numeric(df['Rainfall'], errors='coerce').fillna(0)
else:
    df_long['Rainfall'] = 0

# --- Step 6: Train Model ---
X = df_long[['Crop_Code', 'District_Code', 'Rainfall']]
y = df_long['Area']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = CatBoostRegressor(verbose=0)
model.fit(X_train, y_train)

# --- Step 7: Evaluate Model ---
preds = model.predict(X_test)
rmse = sqrt(mean_squared_error(y_test, preds))
r2 = r2_score(y_test, preds)

print(f"✅ RMSE: {rmse:.2f}")
print(f"✅ R² Score: {r2:.3f}")

# --- Step 8: Save Model & Encoders ---
os.makedirs("models", exist_ok=True)
pickle.dump(model, open(os.path.join("models", "model.pkl"), "wb"))
pickle.dump(encoder_crop, open(os.path.join("models", "encoder_crop.pkl"), "wb"))
pickle.dump(encoder_district, open(os.path.join("models", "encoder_district.pkl"), "wb"))

with open("models/eval.txt", "w") as f:
    f.write(f"RMSE: {rmse:.2f}\nR² Score: {r2:.3f}\n")

print("✅ Model, encoders, and evaluation saved to 'models/' folder.")