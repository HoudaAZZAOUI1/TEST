# Branch: feature/ci-cd-pipeline

## Purpose
Implement automated CI/CD with GitHub Actions.

## Files
- `.github/workflows/ci-cd.yml` - Main pipeline
- `.github/workflows/retrain.yml` - Retraining workflow
- `scripts/smoke-test.sh` - Smoke tests
- `scripts/integration-test.sh` - Integration tests
- `scripts/check-canary-health.sh` - Canary validation
- `tests/test_api.py` - API tests
- `README.md` - This file

## Key Features
- Multi-stage CI/CD pipeline
- Automated testing (unit, integration, load)
- Docker image registry
- Canary deployments
- Automatic rollback
- Environment-specific deployments

## Workflows

### CI/CD Pipeline (`ci-cd.yml`)

Triggers on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

Stages:
1. **Test** - Run all unit tests
2. **Build** - Build and push Docker image
3. **Deploy Staging** - Deploy to staging on `develop` branch
4. **Deploy Production** - Deploy to production on `main` branch with canary strategy

### Model Retraining (`retrain.yml`)

Triggers on:
- Weekly schedule (Sunday 00:00 UTC)
- Manual workflow dispatch

Steps:
1. Preprocess data
2. Train model with MLflow
3. Evaluate model performance
4. Deploy new model if metrics improve

## Scripts

### Smoke Tests

Quick validation tests after deployment:

```bash
bash scripts/smoke-test.sh
```

Tests:
- Health endpoint
- Predict endpoint
- Metrics endpoint

### Integration Tests

End-to-end testing of the recommendation system:

```bash
bash scripts/integration-test.sh
```

Tests:
- Recommendation flow
- Multiple user scenarios
- Error handling

### Canary Health Check

Validates canary deployment before promotion:

```bash
bash scripts/check-canary-health.sh
```

Checks:
- Health status
- Response time
- Error rates
- Comparison with production

## Usage

### Setting Up Secrets

Required GitHub secrets:
- `MLFLOW_TRACKING_URI` - MLflow server URL
- `DOCKER_USERNAME` - Docker registry username
- `DOCKER_PASSWORD` - Docker registry password

### Running Tests Locally

```bash
# Smoke tests
export API_URL=http://localhost:8000
bash scripts/smoke-test.sh

# Integration tests
export API_URL=http://localhost:8000
bash scripts/integration-test.sh
```

### Manual Workflow Dispatch

1. Go to GitHub Actions tab
2. Select "Model Retraining" workflow
3. Click "Run workflow"
4. Choose branch and options
5. Click "Run workflow"

## Deployment Strategy

### Staging Deployment

Automatically deploys when code is pushed to `develop` branch.

### Production Deployment (Canary)

1. Deploy canary (10% of traffic)
2. Run smoke tests
3. Check canary health
4. Monitor for 5 minutes
5. If healthy, promote to 100%
6. If unhealthy, rollback

### Rollback

Automatic rollback triggers:
- Health check failures
- High error rates
- Performance degradation

Manual rollback:
```bash
kubectl rollout undo deployment/recommendation-api -n production
```

## Environment Configuration

### Staging

- URL: https://staging.example.com
- Auto-deploy on `develop` branch
- Full test suite

### Production

- URL: https://production.example.com
- Canary deployment
- Health checks and monitoring
- Automatic rollback

## Monitoring

### CI/CD Metrics

Track in GitHub Actions:
- Build success rate
- Test pass rate
- Deployment frequency
- Mean time to recovery

### Deployment Metrics

Monitor:
- Deployment success rate
- Canary promotion rate
- Rollback frequency
- Time to production

## Troubleshooting

### Tests Failing

```bash
# Run tests locally
pytest feature/*/tests/ -v

# Check specific test
pytest feature/api-development/tests/test_api.py::test_health_check -v
```

### Build Failing

```bash
# Test Docker build locally
cd feature/containerization
docker build -t test-image .
```

### Deployment Failing

1. Check GitHub Actions logs
2. Verify secrets are set
3. Check deployment environment status
4. Review canary health metrics

## Best Practices

✅ Run tests before pushing
✅ Use feature branches for development
✅ Merge to `develop` first
✅ Test in staging before production
✅ Monitor canary deployments
✅ Keep deployment scripts updated
✅ Document deployment procedures

