# Supply Chain Disruption Prediction Platform

An AI-powered system for predicting and preventing supply chain disruptions before they happen.

## What This Does

Modern supply chains are complex and vulnerable to all kinds of disruptions - supplier issues, logistics delays, geopolitical events, natural disasters, you name it. Traditional systems are reactive (they only respond after something goes wrong), but this platform is proactive. It uses machine learning to predict which suppliers and routes are at risk BEFORE disruptions occur.

## The Problem We're Solving

The main challenges with supply chains today:
- No early warning system for potential disruptions  
- Limited visibility into supplier and logistics risks
- Can't easily simulate "what if" scenarios
- Slow, manual mitigation planning
- Data scattered across different systems

This platform brings it all together and gives you actionable intelligence.

## Key Features

1. **Risk Prediction** - Predicts disruption probability from event inputs
2. **Dashboard** - Visual overview of event volume and disruption trends
3. **Flask Full-Stack UI** - Multi-page web app with server-rendered HTML templates
4. **Model Performance Tracking** - Dedicated page for accuracy and metric comparison
5. **Analytics** - Trend and risk analysis using chart-based visualizations

## How It Works

The system uses multiple machine learning models (Random Forest, Gradient Boosting, Logistic Regression) trained on an event-based dataset with the core features below:
- Event type
- Severity level
- Cause
- Country
- Financial impact

It picks the best performing model automatically and uses it for predictions.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone this repo:
```bash
git clone https://github.com/rishabh-rb/Supply_Chain_Disruption_Prediction.git
cd Supply_Chain_Disruption_Prediction
```

2. Create a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage

#### Step 1: Generate the Dataset
First, create the synthetic supply chain data:
```bash
python generate_data.py
```

This creates `data/supply_chain_events.csv` with synthetic event records.

#### Step 2: Train the Model
Train the machine learning models:
```bash
python train_model.py
```

This trains multiple models, compares them, and saves the best one. Takes about 1-2 minutes.

#### Step 3: Run the Web App
Launch the Flask web app:
```bash
python app.py
```

The app runs at `http://127.0.0.1:5000`

## Using the Platform

### Dashboard View
- See overall risk metrics across your supply chain
- Geographic risk distribution map
- Risk breakdown by region and product category
- Top 10 riskiest suppliers

### Prediction View
- Enter event details and get instant disruption probability
- See risk classification and recommended action level

### Model Performance View (Admin)
- Compare performance of different ML models
- View confusion matrix and accuracy metrics
- Understand which features are most important for predictions

### Data Analytics View
- Deep dive into historical trends
- Correlation analysis between risk factors
- Supplier and transportation mode analytics
- Summary statistics for high vs low risk suppliers

## Project Structure

```
Supply_Chain_Disruption_Prediction/
├── app.py                      # Flask application with routes
├── train_model.py              # Model training script
├── generate_data.py            # Event dataset generation
├── requirements.txt            # Python dependencies
├── templates/                  # Jinja HTML templates
├── static/                     # CSS assets
├── data/
│   └── supply_chain_events.csv # Generated dataset
└── model/
  ├── disruption_model.pkl    # Best trained model
  ├── scaler.pkl              # Feature scaler
  ├── encoders.pkl            # Label encoders
  ├── features.pkl            # Feature order for inference
  └── metrics.json            # Model performance metrics
```

## Model Performance

The system trains three different model types and automatically selects the best one:
- **Random Forest**: Good for capturing complex non-linear relationships
- **Gradient Boosting**: Strong predictive power, handles imbalanced data well
- **Logistic Regression**: Fast, interpretable baseline

Typical performance metrics:
- Accuracy: 80-85%
- F1-Score: 85-90%
- ROC-AUC: 90-95%

## Technical Details

### Features Used
The model uses these inference features:
- `event_type`
- `severity_level`
- `cause`
- `country`
- `financial_impact`

### Target Variable
Binary classification:
- **1 (High Risk)**: Disruption likely based on multiple risk factors
- **0 (Low Risk)**: Stable, low probability of disruption

## Real-World Applications

This type of system is valuable for:
- **Manufacturers**: Identify supplier vulnerabilities before they cause production delays
- **Retailers**: Ensure product availability by proactively managing supply risks
- **Logistics Companies**: Optimize route planning based on disruption probability
- **Supply Chain Managers**: Make data-driven decisions about supplier diversification

## Future Enhancements

Some ideas for extending this:
- Real-time data integration with ERP systems
- Reinforcement learning for automated mitigation recommendations
- Time-series forecasting for demand prediction
- Network graph analysis for identifying cascading risks
- Integration with external data sources (news, weather APIs, port data)

## Contributing

Feel free to fork this repo and submit pull requests. Some areas that could use work:
- Adding more sophisticated feature engineering
- Implementing ensemble methods
- Building API endpoints for programmatic access
- Adding unit tests
- Improving the UI/UX

## License

This project is open source and available for educational and commercial use.

## Contact

For questions or collaboration:
- GitHub: [@rishabh-rb](https://github.com/rishabh-rb)
- Repository: [Supply_Chain_Disruption_Prediction](https://github.com/rishabh-rb/Supply_Chain_Disruption_Prediction)

---

**Note**: The dataset used in this project is synthetically generated for demonstration purposes. In a production environment, you would integrate with your actual supply chain management systems to get real-time data.
- Key Functions:
  - Data preprocessing.
  - Model training and evaluation.
  - Saving the trained model.

### `app.py`
- Purpose: Runs a web application to serve predictions.
- Key Features:
  - Loads the trained model.
  - Provides an API or web interface for predictions.

### `requirements.txt`
- Contains the list of Python dependencies required to run the project.

### `data/`
- Directory for storing datasets used for training and testing.

### `models/`
- Directory for saving trained models.

### `static/` and `templates/`
- Used for serving static files (CSS, JS) and HTML templates in the web application.

---

## Dependencies

- Python 3.7+
- Flask
- scikit-learn
- pandas
- numpy
- Any other dependencies listed in `requirements.txt`.

Install them using:
```bash
pip install -r requirements.txt
```

---

## Future Work

- Add more advanced machine learning models.
- Improve the web application UI.
- Integrate real-time data sources for predictions.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
