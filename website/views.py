from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session,
)
from .models import Post, Tag
from . import db
import random

views = Blueprint("views", __name__)


@views.route("/")
def home():
    order = request.args.get("order", default="POPULAR", type=str)
    tag = request.args.get("tag", default="all", type=str)

    if order == "POPULAR":
        posts = (
            Post.query.join(Tag)
            .filter(Tag.name == tag)
            .order_by(Post.likes.desc())
            .all()
        )
    elif order == "RECENT":
        posts = (
            Post.query.filter(Tag.name == tag).order_by(Post.date_created.desc()).all()
        )
    elif order == "OLDEST":
        posts = (
            Post.query.filter(Tag.name == tag).order_by(Post.date_created.asc()).all()
        )
    elif order == "RISING":
        posts = (
            Post.query.filter(Tag.name == tag)
            .order_by(Post.likes.desc(), Post.date_created.desc())
            .all()
        )  # might need to fix this
    else:
        posts = Post.query.order_by(Post.likes.desc()).all()

    return render_template("home.html", posts=posts)


@views.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        tags = []

        for i in range(5):
            tag = request.form.get("tag" + str(i))

            if tag is None:
                break
            else:
                tag = tag.replace(" ", "")
                tags.append(tag)

        post = Post(title=title, desc=desc, likes=0)
        db.session.add(post)
        db.session.commit()

        tag = Tag(name="all", post_id=post.id)
        db.session.add(tag)

        for t in tags:
            tag = Tag(name=t, post_id=post.id)
            db.session.add(tag)

        db.session.commit()

        return redirect(url_for("views.home"))

    return render_template("submit.html")


@views.route("/random")
def random_post():
    posts = Post.query.all()
    post = random.choice(posts)

    return render_template("home.html", posts=[post])


@views.route("/like-post/<post_id>", methods=["POST"])
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
