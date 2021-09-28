from flask import Flask, url_for, session
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = """w[n0l$;TB8IiA|hFuk:<V>M_6'ngdd"""
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix="/")

    from .models import Post, Tag

    # permanent sessions
    @app.before_request
    def make_session_permanent():
        session.permanent = True
        # make session infinite

    @app.before_request
    def create_likes_session():
        if not "likes" in session:
            session["likes"] = []

    # Cache related stuff
    @app.context_processor
    def override_url_for():
        return dict(url_for=dated_url_for)

    def dated_url_for(endpoint, **values):
        if endpoint == "static":
            filename = values.get("filename", None)
            if filename:
                file_path = os.path.join(app.root_path, endpoint, filename)
                values["q"] = int(os.stat(file_path).st_mtime)
        return url_for(endpoint, **values)

    create_database(app)

    return app


def create_database(app):
    if not os.path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Database created successfully")
