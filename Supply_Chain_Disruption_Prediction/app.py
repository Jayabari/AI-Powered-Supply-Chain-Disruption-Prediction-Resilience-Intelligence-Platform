import pandas as pd
import joblib

model = joblib.load("model/supply_chain_model.pkl")

df = pd.read_csv("data/supply_chain.csv")


df['disruption'] = (
    (df['Availability'] < 20) |
    (df['Stock levels'] < 20) |
    (df['Lead time'] > 20) |
    (df['Defect rates'] > 3) |
    (df['Shipping times'] > 7)
).astype(int)

df.drop(['SKU','Customer demographics','Inspection results'], axis=1, inplace=True)

from sklearn.preprocessing import LabelEncoder
cat_cols = [
    'Product type',
    'Shipping carriers',
    'Supplier name',
    'Location',
    'Transportation modes',
    'Routes'
]

le = LabelEncoder()
for col in cat_cols:
    df[col] = le.fit_transform(df[col])

X = df.drop('disruption', axis=1)

df['Predicted Risk'] = model.predict(X)

def recommendation(row):
    if row['Predicted Risk'] == 1:
        if row['Stock levels'] < 30:
            return "Increase inventory and reorder early"
        elif row['Lead time'] > 20:
            return "Switch to alternate supplier or route"
        else:
            return "Monitor supplier closely"
    else:
        return "No immediate action required"

df['Recommendation'] = df.apply(recommendation, axis=1)

print(df[['Supplier name','Predicted Risk','Recommendation']].head(10))
