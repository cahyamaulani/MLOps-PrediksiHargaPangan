import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np

from src.monitoring.drift_detection import calculate_psi

st.set_page_config(page_title="Early Warning Harga Beras")
st.title("Sistem Early Warning Harga Beras")

st.sidebar.header("Filter Data")

komoditas = st.sidebar.selectbox("Komoditas", ["Beras"])
provinsi  = st.sidebar.selectbox("Provinsi", ["Jawa Timur"])

# ── Load data historis ──────────────────────────────────────────────────────
# Coba baca harga_features.csv, fallback ke harga_clean.csv
FEATURES_PATH = "data/processed/harga_features.csv"
CLEAN_PATH    = "data/processed/harga_clean.csv"

if os.path.exists(FEATURES_PATH):
    hist = pd.read_csv(FEATURES_PATH)
elif os.path.exists(CLEAN_PATH):
    hist = pd.read_csv(CLEAN_PATH)
else:
    st.error("File data tidak ditemukan. Pastikan pipeline preprocessing sudah dijalankan.")
    st.stop()

# Normalise nama kolom tanggal → selalu pakai 'tanggal' huruf kecil
if "Tanggal" in hist.columns and "tanggal" not in hist.columns:
    hist = hist.rename(columns={"Tanggal": "tanggal"})

hist["tanggal"] = pd.to_datetime(hist["tanggal"])
hist = hist.sort_values("tanggal").reset_index(drop=True)

# ── Load forecast (opsional) ────────────────────────────────────────────────
FORECAST_PATH = "data/processed/forecast_result.csv"

if os.path.exists(FORECAST_PATH):
    forecast = pd.read_csv(FORECAST_PATH)
    if "Tanggal" in forecast.columns and "tanggal" not in forecast.columns:
        forecast = forecast.rename(columns={"Tanggal": "tanggal"})
    forecast["tanggal"] = pd.to_datetime(forecast["tanggal"])
    has_forecast = True
else:
    # Buat dummy forecast flat jika belum ada
    last_date  = hist["tanggal"].iloc[-1]
    last_nilai = hist["Nilai"].iloc[-1]
    forecast = pd.DataFrame({
        "tanggal": pd.date_range(last_date + pd.Timedelta(days=1), periods=7),
        "Nilai":   [last_nilai] * 7
    })
    has_forecast = False

# ── Load metrics (opsional) ─────────────────────────────────────────────────
METRICS_PATHS = ["metrics.json", "models/model_metrics.json"]

mape = None
for p in METRICS_PATHS:
    if os.path.exists(p):
        with open(p) as f:
            m = json.load(f)
            # key bisa "MAPE" atau "mape"
            mape = m.get("MAPE") or m.get("mape")
        break

# ── Hitung nilai utama ───────────────────────────────────────────────────────
harga_sekarang    = hist["Nilai"].iloc[-1]
prediksi_terakhir = forecast["Nilai"].iloc[-1]
price_change      = (prediksi_terakhir - harga_sekarang) / harga_sekarang

# PSI drift detection (30 hari terakhir vs 30 hari sebelumnya)
recent_actual = hist["Nilai"].tail(30)
recent_old    = hist["Nilai"].iloc[-60:-30]

if len(recent_old) >= 5 and len(recent_actual) >= 5:
    psi = calculate_psi(recent_old, recent_actual)
else:
    psi = 0.0

# ── Metric cards ─────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Harga Saat Ini", f"Rp {harga_sekarang:,.0f}")

with col2:
    st.metric(
        "Prediksi 7 Hari",
        f"Rp {prediksi_terakhir:,.0f}",
        delta=f"{prediksi_terakhir - harga_sekarang:+.0f}"
    )

with col3:
    mape_label = f"{mape*100:.1f}%" if mape is not None else "N/A"
    st.metric("MAPE Model", mape_label)

# ── Indikator Risiko ──────────────────────────────────────────────────────────
st.subheader("Indikator Risiko")

if psi > 0.2:
    st.error(f"🚨 Data drift terdeteksi (PSI = {psi:.3f} > 0.2) — retraining diperlukan")
elif mape is not None and mape > 0.10:
    st.warning(f"⚠️ Akurasi model menurun (MAPE = {mape*100:.1f}% > 10%)")
elif price_change > 0.05:
    st.warning(f"⚠️ Prediksi kenaikan harga {price_change*100:.1f}% dalam 7 hari ke depan")
else:
    st.success(f"✅ Harga relatif stabil (PSI = {psi:.3f})")

st.caption(f"PSI (Population Stability Index): {psi:.4f} — "
           f"{'Stabil' if psi < 0.1 else 'Drift Ringan' if psi < 0.2 else 'Drift Signifikan'}")

# ── Harga historis by tanggal ─────────────────────────────────────────────────
st.subheader("Harga Historis")

col1, col2 = st.columns(2)

with col1:
    tanggal_pilih = st.date_input(
        "Pilih tanggal",
        value=hist["tanggal"].max().date()
    )

with col2:
    harga_historis = hist.loc[
        hist["tanggal"] == pd.to_datetime(tanggal_pilih),
        "Nilai"
    ]
    if not harga_historis.empty:
        st.metric("Harga pada tanggal tersebut", f"Rp {harga_historis.values[0]:,.0f}")
    else:
        st.write("Data tidak tersedia untuk tanggal ini")

# ── Grafik tren ───────────────────────────────────────────────────────────────
st.subheader("Tren Harga Beras")

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(hist["tanggal"], hist["Nilai"], label="Harga Historis", color="#1f77b4")

if has_forecast:
    ax.plot(forecast["tanggal"], forecast["Nilai"],
            color="red", linestyle="--", label="Prediksi Harga")
else:
    ax.plot(forecast["tanggal"], forecast["Nilai"],
            color="orange", linestyle="--", label="Prediksi (flat — jalankan forecast.py dulu)")

ax.set_xlabel("Tanggal")
ax.set_ylabel("Harga (Rp/kg)")
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)

if not has_forecast:
    st.info("💡 Jalankan `python src/models/forecast.py` untuk mendapatkan prediksi 7 hari ke depan.")