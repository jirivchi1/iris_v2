# app/services/embedding_service.py

import os
import numpy as np
from openai import OpenAI
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Connect to MongoDB
mongo_client = MongoClient(os.getenv("MONGODB_URI"))
db = mongo_client["iris_database"]

# Access collections
questions_collection = db["questions"]  # Updated collection name
user_responses_collection = db["user_responses"]  # New collection for user responses


def get_embedding(text):
    """Generates vector embeddings for the given text."""
    response = openai_client.embeddings.create(
        input=[text], model="text-embedding-3-small"
    )
    embedding = response.data[0].embedding
    return embedding


def update_solution_embeddings():
    """Generate embeddings for solutions that don't have them yet."""
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
            print(f"Updated solution embedding for {question['question_id']}")


def update_user_response_embeddings():
    """Generate embeddings for user responses that don't have them yet."""
    for user in user_responses_collection.find():
        updated_responses = []
        needs_update = False
        for response in user.get("responses", []):
            if "embedding" not in response:
                embedding = get_embedding(response["response"])
                response["embedding"] = embedding
                needs_update = True
            updated_responses.append(response)
        if needs_update:
            user_responses_collection.update_one(
                {"_id": user["_id"]}, {"$set": {"responses": updated_responses}}
            )
            print(f"Updated embeddings for user {user['user_name']}")


def cosine_similarity(a, b):
    """Calculates cosine similarity between two vectors."""
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def find_similar_responses(question_id, limit=5):
    """
    Find the most similar user responses to the solution for a specific question.
    Returns a ranking of user names and similarities.
    """
    # Fetch the solution embedding
    question = questions_collection.find_one({"question_id": question_id})
    solution_embedding = question.get("solution_embedding")
    if not solution_embedding:
        print(f"No solution embedding found for {question_id}.")
        return []

    # Fetch user responses for this question
    similarities = []
    for user in user_responses_collection.find():
        user_name = user.get("user_name")
        for response in user.get("responses", []):
            if response.get("question_id") == question_id:
                embedding = response.get("embedding")
                if embedding:
                    sim = cosine_similarity(solution_embedding, embedding)
                    similarities.append(
                        {
                            "user_name": user_name,
                            "similarity": sim,
                            "prompt": response.get("prompt"),  # Include the prompt
                        }
                    )
    # Sort by similarity
    similarities.sort(key=lambda x: x["similarity"], reverse=True)

    # Return top results
    return similarities[:limit]
