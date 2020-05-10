import json


# Test health check passes
def test_health_check_passes(test_app):
    client = test_app.test_client()

    response = client.get("/health")
    assert response.status_code == 200

    data = json.loads(response.json)
    assert data["health"] == "good"


# Test health check fails
def test_health_check_fails(test_app):
    test_app.config["HEALTHCHECK_FILE_PATH"] = "dummy.txt"
    client = test_app.test_client()

    response = client.get("/health")
    assert response.status_code == 404

    data = json.loads(response.json)
    assert data["health"] == "bad"
