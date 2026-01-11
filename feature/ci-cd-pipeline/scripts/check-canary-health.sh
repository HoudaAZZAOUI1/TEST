#!/bin/bash
# Check canary deployment health before promoting

set -e

CANARY_URL="${CANARY_URL:-http://canary.example.com:8000}"
PRODUCTION_URL="${PRODUCTION_URL:-http://production.example.com:8000}"

echo "Checking canary deployment health..."

# Health check
echo "Checking canary health endpoint..."
CANARY_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" "${CANARY_URL}/health")
if [ "$CANARY_HEALTH" != "200" ]; then
    echo "Canary health check failed with status ${CANARY_HEALTH}"
    exit 1
fi
echo "✓ Canary health check passed"

# Performance check
echo "Checking canary performance..."
RESPONSE_TIME=$(curl -o /dev/null -s -w "%{time_total}" "${CANARY_URL}/health")
MAX_RESPONSE_TIME=1.0

if (( $(echo "$RESPONSE_TIME > $MAX_RESPONSE_TIME" | bc -l) )); then
    echo "Canary response time too high: ${RESPONSE_TIME}s"
    exit 1
fi
echo "✓ Canary performance acceptable (${RESPONSE_TIME}s)"

# Compare with production
echo "Comparing canary with production..."
PROD_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" "${PRODUCTION_URL}/health")
if [ "$PROD_HEALTH" != "200" ]; then
    echo "Production health check failed"
    exit 1
fi

# Check error rates (if metrics available)
echo "Checking error rates..."
CANARY_ERROR_RATE=$(curl -s "${CANARY_URL}/metrics" | grep -o 'http_requests_total{status="500"}' | wc -l || echo "0")

if [ "$CANARY_ERROR_RATE" -gt 10 ]; then
    echo "Canary error rate too high: ${CANARY_ERROR_RATE}"
    exit 1
fi
echo "✓ Error rate acceptable"

echo "Canary deployment is healthy and ready for promotion!"

