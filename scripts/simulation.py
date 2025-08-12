from fastapi import APIRouter
import numpy as np
import pandas as pd
from scipy.special import expit, logit
from pydantic import BaseModel

router = APIRouter()


class SimulationRequest(BaseModel):
    title: str


@router.post('/simulate')
def simulate_game(request: SimulationRequest):
    df = pd.read_csv('./data/steam_shap_uplift.csv')
    game_row = df[df['title'] == request.title].iloc[0]
    game_row['original_price'] = game_row.get('original_price', 29.99)

    def simulate_conversion_curve(game_row, num_points=20, elasticity=1.2, shap_scale=0.5, new_release_boost=0.2, noise_std=0.0):
        # Use existing data as anchor
        base_discount = game_row['discount_percent']
        base_conversion = game_row['conversion_prob']
        is_new = game_row['is_new_release']
        shap_uplift = game_row['shap_uplift']
        original_price = float(game_row.get('original_price', 29.99))

        # Simulate range of discount percentages
        discount_range = np.linspace(0.0, .9, num_points)
        prices = (1 - discount_range) * original_price

        # logit of base conversion
        eps = 1e-6
        base_conv_clipped = np.clip(base_conversion, eps, 1 - eps)
        base_logit = logit(base_conv_clipped)

        # Beta
        beta = -float(elasticity)

        # Compute logit for each price point
        log_price_ratio = np.log(prices / original_price)
        logits = base_logit + beta * log_price_ratio
        logits = logits + (shap_scale * shap_uplift) + (new_release_boost * is_new)

        if noise_std > 0:
            logits = logits + np.random.normal(0, noise_std, size=logits.shape)

        # Simulate conversion curve
        conversion_probs = expit(logits)
        conversion_probs = np.clip(conversion_probs, 0, 1)

        revenues = prices * conversion_probs

        return pd.DataFrame({
            'discount_percent': discount_range,
            'conversion_prob': conversion_probs,
            'price': prices,
            'revenue': revenues
        })

    def simulate_revenue_curve(conversion_df):
        conversion_df['expected_revenue'] = (
            conversion_df['price'] * conversion_df['conversion_prob']
        )
        return conversion_df

    df_sim = simulate_conversion_curve(game_row)
    df_sim = simulate_revenue_curve(df_sim)

    return df_sim.to_dict(orient='records')
