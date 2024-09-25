from fastapi import FastAPI, Form, Request, Query, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import sqlite3

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Modelo para los saludos
class Saludo(BaseModel):
    id: int
    nombre: str
    apellido: str
    edad: int


# Conexión a la base de datos SQLite
def get_db_connection():
    conn = sqlite3.connect('saludos.db')
    conn.row_factory = sqlite3.Row
    return conn


# Ruta para la página principal (formulario de saludo)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "saludo": None})


# Ruta para generar un saludo
@app.post("/saludar/")
async def generar_saludo(nombre: str = Form(...), apellido: str = Form(...), edad: int = Form(...)):
    # Guardar el saludo en la base de datos
    conn = get_db_connection()
    conn.execute('INSERT INTO saludos (nombre, apellido, edad) VALUES (?, ?, ?)', (nombre, apellido, edad))
    conn.commit()
    conn.close()

    # Generar mensaje de saludo
    saludo = f"Hola, {nombre} {apellido}! Tienes {edad} años."
    return templates.TemplateResponse("index.html", {"request": Request, "saludo": saludo})


# Ruta para buscar saludos
@app.get("/buscar_saludos/")
async def buscar_saludos(nombre: Optional[str] = Query(None), apellido: Optional[str] = Query(None),
                         id: Optional[int] = Query(None)):
    conn = get_db_connection()
    query = "SELECT * FROM saludos WHERE"
    params = []

    if id is not None:
        query += " id = ?"
        params.append(id)
    elif nombre and apellido:
        query += " nombre = ? AND apellido = ?"
        params.extend([nombre, apellido])
    else:
        return {"error": "Se debe proporcionar un ID, nombre o apellido."}

    saludos = conn.execute(query, params).fetchall()
    conn.close()

    return {"saludos": [dict(saludo) for saludo in saludos]}


# Ruta para ver todos los saludos
@app.get("/saludos/")
async def ver_saludos():
    conn = get_db_connection()
    saludos = conn.execute('SELECT * FROM saludos').fetchall()
    conn.close()

    return templates.TemplateResponse("ver_saludos.html", {"saludos": [dict(saludo) for saludo in saludos]})
