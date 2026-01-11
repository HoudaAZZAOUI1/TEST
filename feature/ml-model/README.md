# Branch: feature/ml-model

## Purpose
Implement collaborative filtering recommendation model with MLflow tracking.

## Files
- `recommendation_model.py` - ML model implementation with MLflow integration
- `run_experiments.py` - Hyperparameter tuning script
- `model_registry.py` - Model registry management script
- `tests/test_model.py` - Model tests
- `mlflow/mlproject` - MLflow project configuration
- `mlflow/conda.yaml` - Conda environment for MLflow
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

## MLflow Setup

### 1. Start MLflow Server

**Option A: Using Docker Compose (Recommended)**
```bash
cd feature/containerization
docker-compose up mlflow -d
# MLflow UI: http://localhost:5000
```

**Option B: Local MLflow Server**
```bash
mlflow server --host 0.0.0.0 --port 5000
# MLflow UI: http://localhost:5000
```

### 2. Train Model with MLflow

```bash
# Set MLflow tracking URI
export MLFLOW_TRACKING_URI=http://localhost:5000

# Train model (single experiment)
cd feature/ml-model
python recommendation_model.py
```

### 3. Run Hyperparameter Experiments

```bash
# Run multiple experiments with different hyperparameters
python run_experiments.py --data-path data/cleaned_data.csv --register-best

# This will:
# - Run 5 experiments with different hyperparameters
# - Track all metrics in MLflow
# - Register the best model to Model Registry
# - Promote best model to Production
```

### 4. Model Registry Management

```bash
# List all model versions
python model_registry.py list

# Get latest Production model
python model_registry.py latest --stage Production

# Promote a model version to Production
python model_registry.py promote --version 1

# Archive a model version
python model_registry.py archive --version 2

# Compare two model versions
python model_registry.py compare --version1 1 --version2 2
```

## MLflow Features

- ✅ **Experiment Tracking**: All runs tracked with parameters and metrics
- ✅ **Model Registry**: Version control for models
- ✅ **Model Stages**: Staging, Production, Archived
- ✅ **Hyperparameter Tuning**: Automated experiments with different parameters
- ✅ **Model Comparison**: Compare different model versions
- ✅ **Artifact Storage**: Models and artifacts stored in MLflow

## Testing
Run tests with:
```bash
pytest tests/test_model.py -v
```

