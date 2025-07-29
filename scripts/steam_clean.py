import numpy as np
import pandas as pd
from datetime import datetime

# Load raw scraped data
steam_df = pd.read_csv('steam_specials.csv')

# Drop rows with missing prices
steam_df = steam_df.dropna(subset=['discounted_price'])

# Fill missing original price with discounted price / discount_percent
steam_df['original_price'] = steam_df['original_price'].fillna(steam_df['discounted_price'] / steam_df['discount_percent'])

# Convert discount percent to positive percentage
steam_df['discount_percent'] = steam_df['discount_percent'] * -1 / 100

# Feature: Release year
steam_df['release_year'] = steam_df['release_date'].str.extract(r'(\d{4})')
steam_df['release_year'] = pd.to_numeric(steam_df['release_year'], errors='coerce')
steam_df = steam_df.dropna(subset=['release_year'])
steam_df['release_year'] = steam_df['release_year'].astype(int)

# Feature: Released in the last two months
current_year = datetime.now().year
steam_df['is_new_release'] = (steam_df['release_year'] >= current_year - 1).astype(int)

# Simulate Conversion (higher discount + recent = higher change)
np.random.seed(26)
steam_df['conversion_prob'] = (
    0.15 +  # base rate
    0.6 * steam_df['discount_percent'] +
    0.2 * steam_df['is_new_release'] +
    0.1 * np.random.rand(len(steam_df))  # noise
).clip(0, 1)

steam_df['converted'] = np.random.binomial(1, steam_df['conversion_prob'])

# Sort and preview
steam_df = steam_df.sort_values(by='conversion_prob', ascending=False)
print(steam_df.head())

# Save to model-ready CSV
steam_df.to_csv('steam_model_dataset.csv', index=False)
print(f'Saved steam_model_dataset with {len(steam_df)} records')
