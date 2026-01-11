# E-commerce Recommendation System

Complete ML-based recommendation system with full DevOps pipeline.

## Project Structure

This project is organized into 6 feature branches, each implementing a specific aspect of the system:

```
project/
├── feature/
│   ├── data-preprocessing/       # Branch 1: Data cleaning and preparation
│   ├── ml-model/                 # Branch 2: ML model implementation
│   ├── api-development/          # Branch 3: REST API with FastAPI
│   ├── containerization/         # Branch 4: Docker and Docker Compose
│   ├── ci-cd-pipeline/           # Branch 5: CI/CD with GitHub Actions
│   └── kubernetes-monitoring/    # Branch 6: K8s deployment and monitoring
├── api/                          # API files (legacy, see feature/api-development)
├── data-preprocessing/           # Data preprocessing (legacy, see feature/data-preprocessing)
├── k8s/                          # Kubernetes configs (legacy, see feature/kubernetes-monitoring)
└── README.md                     # This file
```

## Feature Branches

### Branch 1: feature/data-preprocessing
**Purpose**: Clean and prepare Amazon product review data for the recommendation system.

**Key Features**:
- Removes duplicates and handles missing values
- Parses JSON price and category fields
- Creates aggregated user/product features
- Validates data quality
- Saves cleaned dataset with summary statistics

**Files**:
- `data_preprocessing.py` - Main preprocessing pipeline
- `requirements.txt` - Python dependencies
- `tests/test_preprocessing.py` - Unit tests
- `README.md` - Documentation

**Usage**:
```bash
cd feature/data-preprocessing
python data_preprocessing.py
pytest tests/test_preprocessing.py
```

### Branch 2: feature/ml-model
**Purpose**: Implement collaborative filtering recommendation model with MLflow tracking.

**Key Features**:
- User-item interaction matrix
- Cosine similarity calculations
- Hybrid prediction combining user and item CF
- MLflow tracking for all experiments
- Model evaluation (RMSE, MAE, coverage)

**Files**:
- `recommendation_model.py` - ML model implementation
- `tests/test_model.py` - Model tests
- `mlflow/mlproject` - MLflow project config
- `README.md` - Documentation

**Usage**:
```bash
cd feature/ml-model
python recommendation_model.py
pytest tests/test_model.py
```

### Branch 3: feature/api-development
**Purpose**: Build REST API with FastAPI to serve recommendations.

**Key Features**:
- Multiple endpoints (recommend, health, metrics)
- Prometheus metrics collection
- CORS support for web interface
- Interactive web UI for demonstrations
- Error handling and validation

**Files**:
- `app.py` - FastAPI application
- `static/index.html` - Web interface
- `tests/test_api.py` - API tests
- `tests/test_integration.py` - Integration tests
- `requirements.txt` - Dependencies
- `README.md` - Documentation

**Usage**:
```bash
cd feature/api-development
uvicorn app:app --reload
pytest tests/
```

### Branch 4: feature/containerization
**Purpose**: Containerize application with Docker and Docker Compose.

**Key Features**:
- Optimized multi-stage Docker build
- Complete docker-compose stack
- MLflow, Prometheus, Grafana services
- Volume persistence for models and data
- Health checks and restart policies

**Files**:
- `Dockerfile` - Multi-stage build
- `docker-compose.yml` - Local deployment
- `.dockerignore` - Ignore patterns
- `nginx.conf` - Nginx config
- `README.md` - Documentation

**Usage**:
```bash
cd feature/containerization
docker-compose up -d
docker-compose logs -f
```

### Branch 5: feature/ci-cd-pipeline
**Purpose**: Implement automated CI/CD with GitHub Actions.

**Key Features**:
- Multi-stage CI/CD pipeline
- Automated testing (unit, integration, load)
- Docker image registry
- Canary deployments
- Automatic rollback
- Environment-specific deployments

**Files**:
- `.github/workflows/ci-cd.yml` - Main pipeline
- `.github/workflows/retrain.yml` - Retraining workflow
- `scripts/smoke-test.sh` - Smoke tests
- `scripts/integration-test.sh` - Integration tests
- `scripts/check-canary-health.sh` - Canary validation
- `tests/test_api.py` - API tests
- `README.md` - Documentation

**Usage**:
```bash
# Tests run automatically on push
# Manual workflow dispatch available in GitHub Actions
```

### Branch 6: feature/kubernetes-monitoring
**Purpose**: Deploy to Kubernetes with monitoring and auto-scaling.

**Key Features**:
- Complete K8s deployment configuration
- Auto-scaling based on CPU/memory
- Canary deployment for safe rollouts
- Comprehensive monitoring with Prometheus
- Pre-built Grafana dashboards
- Automated model retraining pipeline
- Alert configurations

**Files**:
- `k8s/` - Kubernetes manifests (deployment, service, HPA, PVC)
- `prometheus/` - Prometheus configuration and alerts
- `grafana/` - Grafana dashboards and datasources
- `scripts/retrain_pipeline.py` - Retraining automation
- `README.md` - Documentation

**Usage**:
```bash
cd feature/kubernetes-monitoring
kubectl apply -f k8s/
kubectl get pods -n ecommerce-recommendation
```

## Quick Start

### Local Development

1. **Data Preprocessing**:
```bash
cd feature/data-preprocessing
pip install -r requirements.txt
python data_preprocessing.py
```

2. **Train Model**:
```bash
cd feature/ml-model
pip install -r requirements.txt
python recommendation_model.py
```

3. **Run API**:
```bash
cd feature/api-development
pip install -r requirements.txt
uvicorn app:app --reload
```

4. **Docker Deployment**:
```bash
cd feature/containerization
docker-compose up -d
```

### Production Deployment

1. **Kubernetes**:
```bash
cd feature/kubernetes-monitoring
kubectl apply -f k8s/
```

2. **Monitor**:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

## Development Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit
3. Push to GitHub: `git push origin feature/your-feature`
4. Create PR to `develop`
5. After review, merge to `develop`
6. Test in staging
7. Merge `develop` to `main` for production

## Merge Strategy

### Step 1: Merge to develop
```bash
git checkout develop
git merge feature/data-preprocessing
git merge feature/ml-model
git merge feature/api-development
git merge feature/containerization
git merge feature/ci-cd-pipeline
git merge feature/kubernetes-monitoring
git push origin develop
```

### Step 2: Merge to main
```bash
git checkout main
git merge develop
git push origin main
```

## Testing

Run tests for each branch:
```bash
# Data preprocessing tests
cd feature/data-preprocessing && pytest tests/

# Model tests
cd feature/ml-model && pytest tests/

# API tests
cd feature/api-development && pytest tests/
```

## Monitoring

- **Prometheus**: Metrics collection and alerting
- **Grafana**: Visualization dashboards
- **MLflow**: Experiment tracking and model registry

## Documentation

Each branch has its own README.md with detailed documentation. See:
- `feature/data-preprocessing/README.md`
- `feature/ml-model/README.md`
- `feature/api-development/README.md`
- `feature/containerization/README.md`
- `feature/ci-cd-pipeline/README.md`
- `feature/kubernetes-monitoring/README.md`

## License

[Your License Here]

## Contributing

[Your Contributing Guidelines Here]
