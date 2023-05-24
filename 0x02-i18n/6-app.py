#!/usr/bin/env python3
"""
0-app
"""
from flask import Flask, g, render_template, request
from flask_babel import Babel
from typing import Optional, Dict


class Config:
    """Class config with language and location settings"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Optional[Dict]:
    """returns a user dictionary or None if the login_as cannot be found
    in users or not passed as part of the request query"""
    login_as = request.args.get("login_as")
    if not login_as:
        return None
    return users.get(int(login_as))


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)


@app.before_request
def before_request() -> None:
    """find a user if any, and set it as a global on flask.g.user"""
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    """determine the best match with our supported languages"""
    url_locale = request.args.get("locale")
    if url_locale and url_locale in app.config["LANGUAGES"]:
        return url_locale
    if g.user and g.user.get("locale") in app.config["LANGUAGES"]:
        return g.user.get("locale")
    header_locale = request.headers.get("locale")
    if header_locale and header_locale in app.config["LANGUAGES"]:
        return header_locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def index() -> str:
    """renders home page"""
    return render_template("6-index.html")


if __name__ == "__main__":
    app.run()
