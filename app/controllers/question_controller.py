from app import db
from app.services.openai_service import get_openai_response


def handle_question_and_response(user_name, question, image_path):
    response = get_openai_response(question, image_path)

    # Guardar en MongoDB
    db.questions_collection.insert_one(
        {
            "user_name": user_name,
            "question": question,
            "response": response,
            "image_path": image_path,
        }
    )

    return response
