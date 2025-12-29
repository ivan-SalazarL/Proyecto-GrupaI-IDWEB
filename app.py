from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import requests  # Para la API de CIMA (España)

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

# --- 1. VISTA DE CATEGORÍAS (RESUMEN) ---
@app.route("/categorias")
def categorias():
    lista_categorias = []
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # Agrupamos los productos por su Forma Farmacéutica y contamos cuántos hay
        query = """
            SELECT forma_farmaceutica as nombre, COUNT(*) as total 
            FROM productos_digemid 
            WHERE forma_farmaceutica != '' 
            GROUP BY forma_farmaceutica 
            ORDER BY total DESC 
            LIMIT 12
        """
        cursor.execute(query)
        lista_categorias = cursor.fetchall()
        db.close()
        
    except Exception as e:
        print(f"Error MySQL Categorías: {e}")
        
    return render_template("categorias.html", categorias=lista_categorias)

# --- 2. VISTA DE CATÁLOGO (DETALLE DE PRODUCTOS) ---
@app.route("/categoria/<string:nombre_categoria>")
def ver_categoria(nombre_categoria):
    productos = []
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # Buscamos los productos que pertenezcan a esa categoría exacta
        sql = "SELECT * FROM productos_digemid WHERE forma_farmaceutica = %s LIMIT 50"
        cursor.execute(sql, (nombre_categoria,))
        productos = cursor.fetchall()
        db.close()
        
    except Exception as e:
        print(f"Error al cargar catálogo: {e}")

    return render_template("ver_categoria.html", productos=productos, categoria=nombre_categoria)

@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")

@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        flash("Mensaje enviado correctamente. Te contactaremos pronto.", "success")
        return redirect(url_for("contacto"))
    return render_template("contacto.html")

# --- BUSCADOR HÍBRIDO ---
@app.route("/buscar_medicamentos", methods=["GET", "POST"])
def buscar_medicamentos():
    resultados = []
    busqueda = ""
    error = None

    if request.method == "GET":
        busqueda = request.args.get("busqueda", "").strip()
    elif request.method == "POST":
        busqueda = request.form.get("busqueda", "").strip()

    if busqueda:
        try:
            # A. BÚSQUEDA LOCAL (DIGEMID)
            db = get_db()
            cursor = db.cursor(dictionary=True)
            sql = """
                SELECT * FROM productos_digemid 
                WHERE nombre_producto LIKE %s OR forma_farmaceutica LIKE %s 
                LIMIT 20
            """
            term = f"%{busqueda}%"
            cursor.execute(sql, (term, term))
            datos_locales = cursor.fetchall()
            db.close()

            if datos_locales:
                for item in datos_locales:
                    resultados.append({
                        "marca": item["nombre_producto"],
                        "generico": item["concentracion"], 
                        "fabricante": item["titular_registro"],
                        "proposito": f"Reg: {item['registro_sanitario']} | {item['forma_farmaceutica']}"
                    })
            else:
                # B. BÚSQUEDA API ESPAÑA (RESPALDO)
                url = f"https://cima.aemps.es/cima/rest/medicamentos?nombre={busqueda}"
                headers = {'User-Agent': 'SistemaFarmaceutico/1.0'}
                respuesta = requests.get(url, headers=headers)
                
                if respuesta.status_code == 200:
                    datos_api = respuesta.json()
                    if "resultados" in datos_api:
                        for item in datos_api["resultados"][:10]:
                            resultados.append({
                                "marca": item.get("nombre", "Sin Nombre"),
                                "generico": item.get("pactivos", "Genérico"),
                                "fabricante": item.get("labtitular", "Laboratorio"),
                                "proposito": "Resultado Internacional (España)"
                            })
                
                if not resultados:
                    error = "No se encontraron resultados."

        except Exception as e:
            error = "Error al buscar."
            print(f"Error buscador: {e}")

    return render_template("buscar_medicamentos.html", resultados=resultados, busqueda=busqueda, error=error)

# --- LOGIN Y REGISTRO ---

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

# --- PROVEEDORES ---

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
    flash("Proveedor agregado", "success")
    return redirect(url_for("proveedores"))

@app.route("/proveedor/eliminar/<int:id>")
def eliminar_proveedor(id):
    if session.get("rol") != "admin":
        flash("Solo admin puede eliminar", "error")
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
        flash("Solo admin puede editar", "error")
        return redirect(url_for("proveedores"))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        nombre = request.form["nombre"]
        contacto = request.form["contacto"]
        telefono = request.form["telefono"]
        estado = request.form["estado"]

        cursor.execute("UPDATE proveedores SET nombre=%s, contacto=%s, telefono=%s, estado=%s WHERE id=%s", 
                      (nombre, contacto, telefono, estado, id))
        db.commit()
        db.close()
        flash("Proveedor actualizado", "success")
        return redirect(url_for("proveedores"))

    cursor.execute("SELECT * FROM proveedores WHERE id=%s", (id,))
    proveedor = cursor.fetchone()
    db.close()
    return render_template("editar_proveedor.html", p=proveedor)

# --- PEDIDOS Y ADMIN ---

@app.route("/nuevo_pedido", methods=["GET", "POST"])
def nuevo_pedido():
    if not session.get("usuario"):
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
        flash("Pedido realizado", "success")
        return redirect(url_for("inicio"))
    cursor.execute("SELECT * FROM proveedores WHERE estado='activo'")
    proveedores = cursor.fetchall()
    db.close()
    return render_template("nuevo_pedido.html", proveedores=proveedores)

@app.route("/admin")
def admin():
    if session.get("rol") != "admin":
        return redirect(url_for("inicio"))
    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT p.id, u.nombre as usuario, prov.nombre as proveedor, p.fecha, p.estado 
        FROM pedidos p JOIN usuarios u ON p.usuario_id = u.id JOIN proveedores prov ON p.proveedor_id = prov.id
        ORDER BY p.fecha DESC
    """
    cursor.execute(query)
    pedidos = cursor.fetchall()
    db.close()
    return render_template("admin.html", pedidos=pedidos)

if __name__ == "__main__":
    app.run(debug=True)