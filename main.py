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
        raise HTTPException(status_code=400, detail="Model not found. Choose from: rf, lr, svm")
    
    prediction = models[model_name].predict([features.data])
    return {
        "model_used": model_name,
        "prediction": int(prediction[0])
    }
