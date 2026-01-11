# Branch: feature/containerization

## Purpose
Containerize application with Docker and Docker Compose.

## Files
- `Dockerfile` - Multi-stage build
- `docker-compose.yml` - Local deployment
- `.dockerignore` - Ignore patterns
- `nginx.conf` - Nginx config
- `README.md` - This file

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
