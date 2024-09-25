from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/ver_saludos", response_class=HTMLResponse)
async def ver_saludos(request: Request):
    # Hacer una solicitud GET para obtener todos los saludos
    response = requests.get("https://middleware-vl7h.onrender.com/saludos/")  # Asegúrate de usar la URL correcta

    if response.status_code == 200:
        saludos = response.json().get("saludos", [])
    else:
        saludos = []  # En caso de error, establecer saludos como una lista vacía

    return templates.TemplateResponse("ver_saludos.html", {"request": request, "saludos": saludos})
