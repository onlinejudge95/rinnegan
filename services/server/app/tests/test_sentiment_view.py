import json


# Test sentiment creation passes
def test_add_sentiment(test_app, test_database, add_user):
    add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
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
def test_add_sentiment_empty_data(test_app, test_database):
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
def test_add_sentiment_invalid_data(test_app, test_database):
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
def test_add_sentiment_unregistered_user(test_app, test_database):
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
def test_add_sentiment_exceeding_quota(test_app, test_database, add_user):
    add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )
    test_app.config["SENTIMENT_QUOTA_LIMIT"] = 6

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


# Test user creation fails due to invalid content-type header
def test_add_user_invalid_header(test_app):
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
        "/users",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 415

    data = response.get_json()
    assert "supported is application/json" in data["message"]


# Test fetching sentiment list passes
def test_get_sentiments(
    test_app, test_database, add_user, login_user, add_sentiments
):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )
    tokens = login_user(user.id)
    add_sentiments(user_id=user.id, keyword="test_keyword_one")
    add_sentiments(user_id=user.id, keyword="test_keyword_two")

    client = test_app.test_client()
    response = client.get(
        "/sentiment",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {tokens.access_token}",
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 2
    assert user.id == data[0]["user_id"]
    assert "test_keyword_one" in data[0]["keyword"]

    assert user.id == data[1]["user_id"]
    assert "test_keyword_two" in data[1]["keyword"]


# Test fetching sentiment list fails due to missing token
def test_get_sentiments_missing_token(test_app, test_database):
    client = test_app.test_client()

    response = client.get("/sentiment", headers={"Accept": "application/json"})
    assert response.status_code == 403

    data = response.get_json()
    assert "Token required" in data["message"]


# Test fetching sentiment list fails due to expired token
def test_get_sentiments_expired_token(
    test_app, test_database, add_user, login_user, add_sentiments
):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )

    test_app.config["ACCESS_TOKEN_EXPIRATION"] = -1

    tokens = login_user(user.id)
    add_sentiments(user_id=user.id, keyword="test_keyword_one")
    add_sentiments(user_id=user.id, keyword="test_keyword_two")

    client = test_app.test_client()

    response = client.get(
        "/sentiment",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {tokens.access_token}",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Token expired" in data["message"]


# Test fetching sentiment list fails due to invalid token
def test_get_sentiments_invalid_token(test_app, test_database):
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
def test_single_sentiment(
    test_app, test_database, add_user, login_user, add_sentiments
):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )
    tokens = login_user(user.id)
    sentiment = add_sentiments(user_id=user.id, keyword="test_keyword_one")

    client = test_app.test_client()

    response = client.get(
        f"/sentiment/{sentiment.id}",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {tokens.access_token}",
        },
    )
    assert response.status_code == 200

    data = response.get_json()
    assert data["id"] == sentiment.id
    assert data["user_id"] == user.id
    assert data["keyword"] == sentiment.keyword


# Test fetching single sentiment fails due to incorrect id
def test_single_sentiment_invalid_id(
    test_app, test_database, add_user, login_user
):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )
    tokens = login_user(user.id)

    client = test_app.test_client()

    response = client.get(
        "/sentiment/1",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {tokens.access_token}",
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
def test_single_sentiment_expired_token(
    test_app, test_database, add_user, login_user
):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )

    test_app.config["ACCESS_TOKEN_EXPIRATION"] = -1

    tokens = login_user(user.id)

    client = test_app.test_client()

    response = client.get(
        "/sentiment/1",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {tokens.access_token}",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Token expired" in data["message"]


# Test fetching single sentiment fails due to invalid token
def test_single_sentiment_invalid_token(test_app, test_database):
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
def test_remove_sentiment(
    test_app, test_database, add_user, login_user, add_sentiments
):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )
    tokens = login_user(user.id)
    sentiment = add_sentiments(user_id=user.id, keyword="test_keyword_one")

    client = test_app.test_client()

    response = client.delete(
        f"/sentiment/{sentiment.id}",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {tokens.access_token}",
        },
    )
    assert response.status_code == 204


# Test removing a sentiment fails due to invalid id
def test_remove_sentiment_invalid_id(
    test_app, test_database, add_user, login_user
):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )
    tokens = login_user(user.id)

    client = test_app.test_client()

    response = client.delete(
        "/sentiment/1",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {tokens.access_token}",
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
def test_remove_sentiment_expired_token(
    test_app, test_database, add_user, login_user
):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )

    test_app.config["ACCESS_TOKEN_EXPIRATION"] = -1

    tokens = login_user(user.id)

    client = test_app.test_client()

    response = client.delete(
        "/sentiment/1",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {tokens.access_token}",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Token expired" in data["message"]


# Test removing a sentiment fails due to invalid token
def test_remove_sentiment_invalid_token(test_app, test_database):
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
def test_update_sentiment(
    test_app, test_database, add_user, login_user, add_sentiments
):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )

    tokens = login_user(user.id)
    sentiment = add_sentiments(user_id=user.id, keyword="test_keyword_one")

    client = test_app.test_client()

    response = client.put(
        f"/sentiment/{sentiment.id}",
        data=json.dumps({"keyword": "test_sentiment_update"}),
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {tokens.access_token}",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 200

    data = response.get_json()
    assert data["id"] == sentiment.id
    assert data["user_id"] == user.id
    assert data["keyword"] == "test_sentiment_update"


# Test update a sentiment fails due to empty data
def test_update_sentiment_empty_data(
    test_app, test_database, add_user, login_user, add_sentiments
):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )

    tokens = login_user(user.id)
    sentiment = add_sentiments(user_id=user.id, keyword="test_keyword_one")

    client = test_app.test_client()

    response = client.put(
        f"/sentiment/{sentiment.id}",
        data=json.dumps({}),
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {tokens.access_token}",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 400

    data = response.get_json()
    assert "Input payload validation failed" in data["message"]


# Test update a sentiment fails due to invalid id
def test_update_sentiment_invalid_id(
    test_app, test_database, add_user, login_user
):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )

    tokens = login_user(user.id)

    client = test_app.test_client()
    response = client.put(
        "/sentiment/1",
        data=json.dumps({"keyword": "test_sentiment_update"}),
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {tokens.access_token}",
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
def test_update_sentiment_missing_token(test_app):
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
def test_update_sentiment_expired_token(
    test_app, test_database, add_user, login_user
):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )

    test_app.config["ACCESS_TOKEN_EXPIRATION"] = -1

    tokens = login_user(user.id)

    client = test_app.test_client()

    response = client.put(
        "/sentiment/1",
        data=json.dumps({"keyword": "test_sentiment_update"}),
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {tokens.access_token}",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Token expired" in data["message"]


# Test update a sentiment fails due to invalid token
def test_update_sentiment_invalid_token(test_app):
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
