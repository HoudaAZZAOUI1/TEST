# Branch: feature/ci-cd-pipeline

## Purpose
Implement automated CI/CD with GitHub Actions.

## Files
- `.github/workflows/ci-cd.yml` - Main pipeline
- `.github/workflows/retrain.yml` - Retraining workflow
- `scripts/smoke-test.sh` - Smoke tests
- `scripts/integration-test.sh` - Integration tests
- `scripts/check-canary-health.sh` - Canary validation
- `scripts/load_test.py` - Load testing script
- `tests/test_api.py` - API tests
- `README.md` - This file

## Setup Instructions

### 1. Enable GitHub Actions

GitHub Actions is automatically enabled when you push the `.github/workflows/` directory.

### 2. Configure Secrets (Required)

Go to your repository Settings → Secrets and variables → Actions, and add:

- `GITHUB_TOKEN` - Automatically provided by GitHub
- `STAGING_URL` (optional) - Staging environment URL
- `PRODUCTION_URL` (optional) - Production environment URL
- `MLFLOW_TRACKING_URI` (optional) - MLflow server URL
- `KUBERNETES_CONFIG` (optional) - Kubernetes config for deployments

### 3. Test Locally

Before pushing, test workflows locally:

```bash
# Install act (GitHub Actions local runner)
# Windows: choco install act-cli
# macOS: brew install act
# Linux: curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run tests
act -j test

# Run specific job
act -j lint
```

### 4. Run Tests Manually

```bash
# Data preprocessing tests
cd feature/data-preprocessing
pytest tests/ -v

# Model tests
cd feature/ml-model
pytest tests/ -v

# API tests
cd feature/api-development
pytest tests/ -v
```

## Workflows

### CI/CD Pipeline (`ci-cd.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Manual workflow dispatch

**Jobs:**

1. **Test** - Runs all tests in parallel matrix
   - Preprocessing tests
   - Model tests
   - API tests
   - Uploads coverage to Codecov

2. **Lint** - Code quality checks
   - flake8 linting
   - black formatting check

3. **Build** - Builds and pushes Docker image
   - Builds multi-stage Docker image
   - Pushes to GitHub Container Registry
   - Uses build cache for faster builds

4. **Deploy Staging** - Deploys to staging
   - Only runs on `develop` branch
   - Deploys to staging environment

5. **Deploy Production** - Deploys to production with canary
   - Only runs on `main` branch
   - Deploys canary version
   - Runs smoke tests
   - Checks canary health
   - Promotes to full deployment if healthy
   - Rolls back on failure

### Model Retraining (`retrain.yml`)

**Triggers:**
- Weekly schedule (Sunday 00:00 UTC)
- Manual workflow dispatch

**Steps:**
1. Preprocess data
2. Train model with MLflow
3. Evaluate model performance
4. Deploy new model if metrics improve

## Scripts

### Smoke Tests (`scripts/smoke-test.sh`)

Quick validation tests after deployment:

```bash
export API_URL=http://localhost:8000
bash scripts/smoke-test.sh
```

Tests:
- Health endpoint
- Predict endpoint
- Metrics endpoint

### Integration Tests (`scripts/integration-test.sh`)

End-to-end testing:

```bash
export API_URL=http://localhost:8000
bash scripts/integration-test.sh
```

### Canary Health Check (`scripts/check-canary-health.sh`)

Validates canary deployment:

```bash
export CANARY_URL=http://canary.example.com:8000
export PRODUCTION_URL=http://production.example.com:8000
bash scripts/check-canary-health.sh
```

### Load Testing (`scripts/load_test.py`)

Load testing for API:

```bash
# Install requests if needed
pip install requests

# Run load test
python scripts/load_test.py --url http://localhost:8000 --requests 100 --concurrency 10

# Test specific endpoint
python scripts/load_test.py --url http://localhost:8000 --endpoint /predict --requests 200 --concurrency 20
```

## Monitoring CI/CD

### View Workflow Runs

1. Go to your repository
2. Click "Actions" tab
3. View workflow runs and logs

### Check Test Coverage

1. After test job completes
2. Coverage reports uploaded to Codecov (if configured)
3. View coverage in Codecov dashboard

### Monitor Deployments

- Staging deployments: Check staging environment URL
- Production deployments: Monitor canary health metrics
- Rollback notifications: Check workflow logs for rollback events

## Troubleshooting

### Tests Failing Locally

```bash
# Install all dependencies
pip install -r feature/data-preprocessing/requirements.txt
pip install -r feature/ml-model/requirements.txt
pip install -r feature/api-development/requirements.txt

# Run tests with verbose output
pytest feature/*/tests/ -v
```

### Docker Build Failing

```bash
# Test Docker build locally
cd feature/containerization
docker build -t test-image .
docker run -p 8000:8000 test-image
```

### GitHub Actions Failing

1. Check workflow logs in Actions tab
2. Verify secrets are configured
3. Check file paths match repository structure
4. Test locally with `act` if possible

### Deployment Failing

1. Check deployment logs
2. Verify environment secrets
3. Check Kubernetes cluster access
4. Verify image exists in registry

## Best Practices

✅ Run tests before pushing
✅ Use feature branches for development
✅ Merge to `develop` first
✅ Test in staging before production
✅ Monitor canary deployments
✅ Keep deployment scripts updated
✅ Document deployment procedures
✅ Review workflow logs regularly

## Next Steps

After CI/CD is working:
1. Configure staging environment
2. Set up production environment
3. Configure monitoring alerts
4. Set up notification channels (Slack, email)
