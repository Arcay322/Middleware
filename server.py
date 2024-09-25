from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel
from typing import List, Optional
import sqlite3

app = FastAPI()


# Conexión a la base de datos SQLite
def get_db_connection():
    conn = sqlite3.connect('saludos.db')
    conn.row_factory = sqlite3.Row
    return conn


# Crear la tabla si no existe
def init_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS saludos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                edad INTEGER NOT NULL,
                saludo TEXT NOT NULL
            )
        ''')
        conn.commit()


init_db()


class Saludo(BaseModel):
    id: int
    nombre: str
    apellido: str
    edad: int
    saludo: str


@app.post("/saludar/", response_model=Saludo)
async def saludar(nombre: str = Form(...), apellido: str = Form(...), edad: int = Form(...)):
    saludo = f"Hola, {nombre} {apellido}!"
    with get_db_connection() as conn:
        cursor = conn.execute('INSERT INTO saludos (nombre, apellido, edad, saludo) VALUES (?, ?, ?, ?)',
                              (nombre, apellido, edad, saludo))
        conn.commit()
        id = cursor.lastrowid

    return {"id": id, "nombre": nombre, "apellido": apellido, "edad": edad, "saludo": saludo}


@app.get("/ver_saludos/", response_model=List[Saludo])
async def ver_saludos():
    with get_db_connection() as conn:
        saludos = conn.execute('SELECT * FROM saludos').fetchall()
        return [dict(saludo) for saludo in saludos]


@app.get("/buscar_saludos/", response_model=List[Saludo])
async def buscar_saludos(nombre: Optional[str] = None, apellido: Optional[str] = None, id: Optional[int] = None):
    query = "SELECT * FROM saludos WHERE 1=1"
    params = []

    if nombre:
        query += " AND nombre = ?"
        params.append(nombre)
    if apellido:
        query += " AND apellido = ?"
        params.append(apellido)
    if id is not None:
        query += " AND id = ?"
        params.append(id)

    with get_db_connection() as conn:
        saludos = conn.execute(query, params).fetchall()
        if not saludos:
            raise HTTPException(status_code=404, detail="No se encontraron saludos para los criterios proporcionados.")
        return [dict(saludo) for saludo in saludos]
