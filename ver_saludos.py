import requests

# Hacer una solicitud GET para obtener todos los saludos
response = requests.get("https://middleware-vl7h.onrender.com/saludos/")

if response.status_code == 200:
    saludos = response.json()["saludos"]
    if saludos:
        print("Saludos almacenados:")
        for saludo in saludos:
            print(f"ID: {saludo[0]}, Nombre: {saludo[1]}, Apellido: {saludo[2]}, Edad: {saludo[3]}, Saludo: {saludo[4]}")
    else:
        print("No hay saludos almacenados.")
else:
    print(f"Ocurrió un error: {response.status_code} - {response.text}")
