from logtail import LogtailHandler
import logging

# Setup Logtail logging
log_handler = LogtailHandler(source_token="sBC83YBeFFdvdLAQSQWnvkDs")
logger = logging.getLogger(__name__)
logger.handlers = []  # Remove default FastAPI/uvicorn loggers
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

# Request format
class Features(BaseModel):
    data: list
    model_name: str

app = FastAPI()

# Load dataset
iris = load_iris()
X, y = iris.data, iris.target

# Train models
models = {
    "rf": RandomForestClassifier(),
    "lr": LogisticRegression(max_iter=200),
    "svm": SVC()
}
for model in models.values():
    model.fit(X, y)

@app.get("/")
def home():
    return {"message": "Multi-model ML API is working!"}

@app.post("/predict")
def predict(features: Features):
    model_name = features.model_name.lower()
    if model_name not in models:
        logger.warning(f"Invalid model: {model_name}")
        raise HTTPException(status_code=400, detail="Model not found. Choose from: rf, lr, svm")

    prediction = models[model_name].predict([features.data])

    # ✅ Log to Logtail
    logger.info({
        "model": model_name,
        "input": features.data,
        "prediction": int(prediction[0])
    })

    return {
        "model_used": model_name,
        "prediction": int(prediction[0])
    }

