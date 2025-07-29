import numpy as np
import pandas as pd

from sklearn.metrics import roc_auc_score, classification_report
from causalml.inference.tree import UpliftTreeClassifier
from causalml.metrics import plot_gain, plot_qini

import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Load data
df = pd.read_csv('steam_model_dataset.csv')

# Simulate A/B test
np.random.seed(26)
df['treatment'] = np.random.binomial(1, 0.5, len(df))

# Apply additional 5% discount clipping to 90% off
df['control_discount'] = df['discount_percent']
df['treatment_discount'] = (df['control_discount'] + 0.05).clip(0, 0.9)
df['effective_discount'] = np.where(df['treatment'] == 1, df['treatment_discount'], df['control_discount'])

# Simulated effect on conversion probability
df['conversion_prob'] = 0.15 + 0.6 * df['effective_discount'] + 0.2 * df['is_new_release'] + 0.05 * np.random.rand(len(df))
df['conversion_prob'] = df['conversion_prob'].clip(0, 1)
df['converted'] = np.random.binomial(1, df['conversion_prob'])

# Features
features = ['discounted_price', 'discount_percent', 'is_new_release']
X = df[features].values
treatment = df['treatment'].astype(str).values
y = df['converted'].values

# Uplift modeling
uplift_model = UpliftTreeClassifier(control_name='0', max_depth=5, min_samples_leaf=100)
uplift_model.fit(X=X, treatment=treatment, y=y)
preds = uplift_model.predict(X)
uplift_scores = preds[:, 1] - preds[:, 0]

plot_df = pd.DataFrame({
    'uplift_scores': uplift_scores,
    'treatment': df['treatment'],
    'outcome': df['converted'],
})

# Attah results
df['uplift_score'] = uplift_scores

# Visuals
plot_gain(df=plot_df, treatment_col='treatment', outcome_col='outcome', treatment_effect_col='uplift_score')
plot_qini(df=plot_df, treatment_col='treatment', outcome_col='outcome', treatment_effect_col='uplift_score')
plt.tight_layout()
plt.show()

# Save for dashboard
df.to_csv('steam_ab_uplift_results.csv', index=False)
