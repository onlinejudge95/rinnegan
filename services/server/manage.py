import os
from app import create_app, db
from flask.cli import FlaskGroup
from app.api.users.models import User


app = create_app(os.getenv("FLASK_ENV"))
cli = FlaskGroup()


@cli.command("flush")
def flush():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed")
def seed():
    db.session.add(
        User(
            username="sentimental_user_one",
            email="sentimental_user_one@gmail.com",
            password="password",
        )
    )
    db.session.add(
        User(
            username="sentimental_user_two",
            email="sentimental_user_two@gmail.com",
            password="password",
        )
    )
    db.session.commit()


if __name__ == "__main__":
    cli()
