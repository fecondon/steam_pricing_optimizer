from fastapi import APIRouter
import pandas as pd

router = APIRouter()


@router.post('/data')
def get_game_data(title):
    df = pd.read_csv('./data/steam_shap_uplift.csv')
    game = df.loc[df['title'] == title]
    return {
        'title': game['title'],
        'discount_percent': game['discount_percent'],
        'conversion_prob': game['conversion_prob'],
        'shap_uplift': game['shap_uplift'],
        'is_new_release': game['is_new_release'],
    }
