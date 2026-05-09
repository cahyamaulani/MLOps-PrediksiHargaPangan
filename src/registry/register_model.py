import mlflow
from mlflow.tracking import MlflowClient


MODEL_NAME = "harga-pangan-model"


client = MlflowClient()

# ambil experiment default
experiment = client.get_experiment_by_name("Default")

# ambil run terbaru
runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["start_time DESC"],
    max_results=1
)

latest_run = runs[0]

run_id = latest_run.info.run_id

# path model dari run terbaru
model_uri = f"runs:/{run_id}/model"

# register model
result = mlflow.register_model(
    model_uri=model_uri,
    name=MODEL_NAME
)

print("Registered model version:", result.version)

# ubah stage otomatis ke Staging
client.transition_model_version_stage(
    name=MODEL_NAME,
    version=result.version,
    stage="Staging"
)

print("Model promoted to Staging")