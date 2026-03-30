import os
import time
from datetime import datetime, timedelta

import pandas as pd
import requests


# ==============================
# CONFIG
# ==============================

BASE_URL = "https://www.bi.go.id/hargapangan/WebSite/Home/GetGridData1"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.bi.go.id/hargapangan"
}


# ==============================
# FETCH DATA PER TANGGAL
# ==============================

def fetch_data_by_date(date, commodity_id):
    """
    Mengambil data harga pangan berdasarkan tanggal dan komoditas.

    Args:
        date (datetime): tanggal yang ingin diambil
        commodity_id (int): ID komoditas

    Returns:
        dict: response JSON dari API
    """

    formatted_date = date.strftime("%m/%d/%Y")

    params = {
        "tanggal": formatted_date,
        "commodity": commodity_id,
        "priceType": 1,
        "isPasokan": 1,
        "jenis": 1,
        "periode": 1,
        "provId": 1,
    }

    response = requests.get(BASE_URL, params=params, headers=HEADERS)
    response.raise_for_status()

    return response.json()


# ==============================
# FETCH DATA 2 TAHUN (ALL COMMODITIES)
# ==============================

def fetch_two_years_all_commodities():
    """
    Mengambil data semua komoditas (1-10) selama 2 tahun terakhir.

    Returns:
        pd.DataFrame: data gabungan semua komoditas
    """

    end_date = datetime.today()
    start_date = end_date - timedelta(days=365 * 2)

    commodity_ids = list(range(1, 11))

    all_data = []
    total_days = (end_date - start_date).days

    print(f"\nTotal hari: {total_days}")
    print(f"Total komoditas: {len(commodity_ids)}\n")

    for cid in commodity_ids:
        print(f"\n===== KOMODITAS {cid} =====")

        current = start_date
        day_count = 0

        while current <= end_date:
            day_count += 1

            print(
                f"[{cid}] {day_count}/{total_days} "
                f"→ {current.date()}"
            )

            try:
                response_data = fetch_data_by_date(current, cid)
                data = response_data.get("data", [])

                if data:
                    for row in data:
                        row["tanggal"] = str(current.date())
                        row["commodity_id"] = cid

                    all_data.extend(data)

            except Exception as error:
                print(
                    f"Error {cid} - {current.date()}: {error}"
                )

            time.sleep(0.2)
            current += timedelta(days=1)

    return pd.DataFrame(all_data)


# ==============================
# SAVE DATA
# ==============================

def save_data(dataframe):
    """
    Menyimpan data ke folder data/raw dengan timestamp.

    Args:
        dataframe (pd.DataFrame): data hasil ingestion
    """

    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..","..")
    )

    data_dir = os.path.join(base_dir, "data", "raw")
    os.makedirs(data_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"harga_pangan_ALL_{timestamp}.csv"

    file_path = os.path.join(data_dir, filename)
    dataframe.to_csv(file_path, index=False)

    print("\nDONE!")
    print("Saved:", file_path)
    print("Total rows:", len(dataframe))


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    df = fetch_two_years_all_commodities()
    save_data(df)