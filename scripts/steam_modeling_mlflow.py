import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score, classification_report
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature
import os

# Set MLFlow tracking URI to local server
mlflow.set_tracking_uri('http://127.0.0.1:5000')
mlflow.set_experiment('Steam Game Pricing Optimization')

# Load the data
steam_df = pd.read_csv('steam_model_dataset.csv')

# Select features and target
features = ['discounted_price', 'discount_percent', 'is_new_release']
X = steam_df[features]
y = steam_df['converted']

# Train-Test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)

# Start MLFlow run
with mlflow.start_run() as run:
    print(run.info.run_id)
    model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3)
    model.fit(X_train, y_train)

    # Predict and evaluate
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    # Metrics
    auc = roc_auc_score(y_test, y_proba)
    report = classification_report(y_test, y_pred, output_dict=True)

    # Input sample and signature
    input_example = X_test.sample(1)
    signature = infer_signature(X_train, model.predict(X_train))

    # Log parameters and metrics
    mlflow.log_param('n_estimators', 100)
    mlflow.log_param('learning_rate', 0.1)
    mlflow.log_param('max_depth', 3)
    mlflow.log_metric('auc', auc)
    mlflow.log_metric('precision', report['1']['precision'])
    mlflow.log_metric('recall', report['1']['recall'])
    mlflow.log_metric('f1_score', report['1']['f1-score'])

    # Log model
    mlflow.sklearn.log_model(
        sk_model=model, 
        name='model',
        input_example=input_example,
        signature=signature,
    )

    print(f'Model logged to MLFlow with AUC: {auc}')

# Attach predictions to dataset for simulation
df_pred = steam_df.copy()
df_pred['predicted_prob'] = model.predict_proba(steam_df[features])[:, 1]
df_pred['expected_revenue'] = df_pred['discounted_price'] * df_pred['predicted_prob']

# Save for next step
df_pred.to_csv('steam_simulated_revenue.csv', index=False)
