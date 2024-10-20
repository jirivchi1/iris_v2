from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


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
        # Aquí validaríamos usuario y contraseña
        if (
            username == "admin" and password == "password"
        ):  # Simulación de login correcto
            return redirect(
                url_for("home")
            )  # Si el login es correcto, redirige al home
        else:
            return "Credenciales inválidas"  # Si es incorrecto, muestra mensaje
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
