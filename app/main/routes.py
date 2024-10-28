# Este archivo está vacío
# app/main/routes.py
from flask import Blueprint, render_template, flash, redirect, url_for, session

main = Blueprint("main", __name__)


@main.route("/")
def home():
    if "username" in session:
        return render_template("main/home.html", username=session["username"])
    else:
        flash("Debes iniciar sesión para acceder a esta página.", "warning")
        return redirect(url_for("auth.login"))


@main.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("main/dashboard.html")
    else:
        flash(
            "Debes iniciar sesión como personal para acceder al dashboard.", "warning"
        )
        return redirect(url_for("auth.login"))
