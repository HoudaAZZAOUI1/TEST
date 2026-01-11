# Branch: feature/ml-model

## Purpose
Implement collaborative filtering recommendation model with MLflow tracking.

## Files
- `recommendation_model.py` - ML model implementation
- `tests/test_model.py` - Model tests
- `mlflow/mlproject` - MLflow project config
- `README.md` - This file

## Key Features
- User-item interaction matrix
- Cosine similarity calculations
- Hybrid prediction combining user and item CF
- MLflow tracking for all experiments
- Model evaluation (RMSE, MAE, coverage)
- Save/load functionality

## Usage

```bash
python recommendation_model.py
pytest tests/test_model.py
```

## Training with MLflow

```bash
# Set MLflow tracking URI
export MLFLOW_TRACKING_URI=http://localhost:5000

# Train model
python recommendation_model.py
```

## Testing
Run tests with:
```bash
pytest tests/test_model.py -v
```

