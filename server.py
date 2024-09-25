from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Modelo de datos
class Saludo(BaseModel):
    nombre: str
    apellido: str
    edad: int

# Crear la base de datos y tabla si no existe
def init_db():
    conn = sqlite3.connect("saludos.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS saludos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        apellido TEXT,
        edad INTEGER,
        saludo TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# Ruta para servir la interfaz
@app.get("/", response_class=HTMLResponse)
async def leer_interfaz(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint para recibir el saludo desde el formulario
@app.post("/saludar")
async def saludar_desde_formulario(nombre: str = Form(...), apellido: str = Form(...), edad: int = Form(...)):
    mensaje = f"Hola, {nombre} {apellido}! Tienes {edad} años."
    try:
        conn = sqlite3.connect("saludos.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO saludos (nombre, apellido, edad, saludo) VALUES (?, ?, ?, ?)",
                       (nombre, apellido, edad, mensaje))
        conn.commit()
        return {"mensaje": mensaje}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
