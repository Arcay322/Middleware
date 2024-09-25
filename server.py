from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from contextlib import closing


# Modelo de datos
class Saludo(BaseModel):
    nombre: str
    apellido: str
    edad: int


app = FastAPI()


# Crear la base de datos y tabla si no existe
def init_db():
    with closing(sqlite3.connect("saludos.db", check_same_thread=False)) as conn:
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


# Llamar a init_db al iniciar la aplicación
init_db()


# Endpoint para la ruta raíz
@app.get("/")
async def read_root():
    return {"message": "Bienvenido a la API de saludos. Usa /saludar/ para enviar un saludo y /saludos/ para ver todos los saludos almacenados."}


# Endpoint para recibir el saludo
@app.post("/saludar/")
async def saludar(saludo: Saludo):
    mensaje = f"Hola, {saludo.nombre} {saludo.apellido}! Tienes {saludo.edad} años."

    try:
        with closing(sqlite3.connect("saludos.db", check_same_thread=False)) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO saludos (nombre, apellido, edad, saludo) VALUES (?, ?, ?, ?)",
                           (saludo.nombre, saludo.apellido, saludo.edad, mensaje))
            conn.commit()

        return {"mensaje": mensaje}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint para ver todos los saludos almacenados
@app.get("/saludos/")
async def obtener_saludos():
    try:
        with closing(sqlite3.connect("saludos.db", check_same_thread=False)) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM saludos")
            resultados = cursor.fetchall()

        # Formatear la respuesta
        saludos_formateados = [{"id": id, "nombre": nombre, "apellido": apellido, "edad": edad, "saludo": saludo}
                                for id, nombre, apellido, edad, saludo in resultados]

        return {"saludos": saludos_formateados}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
        with closing(sqlite3.connect("saludos.db", check_same_thread=False)) as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            resultados = cursor.fetchall()

        if not resultados:
            raise HTTPException(status_code=404, detail="No se encontraron saludos para los criterios proporcionados")

        # Formatear la respuesta
        saludos_formateados = [{"id": id, "nombre": nombre, "apellido": apellido, "edad": edad, "saludo": saludo}
                                for id, nombre, apellido, edad, saludo in resultados]

        return {"saludos": saludos_formateados}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Usa Uvicorn para servir la aplicación
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))  # Usa el puerto definido por Render
