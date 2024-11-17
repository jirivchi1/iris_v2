from flask import Blueprint, render_template, request
from pymongo import MongoClient
from datetime import datetime

quiz = Blueprint("quiz", __name__)

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Ajusta si es necesario
db = client["iris_database"]  # Reemplaza con el nombre de tu base de datos
user_responses_collection = db["user_responses"]


@quiz.route("/test", methods=["GET", "POST"])
def test():
    # Define questions and image paths
    questions_data = [
        {
            "question_id": "question_1",
            "image_path_model": "static/images/test/4_renos.png",
            "image_path_html": "images/test/4_renos.png",
        },
        {
            "question_id": "question_2",
            "image_path_model": "static/images/test/uvas.jpg",
            "image_path_html": "images/test/uvas.jpg",
        },
        {
            "question_id": "question_3",
            "image_path_model": "static/images/test/platano.jpeg",
            "image_path_html": "images/test/platano.jpeg",
        },
    ]

    if request.method == "POST":
        # Capturar información del usuario
        user_name = request.form["user_name"]
        age = request.form["age"]
        career_profession = request.form["career_profession"]

        # Capturar respuestas del formulario
        responses = []
        for question in questions_data:
            prompt = request.form[question["question_id"]]
            responses.append(
                {
                    "question_id": question["question_id"],
                    "prompt": prompt,
                    # No generamos 'ai_response' ni 'ai_embedding' aquí
                }
            )

        # Guardar las respuestas del usuario en la base de datos sin procesar
        user_responses_collection.insert_one(
            {
                "user_name": user_name,
                "age": age,
                "career_profession": career_profession,
                "submission_time": datetime.utcnow(),
                "responses": responses,
            }
        )

        # Renderizar la página de agradecimiento
        return render_template("quiz/thank_you.html", user_name=user_name)

    # Para solicitudes GET, renderizar la plantilla de prueba
    return render_template(
        "quiz/test.html",
        questions=questions_data,
    )
