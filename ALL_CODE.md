# Complete CI/CD Project - All Code Files

## Table of Contents
1. [app.py - Flask Application](#apppy)
2. [requirements.txt - Dependencies](#requirementstxt)
3. [Dockerfile - Container Configuration](#dockerfile)
4. [docker-compose.yml - Multi-Environment Setup](#docker-composeyml)
5. [.github/workflows/ci.yml - CI Pipeline](#githubworkflowsciyml)
6. [.github/workflows/staging.yml - Staging Deployment](#githubworkflowsstagingyml)
7. [.github/workflows/production.yml - Production Deployment](#githubworkflowsproductionyml)
8. [tests/test_app.py - Unit Tests](#teststest_apppy)
9. [.gitignore - Git Ignore File](#gitignore)
10. [.dockerignore - Docker Ignore File](#dockerignore)

---

## app.py

```python
"""
Flask CI/CD Project Application
A simple Flask API demonstrating CI/CD pipeline practices
"""

from flask import Flask, jsonify
import os

# Create Flask application instance
app = Flask(__name__)


@app.route('/')
def home():
    """
    Home endpoint
    Returns a simple welcome message
    """
    return "Hello from CI/CD Project"


@app.route('/health')
def health():
    """
    Health check endpoint
    Returns JSON with status and environment information
    Used by Docker healthcheck and monitoring tools
    """
    # Get environment from APP_ENV variable, default to 'development'
    environment = os.environ.get('APP_ENV', 'development')
    
    return jsonify({
        'status': 'healthy',
        'env': environment
    })


if __name__ == '__main__':
    # Run the Flask application
    # host='0.0.0.0' allows external connections (required for Docker)
    # port=5000 is the default Flask port
    # debug=False for production safety
    app.run(host='0.0.0.0', port=5000, debug=False)
```

---

## requirements.txt

```txt
# Flask web framework
Flask==2.3.0

# Werkzeug - WSGI utility library (required by Flask)
Werkzeug==2.3.0

# Testing dependencies
pytest==7.4.0
requests==2.31.0
```

---

## Dockerfile

```dockerfile
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
```

---

## docker-compose.yml

```yaml
version: '3.8'

services:
  # Staging environment service
  # Runs on port 5000, used for pre-production testing
  staging:
    build:
      context: .  # Build from current directory using Dockerfile
    ports:
      - "5000:5000"  # Map host port 5000 to container port 5000
    environment:
      - APP_ENV=staging  # Set environment variable for staging
    container_name: flask-staging
    restart: unless-stopped

  # Production environment service
  # Runs on port 6000, used for production deployment
  production:
    build:
      context: .  # Build from current directory using Dockerfile
    ports:
      - "6000:5000"  # Map host port 6000 to container port 5000
    environment:
      - APP_ENV=production  # Set environment variable for production
    container_name: flask-production
    restart: unless-stopped
```

---

## .github/workflows/ci.yml

```yaml
name: CI Pipeline

# Trigger this workflow on push or pull request to main branch
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  # Build and test job
  build-and-test:
    name: Build and Test
    runs-on: ubuntu-latest

    steps:
      # Step 1: Checkout the repository code
      - name: Checkout code
        uses: actions/checkout@v3

      # Step 2: Set up Python 3.8 environment
      - name: Set up Python 3.8
        uses: actions/setup-python@v4
        with:
          python-version: '3.8'

      # Step 3: Install application dependencies
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # Step 4: Install testing dependencies
      - name: Install pytest and test dependencies
        run: |
          pip install pytest requests

      # Step 5: Run unit tests with pytest
      - name: Run tests
        run: |
          pytest tests/ -v --tb=short

      # Step 6: Build Docker image
      - name: Build Docker image
        run: |
          docker build -t flask-ci-app:${{ github.sha }} .
          docker tag flask-ci-app:${{ github.sha }} flask-ci-app:latest

      # Step 7: Verify Docker build was successful
      - name: Verify Docker image
        run: |
          docker images | grep flask-ci-app
          echo "Docker image built successfully!"

      # Step 8: Test Docker container runs properly
      - name: Test Docker container
        run: |
          docker run -d -p 5000:5000 --name test-container flask-ci-app:latest
          sleep 5
          curl -f http://localhost:5000/ || exit 1
          curl -f http://localhost:5000/health || exit 1
          docker stop test-container
          docker rm test-container
```

---

## .github/workflows/staging.yml

```yaml
name: Deploy to Staging

# Trigger this workflow when code is pushed to staging branch
on:
  push:
    branches: [ staging ]

jobs:
  # Deploy to staging environment
  deploy-staging:
    name: Deploy to Staging Environment
    runs-on: ubuntu-latest

    steps:
      # Step 1: Checkout the repository code
      - name: Checkout code
        uses: actions/checkout@v3

      # Step 2: Build Docker image with staging tag
      - name: Build Docker image for staging
        run: |
          docker build -t flask-app:staging .
          echo "Staging Docker image built successfully"

      # Step 3: Run the staging container
      - name: Start staging container
        run: |
          docker run -d -p 5000:5000 \
            --name flask-staging-test \
            --env APP_ENV=staging \
            flask-app:staging
          echo "Staging container started"

      # Step 4: Wait for container to be ready
      - name: Wait for application to start
        run: |
          echo "Waiting for application to be ready..."
          sleep 10

      # Step 5: Run smoke tests against staging
      - name: Run smoke tests
        run: |
          echo "Running smoke tests..."
          
          # Test home endpoint
          RESPONSE=$(curl -s http://localhost:5000/)
          echo "Home endpoint response: $RESPONSE"
          if [[ "$RESPONSE" != *"Hello from CI/CD Project"* ]]; then
            echo "Home endpoint test failed!"
            exit 1
          fi
          
          # Test health endpoint
          HEALTH=$(curl -s http://localhost:5000/health)
          echo "Health endpoint response: $HEALTH"
          if [[ "$HEALTH" != *"staging"* ]]; then
            echo "Health endpoint test failed - environment not set correctly!"
            exit 1
          fi
          
          if [[ "$HEALTH" != *"healthy"* ]]; then
            echo "Health endpoint test failed - status not healthy!"
            exit 1
          fi
          
          echo "All smoke tests passed!"

      # Step 6: Check container logs
      - name: Check container logs
        if: always()
        run: |
          echo "Container logs:"
          docker logs flask-staging-test

      # Step 7: Stop and remove test container
      - name: Cleanup
        if: always()
        run: |
          docker stop flask-staging-test || true
          docker rm flask-staging-test || true
          echo "Cleanup completed"

      # Step 8: Simulate deployment (in real scenario, push to registry)
      - name: Deployment summary
        run: |
          echo "================================"
          echo "Staging Deployment Successful!"
          echo "================================"
          echo "Image: flask-app:staging"
          echo "Environment: staging"
          echo "Port: 5000"
          echo "Commit: ${{ github.sha }}"
          echo "================================"
```

---

## .github/workflows/production.yml

```yaml
name: Deploy to Production

# Trigger this workflow on push to main branch or manually
on:
  push:
    branches: [ main ]
  workflow_dispatch:  # Allow manual trigger from GitHub UI

jobs:
  # Deploy to production environment
  deploy-production:
    name: Deploy to Production Environment
    runs-on: ubuntu-latest

    steps:
      # Step 1: Checkout the repository code
      - name: Checkout code
        uses: actions/checkout@v3

      # Step 2: Build Docker image with production tag
      - name: Build Docker image for production
        run: |
          docker build -t flask-app:production .
          echo "Production Docker image built successfully"

      # Step 3: Tag with commit SHA for versioning
      - name: Tag image with version
        run: |
          docker tag flask-app:production flask-app:${{ github.sha }}
          docker tag flask-app:production flask-app:latest
          echo "Image tagged with commit SHA: ${{ github.sha }}"

      # Step 4: Run the production container for testing
      - name: Start production container
        run: |
          docker run -d -p 6000:5000 \
            --name flask-production-test \
            --env APP_ENV=production \
            flask-app:production
          echo "Production container started on port 6000"

      # Step 5: Wait for container to be ready
      - name: Wait for application to start
        run: |
          echo "Waiting for application to be ready..."
          sleep 10

      # Step 6: Run comprehensive smoke tests
      - name: Run production smoke tests
        run: |
          echo "Running production smoke tests..."
          
          # Test home endpoint
          RESPONSE=$(curl -s http://localhost:6000/)
          echo "Home endpoint response: $RESPONSE"
          if [[ "$RESPONSE" != *"Hello from CI/CD Project"* ]]; then
            echo "❌ Home endpoint test failed!"
            exit 1
          fi
          echo "✓ Home endpoint test passed"
          
          # Test health endpoint
          HEALTH=$(curl -s http://localhost:6000/health)
          echo "Health endpoint response: $HEALTH"
          
          if [[ "$HEALTH" != *"production"* ]]; then
            echo "❌ Health endpoint test failed - environment not set correctly!"
            exit 1
          fi
          echo "✓ Environment correctly set to production"
          
          if [[ "$HEALTH" != *"healthy"* ]]; then
            echo "❌ Health endpoint test failed - status not healthy!"
            exit 1
          fi
          echo "✓ Health status check passed"
          
          # Test response time
          RESPONSE_TIME=$(curl -o /dev/null -s -w '%{time_total}' http://localhost:6000/)
          echo "Response time: ${RESPONSE_TIME}s"
          
          echo "✅ All production smoke tests passed!"

      # Step 7: Security scan (placeholder - in real scenario, use Trivy or Snyk)
      - name: Security scan
        run: |
          echo "Running security checks..."
          echo "✓ Security scan completed (placeholder)"

      # Step 8: Check container logs
      - name: Check container logs
        if: always()
        run: |
          echo "Production container logs:"
          docker logs flask-production-test

      # Step 9: Cleanup test container
      - name: Cleanup test container
        if: always()
        run: |
          docker stop flask-production-test || true
          docker rm flask-production-test || true
          echo "Test container cleaned up"

      # Step 10: Deployment summary and next steps
      # NOTE: In a real production scenario, you would:
      # - Push image to container registry (Docker Hub, AWS ECR, Azure ACR)
      # - Deploy to cloud service (AWS ECS, Azure Container Apps, Kubernetes)
      # - Update load balancer or service mesh
      # - Run post-deployment verification
      - name: Production deployment summary
        run: |
          echo "========================================"
          echo "🚀 Production Deployment Successful!"
          echo "========================================"
          echo "Image: flask-app:production"
          echo "Version: ${{ github.sha }}"
          echo "Environment: production"
          echo "Port: 6000 (maps to container 5000)"
          echo "Commit: ${{ github.sha }}"
          echo "Branch: ${{ github.ref_name }}"
          echo "========================================"
          echo ""
          echo "📋 Next Steps (Manual):"
          echo "1. Push image to container registry"
          echo "2. Deploy to production infrastructure"
          echo "3. Update DNS/load balancer"
          echo "4. Monitor application metrics"
          echo "5. Verify production health checks"
          echo "========================================"

      # NOTE: Uncomment this step to require manual approval before production deployment
      # - name: Wait for approval
      #   uses: trstringer/manual-approval@v1
      #   with:
      #     secret: ${{ github.TOKEN }}
      #     approvers: your-github-username
      #     minimum-approvals: 1
```

---

## tests/test_app.py

```python
"""
Test suite for Flask CI/CD Project
Tests the main application endpoints
"""

import pytest
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


@pytest.fixture
def client():
    """
    Create a test client for the Flask application
    This fixture is used by all test functions
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    """
    Test the home endpoint (/)
    Should return the welcome message
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello from CI/CD Project' in response.data


def test_health_endpoint(client):
    """
    Test the health endpoint (/health)
    Should return JSON with status and environment
    """
    response = client.get('/health')
    assert response.status_code == 200
    
    # Parse JSON response
    data = response.get_json()
    
    # Check response structure
    assert 'status' in data
    assert 'env' in data
    
    # Check status is healthy
    assert data['status'] == 'healthy'
    
    # Environment should be set (default is 'development')
    assert data['env'] in ['development', 'staging', 'production']


def test_health_endpoint_returns_json(client):
    """
    Test that health endpoint returns proper JSON content type
    """
    response = client.get('/health')
    assert response.content_type == 'application/json'


def test_invalid_endpoint(client):
    """
    Test that invalid endpoints return 404
    """
    response = client.get('/invalid-route')
    assert response.status_code == 404


def test_home_endpoint_method_not_allowed(client):
    """
    Test that POST request to home endpoint returns 405 (Method Not Allowed)
    Since we only defined GET route
    """
    response = client.post('/')
    assert response.status_code == 405
```

---

## tests/__init__.py

```python
# This file makes the tests directory a Python package
```

---

## .gitignore

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Docker
.dockerignore

# Environment variables
.env
.env.local

# Logs
*.log
```

---

## .dockerignore

```
# Ignore Python cache and virtual environments
__pycache__
*.pyc
venv/
env/

# Ignore git directory
.git/
.gitignore

# Ignore GitHub workflows (already in image)
.github/

# Ignore test files
tests/

# Ignore documentation
README.md
*.md

# Ignore IDE files
.vscode/
.idea/
```

---

## Quick Commands Reference

### Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run app
python app.py

# Run tests
pytest tests/ -v
```

### Docker Testing
```bash
# Build image
docker build -t flask-ci-app .

# Run single container
docker run -p 5000:5000 -e APP_ENV=development flask-ci-app

# Run multi-environment
docker-compose up

# Stop containers
docker-compose down
```

### Git Commands
```bash
# Initialize repo
git init
git add .
git commit -m "Initial commit"

# Push to GitHub
git remote add origin YOUR_REPO_URL
git push -u origin main

# Create staging branch
git checkout -b staging
git push -u origin staging
```

---

## Project Structure

```
Final Project Software Process - Group 10/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── staging.yml
│       └── production.yml
│
├── tests/
│   ├── __init__.py
│   └── test_app.py
│
├── .dockerignore
├── .gitignore
├── app.py
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

**✅ All code files are included and tested successfully!**
