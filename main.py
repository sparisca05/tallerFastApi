from datetime import datetime, date
import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

from script_datos import insert_data

load_dotenv()

db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"

insert_data(DATABASE_URL)

app = FastAPI()

class UserIn(BaseModel):
    uid: str
    display_name: str
    email_address: str
    status: str
    role: str
    last_active: date

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

@app.get("/usuarios/{item_id}")
def read_user(item_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT uid, display_name, email_address, status, role, last_active FROM usuarios WHERE uid = %s", (item_id,))
    usuario = cursor.fetchone()
    conn.close()
    
    if usuario is None:
        return {"error": "Usuario no encontrado"}
    
    result = {
        "uid": usuario[0],
        "display_name": usuario[1],
        "email_address": usuario[2],
        "status": usuario[3],
        "role": usuario[4],
        "last_active": usuario[5],
    }
    
    return {"usuario": result}

@app.get("/usuarios/fecha/")
def read_users_by_date(start_date: str, end_date: str):
    # Convertir las cadenas de fecha a objetos datetime
    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Formato de fecha inválido. Use YYYY-MM-DD."}

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT uid, display_name, email_address, status, role, last_active 
        FROM usuarios 
        WHERE last_active BETWEEN %s AND %s
        LIMIT 100
    """, (start_date, end_date))
    
    usuarios = cursor.fetchall()
    conn.close()
    
    result = [
        {
            "uid": usuario[0],
            "display_name": usuario[1],
            "email_address": usuario[2],
            "status": usuario[3],
            "role": usuario[4],
            "last_active": usuario[5],
        }
        for usuario in usuarios
    ]
    
    return {"usuarios": result}

@app.post("/post/")
def create_users(users: List[UserIn]):
    conn = get_db_connection()
    cursor = conn.cursor()

    registros_agregados = 0
    total_registros = 0

    try:
        for user in users:
            try:
                cursor.execute("""
                    INSERT INTO usuarios (uid, display_name, email_address, status, role, last_active)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (user.uid, user.display_name, user.email_address, user.status, user.role, user.last_active))
                registros_agregados += 1
            except Exception as e:
                print(f"Error al insertar el usuario {user.uid}: {e}")
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al insertar el usuario {user.uid}.")

        conn.commit()

        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_registros = cursor.fetchone()[0]

    except Exception as e:
        print(f"Error general: {e}")
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error general durante la operación")

    finally:
        cursor.close()
        conn.close()

    return {
        "registros_agregados": registros_agregados,
        "total_registros": total_registros
    }