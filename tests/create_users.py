from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Connect to MongoDB with username and password
mongo_client = MongoClient(os.getenv("MONGODB_URI"))  # Assumes URI includes username and password
db = mongo_client["iris_database"]

# Access the users collection
users_collection = db["personal"]

# Initialize the users collection with username and password
users_data = [
    {
        "username": "isma",
        "password": "1234",
    },
    {
        "username": "luz",
        "password": "1234",
    },
]

for user in users_data:
    existing_user = users_collection.find_one({"username": user["username"]})
    if not existing_user:
        users_collection.insert_one(user)
