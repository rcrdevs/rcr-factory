# -*- coding: utf-8 -*-
"""
Oficina -- bancada de testes para os apps em desenvolvimento.
Rode com: python app.py   e acesse http://localhost:5050
"""
import os
import unicodedata

from flask import Flask, abort, render_template

from projects import CATEGORIAS, PROJECTS, get_categoria, get_project, resolve_url

app = Flask(__name__)


def _slug(text):
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return normalized.lower().replace(" ", "-")


def _monograma(nome):
    letras = [w[0] for w in nome.split() if w][:2]
    return "".join(letras).upper()


def _with_extras(project):
    categoria = get_categoria(project["categoria"])
    return {
        **project,
        "url": resolve_url(project),
        "status_slug": _slug(project["status"]),
        "monograma": _monograma(project["nome"]),
        "categoria_cor": categoria["cor"] if categoria else "blue",
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
