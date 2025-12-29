from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import requests  # <--- IMPORTANTE: Necesario para la API openFDA

app = Flask(__name__)
app.secret_key = "clave_secreta_super_segura"

# --- CONFIGURACIÓN DE BASE DE DATOS ---
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", # Ajusta si tu MySQL tiene contraseña
        database="SistemaFarmaceutico"
    )

# --- NUEVA FUNCIÓN: API OPENFDA ---
@app.route("/buscar_medicamentos", methods=["GET", "POST"])
def buscar_medicamentos():
    resultados = []
    busqueda = ""
    error = None

    if request.method == "POST":
        busqueda = request.form.get("busqueda", "").strip()
        
        if busqueda:
            try:
                # Consultamos la API pública de openFDA
                url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:{busqueda}&limit=5"
                
                respuesta = requests.get(url)
                datos = respuesta.json()

                if "results" in datos:
                    for item in datos["results"]:
                        info = {
                            "marca": item.get("openfda", {}).get("brand_name", ["N/A"])[0],
                            "generico": item.get("openfda", {}).get("generic_name", ["N/A"])[0],
                            "fabricante": item.get("openfda", {}).get("manufacturer_name", ["N/A"])[0],
                            "proposito": item.get("purpose", ["No especificado"])[0]
                        }
                        resultados.append(info)
                else:
                    error = "No se encontraron medicamentos con ese nombre."
            except Exception as e:
                error = "Error al conectar con openFDA. Intenta nuevamente."
                print(f"Error API: {e}")

    return render_template("buscar_medicamentos.html", resultados=resultados, busqueda=busqueda, error=error)


# --- RUTAS PÚBLICAS ---

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/categorias")
def categorias():
    return render_template("categorias.html")

@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")

@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        flash("Mensaje enviado correctamente. Te contactaremos pronto.", "success")
        return redirect(url_for("contacto"))
    return render_template("contacto.html")

# --- AUTENTICACIÓN ---

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        db.close()

        if user:
            session["usuario_id"] = user["id"]
            session["usuario"] = user["nombre"]
            session["rol"] = user["rol"]
            flash(f"Bienvenido {user['nombre']}", "success")
            return redirect(url_for("inicio"))
        else:
            flash("Credenciales incorrectas", "error")
            
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = request.form["password"]
        
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, email, password, rol) VALUES (%s,%s,%s,'usuario')", 
                           (nombre, email, password))
            db.commit()
            db.close()
            flash("Registro exitoso, por favor inicia sesión", "success")
            return redirect(url_for("login"))
        except:
            flash("El correo ya está registrado", "error")

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión", "info")
    return redirect(url_for("inicio"))

# --- CRUD PROVEEDORES ---

@app.route("/proveedores")
def proveedores():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM proveedores")
    lista_proveedores = cursor.fetchall()
    db.close()
    return render_template("proveedores.html", proveedores=lista_proveedores)

@app.route("/proveedor/agregar", methods=["POST"])
def agregar_proveedor():
    if not session.get("usuario"):
        return redirect(url_for("login"))
        
    nombre = request.form["nombre"]
    contacto = request.form["contacto"]
    telefono = request.form["telefono"]
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO proveedores (nombre, contacto, telefono, estado) VALUES (%s, %s, %s, 'activo')",
                   (nombre, contacto, telefono))
    db.commit()
    db.close()
    flash("Proveedor agregado correctamente", "success")
    return redirect(url_for("proveedores"))

@app.route("/proveedor/eliminar/<int:id>")
def eliminar_proveedor(id):
    if session.get("rol") != "admin":
        flash("Solo administradores pueden eliminar", "error")
        return redirect(url_for("proveedores"))

    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM proveedores WHERE id=%s", (id,))
    db.commit()
    db.close()
    flash("Proveedor eliminado", "success")
    return redirect(url_for("proveedores"))

@app.route("/proveedor/editar/<int:id>", methods=["GET", "POST"])
def editar_proveedor(id):
    if session.get("rol") != "admin":
        flash("Solo administradores pueden editar", "error")
        return redirect(url_for("proveedores"))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        nombre = request.form["nombre"]
        contacto = request.form["contacto"]
        telefono = request.form["telefono"]
        estado = request.form["estado"]

        cursor.execute("""
            UPDATE proveedores 
            SET nombre=%s, contacto=%s, telefono=%s, estado=%s 
            WHERE id=%s
        """, (nombre, contacto, telefono, estado, id))
        db.commit()
        db.close()
        flash("Proveedor actualizado correctamente", "success")
        return redirect(url_for("proveedores"))

    cursor.execute("SELECT * FROM proveedores WHERE id=%s", (id,))
    proveedor = cursor.fetchone()
    db.close()
    return render_template("editar_proveedor.html", p=proveedor)

# --- PEDIDOS ---

@app.route("/nuevo_pedido", methods=["GET", "POST"])
def nuevo_pedido():
    if not session.get("usuario"):
        flash("Debes iniciar sesión para hacer un pedido", "error")
        return redirect(url_for("login"))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        proveedor_id = request.form["proveedor_id"]
        usuario_id = session["usuario_id"]
        
        cursor.execute("INSERT INTO pedidos (usuario_id, proveedor_id, estado) VALUES (%s, %s, 'Pendiente')",
                       (usuario_id, proveedor_id))
        db.commit()
        db.close()
        flash("Pedido realizado con éxito", "success")
        return redirect(url_for("inicio"))

    cursor.execute("SELECT * FROM proveedores WHERE estado='activo'")
    proveedores = cursor.fetchall()
    db.close()
    return render_template("nuevo_pedido.html", proveedores=proveedores)

# --- PANEL ADMIN ---

@app.route("/admin")
def admin():
    if session.get("rol") != "admin":
        flash("Acceso denegado", "error")
        return redirect(url_for("inicio"))
    
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    query = """
        SELECT p.id, u.nombre as usuario, prov.nombre as proveedor, p.fecha, p.estado 
        FROM pedidos p
        JOIN usuarios u ON p.usuario_id = u.id
        JOIN proveedores prov ON p.proveedor_id = prov.id
        ORDER BY p.fecha DESC
    """
    cursor.execute(query)
    pedidos = cursor.fetchall()
    db.close()
    
    return render_template("admin.html", pedidos=pedidos)

# --- INICIO DEL SERVIDOR ---
if __name__ == "__main__":
    app.run(debug=True)