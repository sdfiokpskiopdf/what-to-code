from flask import Blueprint, render_template, request, redirect, url_for
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

        post = Post(title=title, desc=desc)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for("views.home"))

    return render_template("submit.html")


@views.route("/random")
def random_post():
    posts = Post.query.all()
    post = random.choice(posts)

    return render_template("home.html", posts=[post])
