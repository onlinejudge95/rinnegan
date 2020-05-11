from app import db
from app.api.users.models import User


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def add_user(username, email, password):
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user.id


def get_all_users():
    return User.query.all()
