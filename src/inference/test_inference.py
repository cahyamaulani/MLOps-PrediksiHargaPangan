import mlflow.pyfunc
import pandas as pd

# LOAD MODEL (Production)
model = mlflow.pyfunc.load_model(
    "models:/harga-pangan-model/Production"
)

# LOAD FEATURE DATA
# ambil dataset hasil feature engineering
df = pd.read_csv("data/processed/harga_features.csv")

# pastikan format tanggal benar
df["tanggal"] = pd.to_datetime(df["tanggal"])

# AMBIL DATA TERAKHIR
# ini penting: pakai data terbaru untuk prediksi
last_row = df.iloc[-1]

# SIAPKAN INPUT MODEL
# harus sesuai dengan fitur saat training
input_data = pd.DataFrame({
    "lag_1": [last_row["lag_1"]],
    "lag_7": [last_row["lag_7"]],
    "lag_14": [last_row["lag_14"]],                  
    "rolling_mean_7": [last_row["rolling_mean_7"]],
    "rolling_mean_14": [last_row["rolling_mean_14"]], 
    "rolling_std_7": [last_row["rolling_std_7"]],
    "trend": [last_row["trend"]],                    
    "year": [last_row["tanggal"].year],
    "month": [last_row["tanggal"].month],
    "dayofweek": [last_row["tanggal"].dayofweek]
})

# PREDIKSI
prediction = model.predict(input_data)

print("\n=== HASIL PREDIKSI ===")
print("Tanggal terakhir data :", last_row["tanggal"])
print("Prediksi harga besok  :", prediction[0])