# Branch: feature/kubernetes-monitoring

## Purpose
Deploy to Kubernetes with monitoring and auto-scaling.

## Files
- `k8s/` - Kubernetes manifests
  - `deployment.yaml` - Main deployment
  - `canary-deployment.yaml` - Canary deployment
  - `service.yaml` - Service definition
  - `hpa.yaml` - Auto-scaling
  - `pvc.yaml` - Persistent volumes
- `prometheus/` - Prometheus configuration
  - `prometheus.yml` - Prometheus config
  - `alerts.yml` - Alert rules
- `grafana/` - Grafana configuration
  - `dashboards/` - Pre-built dashboards
    - `api-dashboard.json` - API metrics dashboard
    - `model-dashboard.json` - Model performance dashboard
  - `datasources/` - Datasource configs
    - `prometheus.yml` - Prometheus datasource
- `scripts/` - Automation scripts
  - `retrain_pipeline.py` - Retraining automation
- `README.md` - This file

## Key Features
- Complete K8s deployment configuration
- Auto-scaling based on CPU/memory
- Canary deployment for safe rollouts
- Comprehensive monitoring with Prometheus
- Pre-built Grafana dashboards
- Automated model retraining pipeline
- Alert configurations

## Deployment

### Prerequisites

- Kubernetes cluster (1.20+)
- kubectl configured
- Persistent volumes available

### Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace ecommerce-recommendation

# Deploy ConfigMap
kubectl apply -f k8s/configmap.yaml

# Deploy PersistentVolumeClaims
kubectl apply -f k8s/pvc.yaml

# Deploy main deployment
kubectl apply -f k8s/deployment.yaml

# Deploy service
kubectl apply -f k8s/service.yaml

# Deploy HPA
kubectl apply -f k8s/hpa.yaml

# Check status
kubectl get pods -n ecommerce-recommendation
kubectl get services -n ecommerce-recommendation
kubectl get hpa -n ecommerce-recommendation
```

## Canary Deployment

### Deploy Canary

```bash
# Deploy canary version
kubectl apply -f k8s/canary-deployment.yaml

# Check canary pods
kubectl get pods -l version=canary -n ecommerce-recommendation
```

### Promote Canary

```bash
# Once validated, update main deployment
kubectl set image deployment/recommendation-api \
    recommendation-api=recommendation-api:canary \
    -n ecommerce-recommendation

# Remove canary deployment
kubectl delete deployment recommendation-api-canary \
    -n ecommerce-recommendation
```

## Monitoring

### Prometheus

Prometheus scrapes metrics from all pods with the annotation:
```yaml
prometheus.io/scrape: "true"
prometheus.io/port: "8000"
prometheus.io/path: "/metrics"
```

### Grafana Dashboards

Import dashboards:
1. Access Grafana UI
2. Go to Dashboards > Import
3. Upload `grafana/dashboards/*.json`

Or use provisioning:
```yaml
# Mount dashboards in Grafana deployment
volumeMounts:
  - name: dashboards
    mountPath: /etc/grafana/provisioning/dashboards
```

## Auto-Scaling

### Horizontal Pod Autoscaler (HPA)

The HPA automatically scales pods based on:
- CPU usage (target: 70%)
- Memory usage (target: 80%)

Scaling range: 3-10 replicas

### Manual Scaling

```bash
# Scale deployment
kubectl scale deployment recommendation-api \
    --replicas=5 \
    -n ecommerce-recommendation

# Check HPA status
kubectl get hpa recommendation-api-hpa \
    -n ecommerce-recommendation
```

## Model Retraining

### Automated Retraining

The retraining pipeline can be scheduled via CronJob:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: model-retrain
  namespace: ecommerce-recommendation
spec:
  schedule: "0 0 * * 0"  # Weekly on Sunday
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: retrain
            image: retrain-pipeline:latest
            command: ["python", "retrain_pipeline.py"]
          restartPolicy: OnFailure
```

### Manual Retraining

```bash
# Run retraining script
python scripts/retrain_pipeline.py
```

## Monitoring Dashboards

### API Dashboard

Metrics displayed:
- Request rate
- Error rate
- Response time (95th percentile)
- Active pods

### Model Dashboard

Metrics displayed:
- Recommendation latency
- Recommendations per second
- Model accuracy

## Alerts

Prometheus alerts are configured in `prometheus/alerts.yml`:

- **HighErrorRate** - Error rate > 5% for 5 minutes
- **HighResponseTime** - 95th percentile > 1s for 5 minutes
- **PodCrashLooping** - Pod restarting frequently
- **HighMemoryUsage** - Memory > 90% for 5 minutes
- **HighCPUUsage** - CPU > 80% for 5 minutes
- **DeploymentDown** - Replicas unavailable

## Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -n ecommerce-recommendation

# Check pod logs
kubectl logs <pod-name> -n ecommerce-recommendation

# Describe pod for events
kubectl describe pod <pod-name> -n ecommerce-recommendation
```

### High Resource Usage

```bash
# Check resource usage
kubectl top pods -n ecommerce-recommendation

# Check HPA status
kubectl describe hpa recommendation-api-hpa \
    -n ecommerce-recommendation
```

### Persistent Volume Issues

```bash
# Check PVC status
kubectl get pvc -n ecommerce-recommendation

# Check PV status
kubectl get pv

# Describe PVC
kubectl describe pvc recommendation-models-pvc \
    -n ecommerce-recommendation
```

## Best Practices

✅ Use resource requests and limits
✅ Configure health checks (liveness, readiness, startup)
✅ Enable auto-scaling with HPA
✅ Use persistent volumes for data
✅ Monitor with Prometheus and Grafana
✅ Set up alerting
✅ Use canary deployments
✅ Implement graceful shutdown
✅ Use ConfigMaps for configuration
✅ Secure with network policies

