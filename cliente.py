import requests

nombre = input("¿Cuál es tu nombre? ")
apellido = input("¿Cuál es tu apellido? ")
edad = int(input("¿Cuál es tu edad? "))

response = requests.post("http://127.0.0.1:8000/saludar/", json={"nombre": nombre, "apellido": apellido, "edad": edad})
if response.status_code == 200:
    print(response.json()["mensaje"])
else:
    print(f"Ocurrió un error: {response.status_code} - {response.text}")
