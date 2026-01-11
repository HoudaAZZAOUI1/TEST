# Docker Build Testing Guide

## Quick Test Commands

### 1. Test Docker Build Locally

```bash
cd feature/containerization

# Create api_files directory structure (as CI/CD does)
mkdir -p api_files/static
cp ../api-development/app.py api_files/
cp ../api-development/requirements.txt api_files/
cp ../data-preprocessing/data_preprocessing.py api_files/
cp ../ml-model/recommendation_model.py api_files/

# Copy static files if they exist
if [ -d "../api-development/static" ]; then
  cp -r ../api-development/static/* api_files/static/
else
  echo "<!DOCTYPE html><html><body><h1>API Running</h1></body></html>" > api_files/static/index.html
fi

# Build the Docker image
docker build -t recommendation-api:test .

# Test run the container
docker run -d -p 8000:8000 --name test-api recommendation-api:test

# Check if it's running
docker ps

# Check logs
docker logs test-api

# Test the API
curl http://localhost:8000/health

# Clean up
docker stop test-api
docker rm test-api
```

### 2. Test Docker Compose

```bash
cd feature/containerization

# Ensure api_files directory exists (for local build)
mkdir -p api_files/static
cp ../api-development/app.py api_files/ 2>/dev/null || echo "Files will be built from context"
cp ../api-development/requirements.txt api_files/ 2>/dev/null || echo "Files will be built from context"

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f api

# Test services
curl http://localhost:8000/health
curl http://localhost:8000/docs
curl http://localhost:9090  # Prometheus
curl http://localhost:3000  # Grafana (admin/admin)

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### 3. Test with GHCR Image (After CI/CD Push)

```bash
# Login to GHCR (first time)
echo $GITHUB_TOKEN | docker login ghcr.io -u YOUR_USERNAME --password-stdin

# Pull the image
docker pull ghcr.io/YOUR_USERNAME/YOUR_REPO:latest

# Run it
docker run -d -p 8000:8000 --name api-ghcr ghcr.io/YOUR_USERNAME/YOUR_REPO:latest

# Test
curl http://localhost:8000/health

# Clean up
docker stop api-ghcr
docker rm api-ghcr
```

## Troubleshooting

### Issue: "Cannot find module" errors
- Ensure all required files are in `api_files/` directory
- Check that `requirements.txt` includes all dependencies

### Issue: Port already in use
```bash
# Find what's using the port
netstat -ano | findstr :8000  # Windows
lsof -i :8000  # Linux/Mac

# Stop the process or use a different port
```

### Issue: Docker build fails
- Check Docker is running: `docker ps`
- Check Dockerfile syntax
- Review build logs: `docker build --no-cache -t test .`

### Issue: Container exits immediately
```bash
# Check logs
docker logs <container-name>

# Run interactively to debug
docker run -it --rm recommendation-api:test /bin/bash
```

