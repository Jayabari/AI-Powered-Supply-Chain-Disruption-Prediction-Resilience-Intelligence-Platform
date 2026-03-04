import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


df = pd.read_csv("../data/supply_chain.csv")


df['disruption'] = np.where(
    (df['Availability'] < 20) |
    (df['Stock levels'] < 20) |
    (df['Lead time'] > 20) |
    (df['Defect rates'] > 3) |
    (df['Shipping times'] > 7),
    1, 0
)


df.drop([
    'SKU',
    'Customer demographics',
    'Inspection results'
], axis=1, inplace=True)


categorical_cols = [
    'Product type',
    'Shipping carriers',
    'Supplier name',
    'Location',
    'Transportation modes',
    'Routes'
]

encoder = LabelEncoder()
for col in categorical_cols:
    df[col] = encoder.fit_transform(df[col])


X = df.drop('disruption', axis=1)
y = df['disruption']


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)


y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)
print(classification_report(y_test, y_pred))


joblib.dump(model, "supply_chain_model.pkl")
