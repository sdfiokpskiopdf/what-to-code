from flask import Blueprint, jsonify, request, session, redirect, url_for
from . import db
from .models import Post, Tag
import random

api = Blueprint("api", __name__)


@api.route("/posts/", methods=["GET", "POST"])
def get_posts():
    if request.method == "GET":
        posts = [post.json() for post in Post.query.all()]

        return jsonify({"posts": posts})
    elif request.method == "POST":
        content = request.json

        if (
            "title" in content
            and "desc" in content
            and "tags" in content
            and type(content["tags"]) == list
            and type(content["title"]) == str
            and type(content["desc"]) == str
            and len(content["tags"]) <= 5
        ):
            post = Post(title=content["title"], desc=content["desc"], likes=0)
            db.session.add(post)
            db.session.commit()

            tag = Tag(name="all", post_id=post.id)
            db.session.add(tag)

            for t in content["tags"]:
                tag = Tag(name=t, post_id=post.id)
                db.session.add(tag)

            db.session.commit()

            session["posts"].append(post.id)

            return redirect(url_for("api.get_post", id=post.id))
        else:
            return jsonify({"message": "Invalid POST request"}), 400


@api.route("/posts/<id>/")
def get_post(id):
    post = Post.query.filter_by(id=id).first().json()

    if post is None:
        return jsonify({"message": "Post does not exists "}), 404

    return jsonify({"posts": post})

@api.route("/random/")
def get_random_post():
    posts = Post.query.all()
    post = random.choice(posts)

    return redirect(url_for("api.get_post", id=post.id))



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
