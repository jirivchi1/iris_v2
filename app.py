from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Conexión a MongoDB usando tu base de datos 'iris_database'
client = MongoClient("mongodb://localhost:27017/")
db = client["iris_database"]  # Base de datos 'iris_database'
users_collection = db["users"]  # Colección nueva 'users'


# Ruta para el home
@app.route("/")
def home():
    return render_template("home.html")


# Ruta para el login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users_collection.find_one({"username": username, "password": password})

        if user:  # Si encontramos un usuario con esas credenciales
            return redirect(url_for("home"))
        else:
            return "Credenciales inválidas"
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
