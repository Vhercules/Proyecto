import requests
from PIL import Image


def guardar_imagen_desde_url(url, nombre_archivo):

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Lanza una excepción para códigos de estado de error (4xx o 5xx)
        
        content_type = response.headers.get('Content-Type')
        extension = '.png'  # Valor por defecto
        if content_type:
            if 'image/png' in content_type:
                extension = '.png'
            elif 'image/jpeg' in content_type:
                extension = '.jpg'
            elif 'image/svg+xml' in content_type:
                extension = '.svg'
        
        nombre_archivo_final = f"{nombre_archivo}{extension}"
        with open(nombre_archivo_final, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"Imagen guardada exitosamente como '{nombre_archivo_final}'")
        return nombre_archivo_final
    
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer el request: {e}")
    except IOError as e:
        print(f"Error al escribir el archivo: {e}")
    return None


def mostrar_imagen(file_path):
    
    if not file_path:
        print("No se dió un nombre de archivo para mostrar.")
        return

    try:
        img = Image.open(file_path)
        img.show()
    except Exception as e:
        print(f"Ocurrió un error al intentar mostrar la imagen: {e}")
        
        
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

    def obtener_apartamentos(self):
        data = self.conexion_api("/departments")
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

    def obtener_apartamentos_por_id(self, department_id):
        params = {"departmentId": department_id, "hasImages": "true"}
        data = self.conexion_api("/objects", params=params)
        if data and "objectIDs" in data:
            return data["objectIDs"]
        return []
    
    def buscar_objeto_por_id(self, id):
        params = {"q": id, "hasImages": "true"}
        data = self.conexion_api("/search", params=params)
        if data and "objectIDs" in data:
            return data["objectIDs"]
        return []

    def obtener_detalles_objeto(self, object_id):
        data = self.conexion_api(f"/objects/{object_id}")
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

def buscar_por_departamento(client):
    departamentos = client.obtener_apartamentos()
    if not departamentos:
        print("No se pudieron obtener los departamentos")
        return

    print("\n--- Departamentos disponibles ---")
    for d in departamentos:
        print(d)

    try:
        dep_id = int(input("Ingrese el ID del departamento que desee: "))
        if not any(d.id == dep_id for d in departamentos):
            print("Seleccione un Id valido")
            return

        print(f"\nBuscando obras en el departamento con ID: {dep_id}...")
        object_ids = client.obtener_apartamentos_por_id(dep_id)
        
        if not object_ids:
            print("No se encontraron obras con imágenes en ese departamento.")
            return
        
        print(f"Se encontraron {len(object_ids)} obras. Mostrando las primeras 20:")
        for obj_id in object_ids[:20]:
            obra = client.obtener_detalles_objeto(obj_id)
            if obra:
                print("---------------------------------------------")
                print(obra)
        print("---------------------------------------------------")

    except ValueError:
        print("introduzca una opcion correcta")
    
def buscar_por_nacionalidad(client):
    nacionalidad = input("Ingrese la nacionalidad del autor: ").strip()
    if not nacionalidad:
        print("Debe ingresar una nacionalidad valida")
        return
    nacionalidad_lower = nacionalidad.lower()
    print(f"\nBuscando obras de artistas con nacionalidad: '{nacionalidad}'...")
    object_ids = client.buscar_objeto_por_id(nacionalidad)
    
    if not object_ids:
        print("No se encontraron obras para esa nacionalidad.")
        return
    resultados_filtrados = []
    for obj_id in object_ids:
        obra = client.obtener_detalles_objeto(obj_id)
        
        if obra and obra.nacionalidad_artista:
            nacionalidades_en_obra = [n.strip().lower() for n in obra.nacionalidad_artista.split(',')]
            if nacionalidad_lower in nacionalidades_en_obra:
                resultados_filtrados.append(obra)

    if not resultados_filtrados:
        print("No se encontraron obras de artistas con esa nacionalidad después de la búsqueda detallada.")
        return
    print(f"Se encontraron {len(resultados_filtrados)} obras. Mostrando las primeras 10:")
    for obra_filtrada in resultados_filtrados[:10]:
        print("-------------------------------")
        print(obra_filtrada)
    print("----------------------------------")
    
        
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
    
    creando_objetos = MetroArtAPIClient()
    while True:
        mostrar_menu()
        opcion = input("Ingrese el número de la opción deseada: ")
        if opcion == '1':
            buscar_por_departamento(creando_objetos)
        elif opcion == '2':
            buscar_por_nacionalidad(creando_objetos)
            print("")
        elif opcion == '3':
            #buscar_por_autor()
            print("")
        elif opcion == '4':
            #mostrar_detalles_obra()
            print("")
        elif opcion == '5':
            #print("\nSaliendo del Catálogo MetroArt. Hasta luego, vuelva pronto")
            print("")
            break
        else:
            print("\nSeleccione una opcion valida")

if __name__ == "__main__":
    main()
