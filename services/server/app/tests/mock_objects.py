import jwt


class User(dict):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Token(dict):
    def __init__(self, *args, **kwargs):
        super(Token, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Sentiment(dict):
    def __init__(self, *args, **kwargs):
        super(Sentiment, self).__init__(*args, **kwargs)
        self.__dict__ = self


def get_user_id_by_token(token):
    return 1


def get_invalid_user_id_by_token(token):
    return 2


def password_matches(password, user):
    return True


def password_not_matches(password, user):
    return False


def get_expired_token_exception(token):
    raise jwt.ExpiredSignatureError()


def get_invalid_token_exception(token):
    raise jwt.InvalidTokenError()


def get_no_user_by_email(email):
    return None


def get_user_by_email(email):
    return True


def get_user_object_by_email(email):
    user = User()
    user.update(
        {
            "id": 1,
            "username": "test_user",
            "email": "test_user@mail.com",
            "password": "test_password",
        }
    )
    return user


def add_user(username, email, password):
    user = User()
    user.update(
        {
            "id": 1,
            "username": "test_user",
            "email": "test_user@mail.com",
            "password": "test_password",
        }
    )
    return user


def get_all_users():
    return [
        {
            "id": 1,
            "username": "test_user_one",
            "email": "test_user_one@mail.com",
        },
        {
            "id": 2,
            "username": "test_user_two",
            "email": "test_user_two@mail.com",
        },
    ]


def get_user_by_id(user_id):
    return {
        "id": 1,
        "username": "test_user",
        "email": "test_user@mail.com",
    }


def get_no_user_by_id(user_id):
    return None


def remove_user(user):
    return True


def update_user(user, username, email):
    mock_user = User()
    mock_user.update({"id": 1, "username": username, "email": email})
    return mock_user


def add_token(user_id):
    token = Token()
    token.update(
        {"access_token": "access_token", "refresh_token": "refresh_token"}
    )
    return token


def update_token(token, user_id):
    mock_token = Token()
    mock_token.update(
        {
            "refresh_token": "refresh_token_updated",
            "access_token": "access_token_updated",
        }
    )
    return mock_token


def add_sentiment(keyword, user_id):
    mock_sentiment = Sentiment()
    mock_sentiment.update({"id": 1, "keyword": "keyword", "user_id": 1})
    return mock_sentiment


def user_sentiment_quota_exhausted(user_id):
    return True


def user_sentiment_quota_not_exhausted(user_id):
    return False


def get_all_sentiments():
    return [
        {"id": 1, "user_id": 1, "keyword": "test_keyword_one"},
        {"id": 2, "user_id": 1, "keyword": "test_keyword_two"},
    ]


def get_sentiment_by_id(sentiment_id):
    return {"id": 1, "user_id": 1, "keyword": "test_keyword_one"}


def get_no_sentiment_by_id(sentiment_id):
    return None


def remove_sentiment(sentiment):
    return True


def update_sentiment(sentiment, keyword):
    mock_sentiment = Sentiment()
    mock_sentiment.update({"id": 1, "keyword": keyword, "user_id": 1})
    return mock_sentiment
