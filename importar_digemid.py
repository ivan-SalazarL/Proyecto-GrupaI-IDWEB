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

        # --- NOMBRES EXACTOS SEGÚN TU IMAGEN ---
        # Asignamos las variables a los nombres que vimos en la foto
        columna_registro = 'Num_RegSan'
        columna_nombre   = 'Nom_Prod'
        columna_concent  = 'Concent'
        columna_forma    = 'Nom_Form_Farm'
        columna_titular  = 'Nom_Titular'
        # ---------------------------------------

        # Verificación de seguridad
        if columna_nombre not in df.columns:
            print(f"❌ ERROR: No encuentro la columna '{columna_nombre}' en el Excel.")
            print("   Asegúrate de que la Fila 1 del Excel tenga los encabezados.")
            sys.exit()

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        print(f"✅ Conexión exitosa. Importando {len(df)} registros...")
        
        # Consulta SQL
        sql = """INSERT INTO productos_digemid 
                 (registro_sanitario, nombre_producto, concentracion, forma_farmaceutica, titular_registro) 
                 VALUES (%s, %s, %s, %s, %s)"""
        
        count = 0
        for index, row in df.iterrows():
            valores = (
                row[columna_registro],
                row[columna_nombre],
                row[columna_concent],
                row[columna_forma],
                row[columna_titular]
            )
            cursor.execute(sql, valores)
            count += 1
            
            # Guardar progreso cada 1000 filas
            if count % 1000 == 0:
                print(f"   -> Guardados {count} productos...")
                conn.commit()

        conn.commit() # Guardado final
        print(f"\n🎉 ¡ÉXITO! Se importaron {count} productos a la base de datos.")

    except Exception as e:
        print(f"\n❌ OCURRIÓ UN ERROR: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    importar_excel()