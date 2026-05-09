import pandas as pd


def test_dataset_not_empty():
    """
    Memastikan dataset hasil feature engineering tidak kosong.
    """

    df = pd.read_csv("data/processed/harga_features.csv")

    assert len(df) > 0

def test_required_columns():
    """
    Memastikan fitur penting tersedia.
    """

    df = pd.read_csv("data/processed/harga_features.csv")

    required_columns = [
        "lag_1",
        "lag_7",
        "lag_14",
        "rolling_mean_7",
        "rolling_mean_14",
        "rolling_std_7",
        "trend",
        "Nilai"
    ]

    for col in required_columns:
        assert col in df.columns