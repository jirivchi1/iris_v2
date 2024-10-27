# app/__init__.py
from flask import Flask
from pymongo import MongoClient
import os

# Get the absolute path to the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Inicialización de Flask
app = Flask(
    __name__,
    template_folder=os.path.join(project_root, "templates"),
    static_folder=os.path.join(project_root, "static"),
)
app.secret_key = "mysecretkey"

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["iris_database"]
users_collection = db["users"]
questions_collection = db["questions"]  # Nueva colección para preguntas


# Importar rutas
from app import routes
