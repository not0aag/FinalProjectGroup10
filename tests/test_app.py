import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello from CI/CD Project' in response.data


def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    
    data = response.get_json()
    
    assert 'status' in data
    assert 'env' in data
    assert data['status'] == 'healthy'
    assert data['env'] in ['development', 'staging', 'production']


def test_health_endpoint_returns_json(client):
    response = client.get('/health')
    assert response.content_type == 'application/json'


def test_invalid_endpoint(client):
    response = client.get('/invalid-route')
    assert response.status_code == 404


def test_home_endpoint_method_not_allowed(client):
    response = client.post('/')
    assert response.status_code == 405
