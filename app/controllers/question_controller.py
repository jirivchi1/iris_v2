# app/controllers/question_controller.py

from app import db
from app.services.openai_service import (
    get_openai_response,
    generate_solution_description,
)
from app.services.embedding_service import get_embedding


def process_user_responses():
    """
    Procesa las respuestas de los usuarios que aún no han sido procesadas,
    generando las respuestas de la IA y los embeddings.
    """
    # Obtener todas las preguntas y crear un diccionario para acceder a ellas por 'question_id'
    questions = db.questions.find()
    questions_dict = {question["question_id"]: question for question in questions}

    # Obtener las respuestas de los usuarios que aún no han sido procesadas
    users = db.user_responses.find()
    for user in users:
        updated_responses = []
        needs_update = False
        for response in user.get("responses", []):
            if "ai_response" not in response:
                question_id = response["question_id"]
                question = questions_dict.get(question_id)
                if question:
                    image_path = question["image_path"]
                    prompt = response["prompt"]
                    # Generar la respuesta de la IA utilizando el prompt del usuario y la imagen
                    ai_response_text = get_openai_response(prompt, image_path)
                    # Generar el embedding de la respuesta de la IA
                    ai_response_embedding = get_embedding(ai_response_text)
                    # Actualizar la respuesta
                    response["ai_response"] = ai_response_text
                    response["ai_embedding"] = ai_response_embedding
                    needs_update = True
            updated_responses.append(response)
        if needs_update:
            # Actualizar las respuestas del usuario en la base de datos
            db.user_responses.update_one(
                {"_id": user["_id"]}, {"$set": {"responses": updated_responses}}
            )
