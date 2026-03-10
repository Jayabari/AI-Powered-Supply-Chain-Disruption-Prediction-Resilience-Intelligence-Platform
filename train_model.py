import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
import joblib
import os
import json
from datetime import datetime

print("=" * 60)
print("  SUPPLY CHAIN DISRUPTION PREDICTION MODEL")
print("=" * 60)

# Load data
print("\nLoading event data...")
df = pd.read_csv('data/supply_chain_events.csv')
print(f"Loaded {len(df)} events")

print("\nDistribution:")
print(f"  Disruptions: {df['disruption'].sum()} ({df['disruption'].mean()*100:.1f}%)")
print(f"  Non-disruptions: {(df['disruption']==0).sum()} ({(1-df['disruption'].mean())*100:.1f}%)")

# Prepare features
print("\nPreparing features...")
categorical_cols = ['event_type', 'severity_level', 'cause', 'country']
numerical_cols = ['financial_impact']

# Encode categorical variables
encoders = {}
for col in categorical_cols:
    encoders[col] = LabelEncoder()
    df[col + '_encoded'] = encoders[col].fit_transform(df[col])

# Select features
feature_cols = [col + '_encoded' for col in categorical_cols] + numerical_cols
X = df[feature_cols].copy()
y = df['disruption'].copy()

print(f"Using {len(feature_cols)} features")

# Split data
print("\nSplitting data...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"  Train: {len(X_train)} samples")
print(f"  Test: {len(X_test)} samples")

# Scale features
print("\nScaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train models
print("\nTraining models...")
print("-" * 60)

models = {
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42, max_depth=5),
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000)
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
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
    }

print("\n" + "-" * 60)

# Select best model
best_model_name = max(results.keys(), key=lambda x: results[x]['f1_score'])
best_model = results[best_model_name]['model']

print(f"\nBest: {best_model_name} (F1 = {results[best_model_name]['f1_score']:.3f})")

# Save model
print("\nSaving model...")
os.makedirs('model', exist_ok=True)

joblib.dump(best_model, 'model/disruption_model.pkl')
print("  ✓ model/disruption_model.pkl")

joblib.dump(scaler, 'model/scaler.pkl')
joblib.dump(encoders, 'model/encoders.pkl')
joblib.dump(feature_cols, 'model/features.pkl')

# Save metrics
metrics = {
    'best_model': best_model_name,
    'training_date': datetime.now().isoformat(),
    'dataset_size': len(df),
    'num_features': len(feature_cols),
    'models_performance': {
        name: {
            'accuracy': results[name]['accuracy'],
            'precision': results[name]['precision'],
            'recall': results[name]['recall'],
            'f1_score': results[name]['f1_score'],
            'roc_auc': results[name]['roc_auc'],
            'confusion_matrix': results[name]['confusion_matrix']
        }
        for name in results.keys()
    }
}

with open('model/metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)

print("  ✓ model/metrics.json")

# Print classification report
print("\nClassification Report:\n")
y_pred_best = best_model.predict(X_test_scaled)
print(classification_report(y_test, y_pred_best))

print("=" * 60)
print("  TRAINING COMPLETE!")
print("=" * 60)
