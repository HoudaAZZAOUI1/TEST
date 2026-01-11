# Branch: feature/containerization

## Purpose
Containerize application with Docker and Docker Compose.

## Files
- `Dockerfile` - Multi-stage build
- `docker-compose.yml` - Local deployment
- `.dockerignore` - Ignore patterns
- `nginx.conf` - Nginx config
- `prometheus.yml` - Prometheus metrics configuration
- `README.md` - This file
- `DOCKER_BUILD_TEST.md` - Testing guide

## Key Features
- Optimized multi-stage Docker build
- Complete docker-compose stack
- MLflow, Prometheus, Grafana services
- Volume persistence for models and data
- Health checks and restart policies

## Usage

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild services
docker-compose up -d --build
```

## Services

- **api** - Recommendation API (port 8000)
- **web** - Nginx web interface (port 80)
- **mlflow** - MLflow tracking server (port 5000)
- **prometheus** - Metrics collection (port 9090)
- **grafana** - Visualization dashboard (port 3000)

## Access Points

- API: http://localhost:8000
- Web UI: http://localhost
- MLflow: http://localhost:5000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

## Docker Build Process

The Docker image is automatically built and pushed to GitHub Container Registry (GHCR) on every push to `main` or `develop` branches via CI/CD.

**Image location:** `ghcr.io/YOUR_USERNAME/YOUR_REPO:latest`

### Local Testing

See `DOCKER_BUILD_TEST.md` for detailed testing instructions.

**Quick test:**
```bash
# Build locally
docker build -t recommendation-api:test .

# Run
docker run -p 8000:8000 recommendation-api:test

# Test
curl http://localhost:8000/health
```

## CI/CD Integration

The Docker build is integrated into the GitHub Actions workflow:
- ✅ Automatic build on push
- ✅ Image pushed to GHCR
- ✅ Multiple tags (latest, branch, commit SHA)
- ✅ Build caching for faster builds
