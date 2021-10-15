from . import db
from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    desc = db.Column(db.String(1000))
    likes = db.Column(db.Integer)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.now())
    tags = db.relationship("Tag", backref="post", passive_deletes=True)

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "desc": self.desc,
            "likes": self.likes,
            "date_created": self.date_created,
            "tags": [tag.json() for tag in self.tags],
        }


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(12))
    post_id = db.Column(
        db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False
    )

    def json(self):
        return {"id": self.id, "name": self.name, "post_id": self.post_id}
