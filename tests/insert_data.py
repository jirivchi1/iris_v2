from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Connect to MongoDB
mongo_client = MongoClient(os.getenv("MONGODB_URI"))
db = mongo_client["iris_database"]

# Access collections
questions_collection = db["questions"]  # Updated collection name

# Initialize the questions collection if not already done
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
    existing_question = db.questions.find_one({"question_id": question["question_id"]})
    if not existing_question:
        db.questions.insert_one(question)
