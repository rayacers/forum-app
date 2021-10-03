from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

import pymysql

db = SQLAlchemy()
DB_NAME = "forum"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "thisissecret"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://admin:11041104@forum-db.c4qu0ghpozzb.eu-west-3.rds.amazonaws.com:3306/{DB_NAME}"

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Post, Comment

    db.init_app(app)
    create_db(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_db(app):
    db.create_all(app=app)
    print("create database")
