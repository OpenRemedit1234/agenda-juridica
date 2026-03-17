from flask import Flask, render_template, request, redirect, session
import json
import os

app = Flask(__name__)
app.secret_key = "clave_secreta"

DATA_FILE = "data.json"

# -------------------------
# FUNCIONES DE DATOS
# -------------------------

def cargar_datos():
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        return {"notas": [], "citas": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def guardar_datos(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# -------------------------
# LOGIN
# -------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["usuario"]
        password = request.form["password"]

        if user == "Juan" and password == "Juan":
            session["login"] = True
            return redirect("/")
        else:
            return "Credenciales incorrectas"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("login", None)
    return redirect("/login")

def protegido():
    return "login" in session

# -------------------------
# HOME
# -------------------------

@app.route("/")
def index():
    if not protegido():
        return redirect("/login")

    data = cargar_datos()

    # ordenar citas por fecha
    data["citas"] = sorted(data["citas"], key=lambda x: x["fecha"])

    return render_template("index.html", data=data)

# -------------------------
# NOTAS
# -------------------------

@app.route("/nueva_nota", methods=["GET", "POST"])
def nueva_nota():
    if not protegido():
        return redirect("/login")

    if request.method == "POST":
        data = cargar_datos()
        data["notas"].append({
            "titulo": request.form["titulo"],
            "contenido": request.form["contenido"]
        })
        guardar_datos(data)
        return redirect("/")

    return render_template("nueva_nota.html")

@app.route("/eliminar_nota", methods=["POST"])
def eliminar_nota():
    if not protegido():
        return redirect("/login")

    data = cargar_datos()
    index = int(request.form["index"])
    data["notas"].pop(index)
    guardar_datos(data)
    return redirect("/")

# -------------------------
# CITAS
# -------------------------

@app.route("/nueva_cita", methods=["GET", "POST"])
def nueva_cita():
    if not protegido():
        return redirect("/login")

    if request.method == "POST":
        data = cargar_datos()
        data["citas"].append({
            "fecha": request.form["fecha"],
            "hora": request.form["hora"],
            "cliente": request.form["cliente"],
            "asunto": request.form["asunto"]
        })
        guardar_datos(data)
        return redirect("/")

    return render_template("nueva_cita.html")

@app.route("/eliminar_cita", methods=["POST"])
def eliminar_cita():
    if not protegido():
        return redirect("/login")

    data = cargar_datos()
    index = int(request.form["index"])
    data["citas"].pop(index)
    guardar_datos(data)
    return redirect("/")

# -------------------------
# RUN
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)