#!/bin/bash

# Script to build and push RNC Discover Docker image for multiple platforms
# Usage: ./build-multiarch.sh [TAG] [ACTION]
# Example: ./build-multiarch.sh latest push
#          ./build-multiarch.sh v1.0.0 load
#          ./build-multiarch.sh latest

set -e

# Configuration
DOCKER_HUB_USER="skalena"
IMAGE_NAME="rnc-discover"
TAG="${1:-latest}"
ACTION="${2:-build}"
PLATFORMS="linux/amd64,linux/arm64,linux/arm/v7"
BUILDER_NAME="multiarch-builder"

echo "🐳 Multi-Platform Docker Build Script"
echo "====================================="
echo ""
echo "Configuration:"
echo "  Image:      ${DOCKER_HUB_USER}/${IMAGE_NAME}"
echo "  Tag:        ${TAG}"
echo "  Platforms:  ${PLATFORMS}"
echo "  Action:     ${ACTION}"
echo ""

# Check if buildx is available
if ! docker buildx --help &> /dev/null; then
    echo "❌ Error: Docker buildx is not installed or not available"
    echo "Please ensure you're using Docker Desktop or a Linux system with buildx support"
    exit 1
fi

# Check if builder exists
if ! docker buildx ls | grep -q "$BUILDER_NAME"; then
    echo "📝 Creating buildx builder: $BUILDER_NAME"
    docker buildx create --name "$BUILDER_NAME" --use
else
    echo "✅ Using existing builder: $BUILDER_NAME"
    docker buildx use "$BUILDER_NAME"
fi

# Verify builder is running
echo ""
echo "🔍 Verifying builder..."
docker buildx inspect "$BUILDER_NAME" --bootstrap

echo ""
echo "🏗️  Building for platforms: ${PLATFORMS}"
echo ""

case "${ACTION}" in
    push)
        echo "📤 Building and pushing to Docker Hub..."
        docker buildx build \
            --platform "${PLATFORMS}" \
            -t "${DOCKER_HUB_USER}/${IMAGE_NAME}:${TAG}" \
            --push \
            .
        echo ""
        echo "✅ Successfully pushed to Docker Hub!"
        echo "Image: docker.io/${DOCKER_HUB_USER}/${IMAGE_NAME}:${TAG}"
        ;;
    load)
        echo "⚠️  Load action only works with single platform on some systems"
        echo "Using default platform (current architecture)..."
        docker build -t "${DOCKER_HUB_USER}/${IMAGE_NAME}:${TAG}" .
        echo ""
        echo "✅ Image loaded locally!"
        echo "Run: docker run --rm -v \$(pwd):/data ${DOCKER_HUB_USER}/${IMAGE_NAME}:${TAG} /data"
        ;;
    *)
        echo "🏗️  Building for all platforms (output: image manifest)..."
        docker buildx build \
            --platform "${PLATFORMS}" \
            -t "${DOCKER_HUB_USER}/${IMAGE_NAME}:${TAG}" \
            .
        echo ""
        echo "✅ Build completed!"
        echo ""
        echo "To push the image to Docker Hub, use:"
        echo "  ./build-multiarch.sh ${TAG} push"
        ;;
esac

echo ""
echo "📋 Verify multi-platform image:"
echo "  docker buildx imagetools inspect ${DOCKER_HUB_USER}/${IMAGE_NAME}:${TAG}"
