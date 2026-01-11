#!/bin/bash

# Script to update Kubernetes manifests with your GHCR image
# Usage: ./setup-images.sh YOUR_USERNAME YOUR_REPO

set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 <GITHUB_USERNAME> <REPO_NAME>"
    echo "Example: $0 john-doe my-repo"
    exit 1
fi

USERNAME=$1
REPO=$2
IMAGE="ghcr.io/${USERNAME}/${REPO}"

echo "🔄 Updating Kubernetes manifests with image: ${IMAGE}"
echo "=================================================="

# Update deployment.yaml
if [ -f deployment.yaml ]; then
    sed -i.bak "s|ghcr.io/YOUR_USERNAME/YOUR_REPO|${IMAGE}|g" deployment.yaml
    echo "✅ Updated deployment.yaml"
fi

# Update canary-deployment.yaml
if [ -f canary-deployment.yaml ]; then
    sed -i.bak "s|ghcr.io/YOUR_USERNAME/YOUR_REPO|${IMAGE}|g" canary-deployment.yaml
    echo "✅ Updated canary-deployment.yaml"
fi

# Create image pull secret instructions
echo ""
echo "📝 Next steps:"
echo "1. Create image pull secret for GHCR:"
echo "   kubectl create secret docker-registry ghcr-secret \\"
echo "     --docker-server=ghcr.io \\"
echo "     --docker-username=${USERNAME} \\"
echo "     --docker-password=\$GITHUB_TOKEN \\"
echo "     --namespace=ecommerce-recommendation"
echo ""
echo "2. Or use a Personal Access Token (PAT):"
echo "   export GITHUB_TOKEN=your_pat_token"
echo "   kubectl create secret docker-registry ghcr-secret \\"
echo "     --docker-server=ghcr.io \\"
echo "     --docker-username=${USERNAME} \\"
echo "     --docker-password=\$GITHUB_TOKEN \\"
echo "     --namespace=ecommerce-recommendation"
echo ""
echo "✅ Setup complete! Your manifests are now configured for: ${IMAGE}"

