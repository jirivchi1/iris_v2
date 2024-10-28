# Este archivo está vacío
# app/encuesta/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import insert_survey_response

encuesta = Blueprint("encuesta", __name__)


@encuesta.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        feedback = request.form["feedback"]

        # Insertar los datos en la colección "encuesta"
        insert_survey_response(name, email, feedback)

        flash("Encuesta enviada exitosamente.", "success")
        return redirect(url_for("encuesta.success"))

    return render_template("encuesta/form.html")


@encuesta.route("/success")
def success():
    return render_template("encuesta/success.html")
