import os
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
embeddings_collection = db["embeddings"]


def get_embedding(text):
    """Generates vector embeddings for the given text."""
    response = openai_client.embeddings.create(
        input=[text], model="text-embedding-3-small"
    )
    return response.data[0].embedding


def find_similar_responses(query_text, limit=5):
    """
    Find the most similar responses to the given query text.
    Returns a ranking of user names and questions, with the most similar first.
    """
    query_embedding = get_embedding(query_text)

    results = embeddings_collection.find(
        {
            "embedding": {
                "$nearSphere": {
                    "$geometry": {"type": "Point", "coordinates": query_embedding}
                }
            }
        },
        {"user_name": 1, "question_id": 1, "_id": 0},
    ).limit(limit)

    # Return a list of (user_name, question_id) tuples ranked by similarity
    return [(result["user_name"], result["question_id"]) for result in results]


# Example usage
if __name__ == "__main__":
    query = "Un perro está comiendo un plátano"
    similar_users = find_similar_responses(query)
    print("Most similar responses from users (in order):")
    for i, user in enumerate(similar_users, 1):
        print(f"{i}. {user}")
