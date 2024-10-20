from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient

app = Flask(__name__)

# Configurar una clave secreta para las sesiones y los mensajes flash
app.secret_key = "mysecretkey"

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["iris_database"]
users_collection = db["users"]


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]  # Verificar si es usuario o personal

        if role == "usuario":
            user = users_collection.find_one(
                {"username": username, "password": password}
            )
            if user:
                session["username"] = username
                flash("Login como usuario exitoso", "success")
                return redirect(url_for("home"))
            else:
                flash("Credenciales inválidas. Inténtalo de nuevo.", "danger")
                return redirect(url_for("login"))

        elif role == "personal":
            personal = db.personal.find_one(
                {"username": username, "password": password}
            )
            if personal:
                session["username"] = username
                flash("Login como personal exitoso", "success")
                return redirect(url_for("dashboard"))
            else:
                flash(
                    "Credenciales de personal inválidas. Inténtalo de nuevo.", "danger"
                )
                return redirect(url_for("login"))

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


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()  # Limpiar toda la sesión para evitar acumulación
    flash("Has cerrado sesión exitosamente.", "info")
    return redirect(url_for("login"))


@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        # Recibimos los datos del formulario
        name = request.form["name"]
        email = request.form["email"]
        feedback = request.form["feedback"]

        # Insertamos los datos en la colección "encuesta"
        db.encuesta.insert_one({"name": name, "email": email, "feedback": feedback})

        # Flash message y redirigir a una página diferente
        flash("Encuesta enviada exitosamente.", "success")
        return redirect(url_for("success"))  # Redirigir a una nueva página de éxito

    # Solo renderizamos la página en GET
    return render_template("form.html")


@app.route("/success")
def success():
    return render_template(
        "success.html"
    )  # Crear una nueva plantilla para la página de éxito


@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html")
    else:
        flash(
            "Debes iniciar sesión como personal para acceder al dashboard.", "warning"
        )
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
