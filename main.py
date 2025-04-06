from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

# Define the request format
class Features(BaseModel):
    data: list

# Create the FastAPI app
app = FastAPI()

# Load dataset and train a model (just for demo)
iris = load_iris()
X, y = iris.data, iris.target
model = RandomForestClassifier()
model.fit(X, y)

@app.get("/")
def read_root():
    return {"message": "ML API is working!"}

@app.post("/predict")
def predict(features: Features):
    prediction = model.predict([features.data])
    return {"prediction": int(prediction[0])}
