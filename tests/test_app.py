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
