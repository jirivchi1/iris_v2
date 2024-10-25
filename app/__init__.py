# app/__init__.py
from flask import Flask
from pymongo import MongoClient

# Inicialización de Flask
app = Flask(__name__, template_folder="../templates")
app.secret_key = "mysecretkey"

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["iris_database"]
users_collection = db["users"]

# Importar rutas
from app import routes
