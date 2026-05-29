"""
Modul deteksi data drift menggunakan Population Stability Index (PSI).

Interpretasi PSI:
  PSI < 0.1   → Distribusi stabil, tidak perlu retraining
  PSI 0.1-0.2 → Drift ringan, perlu dipantau
  PSI > 0.2   → Drift signifikan, trigger retraining otomatis
"""

import numpy as np
import pandas as pd


def calculate_psi(expected: pd.Series, actual: pd.Series, bins: int = 10) -> float:
    """
    Menghitung Population Stability Index (PSI) antara dua distribusi data.

    Dipanggil oleh dashboard/app.py:
        psi = calculate_psi(recent_old, recent_actual)

    Args:
        expected : data referensi/lama (misal: harga 30-60 hari lalu)
        actual   : data terkini (misal: harga 30 hari terakhir)
        bins     : jumlah bucket pembagi distribusi (default: 10)

    Returns:
        float: nilai PSI
    """
    expected = expected.dropna()
    actual   = actual.dropna()

    # Buat breakpoints dari gabungan range kedua distribusi
    breakpoints = np.linspace(
        min(expected.min(), actual.min()),
        max(expected.max(), actual.max()),
        bins + 1
    )

    def _proportions(series):
        counts, _ = np.histogram(series, bins=breakpoints)
        props = counts / len(series)
        # Hindari log(0) dengan nilai minimum kecil
        return np.where(props == 0, 1e-6, props)

    expected_props = _proportions(expected)
    actual_props   = _proportions(actual)

    psi = np.sum((actual_props - expected_props) * np.log(actual_props / expected_props))
    return float(psi)


def get_drift_status(psi: float) -> dict:
    """
    Menginterpretasikan nilai PSI menjadi status drift.

    Returns:
        dict dengan keys: psi, level, label, action, trigger_retraining
    """
    if psi < 0.1:
        return {
            "psi": round(psi, 4),
            "level": "stable",
            "label": "Distribusi Stabil",
            "action": "Tidak diperlukan retraining",
            "trigger_retraining": False
        }
    elif psi < 0.2:
        return {
            "psi": round(psi, 4),
            "level": "warning",
            "label": "Drift Ringan",
            "action": "Pantau lebih ketat, pertimbangkan retraining",
            "trigger_retraining": False
        }
    else:
        return {
            "psi": round(psi, 4),
            "level": "critical",
            "label": "Drift Signifikan",
            "action": "Retraining otomatis diperlukan",
            "trigger_retraining": True
        }


def check_drift_from_file(
    data_path: str,
    window_recent: int = 30,
    window_old: int = 30
) -> dict:
    """
    Helper: baca CSV lalu hitung PSI dari dua window waktu.

    Args:
        data_path    : path ke harga_features.csv
        window_recent: jumlah hari terakhir sebagai data aktual
        window_old   : jumlah hari sebelumnya sebagai data referensi

    Returns:
        dict hasil drift detection dari get_drift_status()
    """
    df = pd.read_csv(data_path)
    df["tanggal"] = pd.to_datetime(df["tanggal"])
    df = df.sort_values("tanggal").reset_index(drop=True)

    nilai   = df["Nilai"]
    recent  = nilai.tail(window_recent)
    old     = nilai.iloc[-(window_recent + window_old):-window_recent]

    psi    = calculate_psi(old, recent)
    return get_drift_status(psi)