import os
from app import create_app
from flask.cli import FlaskGroup


app = create_app(os.getenv("FLASK_ENV"))
cli = FlaskGroup()


@cli.command("dummy")
def dummy():
    print("dummy")


if __name__ == "__main__":
    cli()
