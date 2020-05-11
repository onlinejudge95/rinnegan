from app import db
from app.api.users.models import User


def get_user_by_email(email):
    pass


def add_user(username, email, password):
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user.id
