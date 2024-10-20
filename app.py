from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["iris_database"]  # Base de datos
users_collection = db["users"]  # Colección de usuarios


# Ruta para el home
@app.route("/")
def home():
    return render_template("home.html")


# Ruta para el registro
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Verificamos si el usuario ya existe
        existing_user = users_collection.find_one({"username": username})

        if existing_user:
            return "El nombre de usuario ya está registrado"

        # Si no existe, lo registramos
        users_collection.insert_one({"username": username, "password": password})
        return redirect(url_for("login"))  # Redirige al login tras el registro

    return render_template("signup.html")


# Ruta para el login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users_collection.find_one({"username": username, "password": password})

        if user:
            return redirect(url_for("home"))
        else:
            return "Credenciales inválidas"
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
