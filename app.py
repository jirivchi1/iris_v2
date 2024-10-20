from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient

app = Flask(__name__)

# Configurar una clave secreta para las sesiones y los mensajes flash
app.secret_key = "mysecretkey"

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["iris_database"]
users_collection = db["users"]


# Ruta para el login (primera página que verá el usuario)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users_collection.find_one({"username": username, "password": password})

        if user:
            session["username"] = username
            flash("Login exitoso", "success")  # Mensaje flash de éxito
            return redirect(url_for("home"))
        else:
            flash(
                "Credenciales inválidas. Inténtalo de nuevo.", "danger"
            )  # Mensaje flash de error
    return render_template("login.html")


# Ruta para el registro
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = users_collection.find_one({"username": username})

        if existing_user:
            flash(
                "El nombre de usuario ya está registrado.", "danger"
            )  # Mensaje flash de error
            return redirect(url_for("signup"))

        users_collection.insert_one({"username": username, "password": password})
        flash(
            "Registro exitoso. Ahora puedes iniciar sesión.", "success"
        )  # Mensaje flash de éxito
        return redirect(url_for("login"))

    return render_template("signup.html")


# Ruta para el home (protegida)
@app.route("/")
def home():
    if "username" in session:
        return render_template("home.html", username=session["username"])
    else:
        flash("Debes iniciar sesión para acceder a esta página.", "warning")
        return redirect(url_for("login"))


# Ruta para cerrar sesión
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    flash("Has cerrado sesión exitosamente.", "info")  # Mensaje flash al cerrar sesión
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
