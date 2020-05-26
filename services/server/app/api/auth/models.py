from app import db


class Token(db.Model):
    __tablename__ = "tokens"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(128), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    active = db.Column(db.Boolean())

    def __init__(self, token, token_type):
        self.token = token
        self.token_type = token_type
        self.active = True
