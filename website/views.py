from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session,
)
from .models import Post
from . import db
import random

views = Blueprint("views", __name__)


@views.route("/")
def home():
    posts = Post.query.all()
    return render_template("home.html", posts=posts)


@views.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")

        post = Post(title=title, desc=desc, likes=0)
        db.session.add(post)
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
