import os
import mlflow.pyfunc
from mlflow.tracking import MlflowClient
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow-server:5000")
MODEL_NAME          = os.getenv("MODEL_NAME", "harga-pangan-model")
MODEL_STAGE         = os.getenv("MODEL_STAGE", "Production")

app = FastAPI(title="API Prediksi Harga Pangan Jawa Timur", version="1.0.0")

model = None

# TIDAK ada @app.on_event("startup") — server langsung ready


def get_model():
    """Load model on-demand, cache di variable global."""
    global model
    if model is None:
        try:
            mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
            model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/{MODEL_STAGE}")
            logger.info("Model loaded!")
        except Exception as e:
            logger.warning(f"Model tidak bisa dimuat: {e}")
    return model


class PredictRequest(BaseModel):
    lag_1:           float
    lag_7:           float
    lag_14:          float
    rolling_mean_7:  float
    rolling_mean_14: float
    rolling_std_7:   float
    trend:           float
    year:            int
    month:           int
    dayofweek:       int

class ForecastRequest(PredictRequest):
    days: Optional[int] = 7


@app.get("/")
def root():
    return {
        "service": "API Prediksi Harga Pangan Jawa Timur",
        "status": "running",
        "mlflow_uri": MLFLOW_TRACKING_URI
    }


@app.get("/health")
def health():
    mlflow_ok = False
    try:
        import socket
        # Cek koneksi ke mlflow-server port 5000 dengan timeout 2 detik
        sock = socket.create_connection(("mlflow-server", 5000), timeout=2)
        sock.close()
        mlflow_ok = True
    except Exception:
        pass

    return {
        "api_status": "ok",
        "model_loaded": model is not None,
        "mlflow_connected": mlflow_ok,
        "mlflow_uri": MLFLOW_TRACKING_URI
    }


@app.get("/model-info")
def model_info():
    try:
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        versions = MlflowClient().get_latest_versions(MODEL_NAME, stages=[MODEL_STAGE])
        if not versions:
            return {"detail": "Tidak ada model di stage Production"}
        v = versions[0]
        return {"model_name": v.name, "version": v.version,
                "stage": v.current_stage, "run_id": v.run_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict")
def predict(req: PredictRequest):
    m = get_model()
    if m is None:
        raise HTTPException(status_code=503, detail="Model belum tersedia")
    pred = m.predict(pd.DataFrame([req.dict()]))
    return {"predicted_price": round(float(pred[0]), 2), "unit": "IDR/kg"}


@app.post("/forecast")
def forecast(req: ForecastRequest):
    m = get_model()
    if m is None:
        raise HTTPException(status_code=503, detail="Model belum tersedia")

    days    = min(req.days, 7)
    current = req.dict()
    current.pop("days")
    results = []
    recent  = [current["lag_1"]]

    for _ in range(days):
        pred = float(m.predict(pd.DataFrame([current]))[0])
        results.append(round(pred, 2))
        current["lag_14"] = current["lag_7"]
        current["lag_7"]  = current["lag_1"]
        current["lag_1"]  = pred
        current["trend"]  = pred - recent[-1]
        recent.append(pred)
        current["rolling_mean_7"]  = round(float(np.mean(recent[-7:])), 2)
        current["rolling_std_7"]   = round(float(np.std(recent[-7:])), 2)
        current["rolling_mean_14"] = round(float(np.mean(recent[-14:])), 2)
        current["dayofweek"]       = (current["dayofweek"] + 1) % 7

    change_pct = (max(results) - req.lag_1) / req.lag_1 * 100
    warning = None
    if change_pct > 10:
        warning = f"⚠️ Potensi lonjakan harga {change_pct:.1f}% dalam {days} hari!"
    elif change_pct > 5:
        warning = f"⚠️ Kenaikan harga {change_pct:.1f}% dalam {days} hari."

    return {"forecast": results, "days": days, "unit": "IDR/kg", "warning": warning}