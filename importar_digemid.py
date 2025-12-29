import pandas as pd
import mysql.connector
import sys

# --- CONFIGURACIÓN ---
db_config = {
    'host': "localhost",
    'user': "root",
    'password': "", 
    'database': "SistemaFarmaceutico"
}

archivo_excel = 'Listado_Productos.xlsx' 

def importar_excel():
    print(f"--- INICIANDO IMPORTACIÓN DE: {archivo_excel} ---")
    
    try:
        # Leemos el Excel
        df = pd.read_excel(archivo_excel, dtype=str)
        df = df.fillna('') # Rellenar vacíos

        # --- NOMBRES DE COLUMNAS (SOLO LAS QUE TÚ QUIERES) ---
        columna_nombre   = 'Nom_Prod'
        columna_concent  = 'Concent'
        columna_forma    = 'Nom_Form_Farm'
        columna_titular  = 'Nom_Titular'
        # ---------------------------------------

        # Verificación de seguridad
        if columna_nombre not in df.columns:
            print(f"❌ ERROR: No encuentro la columna '{columna_nombre}' en el Excel.")
            sys.exit()

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        print(f"✅ Conexión exitosa. Importando {len(df)} registros...")
        
        # SQL: Mantenemos las 5 columnas para que la BD no falle
        sql = """INSERT INTO productos_digemid 
                 (registro_sanitario, nombre_producto, concentracion, forma_farmaceutica, titular_registro) 
                 VALUES (%s, %s, %s, %s, %s)"""
        
        count = 0
        for index, row in df.iterrows():
            
            # --- TRUCO: ENVIAMOS UN VALOR FALSO AL REGISTRO ---
            val_registro = '-'  # <--- Esto evita el error de "Falta columna"
            
            valores = (
                val_registro,           # 1. Registro (falso)
                row[columna_nombre],    # 2. Nombre
                row[columna_concent],   # 3. Concentración
                row[columna_forma],     # 4. Forma
                row[columna_titular]    # 5. Titular
            )
            cursor.execute(sql, valores)
            count += 1
            
            if count % 1000 == 0:
                print(f"   -> Guardados {count} productos...")
                conn.commit()

        conn.commit()
        print(f"\n🎉 ¡ÉXITO! Se importaron {count} productos (sin usar Registro Sanitario real).")

    except Exception as e:
        print(f"\n❌ OCURRIÓ UN ERROR: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    importar_excel()