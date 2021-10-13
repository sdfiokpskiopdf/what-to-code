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
    page = request.args.get("page", default=1, type=int)
    per_page = 15

    if order == "POPULAR":
        posts = (
            Post.query.join(Tag)
            .filter(Tag.name == tag)
            .order_by(Post.likes.desc())
            .paginate(page=page, per_page=per_page)
        )
    elif order == "RECENT":
        posts = (
            Post.query.filter(Tag.name == tag)
            .order_by(Post.date_created.desc())
            .paginate(page=page, per_page=per_page)
        )
    elif order == "OLDEST":
        posts = (
            Post.query.filter(Tag.name == tag)
            .order_by(Post.date_created.asc())
            .paginate(page=page, per_page=per_page)
        )
    elif order == "RISING":
        posts = (
            Post.query.filter(Tag.name == tag)
            .order_by(Post.likes.desc(), Post.date_created.desc())
            .paginate(page=page, per_page=per_page)
        )  # might need to fix this
    else:
        posts = (
            Post.query.filter(Tag.name == tag)
            .order_by(Post.likes.desc())
            .paginate(page=page, per_page=per_page)
        )

    return render_template(
        "home.html", posts=posts, one=False, likes=[session["likes"]]
    )


@views.route("/submit/", methods=["GET", "POST"])
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
                tag = tag.replace(" ", "").replace("#", "")
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

        session["posts"].append(post.id)

        return redirect(url_for("views.home"))

    return render_template("submit.html")


@views.route("/random/")
def random_post():
    posts = Post.query.all()
    post = random.choice(posts)

    return render_template(
        "home.html", posts=[post], one=True, likes=[session["likes"]]
    )
