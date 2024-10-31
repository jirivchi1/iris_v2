from app import db
from app.services.openai_service import get_openai_response


def handle_questions_and_responses(
    user_name,
    age,
    career_profession,
    question_1,
    question_2,
    image_path_1,
    image_path_2,
):
    # Obtener respuestas para cada pregunta usando OpenAI
    response_1 = get_openai_response(question_1, image_path_1)
    response_2 = get_openai_response(question_2, image_path_2)

    # Guardar en MongoDB
    db.questions_collection.insert_one(
        {
            "user_name": user_name,
            "age": age,
            "career_profession": career_profession,
            "question_1": question_1,
            "response_1": response_1,
            "image_path_1": image_path_1,
            "question_2": question_2,
            "response_2": response_2,
            "image_path_2": image_path_2,
        }
    )

    # Retornar ambas respuestas
    return response_1, response_2
