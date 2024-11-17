# app/workers/routes.py

from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from app import db
from app.services.openai_service import generate_solution_description
from app.services.embedding_service import (
    get_embedding,
    update_solution_embeddings,
    find_similar_responses,
)
from app.controllers.question_controller import (
    process_user_responses,
)  # Importamos la nueva función

workers = Blueprint("workers", __name__)


@workers.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "username" in session:
        if request.method == "POST":
            # Generar descripciones de soluciones y embeddings
            questions = db.questions.find()
            for question in questions:
                if not question.get("solution"):
                    image_path = question["image_path"]
                    # Generar descripción de la solución usando un prompt fijo
                    solution = generate_solution_description(image_path)
                    # Actualizar el documento de la pregunta con la solución
                    db.questions.update_one(
                        {"_id": question["_id"]}, {"$set": {"solution": solution}}
                    )
            # Generar embeddings para las soluciones
            update_solution_embeddings()
            flash(
                "Descripciones de soluciones y embeddings generados exitosamente.",
                "success",
            )
            return redirect(url_for("workers.dashboard"))
        else:
            # Obtener todas las preguntas para mostrar
            questions = list(db.questions.find({}, {"question_id": 1, "_id": 0}))
            return render_template("workers/dashboard.html", questions=questions)
    else:
        flash(
            "Debes iniciar sesión como personal para acceder al dashboard.", "warning"
        )
        return redirect(url_for("auth.login"))


@workers.route("/visualize_ranking", methods=["POST"])
def visualize_ranking():
    if "username" in session:
        question_id = request.form.get("question_id")
        if question_id:
            # Procesar las respuestas de los usuarios antes de calcular el ranking
            process_user_responses()
            # Calcular el ranking
            similar_responses = find_similar_responses(question_id)
            # Obtener la descripción de la solución
            question = db.questions.find_one({"question_id": question_id})
            solution_description = question.get("solution")
            return render_template(
                "workers/dashboard.html",
                similar_responses=similar_responses,
                selected_question=question_id,
                solution_description=solution_description,
                questions=list(db.questions.find({}, {"question_id": 1, "_id": 0})),
            )
        else:
            flash("Por favor, selecciona una pregunta.", "warning")
            return redirect(url_for("workers.dashboard"))
    else:
        flash(
            "Debes iniciar sesión como personal para visualizar el ranking.", "warning"
        )
        return redirect(url_for("auth.login"))
