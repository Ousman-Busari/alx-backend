#!/usr/bin/env python3
"""
0-app
"""
from flask import Flask, render_template
from flask_babel import Babel


class Config:
    """Class config with language and location settings"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """renders home page"""
    return render_template("1-index.html")


if __name__ == "__main__":
    app.run()
