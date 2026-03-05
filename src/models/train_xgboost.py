import pandas as pd
import os
import pickle
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_percentage_error

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

DATA_PATH = os.path.join(BASE_DIR, "data/processed/harga_features.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models/xgboost_model.pkl")
METRIC_PATH = os.path.join(BASE_DIR, "models/model_metrics.json")

df = pd.read_csv(DATA_PATH)

df["Tanggal"] = pd.to_datetime(df["Tanggal"])

features = [
    "lag_1",
    "lag_7",
    "rolling_mean_7",
    "rolling_std_7",
]

train_size = int(len(df) * 0.8)

train = df.iloc[:train_size]
test = df.iloc[train_size:]

X_train = train[features]
y_train = train["Nilai"]

X_test = test[features]
y_test = test["Nilai"]

model = XGBRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=4
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

mape = mean_absolute_percentage_error(y_test, pred)

print("MAPE:", mape)

os.makedirs("models", exist_ok=True)

pickle.dump(model, open(MODEL_PATH, "wb"))

import json

with open(METRIC_PATH, "w") as f:
    json.dump({"mape": float(mape)}, f)

print("Model saved!")