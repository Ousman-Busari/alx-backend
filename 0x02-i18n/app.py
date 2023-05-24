#!/usr/bin/env python3
"""
0-app
"""
from flask import Flask, g, render_template, request
from flask_babel import Babel, format_datetime
from pytz import timezone
import pytz
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
    g.current_time = format_datetime()


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


@babel.timezoneselector
def get_timezone() -> str:
    """determine the time zone"""
    tz = request.args.get("timezone")
    if not tz and g.user:
        tz = g.user.get("timezone")
    try:
        return timezone(tz).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config["BABEL_DEFAULT_TIMEZONE"]


@app.route("/")
def index() -> str:
    """renders home page"""
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
