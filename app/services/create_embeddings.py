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
questions_collection = db["questions_collection"]
embeddings_collection = db["embeddings"]


# Function to get embedding
def get_embedding(text):
    """Generates vector embeddings for the given text."""
    response = openai_client.embeddings.create(
        input=[text], model="text-embedding-3-small"
    )
    return response.data[0].embedding


# Function to create embeddings and store in new collection
def create_and_store_embeddings():
    for doc in questions_collection.find():
        response_text = doc.get("response", "")
        if response_text:
            embedding = get_embedding(response_text)
            embeddings_collection.insert_one(
                {
                    "user_name": doc["user_name"],
                    "response": response_text,
                    "embedding": embedding,
                }
            )
    print("Embeddings created and stored successfully.")


if __name__ == "__main__":
    create_and_store_embeddings()
