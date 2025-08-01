from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import json

load_dotenv()

app = FastAPI()

HF_API_KEY = os.getenv('HF_API_KEY')
HF_MODEL_NAME = os.getenv('HF_MODEL_NAME')

client = InferenceClient(
    model=HF_MODEL_NAME,
    provider='featherless-ai',
    api_key=HF_API_KEY,
)


class GameFeatures(BaseModel):
    title: str
    discount_percent: float
    conversion_prob: float
    shap_uplift: float
    is_new_release: int
    optimal_price: float
    optimal_revenue: float


@app.post('/recommend')
def recommend_pricing(game: GameFeatures):
    prompt = f"""
    You are a pricing optimization expert for video games.
    Based on the following features, provide a 2-3 sentence pricing recommendation:

    Title: {game.title}
    Discount %: {game.discount_percent}
    Predicted Conversion Rate: {game.conversion_prob}
    Uplift from +5% Discount (proxy): {game.shap_uplift}
    Optimal Price: ${game.optimal_price}
    Optimal Revenue: ${game.optimal_revenue}
    New Release: {'Yes' if game.is_new_release else 'No'} 
    """

    try:
        response = client.chat_completion(
            messages=[
                {'role': 'system', 'content': 'You generate pricing strategy summaries for a dashboard'},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.7,
            max_tokens=100
        )
        advice = response.choices[0].message.content.strip()
        return {'recommendation': advice}

    except Exception as e:
        return {'error': str(e)}
