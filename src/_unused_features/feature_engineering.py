import pandas as pd
import os

# PATH
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

DATA_PATH = os.path.join(
    BASE_DIR, "data", "processed", "harga_clean.csv"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR, "data", "processed", "harga_features.csv"
)

# LOAD DATA
def load_data():

    print("Loading clean dataset...")

    df = pd.read_csv(DATA_PATH)

    df["Tanggal"] = pd.to_datetime(df["Tanggal"])

    return df

# FEATURE ENGINEERING
def create_features(df):

    print("Creating time series features...")

    df = df.sort_values("Tanggal")

    df["lag_1"] = df["Nilai"].shift(1)

    df["lag_7"] = df["Nilai"].shift(7)

    df["rolling_mean_7"] = df["Nilai"].rolling(7).mean()

    df["rolling_std_7"] = df["Nilai"].rolling(7).std()

    df = df.dropna()

    return df

# SAVE DATA
def save_data(df):

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    df.to_csv(OUTPUT_PATH, index=False)

    print("Feature dataset saved")

# MAIN
def run_pipeline():

    df = load_data()

    df = create_features(df)

    print("\nPreview Feature Data:")
    print(df.head(15))

    save_data(df)


if __name__ == "__main__":

    run_pipeline()