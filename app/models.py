# app/models.py
from app import db


# Función para encontrar un usuario en la base de datos
def find_user(username, password):
    return db.users.find_one({"username": username, "password": password})


# Función para insertar una respuesta de encuesta en la base de datos
def insert_survey_response(name, email, feedback):
    db.encuesta.insert_one({"name": name, "email": email, "feedback": feedback})
