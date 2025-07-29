import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, roc_auc_score
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
steam_df = pd.read_csv('steam_model_dataset.csv')

# Select features and target
features = ['discounted_price', 'discount_percent', 'is_new_release']
X = steam_df[features]
y = steam_df['converted']
print(steam_df['converted'].value_counts())
# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Train model
model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print(classification_report(y_test, y_pred))
print('AUC: ', roc_auc_score(y_test, y_proba))

# Feature Importance plot
feature_importance = pd.Series(model.feature_importances_, index=features)
sns.barplot(x=feature_importance.values, y=feature_importance.index)
plt.title('Feature Importance')
plt.tight_layout()
plt.show()

# Attach predicted probability back to dataset for simulation
df_pred = steam_df.copy()
df_pred['predicted_prob'] = model.predict_proba(steam_df[features])[:, 1]
df_pred['expected_revenue'] = df_pred['discounted_price'] * df_pred['predicted_prob']

# Save for next step
df_pred.to_csv('steam_simulated_revenue.csv', index=False)
