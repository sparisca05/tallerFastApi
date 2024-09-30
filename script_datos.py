import psycopg2
import csv

def insert_data(database_url): 
    # Configurar la conexión a la base de datos PostgreSQL
    conn = psycopg2.connect(database_url)
    # Ruta del archivo CSV
    csv_file_path = 'https://www.datos.gov.co/resource/jtnk-dmga.json'
    # Crear una conexión y un cursor
    cursor = conn.cursor()

    # Verificar si la tabla ya tiene datos
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    result = cursor.fetchone()
    if result[0] > 0:
        print("La tabla ya contiene datos. No se realizará la inserción.")
        return
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