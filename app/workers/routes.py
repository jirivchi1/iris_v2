# Este archivo está vacío
# app/workers/routes.py
from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from app.services.embedding_service import find_similar_responses

workers = Blueprint("workers", __name__)


# Ruta para el dashboard (solo accesible para personal)
@workers.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("workers/dashboard.html")
    else:
        flash(
            "Debes iniciar sesión como personal para acceder al dashboard.", "warning"
        )
        return redirect(url_for("auth.login"))


@workers.route("/visualize_ranking", methods=["POST"])
def visualize_ranking():
    query_text = request.form.get("query_text")
    if query_text:
        similar_responses = find_similar_responses(query_text)
        return render_template(
            "workers/dashboard.html", similar_responses=similar_responses
        )
    return redirect(url_for("workers.dashboard"))
