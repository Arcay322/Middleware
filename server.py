from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import sqlite3

app = FastAPI()

# Configuración para servir archivos estáticos y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Conexión a la base de datos SQLite
def get_db_connection():
    conn = sqlite3.connect('saludos.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/saludar/")
async def saludar(nombre: str = Form(...), apellido: str = Form(...), edad: int = Form(...)):
    conn = get_db_connection()
    conn.execute("INSERT INTO saludos (nombre, apellido, edad) VALUES (?, ?, ?)",
                 (nombre, apellido, edad))
    conn.commit()
    conn.close()
    return {"mensaje": f"Saludo enviado a {nombre} {apellido}!"}

@app.get("/saludos/", response_class=HTMLResponse)
async def ver_saludos(request: Request):
    conn = get_db_connection()
    saludos = conn.execute("SELECT * FROM saludos").fetchall()
    conn.close()
    return templates.TemplateResponse("ver_saludos.html", {"request": request, "saludos": saludos})

@app.get("/buscar_saludos/")
async def buscar_saludos(nombre: str = "", apellido: str = "", id: int = None):
    conn = get_db_connection()
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

    saludos = conn.execute(query, params).fetchall()
    conn.close()
    return {"saludos": saludos}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
