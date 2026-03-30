import requests
import pandas as pd
from datetime import datetime

BASE_URL = "https://www.bi.go.id/hargapangan/WebSite/Home/GetGridData1"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.bi.go.id/hargapangan"
}

def fetch_sample_data():
    today = datetime.today().strftime("%m/%d/%Y")

    all_data = []

    # coba range ID
    for cid in range(1, 30):  
        params = {
            "tanggal": today,
            "commodity": cid,
            "priceType": 1,
            "isPasokan": 1,
            "jenis": 1,
            "periode": 1,
            "provId": 1
        }

        try:
            response = requests.get(BASE_URL, params=params, headers=HEADERS)
            data = response.json().get("data", [])

            if data:
                for row in data:
                    row["commodity_id"] = cid
                all_data.extend(data)

        except:
            pass

    df = pd.DataFrame(all_data)
    return df


if __name__ == "__main__":
    df = fetch_sample_data()

    print("\nJumlah data:", len(df))

    if not df.empty:
        print("\nKolom:", df.columns.tolist())

        # 🔍 tampilkan struktur biar jelas
        print("\nPreview data:")
        print(df.head())

        print("\nPreview transpose (biar keliatan jelas):")
        print(df.head().T)

        # 🔥 cek jumlah kategori komoditas
        if "komoditas" in df.columns:
            print("\nJumlah komoditas unik:", df["komoditas"].nunique())
            print("\nDaftar komoditas:")
            print(df["komoditas"].unique())

        else:
            print("\n⚠ Belum ketemu kolom 'komoditas', cek manual di atas ya!")

        print("\nJumlah komoditas unik:", df["commodity_id"].nunique())

print("\nDaftar commodity_id:")
print(sorted(df["commodity_id"].unique()))