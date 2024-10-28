# Este archivo está vacío
# app/quiz/routes.py
from flask import Blueprint, render_template, request, flash
from app.controllers.question_controller import handle_question_and_response
from app.services.embedding_service import find_similar_responses


quiz = Blueprint("quiz", __name__)


@quiz.route("/test", methods=["GET", "POST"])
def test():
    relative_image_path = "images/test/uvas.jpg"
    full_image_path = f"static/{relative_image_path}"

    if request.method == "POST":
        user_name = request.form["user_name"]
        question = request.form["question"]
        response = handle_question_and_response(user_name, question, full_image_path)
        return render_template(
            "quiz/response.html",
            image_path=relative_image_path,
            question=question,
            response=response,
            user_name=user_name,
        )

    return render_template("quiz/test.html", image_path=relative_image_path)


@quiz.route("/similar-responses", methods=["GET", "POST"])
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
        "quiz/similar_responses.html", similar_users=similar_users, query=query
    )
