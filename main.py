"""
main.py
FastAPI app for spam detection with optional Redis caching.

Endpoints:
    POST /predict   -> {"text": "..."} -> {"label": "spam"|"ham", "cached": bool}
    GET  /healthz   -> 200 {"status": "ok"} once model loaded

If REDIS_URL is set and reachable, predictions are cached keyed on the
exact input text. If Redis is unreachable, the app degrades gracefully
to no caching (still returns correct predictions).
"""

import os
import hashlib
import time
import joblib
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

MODEL_PATH = os.getenv("MODEL_PATH", "model.joblib")
REDIS_URL = os.getenv("REDIS_URL", "")       # e.g. redis://cache:6379/0
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour

app = FastAPI(title="Spam Detection API", version="1.1.0")

# Load the model at startup
model = joblib.load(MODEL_PATH)
print(f"Loaded model from {MODEL_PATH}")

# Try to connect to Redis (do not crash if unavailable)
cache = None
if REDIS_URL:
    try:
        cache = redis.Redis.from_url(REDIS_URL, decode_responses=True)
        cache.ping()
        print(f"Connected to Redis at {REDIS_URL}")
    except Exception as e:
        print(f"WARNING: could not connect to Redis ({e}); running without cache")
        cache = None


class PredictRequest(BaseModel):
    text: str


class PredictResponse(BaseModel):
    label: str
    cached: bool = False


def cache_key(text: str) -> str:
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return f"spam:pred:{h}"


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="text must be non-empty")

    key = cache_key(req.text)

    # Cache hit path
    if cache is not None:
        try:
            cached_label = cache.get(key)
            if cached_label:
                return PredictResponse(label=cached_label, cached=True)
        except Exception as e:
            print(f"Redis GET failed: {e}")

    # Cache miss (or no cache): compute prediction
    t0 = time.perf_counter()
    label = model.predict([req.text])[0]
    elapsed_ms = (time.perf_counter() - t0) * 1000
    print(f"Predicted {label} for input in {elapsed_ms:.3f} ms")

    # Store in cache
    if cache is not None:
        try:
            cache.setex(key, CACHE_TTL, label)
        except Exception as e:
            print(f"Redis SET failed: {e}")

    return PredictResponse(label=label, cached=False)