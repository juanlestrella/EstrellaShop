# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_talisman import Talisman
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime
import os

#local like the MovieClient
from .client import ProductClient

db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()

from .users.routes import users

from .products.routes import products

csp = {
    'default-src': '\'self\'',
    'style-src': [
        '\'self\'',
        'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css'
        ],
    'img-src': [
        '\'self\'',
        'http://www.w3.org/2000/svg',
        ],
    'script-src': [
        '\'self\'',
        'https://code.jquery.com/jquery-3.4.1.slim.min.js',
        'https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js',
        'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js'
        ],
    'connect-src': '\'self\'',
}


def page_not_found(e):
    return render_template("404.html"), 404


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_pyfile("config.py", silent=False)

    app.config["MONGODB_HOST"] = os.getenv("MONGODB_HOST")

    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(products)

    login_manager.login_view = "users.login"
    Talisman(app, content_security_policy=csp)
    return app
