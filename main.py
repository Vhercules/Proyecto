import requests
class ObraDeArte:
    def __init__(self, id, titulo, nombre_artista, nacionalidad_artista,
                 fecha_nacimiento_artista, fecha_muerte_artista,
                 tipo, anio_creacion, url_imagen, departamento):
        self.id = id
        self.titulo = titulo
        self.nombre_artista = nombre_artista
        self.nacionalidad_artista = nacionalidad_artista
        self.fecha_nacimiento_artista = fecha_nacimiento_artista
        self.fecha_muerte_artista = fecha_muerte_artista
        self.tipo = tipo
        self.anio_creacion = anio_creacion
        self.url_imagen = url_imagen
        self.departamento = departamento

    def __str__(self):
        return (f"ID: {self.id}\n"
                f"Título: {self.titulo}\n"
                f"Artista: {self.nombre_artista} ({self.nacionalidad_artista})\n"
                f"Departamento: {self.departamento}")

    def mostrar_detalles(self):
        print("\n--- Detalles de la Obra ---")
        print(f"ID: {self.id}")
        print(f"Título: {self.titulo}")
        print(f"Artista: {self.nombre_artista}")
        print(f"  Nacionalidad: {self.nacionalidad_artista}")
        print(f"  Fecha de nacimiento: {self.fecha_nacimiento_artista}")
        print(f"  Fecha de muerte: {self.fecha_muerte_artista}")
        print(f"Departamento: {self.departamento}")
        print(f"Tipo: {self.tipo}")
        print(f"Año de creación: {self.anio_creacion}")
        print(f"URL de la imagen: {self.url_imagen}")
        print("--------------------------")

class Departamento:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

    def __str__(self):
        return f"ID: {self.id} - Nombre: {self.nombre}"

class MetroArtAPIClient:
    BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1"

    def conexion_api(self, endpoint, params=None):
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API en {url}: {e}")
            return None


    
def mostrar_menu():
    
    print("----------METROART--------")

    print("\n--- Catálogo MetroArt ---")
    print("1. Ver lista de obras por Departamento")
    print("2. Ver lista de obras por Nacionalidad del Autor")
    print("3. Ver lista de obras por Nombre del Autor")
    print("4. Mostrar detalles de una obra por ID")
    print("5. Salir")
    print("--------------------------")

def main():
    
    
    while True:
        mostrar_menu()
        opcion = input("Ingrese el número de la opción deseada: ")

        if opcion == '1':
            buscar_por_departamento()
        elif opcion == '2':
            buscar_por_nacionalidad()
        elif opcion == '3':
            buscar_por_autor()
        elif opcion == '4':
            mostrar_detalles_obra()
        elif opcion == '5':
            print("\nSaliendo del Catálogo MetroArt. Hasta luego, vuelva pronto")
            break
        else:
            print("\nSeleccione una opcion valida")

if __name__ == "__main__":
    main()
