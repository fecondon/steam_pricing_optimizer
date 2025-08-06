from fastapi import APIRouter
import pandas as pd
import os

router = APIRouter()


# Pull list of games from dataset
@router.get('/games')
def get_games():
    try:
        file_path = './data/steam_specials.csv'
        print('Reading file at:', os.path.abspath(file_path))
        df = pd.read_csv('./data/steam_specials.csv')

        if not os.path.exists(file_path):
            print("❌ File does not exist!")
            return {"error": "File not found"}

        return sorted(df['title'].dropna().unique().tolist())
    except Exception as e:
        return {'error': str(e)}
