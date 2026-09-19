"""
main.py
FastAPI app for spam detection.
Loads model.joblib at startup and exposes:
    POST /predict   -> {"text": "..."} -> {"label": "spam"|"ham"}
    GET  /healthz   -> 200 {"status": "ok"} once model loaded
"""

import os
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

MODEL_PATH = os.getenv("MODEL_PATH", "model.joblib")

app = FastAPI(title="Spam Detection API", version="1.0.0")

# Load the model at import/startup time.
# If the model file is missing, we let the process fail loudly.
model = joblib.load(MODEL_PATH)
print(f"Loaded model from {MODEL_PATH}")


class PredictRequest(BaseModel):
    text: str


class PredictResponse(BaseModel):
    label: str


@app.get("/healthz")
def healthz():
    """Kubernetes readiness/liveness probe target."""
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="text must be non-empty")
    label = model.predict([req.text])[0]
    return PredictResponse(label=label)