#!/bin/bash

# Script to build and push RNC Discover Docker image to Docker Hub (multi-platform)
# Builds for linux/amd64, linux/arm64, and linux/arm/v7 architectures
# Usage: ./push-to-docker-hub.sh [TAG]
# Example: ./push-to-docker-hub.sh latest
#          ./push-to-docker-hub.sh v1.0.0

set -e

# Configuration
IMAGE_NAME="rnc-discover"
DOCKER_HUB_USER="edgars"
TAG="${1:-latest}"
PLATFORMS="linux/amd64,linux/arm64,linux/arm/v7"
REMOTE_IMAGE="${DOCKER_HUB_USER}/${IMAGE_NAME}:${TAG}"
BUILDER_NAME="multiarch-builder"

echo "🐳 Multi-Platform Docker Hub Push Script"
echo "========================================"
echo ""
echo "Configuration:"
echo "  Docker Hub User: ${DOCKER_HUB_USER}"
echo "  Image Name:     ${IMAGE_NAME}"
echo "  Tag:            ${TAG}"
echo "  Remote Image:   ${REMOTE_IMAGE}"
echo "  Platforms:      ${PLATFORMS}"
echo ""

# Check if buildx is available
if ! docker buildx --help &> /dev/null; then
    echo "❌ Error: Docker buildx is not installed or not available"
    echo ""
    echo "Please ensure you're using:"
    echo "  - Docker Desktop (Mac/Windows), or"
    echo "  - Docker with buildx installed on Linux"
    echo ""
    echo "To install buildx on Linux:"
    echo "  https://github.com/docker/buildx#linux-packages"
    exit 1
fi

# Check if builder exists, create if not
if ! docker buildx ls | grep -q "$BUILDER_NAME"; then
    echo "📝 Creating buildx builder: $BUILDER_NAME"
    docker buildx create --name "$BUILDER_NAME" --use
    echo "✅ Builder created successfully!"
else
    echo "✅ Using existing builder: $BUILDER_NAME"
    docker buildx use "$BUILDER_NAME"
fi

echo ""

# Check if user is logged in to Docker Hub
# Check if credentials file exists with auths section
if [ -f ~/.docker/config.json ]; then
    if grep -q '"auths"' ~/.docker/config.json 2>/dev/null; then
        echo "✅ Docker credentials file found"
    else
        echo "⚠️  Warning: Docker credentials file exists but may not be valid"
    fi
else
    echo "⚠️  Warning: Docker credentials file not found"
    echo "You may need to run: docker login"
fi

echo ""

# Bootstrap the builder
echo "� Bootstrapping builder (this may take a moment)..."
docker buildx inspect "$BUILDER_NAME" --bootstrap > /dev/null 2>&1

echo ""
echo "🏗️  Building for platforms: ${PLATFORMS}"
echo "📤 Building and pushing to Docker Hub..."
echo ""

# Build and push multi-platform image
docker buildx build \
    --platform "${PLATFORMS}" \
    -t "${REMOTE_IMAGE}" \
    --push \
    .

echo ""
echo "✅ Image built and pushed successfully!"
echo ""
echo "🎉 Done! Your image is now available at:"
echo "   https://hub.docker.com/r/${DOCKER_HUB_USER}/${IMAGE_NAME}"
echo ""
echo "📋 To verify multi-platform support:"
echo "   docker buildx imagetools inspect ${REMOTE_IMAGE}"
echo ""
echo "🚀 To pull and use:"
echo "   docker pull ${REMOTE_IMAGE}"
echo "   docker run --rm -v \$(pwd)/my-project:/data ${REMOTE_IMAGE} /data"
