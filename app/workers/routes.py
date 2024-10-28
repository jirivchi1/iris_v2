# Este archivo está vacío
# app/workers/routes.py
from flask import Blueprint, render_template, flash, redirect, url_for, session

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
