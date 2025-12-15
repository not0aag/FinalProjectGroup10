import requests, time

def test_health_response_time():
    start = time.time()
    r = requests.get("http://localhost:5000/health")
    elapsed = time.time() - start

    assert r.status_code == 200
    assert elapsed < 0.2
