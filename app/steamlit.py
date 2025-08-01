import streamlit as st
import requests
import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt
from causalml.metrics import plot_gain, plot_qini
from pathlib import Path
import time


# ----------------------------
# Load data & Merge SHAP
# ----------------------------
@st.cache_data
def load_data():
    df_ab = pd.read_csv('data/steam_ab_uplift_results.csv')
    df_shap = pd.read_csv('data/steam_shap_uplift.csv')
    return pd.merge(df_ab, df_shap[['title', 'shap_uplift']], on='title', how='left')


df = load_data()

# ----------------------------
# Sidebar Controls
# ----------------------------
st.sidebar.title('Filter Controls')
st.sidebar.markdown('### Filter Games')
min_discount = st.sidebar.slider('Minimum Discount (%)', 0, 100, 10)
max_discount = st.sidebar.slider('Maximum Discount (%)', min_discount, 100, 25)
min_uplift = st.sidebar.slider('Minimum Uplift Score', -1.0, 1.0, 0.0)

st.sidebar.markdown('---')
st.sidebar.markdown('**Revenue Curve Parameters**')
base_conversion = st.sidebar.slider('Base Conversion Rate', 0.0, 1.0, 0.15, 0.01)
discount_elasticity = st.sidebar.slider('Discount Elasticity', 0.0, 2.0, 0.6, 0.05)
new_release_boost = st.sidebar.slider('New Release Boost', 0.0, 0.5, 0.2, 0.01)

# ----------------------------
# Main Title & Filtered Data
# ----------------------------
st.title('🎮 Steam Price Optimization & Uplift Modeling')
st.caption('Explore the impact of discount pricing strategies on game conversions, uplift, and revenue potential.')

# Filtered data
filtered_df = df[
    (df['discount_percent'] >= min_discount / 100) &
    (df['discount_percent'] <= max_discount / 100) &
    (df['uplift_score'] >= min_uplift)
].sort_values(by='shap_uplift', ascending=False)

st.subheader('Filtered Games Based on Uplift & Discount')
st.dataframe(filtered_df.head(15))

# ----------------------------
# SHAP Feature Visuals
# ----------------------------
st.subheader('Global Feature Importance for Conversion')
#if Path('docs/shap_summary.png'):
#    st.image('docs/shap_summary.png')

st.subheader('Top Drivers of Uplift')
if Path('docs/shap_uplift.png').exists():
    st.image('docs/shap_uplift.png')

try:
    with open('docs/force_plot_example.html') as f:
        st.subheader('Force Plot')
        st.components.v1.html(f.read(), height=300)
except FileNotFoundError:
    st.info('Force plot not found. Run SHAP script to enerate it.')

# ----------------------------
# Revenue Price Curve Plotting
# ----------------------------
st.subheader('Revenue vs. Price Visualization')
selected_game = st.selectbox('Select a game to simulate revenue across prices:', sorted(df['title'].unique()))
game_row = df[df['title'] == selected_game].iloc[0]
base_price = game_row['discounted_price'] / (1 - game_row['discount_percent'])

# Animate the curve if checkbox is enabled
animate = st.checkbox('Animate Revenue Curve', value=False)

price_points = [round(p, 2) for p in np.linspace(base_price * 0.5, base_price * 1.2, 25)]
revenues = []

if animate:
    fig, ax = plt.subplots()
    ax.set_xlabel('Price ($)')
    ax.set_ylabel('Expected Revenue')
    ax.set_title(f'Revenue Curve for: {selected_game}')
    line, = ax.plot([], [], marker='o')

    plot_placeholder = st.empty()

    for i, price in enumerate(price_points):
        discount = 1 - (price / base_price)
        simulated_prob = base_conversion + discount_elasticity * discount + new_release_boost * game_row['is_new_release']
        simulated_prob = min(max(simulated_prob, 0), 1)
        expected_revenue = price * simulated_prob
        revenues.append(expected_revenue)

        line.set_data(price_points[:i+1], revenues)
        ax.relim()
        ax.autoscale_view()
        plot_placeholder.pyplot(fig)
        time.sleep(0.05)

    optimal_idx = int(np.argmax(revenues))
    optimal_price = price_points[optimal_idx]
    optimal_revenue = revenues[optimal_idx]
    ax.axvline(optimal_price, color='red', linestyle='--', label=f'Optimal Price: ${optimal_price:.2f}')
    ax.scatter([optimal_price], [optimal_revenue], color='red')
    ax.legend()
    plot_placeholder.pyplot(fig)
else:
    for price in price_points:
        discount = 1 - (price / base_price)
        simulated_prob = base_conversion + discount_elasticity * discount + new_release_boost * game_row['is_new_release']
        simulated_prob = min(max(simulated_prob, 0), 1)
        expected_revenue = price * simulated_prob
        revenues.append(expected_revenue)

    optimal_idx = int(np.argmax(revenues))
    optimal_price = price_points[optimal_idx]
    optimal_revenue = revenues[optimal_idx]

    fig, ax = plt.subplots()
    ax.plot(price_points, revenues, marker='o')
    ax.axvline(optimal_price, color='red', linestyle='--', label=f'Optimized Price: ${optimal_price:.2f}')
    ax.scatter([optimal_price], [optimal_revenue], color='red')
    ax.set_xlabel('Price ($)')
    ax.set_ylabel('Expected Revenue')
    ax.set_title(f'Revenue Curve for: {selected_game}')
    ax.legend()
    st.pyplot(fig)

# ----------------------------
# LLM Recommendation
# ----------------------------
if st.button('Generate LLM Pricing Advice'):
    payload = {
        'title': str(game_row['title']),
        'discount_percent': float(game_row['discount_percent']),
        'conversion_prob': float(game_row['conversion_prob']),
        'shap_uplift': float(game_row['shap_uplift']),
        'is_new_release': int(game_row['is_new_release']),
        'optimal_price': float(optimal_price),
        'optimal_revenue': float(optimal_revenue)
    }

    try:
        response = requests.post('http://localhost:8000/recommend', json=payload, timeout=10)
        if response.status_code == 200 and 'recommendation' in response.json():
            st.success('LLM Suggestion: ' + response.json()['recommendation'])
        else:
            st.error('Failed to get LLM recommendation.')
    
    except Exception as e:
        st.error(f'LLM API Error: {e}')

# ----------------------------
# Uplift Gain Curve
# ----------------------------
st.markdown('### Uplift Gain Curve')
plot_gain(df=df, treatment_col='treatment', outcome_col='converted', treatment_effect_col='uplift_score')
st.pyplot(plt.gcf())
plt.clf()

# ----------------------------
# Qini Curve
# ----------------------------
st.markdown('### Qini Curve')
plot_qini(df=df, treatment_col='treatment', outcome_col='converted', treatment_effect_col='uplift_score')
st.pyplot(plt.gcf())
plt.clf()

# ----------------------------
# Summary
# ----------------------------
st.subheader('Takeaways')
st.markdown('''
- **Higher uplift scores** indicate games that respond well to larger discounts.
- Use these curves to **target discounts intelligently**, maximizing ROI.
- Aim to discount only games with high positive uplift for better margin efficiency.
''')
