#!/bin/bash
# Integration tests for the recommendation system

set -e

API_URL="${API_URL:-http://localhost:8000}"

echo "Running integration tests against ${API_URL}"

# Test end-to-end recommendation flow
echo "Testing recommendation flow..."

# Create test user
echo "Creating test user recommendations..."
RESPONSE=$(curl -s -X POST "${API_URL}/predict" \
    -H "Content-Type: application/json" \
    -d '{"user_id": 999, "viewed_products": [1, 2, 3]}')

if [ -z "$RESPONSE" ]; then
    echo "Failed to get recommendations"
    exit 1
fi

# Validate response structure
if ! echo "$RESPONSE" | grep -q "recommendations"; then
    echo "Invalid response structure"
    exit 1
fi

echo "✓ Recommendation flow passed"

# Test multiple users
echo "Testing multiple user scenarios..."
for user_id in 1 2 3; do
    RESPONSE=$(curl -s -X POST "${API_URL}/predict" \
        -H "Content-Type: application/json" \
        -d "{\"user_id\": ${user_id}, \"viewed_products\": [${user_id}]}")
    
    if [ -z "$RESPONSE" ]; then
        echo "Failed for user ${user_id}"
        exit 1
    fi
done

echo "✓ Multiple user scenarios passed"

# Test error handling
echo "Testing error handling..."
ERROR_RESPONSE=$(curl -s -X POST "${API_URL}/predict" \
    -H "Content-Type: application/json" \
    -d '{"invalid": "data"}' \
    -o /dev/null -w "%{http_code}")

# Should return error status
if [ "$ERROR_RESPONSE" == "200" ]; then
    echo "Error handling test failed - should reject invalid data"
    exit 1
fi

echo "✓ Error handling passed"

echo "All integration tests passed!"

