import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import time

# CONFIG
BASE_URL = "https://www.bi.go.id/hargapangan/WebSite/Home/GetGridData1"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.bi.go.id/hargapangan"
}

# FETCH DATA PER TANGGAL
def fetch_data_by_date(date, commodity_id=1):
    formatted_date = date.strftime("%b %d, %Y")

    params = {
        "tanggal": formatted_date,
        "commodity": commodity_id,
        "priceType": 1,
        "isPasokan": 1,
        "jenis": 1,
        "periode": 1,
        "provId": 01. 
    }

    response = requests.get(BASE_URL, params=params, headers=HEADERS)
    response.raise_for_status()

    return response.json()

# FETCH 2 TAHUN TERAKHIR 
def fetch_last_2_years(commodity_id=1):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365*2)

    total_days = (end_date - start_date).days
    print(f"\nMengambil data dari {start_date.date()} sampai {end_date.date()}")
    print(f"📊 Total hari: {total_days} hari\n")

    all_data = []
    current = start_date
    day_count = 0

    while current <= end_date:
        day_count += 1
        progress = (day_count / total_days) * 100

        print(f"[{day_count}/{total_days}] ({progress:.2f}%) Fetching: {current.date()}")

        try:
            response_data = fetch_data_by_date(current, commodity_id)
            data = response_data.get("data", [])

            for row in data:
                row["tanggal"] = current.date()

            all_data.extend(data)

        except Exception as e:
            print(f"⚠ Error on {current.date()}:", e)

        time.sleep(0.3)  # prevent rate limit
        current += timedelta(days=1)

    print("\n✅ Fetch selesai!\n")
    return pd.DataFrame(all_data)

# SAVE TO data/raw/
def save_data(df, filename="harga_pangan_2tahun.csv"):
    BASE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")
    )

    DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
    os.makedirs(DATA_DIR, exist_ok=True)

    file_path = os.path.join(DATA_DIR, filename)
    df.to_csv(file_path, index=False)

    print("📁 Data saved at:", file_path)
    print("📦 Total rows:", len(df))

# MAIN
if __name__ == "__main__":
    df = fetch_last_2_years(commodity_id=1)
    save_data(df)