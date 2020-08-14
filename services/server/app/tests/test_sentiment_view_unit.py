import json

from app.api.sentiment import views
from app.tests import mock_objects


# Test sentiment creation passes
def test_add_sentiment(test_app, monkeypatch):
    monkeypatch.setattr(views, "get_user_by_id", mock_objects.get_user_by_id)
    monkeypatch.setattr(views, "add_sentiment", mock_objects.add_sentiment)
    monkeypatch.setattr(
        views,
        "is_user_sentiment_quota_exhausted",
        mock_objects.user_sentiment_quota_not_exhausted,
    )

    client = test_app.test_client()
    response = client.post(
        "/sentiment",
        data=json.dumps({"user_id": 1, "keyword": "test_keyword"}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 201

    data = response.get_json()
    assert "id" in data.keys()
    assert "test_keyword" in data["message"]


# Test sentiment creation fails due to empty data
def test_add_sentiment_empty_data(test_app, monkeypatch):
    monkeypatch.setattr(views, "get_user_by_id", mock_objects.get_user_by_id)
    monkeypatch.setattr(views, "add_sentiment", mock_objects.add_sentiment)

    client = test_app.test_client()
    response = client.post(
        "/sentiment",
        data=json.dumps({}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 400

    data = response.get_json()
    assert "Input payload validation failed" in data["message"]


# Test sentiment creation fails due to invalid data
def test_add_sentiment_invalid_data(test_app, monkeypatch):
    monkeypatch.setattr(views, "get_user_by_id", mock_objects.get_user_by_id)
    monkeypatch.setattr(views, "add_sentiment", mock_objects.add_sentiment)

    client = test_app.test_client()
    response = client.post(
        "/sentiment",
        data=json.dumps({"user_id": 1}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 400

    data = response.get_json()
    assert "Input payload validation failed" in data["message"]


# Test sentiment creation fails due to unregistered user
def test_add_sentiment_unregistered_user(test_app, monkeypatch):
    monkeypatch.setattr(
        views, "get_user_by_id", mock_objects.get_no_user_by_id
    )
    monkeypatch.setattr(views, "add_sentiment", mock_objects.add_sentiment)

    client = test_app.test_client()
    response = client.post(
        "/sentiment",
        data=json.dumps({"user_id": 1, "keyword": "test_keyword"}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 403

    data = response.get_json()
    assert "user is not registered" in data["message"], data


# Test sentiment creation fails due to exceeding quota
def test_add_sentiment_exceeding_quota(test_app, monkeypatch):
    monkeypatch.setattr(views, "get_user_by_id", mock_objects.get_user_by_id)
    monkeypatch.setattr(
        views,
        "is_user_sentiment_quota_exhausted",
        mock_objects.user_sentiment_quota_exhausted,
    )
    monkeypatch.setattr(views, "add_sentiment", mock_objects.add_sentiment)

    client = test_app.test_client()
    response = client.post(
        "/sentiment",
        data=json.dumps({"user_id": 1, "keyword": "test_keyword"}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 403

    data = response.get_json()
    assert "exhausted the quota for keywords" in data["message"], data


# Test sentiment creation fails due to invalid content-type header
def test_add_sentiment_invalid_header(test_app):
    client = test_app.test_client()
    response = client.post(
        "/sentiment",
        data=json.dumps({"user_id": 1}),
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 415

    data = response.get_json()
    assert "define Content-Type header" in data["message"]

    response = client.post(
        "/sentiment",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 415

    data = response.get_json()
    assert "supported is application/json" in data["message"]


# Test fetching sentiment list passes
def test_get_sentiments(test_app, monkeypatch):
    monkeypatch.setattr(
        views, "get_user_id_by_token", mock_objects.get_user_id_by_token,
    )
    monkeypatch.setattr(
        views, "get_all_sentiments", mock_objects.get_all_sentiments
    )

    client = test_app.test_client()
    response = client.get(
        "/sentiment",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer access_token",
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 2
    assert 1 == data[0]["user_id"]
    assert "test_keyword_one" in data[0]["keyword"]

    assert 1 == data[1]["user_id"]
    assert "test_keyword_two" in data[1]["keyword"]


# Test fetching sentiment list fails due to missing token
def test_get_sentiments_missing_token(test_app):
    client = test_app.test_client()

    response = client.get("/sentiment", headers={"Accept": "application/json"})
    assert response.status_code == 403

    data = response.get_json()
    assert "Token required" in data["message"]


# Test fetching sentiment list fails due to expired token
def test_get_sentiments_expired_token(test_app, monkeypatch):
    monkeypatch.setattr(
        views,
        "get_user_id_by_token",
        mock_objects.get_expired_token_exception,
    )

    client = test_app.test_client()

    response = client.get(
        "/sentiment",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer access_token",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Token expired" in data["message"]


# Test fetching sentiment list fails due to invalid token
def test_get_sentiments_invalid_token(test_app, monkeypatch):
    monkeypatch.setattr(
        views,
        "get_user_id_by_token",
        mock_objects.get_invalid_token_exception,
    )
    client = test_app.test_client()

    response = client.get(
        "/sentiment",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer access_token",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Invalid token" in data["message"]


# Test fetching single sentiment passes
def test_single_sentiment(test_app, monkeypatch):
    monkeypatch.setattr(
        views, "get_user_id_by_token", mock_objects.get_user_id_by_token,
    )

    monkeypatch.setattr(
        views, "get_sentiment_by_id", mock_objects.get_sentiment_by_id
    )

    client = test_app.test_client()

    response = client.get(
        "/sentiment/1",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer access_token",
        },
    )
    assert response.status_code == 200

    data = response.get_json()
    assert data["id"] == 1
    assert data["user_id"] == 1
    assert data["keyword"] == "test_keyword_one"


# Test fetching single sentiment fails due to incorrect id
def test_single_sentiment_invalid_id(test_app, monkeypatch):
    monkeypatch.setattr(
        views, "get_user_id_by_token", mock_objects.get_user_id_by_token,
    )

    monkeypatch.setattr(
        views, "get_sentiment_by_id", mock_objects.get_no_sentiment_by_id
    )

    client = test_app.test_client()

    response = client.get(
        "/sentiment/1",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer access_token",
        },
    )
    assert response.status_code == 404

    data = response.get_json()
    assert "does not exist" in data["message"]


# Test fetching single sentiment fails due to missing token
def test_single_sentiment_missing_token(test_app):
    client = test_app.test_client()

    response = client.get(
        "/sentiment/1", headers={"Accept": "application/json"}
    )

    assert response.status_code == 403

    data = response.get_json()
    assert "Token required" in data["message"]


# Test fetching single sentiment fails due to expired token
def test_single_sentiment_expired_token(test_app, monkeypatch):
    monkeypatch.setattr(
        views,
        "get_user_id_by_token",
        mock_objects.get_expired_token_exception,
    )

    monkeypatch.setattr(
        views, "get_sentiment_by_id", mock_objects.get_expired_token_exception
    )

    client = test_app.test_client()

    response = client.get(
        "/sentiment/1",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer access_token",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Token expired" in data["message"]


# Test fetching single sentiment fails due to invalid token
def test_single_sentiment_invalid_token(test_app, monkeypatch):
    monkeypatch.setattr(
        views,
        "get_user_id_by_token",
        mock_objects.get_invalid_token_exception,
    )

    monkeypatch.setattr(
        views, "get_sentiment_by_id", mock_objects.get_invalid_token_exception
    )

    client = test_app.test_client()

    response = client.get(
        "/sentiment/1",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer access_token",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Invalid token" in data["message"]


# Test removing a sentiment passes
def test_remove_sentiment(test_app, monkeypatch):
    monkeypatch.setattr(
        views, "get_user_id_by_token", mock_objects.get_user_id_by_token,
    )

    monkeypatch.setattr(
        views, "get_sentiment_by_id", mock_objects.get_sentiment_by_id
    )
    monkeypatch.setattr(
        views, "remove_sentiment", mock_objects.remove_sentiment
    )

    client = test_app.test_client()

    response = client.delete(
        "/sentiment/1",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer access_token",
        },
    )
    assert response.status_code == 204


# Test removing a sentiment fails due to incorrect id
def test_remove_sentiment_invalid_id(test_app, monkeypatch):
    monkeypatch.setattr(
        views, "get_user_id_by_token", mock_objects.get_user_id_by_token,
    )

    monkeypatch.setattr(
        views, "get_sentiment_by_id", mock_objects.get_no_sentiment_by_id
    )

    client = test_app.test_client()

    response = client.delete(
        "/sentiment/1",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer access_token",
        },
    )
    assert response.status_code == 404

    data = response.get_json()
    assert "does not exist" in data["message"]


# Test removing a sentiment fails due to missing token
def test_remove_sentiment_missing_token(test_app):
    client = test_app.test_client()

    response = client.delete(
        "/sentiment/1", headers={"Accept": "application/json"}
    )

    assert response.status_code == 403

    data = response.get_json()
    assert "Token required" in data["message"]


# Test removing a sentiment fails due to expired token
def test_remove_sentiment_expired_token(test_app, monkeypatch):
    monkeypatch.setattr(
        views,
        "get_user_id_by_token",
        mock_objects.get_expired_token_exception,
    )

    monkeypatch.setattr(
        views, "get_sentiment_by_id", mock_objects.get_expired_token_exception
    )

    client = test_app.test_client()

    response = client.delete(
        "/sentiment/1",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer access_token",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Token expired" in data["message"]


# Test removing a sentiment fails due to invalid token
def test_remove_sentiment_invalid_token(test_app, monkeypatch):
    monkeypatch.setattr(
        views,
        "get_user_id_by_token",
        mock_objects.get_invalid_token_exception,
    )

    monkeypatch.setattr(
        views, "get_sentiment_by_id", mock_objects.get_invalid_token_exception
    )

    client = test_app.test_client()

    response = client.delete(
        "/sentiment/1",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer access_token",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Invalid token" in data["message"]


# Test update a sentiment passes
def test_update_sentiment(test_app, monkeypatch):
    monkeypatch.setattr(
        views, "get_user_id_by_token", mock_objects.get_user_id_by_token,
    )

    monkeypatch.setattr(
        views, "get_sentiment_by_id", mock_objects.get_sentiment_by_id
    )
    monkeypatch.setattr(
        views, "update_sentiment", mock_objects.update_sentiment
    )

    client = test_app.test_client()

    response = client.put(
        "/sentiment/1",
        data=json.dumps({"keyword": "test_sentiment_update"}),
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer access_token",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 200

    data = response.get_json()
    assert data["id"] == 1
    assert data["user_id"] == 1
    assert data["keyword"] == "test_sentiment_update"


# Test update a sentiment fails due to empty data
def test_update_sentiment_empty_data(test_app, monkeypatch):
    monkeypatch.setattr(
        views, "get_user_id_by_token", mock_objects.get_user_id_by_token,
    )

    client = test_app.test_client()

    response = client.put(
        "/sentiment/1",
        data=json.dumps({}),
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer access_token",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 400

    data = response.get_json()
    assert "Input payload validation failed" in data["message"]


# Test update a sentiment fails due to invalid id
def test_update_sentiment_invalid_id(test_app, monkeypatch):
    monkeypatch.setattr(
        views, "get_user_id_by_token", mock_objects.get_user_id_by_token,
    )

    monkeypatch.setattr(
        views, "get_sentiment_by_id", mock_objects.get_no_sentiment_by_id
    )

    client = test_app.test_client()
    response = client.put(
        "/sentiment/1",
        data=json.dumps({"keyword": "test_sentiment_update"}),
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer access_token",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 404

    data = response.get_json()
    assert "does not exist" in data["message"]


# Test update a sentiment fails due to invalid headers
def test_update_sentiment_invalid_headers(test_app):
    client = test_app.test_client()
    response = client.put(
        "/sentiment/1",
        data=json.dumps({"keyword": "test_sentiment_update"}),
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 415

    data = response.get_json()
    assert "define Content-Type header" in data["message"]

    response = client.put(
        "/sentiment/1",
        data=json.dumps({"keyword": "test_sentiment_update"}),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 415

    data = response.get_json()
    assert "supported is application/json" in data["message"]


# Test update a sentiment fails due to missing token
def test_update_sentiment_missing_token(test_app, monkeypatch):
    monkeypatch.setattr(
        views, "get_user_id_by_token", mock_objects.get_user_id_by_token,
    )

    monkeypatch.setattr(
        views, "get_sentiment_by_id", mock_objects.get_sentiment_by_id
    )

    client = test_app.test_client()

    response = client.put(
        "/sentiment/1",
        data=json.dumps({"keyword": "test_sentiment_update"}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 403

    data = response.get_json()
    assert "Token required" in data["message"]


# Test update a sentiment fails due to expired token
def test_update_sentiment_expired_token(test_app, monkeypatch):
    monkeypatch.setattr(
        views,
        "get_user_id_by_token",
        mock_objects.get_expired_token_exception,
    )

    monkeypatch.setattr(
        views, "get_sentiment_by_id", mock_objects.get_sentiment_by_id
    )

    client = test_app.test_client()

    response = client.put(
        "/sentiment/1",
        data=json.dumps({"keyword": "test_sentiment_update"}),
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer access_token",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Token expired" in data["message"]


# Test update a sentiment fails due to invalid token
def test_update_sentiment_invalid_token(test_app, monkeypatch):
    monkeypatch.setattr(
        views,
        "get_user_id_by_token",
        mock_objects.get_invalid_token_exception,
    )

    monkeypatch.setattr(
        views, "get_sentiment_by_id", mock_objects.get_sentiment_by_id
    )

    client = test_app.test_client()

    response = client.put(
        "/sentiment/1",
        data=json.dumps({"keyword": "test_sentiment_update"}),
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer access_token",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Invalid token" in data["message"]
