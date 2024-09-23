from datetime import datetime
import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class User(BaseModel):
    uid: str
    display_name: str
    email_address: str
    status: str
    role: str
    last_active: str

def get_db_connection():
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="users",
        user="postgres",
        password="Simon2604*"
    )
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