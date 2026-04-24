import glob
import os
import pandas as pd


# ==============================
# PATH CONFIGURATION
# ==============================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
OUTPUT_PATH = os.path.join(
    BASE_DIR, "data", "processed", "harga_clean.csv"
)


# ==============================
# LOAD LATEST DATA
# ==============================

def load_latest_data():
    print("Loading latest raw data...")

    files = glob.glob(os.path.join(RAW_DIR, "*.csv"))

    if not files:
        raise FileNotFoundError("No raw data found")

    latest_file = max(files, key=os.path.getctime)

    print("Using file:", latest_file)

    dataframe = pd.read_csv(latest_file)

    print("Total rows:", len(dataframe))

    return dataframe


# ==============================
# CLEAN DATA
# ==============================

def clean_data(dataframe):
    print("\nCleaning data...")

    # hapus duplikasi
    dataframe = dataframe.drop_duplicates()

    # rapikan nama kolom
    dataframe.columns = dataframe.columns.str.strip()

    # konversi tanggal ke datetime
    if "tanggal" in dataframe.columns:
        dataframe["tanggal"] = pd.to_datetime(dataframe["tanggal"])

    # isi missing value
    if "NilaiDiff" in dataframe.columns:
        dataframe["NilaiDiff"] = dataframe["NilaiDiff"].fillna(0)

    # =========================
    # KONVERSI HARGA KE NUMERIK
    # =========================

    # kolom Nilai
    if "Nilai" in dataframe.columns:
        dataframe["Nilai"] = (
            dataframe["Nilai"]
            .astype(str)
            .str.replace("Rp", "", regex=False)
            .str.replace(".", "", regex=False)
            .str.replace(",", "", regex=False)
        )

        dataframe["Nilai"] = pd.to_numeric(dataframe["Nilai"], errors="coerce")

    # kolom NilaiDiff
    if "NilaiDiff" in dataframe.columns:
        dataframe["NilaiDiff"] = (
            dataframe["NilaiDiff"]
            .astype(str)
            .str.replace("Rp", "", regex=False)
            .str.replace(".", "", regex=False)
            .str.replace(",", "", regex=False)
        )

        dataframe["NilaiDiff"] = pd.to_numeric(dataframe["NilaiDiff"], errors="coerce")

    # hapus data penting yang kosong
    dataframe = dataframe.dropna(subset=["Nilai"])

    return dataframe


# ==============================
# SELECT IMPORTANT COLUMNS
# ==============================

def select_columns(dataframe):
    print("\nSelecting important columns...")

    selected_columns = [
        "tanggal",
        "Provinsi",
        "commodity_id",
        "Nilai",
        "NilaiDiff",
    ]

    dataframe = dataframe[selected_columns]

    return dataframe


# ==============================
# SORT TIME-SERIES DATA
# ==============================

def sort_data(dataframe):
    print("\nSorting data...")

    dataframe = dataframe.sort_values(
        by=["commodity_id", "tanggal"]
    )

    return dataframe


# ==============================
# SAVE DATA
# ==============================

def save_data(dataframe):
    print("\nSaving processed data...")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    dataframe.to_csv(OUTPUT_PATH, index=False)

    print("Saved to:", OUTPUT_PATH)


# ==============================
# MAIN PIPELINE
# ==============================

def run_pipeline():
    dataframe = load_latest_data()
    dataframe = clean_data(dataframe)
    dataframe = select_columns(dataframe)
    dataframe = sort_data(dataframe)

    print("\nPreview hasil preprocessing:")
    print(dataframe.head())

    save_data(dataframe)

    print("\nPreprocessing DONE!")


if __name__ == "__main__":
    run_pipeline()