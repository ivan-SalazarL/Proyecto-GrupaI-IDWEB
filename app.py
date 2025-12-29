from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import requests  # Necesario para conectar con CIMA y FDA

app = Flask(__name__)
app.secret_key = "clave_secreta_super_segura"

# --- CONFIGURACIÓN DE BASE DE DATOS ---
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="SistemaFarmaceutico"
    )

# --- RUTAS PÚBLICAS ---

@app.route("/")
def inicio():
    return render_template("index.html")

# --- CATEGORÍAS (API FDA) ---
# Usamos FDA aquí para llenar las categorías automáticamente sin escribir a mano.
@app.route("/categorias")
def categorias():
    # Consultamos las clases farmacológicas más comunes
    url = "https://api.fda.gov/drug/label.json?count=openfda.pharm_class_epc.exact&limit=12"
    lista_categorias = []
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if "results" in data:
            lista_categorias = data["results"]
            
    except Exception as e:
        print(f"Error API FDA: {e}")
        
    return render_template("categorias.html", categorias=lista_categorias)

@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")

@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        flash("Mensaje enviado correctamente. Te contactaremos pronto.", "success")
        return redirect(url_for("contacto"))
    return render_template("contacto.html")

# --- BUSCADOR DE MEDICAMENTOS (API CIMA - ESPAÑA) ---
# Mejor opción para consumidores peruanos por el idioma español.
@app.route("/buscar_medicamentos", methods=["GET", "POST"])
def buscar_medicamentos():
    resultados = []
    busqueda = ""
    error = None

    if request.method == "POST":
        busqueda = request.form.get("busqueda", "").strip()
        
        if busqueda:
            try:
                # Conexión a la API de la AEMPS (España)
                url = f"https://cima.aemps.es/cima/rest/medicamentos?nombre={busqueda}"
                
                # CIMA a veces requiere headers básicos para no bloquear bots, por seguridad:
                headers = {'User-Agent': 'SistemaFarmaceutico/1.0'}
                respuesta = requests.get(url, headers=headers)
                
                if respuesta.status_code == 200:
                    datos = respuesta.json()
                    
                    # La API devuelve una lista bajo la clave "resultados"
                    if "resultados" in datos and len(datos["resultados"]) > 0:
                        # Limitamos a 10 para mantener la vista limpia
                        for item in datos["resultados"][:10]:
                            info = {
                                "marca": item.get("nombre", "Sin Nombre Comercial"),
                                "generico": item.get("pactivos", "No especificado"),
                                "fabricante": item.get("labtitular", "Laboratorio Desconocido"),
                                # CIMA usa 'receta' como booleano o string
                                "proposito": "Requiere Receta Médica" if item.get("receta") else "Venta Libre / Sin datos"
                            }
                            resultados.append(info)
                    else:
                        error = "No se encontraron medicamentos con ese nombre en el registro."
                else:
                    error = "La API externa no respondió correctamente."
                    
            except Exception as e:
                error = "Error de conexión con el servidor de medicamentos."
                print(f"Error API CIMA: {e}")

    return render_template("buscar_medicamentos.html", resultados=resultados, busqueda=busqueda, error=error)


# --- AUTENTICACIÓN (LOGIN / REGISTRO) ---

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
            # Se asigna rol 'usuario' por defecto
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

# --- GESTIÓN DE PROVEEDORES (CRUD) ---

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