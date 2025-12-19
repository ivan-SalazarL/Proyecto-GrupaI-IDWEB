from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "clave_secreta_simple"

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="SistemaFarmaceutico"
    )

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/categorias")
def categorias():
    return render_template("categorias.html")

@app.route("/proveedores")
def proveedores():
    return render_template("proveedores.html")

@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")

@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        asunto = request.form["asunto"]
        mensaje = request.form["mensaje"]
    return render_template("contacto.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM usuarios WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()

        if user:
            session["usuario"] = user["nombre"]
            session["rol"] = user["rol"]
            return redirect(url_for("inicio"))

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password, rol) VALUES (%s,%s,%s,'usuario')",
            (nombre, email, password)
        )
        db.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("inicio"))

@app.route("/admin")
def admin():
    if session.get("rol") != "admin":
        return "Acceso denegado"
    return "Panel de administrador"

if __name__ == "__main__":
    app.run(debug=True)
