from flask import Blueprint, render_template, request, flash
from app.controllers.question_controller import handle_questions_and_responses

quiz = Blueprint("quiz", __name__)


@quiz.route("/test", methods=["GET", "POST"])
def test():
    # Rutas completas para el modelo
    model_image_path_1 = "static/images/test/4_renos.png"
    model_image_path_2 = "static/images/test/uvas.jpg"

    # Rutas relativas para el HTML
    html_image_path_1 = "images/test/4_renos.png"
    html_image_path_2 = "images/test/uvas.jpg"

    if request.method == "POST":
        # Capturar datos del formulario
        user_name = request.form["user_name"]
        age = request.form["age"]
        career_profession = request.form["career_profession"]
        question_1 = request.form["question_1"]
        question_2 = request.form["question_2"]

        # Procesar las respuestas para cada pregunta y guardar en MongoDB
        response_1, response_2 = handle_questions_and_responses(
            user_name,
            age,
            career_profession,
            question_1,
            question_2,
            model_image_path_1,
            model_image_path_2,
        )

        # Renderizar la respuesta en response.html
        return render_template(
            "quiz/response.html",
            user_name=user_name,
            age=age,
            career_profession=career_profession,
            question_1=question_1,
            response_1=response_1,
            image_path_1=html_image_path_1,
            question_2=question_2,
            response_2=response_2,
            image_path_2=html_image_path_2,
        )

    # Pasar las rutas de las imágenes a test.html para el formulario inicial
    return render_template(
        "quiz/test.html", image_path_1=html_image_path_1, image_path_2=html_image_path_2
    )
