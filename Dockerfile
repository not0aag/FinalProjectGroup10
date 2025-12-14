# Use official Python runtime as base image
# python:3.8-slim provides a lightweight Python 3.8 environment
FROM python:3.8-slim

# Set working directory in container
# All subsequent commands will be run from this directory
WORKDIR /app

# Copy requirements first for better layer caching
# Docker caches layers, so if requirements don't change, this layer is reused
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir reduces image size by not storing pip cache
RUN pip install --no-cache-dir -r requirements.txt

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy application code to container
# This is done after pip install to leverage Docker layer caching
COPY . .

# Expose port 5000 for the Flask application
# This is a documentation feature; actual port mapping happens at runtime
EXPOSE 5000

# Add healthcheck to monitor container health
# Checks /health endpoint every 30 seconds
# Timeout after 3 seconds, retry up to 3 times
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Command to run the application
# Uses Python to execute app.py
CMD ["python", "app.py"]
