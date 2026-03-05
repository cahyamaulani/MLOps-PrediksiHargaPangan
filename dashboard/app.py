import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json

from src.monitoring.drift_detection import calculate_psi

st.set_page_config(page_title="Early Warning Harga Beras")

st.title("Sistem Early Warning Harga Beras")

hist = pd.read_csv("data/processed/harga_features.csv")
forecast = pd.read_csv("data/processed/forecast_result.csv")

with open("models/model_metrics.json") as f:
    metrics = json.load(f)

mape = metrics["mape"]

harga_sekarang = hist["Nilai"].iloc[-1]
prediksi_terakhir = forecast["Nilai"].iloc[-1]

price_change = (prediksi_terakhir - harga_sekarang) / harga_sekarang

recent_actual = hist["Nilai"].tail(30)
recent_old = hist["Nilai"].iloc[-60:-30]

psi = calculate_psi(recent_old, recent_actual)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Harga Saat Ini",
        f"Rp {harga_sekarang:,.0f}"
    )

with col2:
    st.metric(
        "Prediksi 7 Hari",
        f"Rp {prediksi_terakhir:,.0f}",
        delta=f"{prediksi_terakhir-harga_sekarang:.0f}"
    )

st.subheader("Indikator Risiko")

if psi > 0.2:

    st.error("🚨 Data drift terdeteksi (PSI tinggi)")

elif mape > 0.10:

    st.warning("⚠️ Akurasi model menurun (MAPE tinggi)")

elif price_change > 0.05:

    st.warning("⚠️ Prediksi kenaikan harga signifikan")

else:

    st.success("Harga relatif stabil")

plot_df = pd.concat([

    hist[["Tanggal","Nilai"]],

    forecast

])

plt.figure(figsize=(10,5))

plt.plot(
    hist["Tanggal"],
    hist["Nilai"],
    label="Actual Price"
)

plt.plot(
    forecast["Tanggal"],
    forecast["Nilai"],
    color="red",
    label="Forecast Price"
)

plt.legend()

plt.xlabel("Tanggal")

plt.ylabel("Harga")

st.pyplot(plt)

st.subheader("Data Forecast")

st.dataframe(forecast)