from flask import Blueprint, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime

quiz = Blueprint("quiz", __name__)

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Ajusta si es necesario
db = client["iris_database"]  # Reemplaza con el nombre de tu base de datos
user_responses_collection = db["user_responses"]
questions_collection = db["questions"]  # Colección de preguntas


@quiz.route("/test", methods=["GET", "POST"])
def test():
    # Recuperar preguntas desde MongoDB
    questions_data = list(
        questions_collection.find(
            {}, {"_id": 0, "question_id": 1, "image_path": 1, "ejemplo": 1}
        )
    )

    # Adaptar los paths de imagen para usarlos en el template
    for question in questions_data:
        question["image_path_html"] = question["image_path"].replace("static/", "")

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
        # Redirigir al ranking después de mostrar el agradecimiento
        return redirect(url_for("quiz.ranking"))

    # Para solicitudes GET, renderizar la plantilla de prueba con preguntas dinámicas
    return render_template(
        "quiz/test.html",
        questions=questions_data,
    )


@quiz.route("/ranking", methods=["GET"])
def ranking():
    # Recuperar todas las preguntas desde la colección de preguntas
    questions_data = list(questions_collection.find({}, {"_id": 0, "question_id": 1}))
    # print("Questions Data:", questions_data)  # Verificar qué datos se obtienen

    # Recuperar datos de las respuestas de los usuarios desde MongoDB
    user_data = user_responses_collection.find(
        {},
        {"user_name": 1, "responses": 1, "_id": 0},
    )

    # Procesar las respuestas para estructurarlas de forma plana
    response_data = []
    for user in user_data:
        user_name = user.get("user_name", "Unknown")
        for response in user.get("responses", []):
            response_data.append(
                {
                    "user_name": user_name,
                    "question_id": response.get("question_id"),
                    "prompt": response.get("prompt", "N/A"),
                    "ai_response": response.get("ai_response", "N/A"),
                }
            )

    # Renderizar el template con las preguntas y datos procesados
    return render_template(
        "quiz/ranking.html", questions=questions_data, data=response_data
    )
