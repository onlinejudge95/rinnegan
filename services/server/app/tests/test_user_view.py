import json

# Test user creation passes
def test_add_user(test_app, test_database):
    client = test_app.test_client()
    response = client.post(
        "/user",
        data=json.dumps(
            {
                "username": "test_user",
                "email": "test_user@gmail.com",
                "password": "test_password",
            }
        ),
        headers={"Accept": "application/json", "Content-Type": "application/json"},
    )

    assert response.status_code == 201

    data = json.loads(response.get_json())
    assert 1 == 2
