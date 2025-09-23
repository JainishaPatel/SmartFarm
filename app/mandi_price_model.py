import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()
CSV_PATH = os.getenv("PRICES_DATASET_PATH")
MODEL_PATH = "market_price_model.pkl"
ENCODERS_PATH = "label_encoders.pkl"

# Load CSV
df = pd.read_csv(CSV_PATH)

# Ensure correct types
categorical_cols = ['STATE','District Name','Market Name','Commodity','Variety','Grade']
numeric_cols = ['Min_Price','Max_Price','Modal_Price']

for col in categorical_cols:
    df[col] = df[col].astype(str)
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df[categorical_cols] = df[categorical_cols].fillna('Unknown')
df[numeric_cols] = df[numeric_cols].fillna(0)

# Encode categorical features
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Features & target
X = df[categorical_cols + ['Min_Price','Max_Price']]
y = df['Modal_Price']

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and encoders
with open(MODEL_PATH, 'wb') as f:
    pickle.dump(model, f)
with open(ENCODERS_PATH, 'wb') as f:
    pickle.dump(label_encoders, f)

print("✅ Model and encoders saved successfully!")
