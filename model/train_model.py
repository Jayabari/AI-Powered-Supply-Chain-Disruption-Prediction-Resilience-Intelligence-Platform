import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import json

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, classification_report
)

print("\n" + "="*60)
print("  SUPPLY CHAIN DISRUPTION PREDICTION MODEL")
print("="*60 + "\n")

# Load data
print("Loading event data...")
df = pd.read_csv("data/supply_chain_events.csv")
print(f"Loaded {len(df)} events\n")

print("Distribution:")
print(f"  Disruptions: {df['disruption'].sum()} ({df['disruption'].sum()/len(df)*100:.1f}%)")
print(f"  Non-disruptions: {(1-df['disruption']).sum()} ({(1-df['disruption']).sum()/len(df)*100:.1f}%)\n")

# Prepare features
print("Preparing features...")
categorical_cols = ['event_type', 'severity_level', 'cause', 'country']

encoders = {}
for col in categorical_cols:
    encoder = LabelEncoder()
    df[col + '_encoded'] = encoder.fit_transform(df[col])
    encoders[col] = encoder

features = ['event_type_encoded', 'severity_level_encoded', 'cause_encoded', 'country_encoded', 'financial_impact']
print(f"Using {len(features)} features\n")

X = df[features]
y = df['disruption']

# Train test split
print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"  Train: {len(X_train)} samples")
print(f"  Test: {len(X_test)} samples\n")

# Scale features
print("Scaling features...\n")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train multiple models
print("Training models...")
print("-"*60)

models = {
    'Random Forest': RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=150, max_depth=7, random_state=42),
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42)
}

results = {}

for name, model in models.items():
    print(f"\n{name}...")
    model.fit(X_train_scaled, y_train)
    
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc = roc_auc_score(y_test, y_pred_proba)
    conf = confusion_matrix(y_test, y_pred).tolist()
    
    print(f"  Accuracy:  {acc:.3f}")
    print(f"  Precision: {prec:.3f}")
    print(f"  Recall:    {rec:.3f}")
    print(f"  F1:        {f1:.3f}")
    print(f"  ROC-AUC:   {roc:.3f}")
    
    results[name] = {
        'model': model,
        'accuracy': acc,
        'precision': prec,
        'recall': rec,
        'f1_score': f1,
        'roc_auc': roc,
        'confusion_matrix': conf,
        'y_pred': y_pred
    }

print("\n" + "-"*60)

# Select best model
best_name = max(results, key=lambda x: results[x]['f1_score'])
best_model = results[best_name]['model']
best_pred = results[best_name]['y_pred']

print(f"\nBest: {best_name} (F1 = {results[best_name]['f1_score']:.3f})")

# Save model and artifacts
print("\nSaving model...")
joblib.dump(best_model, "model/disruption_model.pkl")
print("  ✓ model/disruption_model.pkl")

joblib.dump(scaler, "model/scaler.pkl")
print("  ✓ model/scaler.pkl")

joblib.dump(encoders, "model/encoders.pkl")
print("  ✓ model/encoders.pkl")

joblib.dump(features, "model/features.pkl")
print("  ✓ model/features.pkl")

# Save metrics
metrics = {
    'best_model': best_name,
    'training_date': datetime.now().isoformat(),
    'dataset_size': len(df),
    'num_features': len(features),
    'models_performance': {
        name: {
            'accuracy': results[name]['accuracy'],
            'precision': results[name]['precision'],
            'recall': results[name]['recall'],
            'f1_score': results[name]['f1_score'],
            'roc_auc': results[name]['roc_auc'],
            'confusion_matrix': results[name]['confusion_matrix']
        }
        for name in results
    }
}

with open('model/metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)
print("  ✓ model/metrics.json")

# Display classification report
print("\nClassification Report:\n")
print(classification_report(y_test, best_pred, target_names=['Manageable', 'Disruption']))

print("="*60)
print("  TRAINING COMPLETE!")
print("="*60 + "\n")
