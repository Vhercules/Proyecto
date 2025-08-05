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

    def _make_request(self, endpoint, params=None):
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API en {url}: {e}")
            return None

    def get_all_departments(self):
        data = self._make_request("/departments")
        if data and "departments" in data:
            lista_departamentos = []
            for d in data["departments"]:
                nuevo_departamento = Departamento(
                    id=d["departmentId"],
                    nombre=d["displayName"]
                )
                lista_departamentos.append(nuevo_departamento)
            return lista_departamentos
        return []

    def get_object_ids_by_department(self, department_id):
        params = {"departmentId": department_id, "hasImages": "true"}
        data = self._make_request("/objects", params=params)
        if data and "objectIDs" in data:
            return data["objectIDs"]
        return []
    
    def search_object_ids(self, query):
        params = {"q": query, "hasImages": "true"}
        data = self._make_request("/search", params=params)
        if data and "objectIDs" in data:
            return data["objectIDs"]
        return []

    def get_object_details(self, object_id):
        data = self._make_request(f"/objects/{object_id}")
        if data and data.get("objectID"):
            obra_de_arte = ObraDeArte(
                id=data.get("objectID"),
                titulo=data.get("title", "Desconocido"),
                nombre_artista=data.get("artistDisplayName", "Desconocido"),
                nacionalidad_artista=data.get("artistNationality", "Desconocida"),
                fecha_nacimiento_artista=data.get("artistBeginDate", "N/A"),
                fecha_muerte_artista=data.get("artistEndDate", "N/A"),
                tipo=data.get("classification", "Desconocido"),
                anio_creacion=data.get("objectDate", "N/A"),
                url_imagen=data.get("primaryImage", ""),
                departamento=data.get("department", "Desconocido")
            )
            return obra_de_arte
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
