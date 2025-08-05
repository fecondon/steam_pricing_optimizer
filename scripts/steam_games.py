from fastapi import APIRouter
import pandas as pd

router = APIRouter()


# Pull list of games from dataset
@router.get('/games')
def get_games():
    df = pd.read_csv('./data/steam_specials.csv')
    return df['title'].unique()
