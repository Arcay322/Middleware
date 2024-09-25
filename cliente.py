import requests
from ver_saludos import ver_saludos  # Asegúrate de que esta función esté definida correctamente
from buscar_saludo import main_busqueda  # Importa la función de búsqueda

def generar_saludo():
    nombre = input("¿Cuál es tu nombre? ")
    apellido = input("¿Cuál es tu apellido? ")
    edad = int(input("¿Cuál es tu edad? "))

    response = requests.post("https://middleware-vl7h.onrender.com/saludar/", json={"nombre": nombre, "apellido": apellido, "edad": edad})

    if response.status_code == 200:
        print(response.json()["mensaje"])
    else:
        print(f"Ocurrió un error al guardar tu saludo: {response.status_code} - {response.text}")

def main():
    print("¡Hola! ¿Cómo estás?")

    while True:
        print("\nMenú de Opciones:")
        print("1. Generar un saludo")
        print("2. Ver todos los saludos")
        print("3. Buscar un saludo")
        print("4. Salir")

        opcion = input("Elige una opción (1-4): ")

        if opcion == "1":
            generar_saludo()  # Llama a la función para generar un saludo
        elif opcion == "2":
            ver_saludos()  # Llama a la función para ver saludos
        elif opcion == "3":
            main_busqueda()  # Llama a la función de búsqueda
        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Por favor, elige una opción entre 1 y 4.")

if __name__ == "__main__":
    main()
