from flask import (
    Blueprint,
    jsonify,
    session,
)
from . import db
from .models import Post, Tag

api = Blueprint("api", __name__)


@api.route("/posts/")
def get_posts():
    posts = [post.json() for post in Post.query.all()]

    return jsonify({"posts": posts})


@api.route("/posts/<id>/")
def get_post(id):
    post = Post.query.filter_by(id=id).first().json()

    if post is None:
        return jsonify({"message": "Post does not exists "}), 404

    return jsonify({"posts": post})


@api.route("/tags/")
def get_tags():
    tags = [tag.json() for tag in Tag.query.all()]

    return jsonify({"tags": tags})


@api.route("/tags/<id>")
def get_tag(id):
    tag = Tag.query.filter_by(id=id).first().json()

    if tag is None:
        return jsonify({"message": "Tag does not exists "}), 404

    return jsonify({"tags": tag})


@api.route("/like-post/<post_id>/", methods=["POST"])
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    liked = False

    if not post:
        return jsonify({"error": "Post does not exist."}, 400)
    elif int(post_id) in session["likes"]:
        post.likes -= 1
        db.session.commit()
        session["likes"].remove(int(post_id))
    else:
        liked = True
        post.likes += 1
        db.session.commit()
        session["likes"].append(int(post_id))

    return jsonify({"likes": post.likes, "liked": liked})
