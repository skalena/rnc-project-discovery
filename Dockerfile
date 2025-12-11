# Multi-architecture Docker image for RNC Project Discovery
# Supports: linux/amd64, linux/arm64, linux/arm/v7

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Add metadata labels for multi-architecture support
LABEL org.opencontainers.image.title="RNC Project Discovery"
LABEL org.opencontainers.image.description="Docker-based utility for analyzing Java and JSF projects"
LABEL org.opencontainers.image.authors="skalena"
LABEL org.opencontainers.image.version="1.0.0"

# Install Python dependencies
RUN pip install --no-cache-dir openpyxl javalang

# Copy the script to the container
COPY discover.py .
COPY entrypoint.sh .

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Set the default entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command (can be overridden)
CMD ["--help"]
