import pandas as pd
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

DATA_PATH = os.path.join(BASE_DIR, "data/processed/harga_clean.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data/processed/harga_features.csv")


def load_data():
    """
    Load data hasil preprocessing.
    """
    print("Loading clean dataset...")
    df = pd.read_csv(DATA_PATH)

    # pastikan nama kolom konsisten
    df["tanggal"] = pd.to_datetime(df["tanggal"])
    return df


def create_features(df):
    """
    Membuat fitur time-series:
    - lag (historical values)
    - rolling mean & std
    """

    print("Creating time-series features...")

    # WAJIB: sort berdasarkan komoditas & waktu
    df = df.sort_values(["commodity_id", "tanggal"])

    # LAG FEATURES
    # harga hari sebelumnya
    df["lag_1"] = df.groupby("commodity_id")["Nilai"].shift(1)

    # harga 7 hari lalu
    df["lag_7"] = df.groupby("commodity_id")["Nilai"].shift(7)

    # lag 14 (harga 2 minggu lalu)
    df["lag_14"] = df["Nilai"].shift(14)

    # ROLLING FEATURES
    # rata-rata 7 hari terakhir
    df["rolling_mean_7"] = (
        df.groupby("commodity_id")["Nilai"]
        .rolling(7)
        .mean()
        .reset_index(level=0, drop=True)
    )

    # rolling mean 14 hari (lebih stabil dari 7 hari)
    df["rolling_mean_14"] = df["Nilai"].rolling(14).mean()

    # standar deviasi (volatilitas)
    df["rolling_std_7"] = (
        df.groupby("commodity_id")["Nilai"]
        .rolling(7)
        .std()
        .reset_index(level=0, drop=True)
    )

    # trend (perubahan harga harian)
    df["trend"] = df["Nilai"].diff()

    # DROP NA akibat lag
    df = df.dropna()

    return df


def save_data(df):
    """
    Simpan dataset fitur
    """
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print("Feature dataset saved!")


def run_pipeline():
    df = load_data()
    df = create_features(df)

    print("\nPreview Feature Data:")
    print(df.head())

    save_data(df)


if __name__ == "__main__":
    run_pipeline()