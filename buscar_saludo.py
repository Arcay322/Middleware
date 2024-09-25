from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Form

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/buscar_saludos", response_class=HTMLResponse)
async def buscar_saludos(request: Request, criterio: str = None, valor: str = None):
    saludos = []

    if criterio and valor:
        # Hacer una solicitud GET para buscar saludos según el criterio
        params = {criterio: valor}
        response = requests.get("https://middleware-vl7h.onrender.com/buscar_saludos/", params=params)

        if response.status_code == 200:
            saludos = response.json().get("saludos", [])
        else:
            saludos = []  # En caso de error, establecer saludos como una lista vacía

    return templates.TemplateResponse("buscar_saludos.html", {"request": request, "saludos": saludos})
