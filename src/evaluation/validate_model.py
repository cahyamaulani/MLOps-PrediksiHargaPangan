import json

# threshold performa
THRESHOLD = 0.20

# baca metric model terbaru
with open("metrics.json") as f:
    metrics = json.load(f)

mape = metrics["MAPE"]

print("MAPE:", mape)

# validasi model
if mape < THRESHOLD:
    print("Model PASSED validation")
else:
    raise Exception("Model FAILED validation")