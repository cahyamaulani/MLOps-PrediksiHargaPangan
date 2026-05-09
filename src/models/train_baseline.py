import pandas as pd
import mlflow
import mlflow.sklearn

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("data/processed/harga_clean.csv")

# feature engineering
# model ML tidak bisa membaca tanggal langsung
df["tanggal"] = pd.to_datetime(df["tanggal"])
df["year"] = df["tanggal"].dt.year
df["month"] = df["tanggal"].dt.month
df["day"] = df["tanggal"].dt.day

df = pd.get_dummies(df, columns=["Provinsi", "commodity_id"], drop_first=True)

X = df.drop(columns=["Nilai", "tanggal"])
y = df["Nilai"]

# split time-series
train_size = int(len(df) * 0.8)

X_train = X[:train_size]
X_test = X[train_size:]

y_train = y[:train_size]
y_test = y[train_size:]


# =========================
# PARAMETER (ini nanti diubah-ubah)
# =========================
n_estimators = 200
max_depth = 10

# =========================
# MLFLOW START
# =========================
with mlflow.start_run():

    model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mape = mean_absolute_percentage_error(y_test, y_pred)

    # =========================
    # LOGGING
    # =========================
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)

    mlflow.log_metric("MAPE", mape)

    mlflow.sklearn.log_model(model, "model")

    print("MAPE:", mape)