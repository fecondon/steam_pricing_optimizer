import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingClassifier
import mlflow.sklearn
import shap
import joblib

# Load the model from MLFlow
mlflow.set_tracking_uri('http://127.0.0.1:5000')
logged_model_uri = 'runs:/f980da061f4a43a2b0f084f7c2515505/model'
model = mlflow.sklearn.load_model(logged_model_uri)

# Load data
df = pd.read_csv('data/steam_model_dataset.csv')

features = ['discounted_price', 'discount_percent', 'is_new_release']
X = df[features]

# Initialize SHAP
explainer = shap.Explainer(model.predict_proba, X)
shap_values = explainer(X)

# SHAP force plot
shap.initjs()
sample = X.iloc[[0]]
force_plot = shap.force_plot(explainer.expected_value[1], shap_values[0][:, 1], sample)
shap.save_html('docs/force_plot_example.html', force_plot)

# SHAP Uplift Simulation
df_control = df.copy()
df_treatment = df.copy()

treatment = 0.05

df_control['discount_percent'] = df_control['discount_percent']
df_treatment['discount_percent'] = (df_treatment['discount_percent'] + treatment).clip(0, 0.9)

df_control['discounted_price'] = df_control['discount_price']
df_treatment['discounted_price'] = df_treatment['discounted_price'] * (1 - treatment)

X_control = df_control[features]
X_treatment = df_treatment[features]

shap_control = explainer(X_control)
shap_treatment = explainer(X_treatment)

# Estimate Uplift SHAP
shap_diff = shap_treatment.values[:, 1] - shap_control.values[:, 1]
df['shap_uplift'] = shap_diff

# Plot uplift features
avg_uplift_importance = np.abs(shap_treatment.values[:,1 ] - shap_control.values[:, 1]).mean(axis=0)
shap.summary_plot(shap_treatment.values - shap_control.values, X, plot_type='bar', show=False)
plt.title('Uplift Feature Importance')
plt.savefig('docs/shap_uplift.png')
plt.close()

# Save SHAP dataset
df.to_csv('data/steam_shap_uplift.csv', index=False)
print('SHAP explanations completed and saved')
