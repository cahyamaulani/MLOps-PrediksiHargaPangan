import pandas as pd
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

RAW_DATA_PATH = os.path.join(
    BASE_DIR, "data", "raw", "harga_pangan_2tahun.csv"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR, "data", "processed", "harga_clean.csv"
)

# LOAD DATA
def load_data():

    print("Loading raw dataset...")

    df = pd.read_csv(RAW_DATA_PATH)

    print("Dataset loaded")
    print("Total rows:", len(df))

    return df

# CONVERT INDONESIAN MONTH
def convert_indonesian_month(df):

    month_map = {
        "Jan": "Jan",
        "Feb": "Feb",
        "Mar": "Mar",
        "Apr": "Apr",
        "Mei": "May",
        "Jun": "Jun",
        "Jul": "Jul",
        "Agu": "Aug",
        "Agt": "Aug",
        "Sep": "Sep",
        "Okt": "Oct",
        "Nov": "Nov",
        "Des": "Dec"
    }

    for indo, eng in month_map.items():
        df["Tanggal"] = df["Tanggal"].str.replace(indo, eng, regex=False)

    return df

# DATA CLEANING
def clean_data(df):

    print("Cleaning data...")

    df = df.drop_duplicates()

    # convert Indonesian month
    df = convert_indonesian_month(df)

    # convert date
    df["Tanggal"] = pd.to_datetime(df["Tanggal"], format="%d %b %y")

    # handle missing values
    df["NilaiDiff"] = df["NilaiDiff"].fillna(0)

    df = df.dropna(subset=["Nilai"])

    df = df.sort_values("Tanggal")

    return df

# SELECT COLUMNS
def select_columns(df):

    df = df[
        [
            "Tanggal",
            "Provinsi",
            "Komoditas",
            "Nilai",
            "NilaiDiff"
        ]
    ]

    return df

# SAVE DATA
def save_data(df):

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    df.to_csv(OUTPUT_PATH, index=False)

    print("Clean dataset saved to:")
    print(OUTPUT_PATH)

# MAIN PIPELINE
def run_pipeline():

    df = load_data()

    df = select_columns(df)

    df = clean_data(df)

    save_data(df)

    print("Data cleaning completed!")


if __name__ == "__main__":

    run_pipeline()