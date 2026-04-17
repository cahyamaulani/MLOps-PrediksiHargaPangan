# Sistem Early Warning dan Prediksi Lonjakan Harga Pangan di Jawa Timur

Proyek ini merupakan implementasi sistem **Early Warning dan Prediksi Lonjakan Harga Pangan di Jawa Timur** yang bertujuan untuk memantau serta memprediksi perubahan harga komoditas pangan. Sistem monitoring fluktuasi harga pangan yang tersedia saat ini umumnya hanya menampilkan data historis tanpa kemampuan prediktif, sehingga sulit untuk mengantisipasi lonjakan harga secara lebih awal. Proyek ini mengembangkan sistem prediksi harga berbasis **Machine Learning Time-Series Forecasting** menggunakan model regresi. Model digunakan untuk memprediksi harga beras hingga **7 hari ke depan** berdasarkan data historis harga. Selain melakukan prediksi harga, sistem juga dilengkapi dengan mekanisme **early warning** untuk mendeteksi potensi kenaikan harga secara lebih dini.

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

# LK-04: Data Acquisition & Preprocessing Pipeline

Pipeline mencakup dua tahap utama:

* **Data Ingestion (Acquisition)**
* **Data Preprocessing (Cleaning)**

---

## Instalasi Dependencies

Pastikan Python sudah terinstall, lalu jalankan:

```bash
pip install -r requirements.txt
```

---

## Ingestion

Script ingestion digunakan untuk mengambil data harga pangan dari API selama **2 tahun terakhir** untuk seluruh komoditas.

Jalankan:

```bash
python src/ingest_data.py
```
output akan tersimpan di: 
```
data/raw/
```
denganormat file:

```
harga_pangan_ALL_YYYYMMDD_HHMMSS.csv
```

---

## Preprocessing

Script preprocessing digunakan untuk membersihkan dan menyiapkan data sebelum digunakan untuk modeling.

Jalankan:

```bash
python src/preprocess.py
```
output akan tersimpan di: 
```
data/processed/harga_clean.csv
```

---

## Struktur Data Output

### 1. Raw Data (`data/raw/`)

Berisi data mentah hasil ingestion:

* Semua komoditas
* Rentang waktu 2 tahun
* Format CSV dengan timestamp

---

### 2. Processed Data (`data/processed/`)

Berisi data yang sudah dibersihkan dan siap digunakan.

Kolom yang digunakan:

* `tanggal` → tanggal data (datetime)
* `Provinsi` → lokasi
* `commodity_id` → ID komoditas
* `Nilai` → harga
* `NilaiDiff` → perubahan harga

---

## Pipeline Overview

1. **Ingestion**

   * Mengambil data dari API per tanggal
   * Menggabungkan semua komoditas
   * Menyimpan ke CSV

2. **Preprocessing**

   * Menghapus duplikasi
   * Handling missing values
   * Konversi tipe data
   * Sorting data time-series

---

---

# LK-05: Data Versioning & Data Lineage (DVC)

Pada tahap ini, proyek mengimplementasikan **Data Version Control (DVC)** untuk mengelola dataset secara terstruktur dan mendukung prinsip **MLOps**, khususnya dalam hal versioning dan reproducibility.

---

## Tujuan Implementasi DVC

- Mengelola dataset secara terpisah dari Git (menghindari penyimpanan file besar di repository)
- Melacak perubahan dataset dari waktu ke waktu (data versioning)
- Mendukung proses **continual learning** dengan penambahan data baru
- Menyediakan transparansi silsilah data (data lineage)

---

## Konsep yang Digunakan

Dalam implementasi ini, penyimpanan data dibagi menjadi dua bagian:
- Git Repository → menyimpan metadata (.dvc)
- MinIO Storage → menyimpan data asli (CSV) - external storage

## Ringkasan Workflow
Ingestion → Update Dataset → dvc add → Git Commit → dvc push

## 👩‍💻 Author

Dwi Cahya Maulani

