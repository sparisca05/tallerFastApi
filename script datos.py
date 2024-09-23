import psycopg2
import csv

# Configurar la conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="datosfastapi",
    user="postgres",
    password="Simon2604*"
)

# Ruta del archivo CSV
csv_file_path = "C:/Users/cpari/Downloads/Usuarios_portal_datos_abiertos_datos.gov.co_20240919.csv"

# Crear una conexión y un cursor
cursor = conn.cursor()

# Leer el archivo CSV y cargar los datos en la tabla
try:
    with open(csv_file_path, mode='r', encoding='latin1') as file:  # Cambiar a 'utf-8' si el archivo ya está en ese formato
        csv_reader = csv.reader(file)
        next(csv_reader)  # Saltar la fila de encabezado si el CSV tiene encabezados
        
        for row in csv_reader:
            # Asumiendo que el CSV tiene las columnas en el orden: uid, display_name, email_address, status, role, last_active
            cursor.execute("""
                INSERT INTO usuarios (uid, display_name, email_address, status, role, last_active)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (row[0], row[1], row[2], row[3], row[4], row[5]))

    # Confirmar los cambios
    conn.commit()
    print("Datos cargados exitosamente en la tabla.")
except Exception as e:
    print(f"Ocurrió un error: {e}")
    conn.rollback()
finally:
    # Cerrar el cursor y la conexión
    cursor.close()
    conn.close()
