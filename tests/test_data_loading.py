import pandas as pd
import os


def test_steam_data_exists():
    assert os.path.exists('data/steam_specials.csv')


def test_data_has_expected_columns():
    df = pd.read_csv('data/steam_model_dataset.csv', nrows=5)
    expected_cols = ['discounted_price', 'discount_percent', 'is_new_release']
    assert expected_cols.issubset(df.columns)
