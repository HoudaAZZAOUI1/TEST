#!/bin/bash
# Smoke tests for deployment validation

set -e

API_URL="${API_URL:-http://localhost:8000}"

echo "Running smoke tests against ${API_URL}"

# Test health endpoint
echo "Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "${API_URL}/health")
if [ "$HEALTH_RESPONSE" != "200" ]; then
    echo "Health check failed with status ${HEALTH_RESPONSE}"
    exit 1
fi
echo "✓ Health check passed"

# Test predict endpoint
echo "Testing predict endpoint..."
PREDICT_RESPONSE=$(curl -s -X POST "${API_URL}/predict" \
    -H "Content-Type: application/json" \
    -d '{"user_id": 1, "viewed_products": [1, 2, 3]}' \
    -o /dev/null -w "%{http_code}")

if [ "$PREDICT_RESPONSE" != "200" ]; then
    echo "Predict endpoint failed with status ${PREDICT_RESPONSE}"
    exit 1
fi
echo "✓ Predict endpoint passed"

# Test metrics endpoint
echo "Testing metrics endpoint..."
METRICS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "${API_URL}/metrics")
if [ "$METRICS_RESPONSE" != "200" ]; then
    echo "Metrics endpoint failed with status ${METRICS_RESPONSE}"
    exit 1
fi
echo "✓ Metrics endpoint passed"

echo "All smoke tests passed!"

