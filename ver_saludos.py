import requests

# Hacer una solicitud GET para obtener todos los saludos
response = requests.get("https://middleware-vl7h.onrender.com/saludos/")  # Asegúrate de usar la URL correcta

if response.status_code == 200:
    saludos = response.json().get("saludos", [])  # Cambia esto para acceder a los elementos correctamente
    if saludos:
        print("Saludos almacenados:")
        for saludo in saludos:
            # Acceso a los elementos según la estructura de la respuesta
            print(f"ID: {saludo[0]}, Nombre: {saludo[1]}, Apellido: {saludo[2]}, Edad: {saludo[3]}, Saludo: {saludo[4]}")
    else:
        print("No hay saludos almacenados.")
else:
    print(f"Ocurrió un error: {response.status_code} - {response.text}")
