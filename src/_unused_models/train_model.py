import pandas as pd
import os
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error
import matplotlib.pyplot as plt

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

DATA_PATH = os.path.join(
    BASE_DIR, "data", "processed", "harga_features.csv"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR, "data", "processed", "prediction_result.csv"
)

# LOAD DATA
def load_data():

    print("Loading dataset...")

    df = pd.read_csv(DATA_PATH)

    df["Tanggal"] = pd.to_datetime(df["Tanggal"])

    return df

# TRAIN TEST SPLIT (TIME SERIES)
def split_data(df):

    train_size = int(len(df) * 0.8)

    train = df.iloc[:train_size]

    test = df.iloc[train_size:]

    print("Train size:", len(train))
    print("Test size:", len(test))

    return train, test

# TRAIN MODEL
def train_model(train, test):

    features = ["lag_1", "lag_7", "rolling_mean_7"]

    X_train = train[features]
    y_train = train["Nilai"]

    X_test = test[features]
    y_test = test["Nilai"]

    model = LinearRegression()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mape = mean_absolute_percentage_error(y_test, predictions)

    print("MAPE:", mape)

    result = test.copy()

    result["Predicted"] = predictions

    return result

# save hasil training
def save_result(result):

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    result.to_csv(OUTPUT_PATH, index=False)

    print("Prediction result saved")

# MAIN PIPELINE
def run_pipeline():

    df = load_data()

    train, test = split_data(df)

    result = train_model(train, test)

    save_result(result)


if __name__ == "__main__":

    run_pipeline()