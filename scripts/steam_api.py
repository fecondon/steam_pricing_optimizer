from fastapi import FastAPI
from pydantic import BaseModel
import mlflow.sklearn
import pandas as pd
import numpy as np
import uvicorn

# Load the model from MLFlow
mlflow.set_tracking_uri('http://127.0.0.1:5000')
logged_model_uri = 'runs:/f980da061f4a43a2b0f084f7c2515505/model'
model = mlflow.sklearn.load_model(logged_model_uri)

# Define app
app = FastAPI(title='Steam Game Price Optimizer API')


# Define input schema
class GameFeatures(BaseModel):
    discounted_price: float
    discount_percent: float
    is_new_release: int


# Define predict endpoint
@app.post('/predict')
def predict_conversion(data: GameFeatures):
    input_df = pd.DataFrame([data.dict()])
    prob = model.predict_proba(input_df)[:, 1][0]
    expected_revenue = data.discounted_price * prob
    return {
        'predicted_conversion_probability': round(prob, 4),
        'expected_revenue': round(expected_revenue, 2)
    }


# Run with: uvicorn steam_app:app --reload
if __name__ == '__main__':
    uvicorn.run('steam_api:app', host='0.0.0.0', port=8000,)
