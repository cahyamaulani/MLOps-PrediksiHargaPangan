import pandas as pd
import mlflow
import mlflow.sklearn
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_percentage_error

# LOAD DATA
df = pd.read_csv("data/processed/harga_features.csv")

df["tanggal"] = pd.to_datetime(df["tanggal"])

# TIME FEATURE
df["year"] = df["tanggal"].dt.year
df["month"] = df["tanggal"].dt.month
df["dayofweek"] = df["tanggal"].dt.dayofweek

# FEATURES & TARGET
features = [
    "lag_1",
    "lag_7",
    "lag_14",              
    "rolling_mean_7",
    "rolling_mean_14",     
    "rolling_std_7",
    "trend",               
    "year",
    "month",
    "dayofweek"
]

X = df[features]
y = df["Nilai"]

# SPLIT TIME SERIES
train_size = int(len(df) * 0.8)

X_train = X[:train_size]
X_test = X[train_size:]

y_train = y[:train_size]
y_test = y[train_size:]

# PARAMETER
n_estimators = 250 # n_estimators: jumlah pohon, makin banyak → model lebih kuat tapi bisa overfit
max_depth = 4 # max_depth: kedalaman tree, makin dalam → model lebih kompleks
learning_rate = 0.08 # learning_rate: kecepatan belajar, makin kecil → lebih stabil tapi butuh banyak tree
subsample = 0.7 # subsample: pakai sebagian data → kurangi overfitting
colsample_bytree = 0.7 # colsample_bytree: pakai sebagian fitur → model tidak terlalu bergantung pada satu fitur
min_child_weight = 5 # min_child_weight: semakin besar → model lebih sederhana (anti overfit)

# MLFLOW
with mlflow.start_run():

    model = XGBRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mape = mean_absolute_percentage_error(y_test, y_pred)


    # logging ke MLflow
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_param("learning_rate", learning_rate)
    mlflow.log_param("subsample", learning_rate)
    mlflow.log_param("colsample_bytree", learning_rate)
    mlflow.log_param("min_child_weight", learning_rate)
    mlflow.log_metric("MAPE", mape)

    mlflow.sklearn.log_model(model, "model")

    print("MAPE:", mape)