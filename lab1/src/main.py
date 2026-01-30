from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from predict import predict_data

app = FastAPI()

# ---- Request & Response Models ----

class CancerData(BaseModel):
    mean_radius: float
    mean_texture: float
    mean_perimeter: float
    mean_area: float

class PredictionResponse(BaseModel):
    response: int  # 0 = malignant, 1 = benign

# ---- Health Check ----

@app.get("/", status_code=status.HTTP_200_OK)
async def health_ping():
    return {"status": "healthy"}

# ---- Prediction Endpoint ----

@app.post("/predict", response_model=PredictionResponse)
async def predict_cancer(cancer_features: CancerData):
    try:
        features = [[
            cancer_features.mean_radius,
            cancer_features.mean_texture,
            cancer_features.mean_perimeter,
            cancer_features.mean_area
        ]]

        prediction = predict_data(features)
        return PredictionResponse(response=int(prediction[0]))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))