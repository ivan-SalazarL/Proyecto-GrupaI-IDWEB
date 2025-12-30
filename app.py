from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import requests

app = Flask(__name__)
app.secret_key = "clave_secreta_super_segura"

# -------------------------------------------------
# CONFIGURACIÓN DE BASE DE DATOS
# -------------------------------------------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="SistemaFarmaceutico"
    )

# -------------------------------------------------
# RUTAS PÚBLICAS
# -------------------------------------------------
@app.route("/")
def inicio():
    db = get_db()
    cursor = db.cursor()
    
    # 1. Contar Total de Productos registrados
    cursor.execute("SELECT COUNT(*) FROM productos_digemid")
    total_productos = cursor.fetchone()[0]
    
    # 2. Contar Productos con Stock Bajo (ejemplo: menos de 20 unidades)
    # Si acabas de crear la columna, esto funcionará perfecto.
    try:
        cursor.execute("SELECT COUNT(*) FROM productos_digemid WHERE stock < 20")
        stock_bajo = cursor.fetchone()[0]
    except:
        stock_bajo = 0 # Por si acaso falle la consulta
        
    db.close()
    
    return render_template("index.html", total=total_productos, bajo=stock_bajo)

@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")

# -------------------------------------------------
# CONTACTO (GUARDA EN BD)
# -------------------------------------------------
@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        mensaje = request.form["mensaje"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO contactos (nombre, email, mensaje) VALUES (%s, %s, %s)",
            (nombre, email, mensaje)
        )
        db.commit()
        db.close()

        flash("Mensaje enviado y guardado correctamente", "success")
        return redirect(url_for("contacto"))

    return render_template("contacto.html")

# -------------------------------------------------
# CATEGORÍAS
# -------------------------------------------------
@app.route("/categorias")
def categorias():
    grupos = [
        {"nombre": "Analgésicos", "desc": "Alivio del dolor y fiebre", "keyword": "PARACETAMOL"},
        {"nombre": "Antiinflamatorios", "desc": "Reduce inflamación", "keyword": "IBUPROFENO"},
        {"nombre": "Antibióticos", "desc": "Infecciones bacterianas", "keyword": "AMOXICILINA"},
        {"nombre": "Gástricos", "desc": "Protección estomacal", "keyword": "OMEPRAZOL"}
    ]

    resultado = []
    db = get_db()
    cursor = db.cursor()

    for g in grupos:
        cursor.execute(
            "SELECT COUNT(*) FROM productos_digemid WHERE nombre_producto LIKE %s",
            (f"%{g['keyword']}%",)
        )
        total = cursor.fetchone()[0]
        resultado.append({
            "nombre": g["nombre"],
            "descripcion": g["desc"],
            "total": total,
            "busqueda": g["keyword"]
        })

    db.close()
    return render_template("categorias.html", categorias=resultado)

# -------------------------------------------------
# BUSCADOR
# -------------------------------------------------
@app.route("/buscar_medicamentos", methods=["GET", "POST"])
def buscar_medicamentos():
    resultados = []
    busqueda = request.args.get("busqueda") or request.form.get("busqueda")

    if busqueda:
        try:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM productos_digemid WHERE nombre_producto LIKE %s LIMIT 20",
                (f"%{busqueda}%",)
            )
            datos = cursor.fetchall()
            db.close()

            if datos:
                for d in datos:
                    resultados.append({
                        "marca": d["nombre_producto"],
                        "generico": d["concentracion"],
                        "fabricante": d["titular_registro"],
                        "proposito": d["forma_farmaceutica"]
                    })
            else:
                url = f"https://cima.aemps.es/cima/rest/medicamentos?nombre={busqueda}"
                r = requests.get(url)
                if r.status_code == 200:
                    for item in r.json().get("resultados", [])[:10]:
                        resultados.append({
                            "marca": item.get("nombre"),
                            "generico": item.get("pactivos"),
                            "fabricante": item.get("labtitular"),
                            "proposito": "Resultado internacional"
                        })

        except Exception as e:
            print(e)

    return render_template("buscar_medicamentos.html", resultados=resultados, busqueda=busqueda)

# -------------------------------------------------
# AUTENTICACIÓN
# -------------------------------------------------
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
        db.close()

        if user:
            session["usuario_id"] = user["id"]
            session["usuario"] = user["nombre"]
            session["rol"] = user["rol"]
            flash("Bienvenido", "success")
            return redirect(url_for("inicio"))

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
            cursor.execute(
                "INSERT INTO usuarios (nombre, email, password) VALUES (%s,%s,%s)",
                (nombre, email, password)
            )
            db.commit()
            db.close()
            flash("Registro exitoso", "success")
            return redirect(url_for("login"))
        except:
            flash("Correo ya registrado", "error")

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada", "info")
    return redirect(url_for("inicio"))

# -------------------------------------------------
# PROVEEDORES (SOLO LISTAR / EDITAR / ELIMINAR)
# -------------------------------------------------
@app.route("/proveedores")
def proveedores():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM proveedores")
    data = cursor.fetchall()
    db.close()
    return render_template("proveedores.html", proveedores=data)

@app.route("/proveedor/eliminar/<int:id>")
def eliminar_proveedor(id):
    if session.get("rol") != "admin":
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
        return redirect(url_for("proveedores"))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        cursor.execute(
            "UPDATE proveedores SET nombre=%s, contacto=%s, telefono=%s, estado=%s WHERE id=%s",
            (
                request.form["nombre"],
                request.form["contacto"],
                request.form["telefono"],
                request.form["estado"],
                id
            )
        )
        db.commit()
        db.close()
        flash("Proveedor actualizado", "success")
        return redirect(url_for("proveedores"))

    cursor.execute("SELECT * FROM proveedores WHERE id=%s", (id,))
    proveedor = cursor.fetchone()
    db.close()
    return render_template("editar_proveedor.html", p=proveedor)

# -------------------------------------------------
# PEDIDOS
# -------------------------------------------------
@app.route("/nuevo_pedido", methods=["GET", "POST"])
def nuevo_pedido():
    if not session.get("usuario"):
        return redirect(url_for("login"))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        proveedor_id = request.form["proveedor_id"]
        detalle = request.form["detalle"]  # <--- 1. Capturamos el texto

        cursor.execute(
            # <--- 2. Agregamos 'detalle' al INSERT
            "INSERT INTO pedidos (usuario_id, proveedor_id, detalle, estado) VALUES (%s, %s, %s, 'Pendiente')",
            (session["usuario_id"], proveedor_id, detalle)
        )
        db.commit()
        db.close()
        flash("Pedido realizado correctamente", "success")
        return redirect(url_for("inicio"))

    cursor.execute("SELECT * FROM proveedores WHERE estado='activo'")
    proveedores = cursor.fetchall()
    db.close()
    return render_template("nuevo_pedido.html", proveedores=proveedores)

# -------------------------------------------------
# ADMIN
# -------------------------------------------------
@app.route("/admin")
def admin():
    if session.get("rol") != "admin":
        return redirect(url_for("inicio"))

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.id, u.nombre usuario, prov.nombre proveedor, p.detalle, p.fecha, p.estado
        FROM pedidos p
        JOIN usuarios u ON p.usuario_id = u.id
        JOIN proveedores prov ON p.proveedor_id = prov.id
        ORDER BY p.fecha DESC
    """)
    pedidos = cursor.fetchall()
    db.close()
    return render_template("admin.html", pedidos=pedidos)
# -------------------------------------------------
# ADMIN - CONTACTOS
# -------------------------------------------------
@app.route("/admin/contactos")
def admin_contactos():
    if session.get("rol") != "admin":
        return redirect(url_for("inicio"))

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, nombre, email, mensaje, fecha
        FROM contactos
        ORDER BY fecha DESC
    """)
    contactos = cursor.fetchall()
    db.close()

    return render_template("admin_contactos.html", contactos=contactos)

# -------------------------------------------------
# ADMIN - GESTIÓN DE PEDIDOS (CRUD: UPDATE / DELETE)
# -------------------------------------------------
@app.route("/admin/pedido/estado/<int:id>", methods=["POST"])
def cambiar_estado_pedido(id):
    if session.get("rol") != "admin":
        return redirect(url_for("inicio"))
    
    nuevo_estado = request.form["nuevo_estado"]
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE pedidos SET estado = %s WHERE id = %s", (nuevo_estado, id))
    db.commit()
    db.close()
    
    flash(f"Estado del pedido #{id} actualizado a '{nuevo_estado}'", "success")
    return redirect(url_for("admin"))

@app.route("/admin/pedido/eliminar/<int:id>")
def eliminar_pedido(id):
    if session.get("rol") != "admin":
        return redirect(url_for("inicio"))
        
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM pedidos WHERE id = %s", (id,))
    db.commit()
    db.close()
    
    flash(f"Pedido #{id} eliminado correctamente", "success")
    return redirect(url_for("admin"))
if __name__ == "__main__":
    app.run(debug=True)
