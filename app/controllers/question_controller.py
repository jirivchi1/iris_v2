# app/controllers/question_controller.py
from app import db
from app.services.openai_service import (
    get_openai_response,
    generate_solution_description,
)
from app.services.embedding_service import get_embedding


def handle_questions_and_responses(
    user_name,
    age,
    career_profession,
    question_1,
    question_2,
    image_path_1,
    image_path_2,
):
    # List of questions
    questions_data = [
        {
            "question_id": "question_1",
            "question_text": question_1,
            "image_path": image_path_1,
        },
        {
            "question_id": "question_2",
            "question_text": question_2,
            "image_path": image_path_2,
        },
    ]

    # Process each question
    for question in questions_data:
        # Check if the question already exists
        existing_question = db.questions.find_one(
            {"question_id": question["question_id"]}
        )

        if not existing_question:
            # Generate solution description using fixed prompt
            solution = generate_solution_description(question["image_path"])
            # Generate embedding for the solution
            solution_embedding = get_embedding(solution)
            # Insert into questions collection
            db.questions.insert_one(
                {
                    "question_id": question["question_id"],
                    "question_text": question["question_text"],
                    "image_path": question["image_path"],
                    "solution": solution,
                    "solution_embedding": solution_embedding,
                }
            )

    # Generate user responses
    responses = []
    for question in questions_data:
        response_text = get_openai_response(
            question["question_text"], question["image_path"]
        )
        response_embedding = get_embedding(response_text)
        responses.append(
            {
                "question_id": question["question_id"],
                "prompt": question["question_text"],  # store user's prompt
                "response": response_text,
                "embedding": response_embedding,
            }
        )

    # Insert user responses into user_responses collection
    db.user_responses.insert_one(
        {
            "user_name": user_name,
            "age": age,
            "career_profession": career_profession,
            "responses": responses,
        }
    )

    # Return responses for use in templates
    return responses[0]["response"], responses[1]["response"]
