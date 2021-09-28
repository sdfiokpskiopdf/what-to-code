from . import db
from sqlalchemy.sql import func


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    desc = db.Column(db.String(1000))
    likes = db.Column(db.Integer)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
