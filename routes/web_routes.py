from flask import Blueprint, render_template

web_blueprint = Blueprint("web_routes", __name__)

@web_blueprint.route("/")
def index():
    return render_template("index.html")

@web_blueprint.route("/links")
def links():
    return render_template("links.html")

@web_blueprint.route("/notes")
def notes():
    return render_template("notes.html")

@web_blueprint.route("/categories")
def categories():
    return render_template("categories.html")
