from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd

router = APIRouter()


class GameRequest(BaseModel):
    title: str


@router.post('/data')
def get_game_data(request: GameRequest):
    df = pd.read_csv('./data/steam_shap_uplift.csv')
    game = df.loc[df['title'] == request.title]

    if game.empty:
        return {'error': f'No data found for title: {request.title}'}

    return {
        'title': game['title'].values[0],
        'discount_percent': float(game['discount_percent'].values[0]),
        'conversion_prob': float(game['conversion_prob'].values[0]),
        'shap_uplift': float(game['shap_uplift'].values[0]),
        'is_new_release': int(game['is_new_release'].values[0]),
    }
