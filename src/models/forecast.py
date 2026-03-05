import pandas as pd
import pickle
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

DATA_PATH = os.path.join(BASE_DIR, "data/processed/harga_features.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models/xgboost_model.pkl")
OUTPUT_PATH = os.path.join(BASE_DIR, "data/processed/forecast_result.csv")

model = pickle.load(open(MODEL_PATH, "rb"))

df = pd.read_csv(DATA_PATH)
df["Tanggal"] = pd.to_datetime(df["Tanggal"])

future_days = 7

forecast_list = []

last_data = df.copy()

for i in range(future_days):

    last_row = last_data.iloc[-1:]

    X = last_row[[
        "lag_1",
        "lag_7",
        "rolling_mean_7",
        "rolling_std_7",
    ]]

    pred = model.predict(X)[0]

    next_date = last_row["Tanggal"].values[0] + pd.Timedelta(days=1)

    new_row = {
        "Tanggal": next_date,
        "Nilai": pred
    }

    forecast_list.append(new_row)

    last_data = pd.concat([
        last_data,
        pd.DataFrame([new_row])
    ])

forecast_df = pd.DataFrame(forecast_list)

forecast_df.to_csv(OUTPUT_PATH, index=False)

print("Forecast created!")