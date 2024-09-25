from fastapi import FastAPI, HTTPException, Form, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Definición del modelo de Saludo
class Saludo(BaseModel):
    id: int
    nombre: str
    apellido: str
    edad: int


# Base de datos en memoria para los saludos
saludos_db = []
current_id = 1  # ID para los saludos


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):  # Asegúrate de importar Request
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/saludar/")
async def saludar(
        nombre: str = Form(...),
        apellido: str = Form(...),
        edad: int = Form(...)
):
    global current_id
    nuevo_saludo = Saludo(id=current_id, nombre=nombre, apellido=apellido, edad=edad)
    saludos_db.append(nuevo_saludo)
    current_id += 1
    return {"mensaje": f"Hola, {nombre} {apellido}! Tienes {edad} años."}


@app.get("/saludos/", response_model=List[Saludo])
async def ver_saludos():
    return saludos_db


@app.get("/buscar_saludos/", response_model=List[Saludo])
async def buscar_saludos(nombre: Optional[str] = Query(None), apellido: Optional[str] = Query(None),
                         id: Optional[int] = Query(None)):
    resultados = []

    if id is not None:
        for saludo in saludos_db:
            if saludo.id == id:
                resultados.append(saludo)
    elif nombre and apellido:
        for saludo in saludos_db:
            if saludo.nombre.lower() == nombre.lower() and saludo.apellido.lower() == apellido.lower():
                resultados.append(saludo)

    if not resultados:
        raise HTTPException(status_code=404, detail="Saludo no encontrado")

    return resultados


# Ejecutar el servidor
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


@app.get("/buscar_saludos/", response_model=List[Saludo])
async def buscar_saludos(nombre: Optional[str] = Query(None), apellido: Optional[str] = Query(None),
                         id: Optional[int] = Query(None)):
    resultados = []

    if id is not None:
        for saludo in saludos_db:
            if saludo.id == id:
                resultados.append(saludo)
    elif nombre and apellido:
        for saludo in saludos_db:
            if saludo.nombre.lower() == nombre.lower() and saludo.apellido.lower() == apellido.lower():
                resultados.append(saludo)

    if not resultados:
        raise HTTPException(status_code=404, detail="Saludo no encontrado")

    return resultados


# Ejecutar el servidor
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
