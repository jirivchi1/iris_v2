# app/services/embedding_service.py

import os
import numpy as np
from openai import OpenAI
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar el cliente de OpenAI
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Conectar a MongoDB
mongo_client = MongoClient(os.getenv("MONGODB_URI"))
db = mongo_client["iris_database"]

# Acceder a las colecciones
questions_collection = db["questions"]
user_responses_collection = db["user_responses"]


def get_embedding(text):
    """Genera el embedding vectorial para un texto dado."""
    response = openai_client.embeddings.create(
        input=[text], model="text-embedding-ada-002"
    )
    embedding = response.data[0].embedding
    return embedding


def update_solution_embeddings():
    """Genera embeddings para las soluciones que aún no los tienen."""
    for question in questions_collection.find(
        {"solution_embedding": {"$exists": False}}
    ):
        solution = question.get("solution")
        if solution:
            solution_embedding = get_embedding(solution)
            questions_collection.update_one(
                {"_id": question["_id"]},
                {"$set": {"solution_embedding": solution_embedding}},
            )
            print(
                f"Actualizado embedding de la solución para {question['question_id']}"
            )


def find_similar_responses(question_id, limit=20):
    """
    Encuentra las respuestas de la IA más similares a la solución para una pregunta específica.
    Devuelve un ranking de nombres de usuarios y similitudes.
    """
    # Obtener el embedding de la solución
    question = questions_collection.find_one({"question_id": question_id})
    solution_embedding = question.get("solution_embedding")
    if not solution_embedding:
        print(f"No se encontró embedding de la solución para {question_id}.")
        return []

    # Obtener las respuestas de los usuarios para esta pregunta
    similarities = []
    for user in user_responses_collection.find():
        user_name = user.get("user_name")
        for response in user.get("responses", []):
            if response.get("question_id") == question_id:
                ai_embedding = response.get("ai_embedding")
                if ai_embedding:
                    sim = cosine_similarity(solution_embedding, ai_embedding)
                    similarities.append(
                        {
                            "user_name": user_name,
                            "similarity": sim,
                            "user_prompt": response.get("prompt"),
                            "ai_response": response.get("ai_response"),
                        }
                    )
    # Ordenar por similitud
    similarities.sort(key=lambda x: x["similarity"], reverse=True)

    # Devolver los mejores resultados
    return similarities[:limit]


def cosine_similarity(a, b):
    """Calcula la similitud coseno entre dos vectores."""
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# Si necesitas la función para procesar respuestas de usuarios en segundo plano, puedes agregarla
# En este caso, como ya estamos generando las respuestas y embeddings en tiempo real en question_controller.py,
# no es necesario incluirla aquí.
