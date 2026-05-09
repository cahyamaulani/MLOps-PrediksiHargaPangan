import mlflow
from mlflow.tracking import MlflowClient

# pakai local tracking
mlflow.set_tracking_uri("file:./mlruns")

# nama experiment
EXPERIMENT_NAME = "Harga Pangan Experiment"

# buat experiment kalau belum ada
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

if experiment is None:
    experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)
else:
    experiment_id = experiment.experiment_id

# set experiment aktif
mlflow.set_experiment(EXPERIMENT_NAME)

client = MlflowClient()

# cari run terbaru
runs = client.search_runs(
    experiment_ids=[experiment_id],
    order_by=["start_time DESC"],
    max_results=1
)

if len(runs) == 0:
    raise Exception("No MLflow runs found!")

latest_run = runs[0]

run_id = latest_run.info.run_id

# model uri
model_uri = f"runs:/{run_id}/model"

# register model
registered_model = mlflow.register_model(
    model_uri=model_uri,
    name="harga-pangan-model"
)

print("Model registered successfully!")
print("Model Version:", registered_model.version)

# pindah ke staging
client.transition_model_version_stage(
    name="harga-pangan-model",
    version=registered_model.version,
    stage="Staging"
)

print("Model moved to STAGING")