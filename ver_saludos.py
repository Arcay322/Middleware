import requests


def ver_saludos():
    response = requests.get("https://middleware-vl7h.onrender.com/saludos/")

    # Verifica el estado de la respuesta
    if response.status_code == 200:
        try:
            saludos = response.json().get("saludos", [])
            for saludo in saludos:
                print(
                    f"ID: {saludo[0]}, Nombre: {saludo[1]}, Apellido: {saludo[2]}, Edad: {saludo[3]}, Saludo: {saludo[4]}")
        except ValueError:
            print("Error: La respuesta no es un JSON válido.")
            print("Respuesta del servidor:", response.text)
    else:
        print(f"Error en la solicitud: {response.status_code} - {response.text}")
