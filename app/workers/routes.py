# app/workers/routes.py

from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from app import db
from app.services.openai_service import generate_solution_description
from app.services.embedding_service import (
    get_embedding,
    update_solution_embeddings,
    update_user_response_embeddings,
    find_similar_responses,
)

workers = Blueprint("workers", __name__)


@workers.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "username" in session:
        if request.method == "POST":
            # Generate solution descriptions and embeddings
            fixed_prompt = "Please provide a detailed description of the image."
            questions = db.questions.find()
            for question in questions:
                if not question.get("solution"):
                    image_path = question["image_path"]
                    # Generate solution description using fixed prompt
                    solution = generate_solution_description(image_path)
                    # Update the question document with the solution
                    db.questions.update_one(
                        {"_id": question["_id"]}, {"$set": {"solution": solution}}
                    )
            # Generate embeddings for the solutions
            update_solution_embeddings()
            flash(
                "Descripciones de soluciones y embeddings generados exitosamente.",
                "success",
            )
            return redirect(url_for("workers.dashboard"))
        else:
            # Fetch all questions to display
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
            # Ensure user response embeddings are updated
            update_user_response_embeddings()
            similar_responses = find_similar_responses(question_id)
            # Fetch the solution description
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


# Optional: Route to initialize questions collection (if needed)
@workers.route("/initialize_questions")
def initialize_questions():
    if "username" in session:
        # Define your questions and image paths
        questions_data = [
            {
                "question_id": "question_1",
                "image_path": "static/images/test/4_renos.png",
            },
            {
                "question_id": "question_2",
                "image_path": "static/images/test/uvas.jpg",
            },
        ]
        for question in questions_data:
            existing_question = db.questions.find_one(
                {"question_id": question["question_id"]}
            )
            if not existing_question:
                db.questions.insert_one(question)
        flash("Colección de preguntas inicializada.", "success")
        return redirect(url_for("workers.dashboard"))
    else:
        flash(
            "Debes iniciar sesión como personal para inicializar las preguntas.",
            "warning",
        )
        return redirect(url_for("auth.login"))
