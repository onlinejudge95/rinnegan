# Test passwords are randomly hashed
def test_passwords_hashed_randomly(test_app, test_database, add_user):
    user_one = add_user(
        "test_user_one", "test_user_one@mail.com", "test_password"
    )
    user_two = add_user(
        "test_user_two", "test_user_two@mail.com", "test_password"
    )

    assert user_one.password != user_two.password
    assert user_one.password != "test_password"
    assert user_two.password != "test_password"
