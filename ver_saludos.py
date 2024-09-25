import requests

# Hacer una solicitud GET para obtener todos los saludos
response = requests.get("https://middleware-vl7h.onrender.com/saludos/")  # Asegúrate de usar la URL correcta

if response.status_code == 200:
    saludos = response.json()["saludos"]
    print("Respuesta completa:", saludos)  # Imprime la respuesta completa para depurar
    if saludos:
        print("Saludos almacenados:")
        for saludo in saludos:
            # Cambia esto para acceder a los elementos correctamente
            print(f"ID: {saludo['id']}, Nombre: {saludo['nombre']}, Apellido: {saludo['apellido']}, Edad: {saludo['edad']}, Saludo: {saludo['saludo']}")
    else:
        print("No hay saludos almacenados.")
else:
    print(f"Ocurrió un error: {response.status_code} - {response.text}")
