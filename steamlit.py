import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from causalml.metrics import plot_gain, plot_qini

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('steam_ab_uplift_results.csv')

df = load_data()

# Sidebar controls
st.sidebar.title('Filter Settings')
min_discount = st.sidebar.slider('Minimum Discount (%)', 0, 100, 10)
max_discount = st.sidebar.slider('Maximum Discount (%)', min_discount, 100, 25)
min_uplift = st.sidebar.slider('Minimum Uplift Score', -1.0, 1.0, 0.0)

# Header
st.title('🎮 Steam Price Optimization & Uplift Modeling')
st.markdown('''
This dashboard shows simulation results from a pricing experiment on Steam games. We estimate how discounts influence conversion using causal uplift modeling.
''')

# Filtered data
filtered_df = df[
    (df['discount_percent'] >= min_discount / 100) &
    (df['discount_percent'] <= max_discount / 100) &
    (df['uplift_score'] >= min_uplift)
]

st.subheader('Filtered Game Samplme')
st.dataframe(filtered_df.head(15))

# Plots
st.markdown('### Uplift Gain Curve')
plot_gain(df=df, treatment_col='treatment', outcome_col='converted', treatment_effect_col='uplift_score')
st.pyplot(plt.gcf())
plt.clf()

st.markdown('### Qini Curve')
plot_qini(df=df, treatment_col='treatment', outcome_col='converted', treatment_effect_col='uplift_score')
st.pyplot(plt.gcf())
plt.clf()

# Summary
st.subheader('Takeaways')
st.markdown('''
- **Higher uplift scores** indicate games that respond well to larger discounts.
- Use these curves to **target discounts intelligently**, maximizing ROI.
- Aim to discount only games with high positive uplift for better margin efficiency.
''')
