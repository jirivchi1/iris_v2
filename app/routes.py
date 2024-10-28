# app/routes.py
from flask import render_template, request, redirect, url_for, session, flash
from app import app, db, users_collection
from app.models import find_user, insert_survey_response

from app.controllers.question_controller import handle_question_and_response
from app.services.embedding_service import find_similar_responses


# Ruta para el formulario
@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        feedback = request.form["feedback"]

        # Insertar los datos en la colección "encuesta"
        insert_survey_response(name, email, feedback)

        flash("Encuesta enviada exitosamente.", "success")
        return redirect(url_for("success"))

    return render_template("form.html")


# Ruta para la página de éxito
@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/test", methods=["GET", "POST"])
def test():
    relative_image_path = "images/test/uvas.jpg"
    full_image_path = f"static/{relative_image_path}"

    if request.method == "POST":
        user_name = request.form["user_name"]
        question = request.form["question"]
        response = handle_question_and_response(user_name, question, full_image_path)
        return render_template(
            "response.html",
            image_path=relative_image_path,
            question=question,
            response=response,
            user_name=user_name,
        )

    return render_template("test.html", image_path=relative_image_path)


@app.route("/similar-responses", methods=["GET", "POST"])
def similar_responses():
    similar_users = []
    query = ""
    if request.method == "POST":
        query = request.form.get("query")
        if query:
            similar_users = find_similar_responses(query)
        else:
            flash("Please enter a query.", "warning")

    return render_template(
        "similar_responses.html", similar_users=similar_users, query=query
    )
