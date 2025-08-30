import os
import pandas as pd
from dotenv import load_dotenv
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

load_dotenv()

DATA_PATH = os.getenv("DATASET_PATH")

# 1. Load dataset
df = pd.read_csv(DATA_PATH)

# 2. Encode Season, State, and Crop using LabelEncoder
season_encoder = LabelEncoder()
state_encoder = LabelEncoder()
crop_encoder = LabelEncoder()

df['Season'] = season_encoder.fit_transform(df['Season'])
df['State'] = state_encoder.fit_transform(df['State'])
df['Crop'] = crop_encoder.fit_transform(df['Crop'])

# 3. Define input features (X) and label (y)
X = df[['Season', 'State', 'temperature', 'humidity', 'rainfall']]
y = df['Crop']

# 4. Train model
model = RandomForestClassifier()
model.fit(X, y)

# 5. Save model and encoders
with open("crop_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("season_encoder.pkl", "wb") as f:
    pickle.dump(season_encoder, f)

with open("state_encoder.pkl", "wb") as f:
    pickle.dump(state_encoder, f)

with open("crop_encoder.pkl", "wb") as f:
    pickle.dump(crop_encoder, f)

print("✅ Model and encoders saved successfully.")
