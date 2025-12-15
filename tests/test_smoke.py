import os
import pytest
import requests

CI = os.getenv("CI") == "true"

@pytest.mark.skipif(CI, reason="CI environment does not run Docker containers")
def test_health_endpoint():
    r = requests.get("http://localhost:5000/health")
    assert r.status_code == 200
