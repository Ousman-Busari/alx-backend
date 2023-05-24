#!/usr/bin/env python3
"""
0-app
"""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """Class config with language and location settings"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)


@babel.localeselector
def get_locale() -> str:
    """determine the best match with our supported languages"""
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def index() -> str:
    """renders home page"""
    return render_template("3-index.html")


if __name__ == "__main__":
    app.run()
