# Sistem Early Warning dan Prediksi Lonjakan Harga Pangan di Jawa Timur

Proyek ini merupakan implementasi sistem **Early Warning dan Prediksi Lonjakan Harga Pangan di Jawa Timur** yang bertujuan untuk memantau serta memprediksi perubahan harga komoditas pangan. Sistem monitoring fluktuasi harga pangan yang tersedia saat ini umumnya hanya menampilkan data historis tanpa kemampuan prediktif, sehingga sulit untuk mengantisipasi lonjakan harga secara lebih awal.

Untuk mengatasi permasalahan tersebut, proyek ini mengembangkan sistem prediksi harga berbasis **Machine Learning Time-Series Forecasting** menggunakan model regresi. Model digunakan untuk memprediksi harga beras hingga **7 hari ke depan** berdasarkan data historis harga. Selain melakukan prediksi harga, sistem juga dilengkapi dengan mekanisme **early warning** untuk mendeteksi potensi kenaikan harga secara lebih dini.

Sistem ini dirancang menggunakan pendekatan **Machine Learning Operations (MLOps)** sehingga proses pengolahan data, pelatihan model, prediksi, serta monitoring model dapat berjalan secara terstruktur dan berkelanjutan.

---

## Tujuan Proyek
- Membangun sistem prediksi harga pangan berbasis **Machine Learning** menggunakan pendekatan time-series forecasting.
- Memprediksi harga komoditas pangan hingga **7 hari ke depan** berdasarkan data historis harga.
- Menyediakan sistem **early warning** untuk mendeteksi potensi lonjakan harga lebih awal.
- Membantu distributor, pelaku pasar, serta pemerintah daerah dalam mengambil keputusan terkait manajemen stok dan distribusi pangan.
- Mengimplementasikan pipeline **Machine Learning Operations (MLOps)** untuk memastikan sistem prediksi dapat dimonitor, diperbarui, dan ditingkatkan secara berkelanjutan.

---

## Fitur Utama Sistem
- **Prediksi harga beras 7 hari ke depan** menggunakan model machine learning berbasis time-series forecasting.
- **Dashboard monitoring harga** untuk menampilkan harga historis dan hasil prediksi secara visual.
- **Indikator risiko lonjakan harga** yang memberikan peringatan dini apabila terdeteksi potensi kenaikan harga kedepannya.
- **Monitoring performa model** menggunakan metrik evaluasi Mean Absolute Percentage Error (MAPE).
- **Deteksi perubahan distribusi data (data drift)** menggunakan metode Population Stability Index (PSI).
- **Sistem retraining model** yang dapat dipicu secara otomatis apabila performa model menurun atau terjadi perubahan distribusi data yang signifikan.

---

## Arsitektur Sistem

Pipeline sistem terdiri dari beberapa tahap berikut:
```
Data Source
↓
Data Ingestion
↓
Data Cleaning
↓
Feature Engineering
↓
Model Training (XGBoost)
↓
Forecast 7 Hari
↓
Dashboard Monitoring & Early Warning
```
---

## Struktur Direktori Proyek
```
MLOps-PrediksiHargaPangan
│
├── data
│ ├── raw
│ └── processed
│
├── src
│ ├── data
│ │ └── ingestion.py
│ │
│ ├── features
│ │ ├── data_cleaning.py
│ │ └── feature_engineering.py
│ │
│ ├── models
│ │ ├── train_xgboost.py
│ │ └── forecast.py
│ │
│ └── monitoring
│ └── drift_detection.py
│
├── dashboard
│ └── app.py
│
├── models
│ └── xgboost_model.pkl
│
├── notebooks
│ ├── 01_eda.ipynb
│ ├── 02_feature_engineering.ipynb
│ └── 03_model_pipeline.ipynb
│
├── requirements.txt
└── README.md
```
