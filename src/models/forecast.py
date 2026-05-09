import pandas as pd
import mlflow.pyfunc

# load model dari MLflow (production)
model = mlflow.pyfunc.load_model("models:/harga-pangan-model/Production")

# load data fitur
df = pd.read_csv("data/processed/harga_features.csv")
df["tanggal"] = pd.to_datetime(df["tanggal"])

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
        "year",
        "month",
        "dayofweek"
    ]]

    pred = model.predict(X)[0]

    next_date = last_row["tanggal"].values[0] + pd.Timedelta(days=1)

    new_row = last_row.copy()
    new_row["tanggal"] = next_date
    new_row["Nilai"] = pred

    new_row["lag_1"] = pred

    # update lag_7
    if len(last_data) >= 7:
        new_row["lag_7"] = last_data.iloc[-7]["Nilai"]

    # update rolling
    window = last_data["Nilai"].tail(6).tolist() + [pred]
    new_row["rolling_mean_7"] = sum(window) / 7

    last_data = pd.concat([last_data, new_row])

    forecast_list.append(pred)

print("Forecast 7 hari:", forecast_list)