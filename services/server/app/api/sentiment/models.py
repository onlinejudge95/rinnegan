from app import db


class Sentiment(db.Model):

    __tablename__ = "sentiment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    keyword = db.Column(db.String(128), nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="cascade"),
        nullable=False,
    )

    def __init__(self, keyword, user_id):
        self.keyword = keyword
        self.user_id = user_id
