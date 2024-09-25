from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

# Crear la base de datos y tabla
conn = sqlite3.connect("saludos.db", check_same_thread=False)  # Asegurarse de que la conexión sea segura
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


# Modelo de datos
class Saludo(BaseModel):
    nombre: str
    apellido: str
    edad: int


app = FastAPI()


# Endpoint para recibir el saludo
@app.post("/saludar/")
async def saludar(saludo: Saludo):
    mensaje = f"Hola, {saludo.nombre} {saludo.apellido}! Tienes {saludo.edad} años."

    try:
        # Guardar en la base de datos
        cursor.execute("INSERT INTO saludos (nombre, apellido, edad, saludo) VALUES (?, ?, ?, ?)",
                       (saludo.nombre, saludo.apellido, saludo.edad, mensaje))
        conn.commit()
        return {"mensaje": mensaje}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint para ver todos los saludos almacenados
@app.get("/saludos/")
async def obtener_saludos():
    cursor.execute("SELECT * FROM saludos")
    resultados = cursor.fetchall()
    return {"saludos": resultados}


# Endpoint para buscar saludos por nombre
@app.get("/buscar_saludos/")
async def buscar_saludos(nombre: str = None, apellido: str = None, id: int = None):
    query = "SELECT * FROM saludos WHERE 1=1"
    parameters = []

    if nombre:
        query += " AND nombre = ?"
        parameters.append(nombre)
    if apellido:
        query += " AND apellido = ?"
        parameters.append(apellido)
    if id is not None:
        query += " AND id = ?"
        parameters.append(id)

    cursor.execute(query, parameters)
    resultados = cursor.fetchall()

    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron saludos para los criterios proporcionados")

    return {"saludos": resultados}