from flask import Blueprint, render_template, request
from app.controllers.question_controller import handle_questions_and_responses

quiz = Blueprint("quiz", __name__)


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
    ]

    if request.method == "POST":
        # Capture user information
        user_name = request.form["user_name"]
        age = request.form["age"]
        career_profession = request.form["career_profession"]

        # Capture questions from the form
        question_texts = []
        for idx, question in enumerate(questions_data, start=1):
            question_text = request.form[f"question_{idx}"]
            question["question_text"] = question_text
            question_texts.append(question_text)

        # Prepare image paths for the model
        model_image_paths = [q["image_path_model"] for q in questions_data]

        # Process responses and save to MongoDB
        response_1, response_2 = handle_questions_and_responses(
            user_name,
            age,
            career_profession,
            question_texts[0],
            question_texts[1],
            model_image_paths[0],
            model_image_paths[1],
        )

        # Prepare data to render in the template
        responses = [
            {
                "question": question_texts[0],
                "response": response_1,
                "image_path": questions_data[0]["image_path_html"],
            },
            {
                "question": question_texts[1],
                "response": response_2,
                "image_path": questions_data[1]["image_path_html"],
            },
        ]

        # Render the response template
        return render_template(
            "quiz/response.html",
            user_name=user_name,
            age=age,
            career_profession=career_profession,
            responses=responses,
        )

    # For GET requests, render the test template
    return render_template(
        "quiz/test.html",
        questions=questions_data,
    )
