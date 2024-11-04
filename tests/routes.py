# app/routes.py
from flask import render_template, request, redirect, url_for, session, flash
from app import app, db, users_collection
from iris_v2.app.models.models import find_user, insert_survey_response

from app.controllers.question_controller import handle_question_and_response
from app.services.embedding_service import find_similar_responses


# Ruta para login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        if role == "usuario":
            user = find_user(username, password)
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
            flash("El nombre de usuario ya está registrado.", "danger")
            return redirect(url_for("signup"))

        users_collection.insert_one({"username": username, "password": password})
        flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
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
    session.clear()
    flash("Has cerrado sesión exitosamente.", "info")
    return redirect(url_for("login"))


# Ruta para el formulario
@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        feedback = request.form["feedback"]

        # Insertar los datos en la colección "encuesta"
        insert_survey_response(name, email, feedback)

        flash("Encuesta enviada exitosamente.", "success")
        return redirect(url_for("success"))

    return render_template("form.html")


# Ruta para la página de éxito
@app.route("/success")
def success():
    return render_template("success.html")


# Ruta para el dashboard (solo accesible para personal)
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html")
    else:
        flash(
            "Debes iniciar sesión como personal para acceder al dashboard.", "warning"
        )
        return redirect(url_for("login"))


@app.route("/test", methods=["GET", "POST"])
def test():
    relative_image_path = "images/test/uvas.jpg"
    full_image_path = f"static/{relative_image_path}"

    if request.method == "POST":
        user_name = request.form["user_name"]
        question = request.form["question"]
        response = handle_question_and_response(user_name, question, full_image_path)
        return render_template(
            "response.html",
            image_path=relative_image_path,
            question=question,
            response=response,
            user_name=user_name,
        )

    return render_template("test.html", image_path=relative_image_path)


@app.route("/similar-responses", methods=["GET", "POST"])
def similar_responses():
    similar_users = []
    query = ""
    if request.method == "POST":
        query = request.form.get("query")
        if query:
            similar_users = find_similar_responses(query)
        else:
            flash("Please enter a query.", "warning")

    return render_template(
        "similar_responses.html", similar_users=similar_users, query=query
    )
