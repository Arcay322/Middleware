import requests

# Solicitar datos al usuario
nombre = input("¿Cuál es tu nombre? ")
apellido = input("¿Cuál es tu apellido? ")

# Validar la entrada de la edad
while True:
    try:
        edad = int(input("¿Cuál es tu edad? "))
        if edad < 0:
            print("Por favor, ingrese una edad válida (número positivo).")
            continue
        break
    except ValueError:
        print("Por favor, ingrese un número válido para la edad.")

# Hacer una solicitud POST al endpoint de saludar
response = requests.post("http://Arcay.pythonanywhere.com/saludar/", json={"nombre": nombre, "apellido": apellido, "edad": edad})

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    print(response.json()["mensaje"])  # Imprimir el mensaje de saludo
else:
    print(f"Ocurrió un error: {response.status_code} - {response.text}")  # Mostrar error si no fue exitoso
