from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

# Modelo de datos
class Saludo(BaseModel):
    nombre: str
    apellido: str
    edad: int

app = FastAPI()

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

# Llamar a init_db al iniciar la aplicación
init_db()

# Endpoint para la ruta raíz
@app.get("/")
async def read_root():
    return ("Bienvenido a la Aplicación de Saludos.\n"
            "Por favor, ingresa tu nombre, apellido y edad usando el cliente.\n"
            "Puedes acceder a la función de saludar utilizando el endpoint /saludar/.")

# Endpoint para recibir el saludo
@app.post("/saludar/")
async def saludar(saludo: Saludo):
    mensaje = f"Hola, {saludo.nombre} {saludo.apellido}! Tienes {saludo.edad} años."

    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("saludos.db", check_same_thread=False)
        cursor = conn.cursor()

        # Guardar en la base de datos
        cursor.execute("INSERT INTO saludos (nombre, apellido, edad, saludo) VALUES (?, ?, ?, ?)",
                       (saludo.nombre, saludo.apellido, saludo.edad, mensaje))
        conn.commit()

        return {"mensaje": mensaje}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()  # Cerrar la conexión

# Endpoint para ver todos los saludos almacenados
@app.get("/saludos/")
async def obtener_saludos():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("saludos.db", check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM saludos")
        resultados = cursor.fetchall()

        return {"saludos": resultados}
    finally:
        conn.close()  # Cerrar la conexión

# Endpoint para buscar saludos por nombre, apellido o ID
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

    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("saludos.db", check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute(query, parameters)
        resultados = cursor.fetchall()

        if not resultados:
            raise HTTPException(status_code=404, detail="No se encontraron saludos para los criterios proporcionados")

        return {"saludos": resultados}
    finally:
        conn.close()  # Cerrar la conexión

# Usa Uvicorn para servir la aplicación
if __name__ == "__server__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
