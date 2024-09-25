import requests

def buscar_saludo_por_nombre():
    nombre = input("¿Cuál es el nombre que deseas buscar? ")
    response = requests.get(f"https://middleware-vl7h.onrender.com/buscar_saludos/", params={"nombre": nombre})
    return response

def buscar_saludo_por_apellido():
    apellido = input("¿Cuál es el apellido que deseas buscar? ")
    response = requests.get(f"https://middleware-vl7h.onrender.com/buscar_saludos/", params={"apellido": apellido})
    return response

def buscar_saludo_por_id():
    id_input = input("¿Cuál es el ID que deseas buscar? ")
    if id_input.isdigit():  # Verifica que sea un número
        response = requests.get(f"https://middleware-vl7h.onrender.com/buscar_saludos/", params={"id": int(id_input)})
        return response
    else:
        print("Por favor, ingresa un ID válido.")
        return None

def main():
    while True:
        print("\nMenú de Opciones:")
        print("1. Buscar saludo por nombre")
        print("2. Buscar saludo por apellido")
        print("3. Buscar saludo por ID")
        print("4. Salir")

        opcion = input("Elige una opción (1-4): ")

        if opcion == "1":
            response = buscar_saludo_por_nombre()
        elif opcion == "2":
            response = buscar_saludo_por_apellido()
        elif opcion == "3":
            response = buscar_saludo_por_id()
        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Por favor, elige una opción entre 1 y 4.")
            continue

        if response and response.status_code == 200:
            saludos = response.json()["saludos"]
            if saludos:
                for saludo in saludos:
                    print(f"ID: {saludo[0]}, Nombre: {saludo[1]}, Apellido: {saludo[2]}, Edad: {saludo[3]}, Saludo: {saludo[4]}")
            else:
                print("No se encontraron saludos para los criterios proporcionados.")
        elif response:
            print(f"Ocurrió un error: {response.status_code} - {response.text}")

        # Preguntar al usuario si desea buscar otro saludo
        otra_busqueda = input("\n¿Deseas buscar otro saludo? (s/n): ").strip().lower()
        if otra_busqueda != 's':
            print("Saliendo...")
            break

if __name__ == "__main__":
    main()

