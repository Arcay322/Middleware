from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import sqlite3

app = FastAPI()

# Montar la carpeta "static" para archivos CSS y JS si es necesario
app.mount("/static", StaticFiles(directory="static"), name="static")


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


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Saludar</title>
        </head>
        <body>
            <h1>Enviar Saludo</h1>
            <form action="/saludar/" method="post">
                <label>Nombre: <input type="text" name="nombre" required></label><br>
                <label>Apellido: <input type="text" name="apellido" required></label><br>
                <label>Edad: <input type="number" name="edad" required></label><br>
                <button type="submit">Enviar Saludo</button>
            </form>
            <h1>Opciones</h1>
            <a href="/ver_saludos">Ver Saludos</a><br>
            <a href="/buscar_saludos">Buscar Saludos</a>
        </body>
    </html>
    """


@app.get("/ver_saludos/", response_class=HTMLResponse)
async def ver_saludos():
    with get_db_connection() as conn:
        saludos = conn.execute('SELECT * FROM saludos').fetchall()
        saludos_list = "".join(
            f"<p>ID: {saludo['id']}, Nombre: {saludo['nombre']}, Apellido: {saludo['apellido']}, Edad: {saludo['edad']}, Saludo: {saludo['saludo']}</p>"
            for saludo in saludos
        )
        return f"""
        <html>
            <head>
                <title>Ver Saludos</title>
            </head>
            <body>
                <h1>Saludos Almacenados</h1>
                {saludos_list if saludos else "<p>No hay saludos almacenados.</p>"}
                <a href="/">Regresar</a>
            </body>
        </html>
        """


@app.get("/buscar_saludos/", response_class=HTMLResponse)
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
            return f"""
            <html>
                <head>
                    <title>Buscar Saludos</title>
                </head>
                <body>
                    <h1>No se encontraron saludos para los criterios proporcionados.</h1>
                    <a href="/">Regresar</a>
                </body>
            </html>
            """
        else:
            saludos_list = "".join(
                f"<p>ID: {saludo['id']}, Nombre: {saludo['nombre']
