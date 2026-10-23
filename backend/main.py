import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from .schemas import (
    OrderPredictionInput,
    RegressionResponse,
    ClassificationResponse,
    HealthResponse
)
app = FastAPI(
    title="Sales Prediction API",
    description="Production-grade API for Profit Prediction and Return Risk Classification",
    version="1.0.0"
)

# Enable CORS for local frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REGRESSION_MODEL = None
CLASSIFICATION_MODEL = None

REG_MODEL_PATH = "models/profit_regression.joblib"
CLF_MODEL_PATH = "models/return_classifier.joblib"

@app.on_event("startup")
def load_models():
    global REGRESSION_MODEL, CLASSIFICATION_MODEL
    if os.path.exists(REG_MODEL_PATH):
        REGRESSION_MODEL = joblib.load(REG_MODEL_PATH)
        print("Loaded profit regression model.")
    else:
        print(f"Warning: {REG_MODEL_PATH} not found.")

    if os.path.exists(CLF_MODEL_PATH):
        CLASSIFICATION_MODEL = joblib.load(CLF_MODEL_PATH)
        print("Loaded return classification model.")
    else:
        print(f"Warning: {CLF_MODEL_PATH} not found.")

@app.get("/health", response_model=HealthResponse)
def health_check():
    return {
        "status": "healthy" if (REGRESSION_MODEL and CLASSIFICATION_MODEL) else "degraded",
        "regression_model_loaded": REGRESSION_MODEL is not None,
        "classification_model_loaded": CLASSIFICATION_MODEL is not None
    }

@app.post("/predict/regression", response_model=RegressionResponse)
def predict_profit(payload: OrderPredictionInput):
    if not REGRESSION_MODEL:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Regression model is not loaded."
        )
    try:
        input_df = pd.DataFrame([payload.model_dump()])
        prediction = REGRESSION_MODEL.predict(input_df)[0]
        return {
            "predicted_profit_inr": round(float(prediction), 2),
            "currency": "INR",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/predict/classification", response_model=ClassificationResponse)
def predict_return(payload: OrderPredictionInput):
    if not CLASSIFICATION_MODEL:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Classification model is not loaded."
        )
    try:
        input_df = pd.DataFrame([payload.model_dump()])
        prediction_code = CLASSIFICATION_MODEL.predict(input_df)[0]
        probabilities = CLASSIFICATION_MODEL.predict_proba(input_df)[0]
        
        prob_return = round(float(probabilities[1]), 4)
        prob_keep = round(float(probabilities[0]), 4)
        label = "Yes" if prediction_code == 1 else "No"

        return {
            "predicted_returned": label,
            "return_probability": prob_return,
            "keep_probability": prob_keep,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")