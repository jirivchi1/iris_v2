# app/auth/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db, users_collection
from app.models import find_user

auth = Blueprint("auth", __name__)


# Este archivo está vacío
# Ruta para login
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        if role == "usuario":
            user = find_user(username, password)
            if user:
                session["username"] = username
                flash("Login como usuario exitoso", "success")
                return redirect(url_for("main.home"))
            else:
                flash("Credenciales inválidas. Inténtalo de nuevo.", "danger")
                return redirect(url_for("auth.login"))
        elif role == "personal":
            personal = db.personal.find_one(
                {"username": username, "password": password}
            )
            if personal:
                session["username"] = username
                flash("Login como personal exitoso", "success")
                return redirect(url_for("workers.dashboard"))
            else:
                flash(
                    "Credenciales de personal inválidas. Inténtalo de nuevo.", "danger"
                )
                return redirect(url_for("auth.login"))

    return render_template("auth/login.html")


# Ruta para el registro
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = users_collection.find_one({"username": username})

        if existing_user:
            flash("El nombre de usuario ya está registrado.", "danger")
            return redirect(url_for("auth.signup"))

        users_collection.insert_one({"username": username, "password": password})
        flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/signup.html")


# Ruta para cerrar sesión
@auth.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Has cerrado sesión exitosamente.", "info")
    return redirect(url_for("auth.login"))
