from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from functools import wraps
from pathlib import Path

app = Flask(__name__)
app.secret_key = "CAMBIA_ESTA_CLAVE_POR_UNA_LARGA_Y_PRIVADA"
DB_PATH = Path(__file__).with_name("eduplay.db")


def conectar():
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    return conexion


def inicializar_bd():
    with conectar() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS resultados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                materia TEXT NOT NULL,
                correctas INTEGER NOT NULL,
                total INTEGER NOT NULL,
                fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)


def requiere_sesion(vista):
    @wraps(vista)
    def wrapper(*args,  **kwargs):
        if "usuario_id" not in session:
            flash("Inicia sesión para entrar a las actividades.", "info")
            return redirect(url_for("login"))
        return vista(*args, **kwargs)
    return wrapper


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not nombre or not email or len(password) < 8:
            flash("Completa todos los campos. La contraseña debe tener al menos 8 caracteres.", "error")
            return render_template("registro.html")

        try:
            with conectar() as db:
                db.execute(
                    "INSERT INTO usuarios (nombre, email, password_hash) VALUES (?, ?, ?)",
                    (nombre, email, generate_password_hash(password))
                )
            flash("Cuenta creada. Ya puedes iniciar sesión.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Ese correo ya está registrado.", "error")

    return render_template("registro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        with conectar() as db:
            usuario = db.execute(
                "SELECT id, nombre, email, password_hash FROM usuarios WHERE email = ?",
                (email,)
            ).fetchone()

        if usuario and check_password_hash(usuario["password_hash"], password):
            session.clear()
            session["usuario_id"] = usuario["id"]
            session["nombre"] = usuario["nombre"]
            return redirect(url_for("panel"))
        flash("Correo o contraseña incorrectos.", "error")

    return render_template("login.html")


@app.route("/salir")
def salir():
    session.clear()
    flash("Cerraste sesión.", "info")
    return redirect(url_for("inicio"))


@app.route("/panel")
@requiere_sesion
def panel():
    with conectar() as db:
        resultados = db.execute(
            """SELECT materia, correctas, total, fecha FROM resultados
               WHERE usuario_id = ? ORDER BY id DESC LIMIT 10""",
            (session["usuario_id"],)
        ).fetchall()
    return render_template("panel.html", resultados=resultados)


@app.route("/lectura")
@requiere_sesion
def lectura():
    return render_template("lectura.html")


@app.route("/matematicas")
@requiere_sesion
def matematicas():
    return render_template("matematicas.html")


@app.route("/api/resultado", methods=["POST"])
@requiere_sesion
def guardar_resultado():
    datos = request.get_json(silent=True) or {}
    materia = datos.get("materia")
    correctas = datos.get("correctas")
    total = datos.get("total")

    if materia not in ("Lectura", "Matemáticas"):
        return jsonify({"error": "Materia no válida."}), 400
    if not isinstance(correctas, int) or not isinstance(total, int):
        return jsonify({"error": "El resultado debe contener números enteros."}), 400
    if total < 1 or correctas < 0 or correctas > total or total > 100:
        return jsonify({"error": "El resultado no es válido."}), 400

    with conectar() as db:
        db.execute(
            "INSERT INTO resultados (usuario_id, materia, correctas, total) VALUES (?, ?, ?, ?)",
            (session["usuario_id"], materia, correctas, total)
        )
    return jsonify({"mensaje": "Resultado guardado."})


if __name__ == "__main__":
    inicializar_bd()
    app.run(debug=True)
