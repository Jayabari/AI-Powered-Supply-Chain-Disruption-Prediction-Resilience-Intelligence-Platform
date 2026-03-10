import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_supply_chain_events(num_events=650):
    """Generate synthetic supply chain event dataset"""
    
    np.random.seed(42)
    
    event_types = [
        'Port Congestion', 'Supplier Delay', 'Quality Issue', 
        'Natural Disaster', 'Labor Strike', 'Equipment Failure',
        'Geopolitical', 'Cyber Attack', 'Regulatory Change'
    ]
    
    severity_levels = ['Low', 'Medium', 'High', 'Critical']
    
    causes = [
        'Weather', 'Equipment Malfunction', 'Human Error', 'Supplier Fault',
        'Demand Surge', 'Inventory Issue', 'Transportation', 'Documentation',
        'System Failure', 'Policy Change'
    ]
    
    countries = [
        'USA', 'China', 'India', 'Germany', 'Japan',
        'Brazil', 'Mexico', 'Vietnam', 'Thailand', 'Indonesia'
    ]
    
    start_date = datetime(2024, 1, 1)
    
    data = {
        'event_id': [f'EVT-{i:04d}' for i in range(1, num_events + 1)],
        'event_date': [start_date + timedelta(days=int(i * 365 / num_events)) for i in range(num_events)],
        'event_type': np.random.choice(event_types, num_events),
        'severity_level': np.random.choice(severity_levels, num_events),
        'cause': np.random.choice(causes, num_events),
        'affected_product_id': [f'PROD-{np.random.randint(1000, 9999)}' for _ in range(num_events)],
        'affected_supplier_id': [f'SUP-{np.random.randint(100, 999)}' for _ in range(num_events)],
        'country': np.random.choice(countries, num_events),
        'city': [f'City_{np.random.randint(1, 50)}' for _ in range(num_events)],
        'financial_impact': np.random.randint(10000, 500000, num_events),
    }
    
    df = pd.DataFrame(data)
    
    # Calculate disruption label
    severity_weights = {'Low': 0.2, 'Medium': 0.5, 'High': 0.8, 'Critical': 1.0}
    event_type_weights = {
        'Natural Disaster': 1.0, 'Labor Strike': 0.9, 'Port Congestion': 0.8,
        'Geopolitical': 0.7, 'Cyber Attack': 0.85, 'Supplier Delay': 0.6,
        'Quality Issue': 0.5, 'Equipment Failure': 0.6, 'Regulatory Change': 0.4
    }
    cause_weights = {
        'Weather': 0.9, 'Equipment Malfunction': 0.7, 'Human Error': 0.4,
        'Supplier Fault': 0.6, 'Demand Surge': 0.3, 'Inventory Issue': 0.5,
        'Transportation': 0.6, 'Documentation': 0.2, 'System Failure': 0.8,
        'Policy Change': 0.3
    }
    
    disruption_scores = []
    for idx, row in df.iterrows():
        score = (
            severity_weights[row['severity_level']] * 0.4 +
            event_type_weights[row['event_type']] * 0.35 +
            cause_weights[row['cause']] * 0.15 +
            (min(row['financial_impact'], 300000) / 300000) * 0.1
        )
        disruption_scores.append(1 if score > 0.55 else 0)
    
    df['disruption'] = disruption_scores
    
    # Create data directory if needed
    os.makedirs('data', exist_ok=True)
    
    # Save to CSV
    df.to_csv('data/supply_chain_events.csv', index=False)
    
    print("Creating supply chain events dataset...")
    print(f"\n✓ Created {num_events} events")
    print(f"✓ Disruptions: {df['disruption'].sum()} ({df['disruption'].mean()*100:.1f}%)")
    print(f"✓ Non-disruptions: {(df['disruption']==0).sum()} ({(1-df['disruption'].mean())*100:.1f}%)")
    
    print("\nSeverity breakdown:")
    for severity in severity_levels:
        count = (df['severity_level'] == severity).sum()
        print(f"  {severity}: {count} ({count/num_events*100:.1f}%)")
    
    print(f"\nSaved to: data/supply_chain_events.csv")
    print("Done!")

if __name__ == "__main__":
    generate_supply_chain_events()
