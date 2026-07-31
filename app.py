# -*- coding: utf-8 -*-
"""
Oficina -- bancada de testes para os apps em desenvolvimento.
Rode com: python app.py   e acesse http://localhost:5050
"""
import os
import unicodedata

from flask import Flask, abort, render_template

from projects import CATEGORIAS, PROJECTS, get_project, preview_url, resolve_url

app = Flask(__name__)


def _slug(text):
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return normalized.lower().replace(" ", "-")


def _with_extras(project):
    return {
        **project,
        "url": resolve_url(project),
        "preview": preview_url(project),
        "status_slug": _slug(project["status"]),
    }


@app.route("/")
def index():
    projects = [_with_extras(p) for p in PROJECTS]
    columns = [
        {**cat, "projects": [p for p in projects if p["categoria"] == cat["slug"]]}
        for cat in CATEGORIAS
    ]
    return render_template("index.html", projects=projects, columns=columns)


@app.route("/app/<project_id>")
def app_view(project_id):
    project = get_project(project_id)
    if project is None:
        abort(404)
    return render_template("app_view.html", project=_with_extras(project))


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(debug=debug, host="0.0.0.0", port=int(os.environ.get("PORT", 5050)))
