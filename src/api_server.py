from pathlib import Path
import sys
from typing import Optional, Tuple

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src import logreg as src_logreg


sys.modules.setdefault("logreg", src_logreg)


BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "models" / "phishing_detector.pkl"
VECTORIZER_PATH = BASE_DIR / "data" / "preprocessed_data.pkl"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
_assets: Optional[Tuple[object, object]] = None


class PredictRequest(BaseModel):
    text: str


def _load_assets() -> Tuple[object, object]:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
    if not VECTORIZER_PATH.exists():
        raise FileNotFoundError(f"Vectorizer not found at {VECTORIZER_PATH}")
    model = joblib.load(MODEL_PATH)
    _, _, vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer


def _get_assets() -> Tuple[object, object]:
    global _assets
    if _assets is None:
        _assets = _load_assets()
    return _assets


def _safe_probability(value: object) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (list, tuple, np.ndarray)):
        flat = np.asarray(value).reshape(-1)
        return float(flat[0]) if flat.size else None
    return float(value)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/predict")
def predict(request: PredictRequest) -> dict:
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is required.")
    try:
        model, vectorizer = _get_assets()
    except (FileNotFoundError, ModuleNotFoundError) as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    features = vectorizer.transform([text]).toarray()
    prediction = model.predict(features)[0]
    probability = None
    if hasattr(model, "predict_proba"):
        probability = _safe_probability(model.predict_proba(features)[0])
    return {"prediction": int(prediction), "probability": probability}
