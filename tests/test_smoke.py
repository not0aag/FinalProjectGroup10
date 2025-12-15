import requests

def test_health_endpoint():
    r = requests.get("http://localhost:5000/health")
    assert r.status_code == 200
