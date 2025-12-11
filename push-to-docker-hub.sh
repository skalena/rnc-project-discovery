#!/bin/bash

# Script to tag and push the RNC Discover Docker image to Docker Hub
# Usage: ./push-to-docker-hub.sh [TAG]
# Example: ./push-to-docker-hub.sh latest
#          ./push-to-docker-hub.sh v1.0.0

set -e

# Configuration
IMAGE_NAME="rnc-discover"
DOCKER_HUB_USER="edgars"
TAG="${1:-latest}"
LOCAL_IMAGE="${IMAGE_NAME}:${TAG}"
REMOTE_IMAGE="${DOCKER_HUB_USER}/${IMAGE_NAME}:${TAG}"

echo "🐳 Docker Image Push Script"
echo "================================"
echo "Local Image:  ${LOCAL_IMAGE}"
echo "Remote Image: ${REMOTE_IMAGE}"
echo ""

# Check if image exists locally
if ! docker image inspect "${LOCAL_IMAGE}" > /dev/null 2>&1; then
    echo "❌ Error: Image '${LOCAL_IMAGE}' not found locally"
    echo ""
    echo "Please build the image first using:"
    echo "  make build"
    echo "  Or: docker build -t ${LOCAL_IMAGE} ."
    exit 1
fi

# Check if user is logged in to Docker Hub
if ! docker info 2>/dev/null | grep -q "Username"; then
    echo "⚠️  Note: You may not be logged into Docker Hub"
    echo "Please log in first using:"
    echo "  docker login"
    echo ""
fi

# Tag the image
echo "📝 Tagging image as '${REMOTE_IMAGE}'..."
docker tag "${LOCAL_IMAGE}" "${REMOTE_IMAGE}"
echo "✅ Image tagged successfully!"

# Push the image
echo ""
echo "📤 Pushing image to Docker Hub..."
docker push "${REMOTE_IMAGE}"
echo ""
echo "✅ Image pushed successfully!"
echo ""
echo "🎉 Done! Your image is now available at:"
echo "   https://hub.docker.com/r/${DOCKER_HUB_USER}/${IMAGE_NAME}"
