# app/__init__.py
from flask import Flask
from pymongo import MongoClient
import os

# Inicialización de Flask
app = Flask(
    __name__,
    template_folder=os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates"
    ),
    static_folder=os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static"
    ),
)
app.secret_key = "mysecretkey"

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["iris_database"]
users_collection = db["users"]
questions_collection = db["questions"]

# Registrar los blueprints
from app.auth.routes import auth as auth_blueprint
from app.main.routes import main as main_blueprint
from app.encuesta.routes import encuesta as encuesta_blueprint
from app.quiz.routes import quiz as quiz_blueprint
from app.workers.routes import workers as workers_blueprint
from app.models.models import find_user, insert_survey_response


app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(main_blueprint)
app.register_blueprint(encuesta_blueprint, url_prefix="/encuesta")
app.register_blueprint(quiz_blueprint, url_prefix="/quiz")
app.register_blueprint(workers_blueprint, url_prefix="/workers")
