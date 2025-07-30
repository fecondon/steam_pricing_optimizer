import pandas as pd

def test_expected_revenue():
    df = pd.DataFrame({
        'discounted_price': [10.0, 20.0],
        'conversion_prob': [0.5, 0.1]
    })

    df['expected_revenue'] = df['discount_price'] * df['conversion_prob']
    assert df['expected_revenue'].iloc[0] == 5.0
    assert df['expected_revenue'].iloc[1] == 2.0