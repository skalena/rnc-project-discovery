# RNC Discover - Docker Makefile
# Convenient commands for building and running the Docker container

.PHONY: help build run clean rebuild bash

# Docker image details
IMAGE_NAME := rnc-discover
IMAGE_TAG := latest
CONTAINER_NAME := rnc-discover-container

help:
	@echo "RNC Discover - Docker Makefile"
	@echo ""
	@echo "Available commands:"
	@echo "  make build              Build the Docker image"
	@echo "  make run PROJECT=<path> Run analysis on a project"
	@echo "  make bash               Open bash shell in container"
	@echo "  make clean              Remove the Docker image"
	@echo "  make rebuild            Rebuild the Docker image"
	@echo ""
	@echo "Examples:"
	@echo "  make build"
	@echo "  make run PROJECT=/path/to/java/project"
	@echo "  make run PROJECT=\$$(pwd)/my-project"

build:
	@echo "Building Docker image: $(IMAGE_NAME):$(IMAGE_TAG)"
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .
	@echo "✅ Image built successfully!"

run:
	@if [ -z "$(PROJECT)" ]; then \
		echo "❌ Error: PROJECT variable is required"; \
		echo "Usage: make run PROJECT=/path/to/project"; \
		exit 1; \
	fi
	@echo "Running analysis on: $(PROJECT)"
	docker run --rm \
		-v $(PROJECT):/data \
		$(IMAGE_NAME):$(IMAGE_TAG) /data

bash:
	@echo "Opening bash shell in $(IMAGE_NAME):$(IMAGE_TAG)"
	docker run --rm -it \
		-v $(PWD):/data \
		$(IMAGE_NAME):$(IMAGE_TAG) /bin/bash

clean:
	@echo "Removing Docker image: $(IMAGE_NAME):$(IMAGE_TAG)"
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG) || true
	@echo "✅ Image removed!"

rebuild: clean build
	@echo "✅ Rebuild complete!"

.DEFAULT_GOAL := help
