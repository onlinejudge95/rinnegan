import json


# Test health check passes
def test_health_check_passes(test_app):
    client = test_app.test_client()

    response = client.get("/health", headers={"Accept": "application/json"})
    assert response.status_code == 200

    data = json.loads(response.get_json())
    assert data["health"] == "good"


# Test health check fails
def test_health_check_fails(test_app):
    test_app.config["HEALTHCHECK_FILE_PATH"] = "dummy.txt"
    client = test_app.test_client()

    response = client.get("/health", headers={"Accept": "application/json"})
    assert response.status_code == 404

    data = json.loads(response.get_json())
    assert data["health"] == "bad"


# Test health check fails due to invalid headers
def test_health_check_fails_invalid_headers(test_app):
    test_app.config["HEALTHCHECK_FILE_PATH"] = "dummy.txt"
    client = test_app.test_client()

    response = client.get("/health")
    assert response.status_code == 415

    data = response.get_json()
    assert "application/json" in data["message"]
