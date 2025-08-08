import requests
from PIL import Image

def guardar_imagen_desde_url(url, nombre_archivo):
    """
    Descarga una imagen desde una URL y la guarda localmente con un nombre específico.

    Args:
        url (str): La URL de la imagen a descargar.
        nombre_archivo (str): El nombre base con el que se guardará el archivo.

    Returns:
        str: El nombre completo del archivo guardado (ej. 'nombre.jpg') o None si falla.
    """
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
    """
    Abre y muestra una imagen desde una ruta de archivo local utilizando Pillow.

    Args:
        file_path (str): La ruta del archivo de imagen a mostrar.
    """
    if not file_path:
        print("No se dió un nombre de archivo para mostrar.")
        return

    try:
        img = Image.open(file_path)
        img.show()
    except Exception as error:
        print(f"Ocurrió un error al intentar mostrar la imagen: {error}")
        
        
class ObraDeArte:
    """
    Clase para representar una obra de arte del Met Museum.
    
    Guarda información detallada sobre una obra, como título, artista,
    nacionalidad, año, etc.
    """
    def __init__(self, id, titulo, nombre_artista, nacionalidad_artista,
                 fecha_nacimiento_artista, fecha_muerte_artista,
                 tipo, anio_creacion, url_imagen, departamento):
        """
        Inicializa una instancia de ObraDeArte.

        Args:
            id (int): El ID único de la obra.
            titulo (str): El título de la obra.
            nombre_artista (str): El nombre del artista.
            nacionalidad_artista (str): La nacionalidad del artista.
            fecha_nacimiento_artista (str): La fecha de nacimiento del artista.
            fecha_muerte_artista (str): La fecha de muerte del artista.
            tipo (str): La clasificación o tipo de la obra.
            anio_creacion (str): El año de creación de la obra.
            url_imagen (str): La URL de la imagen principal.
            departamento (str): El departamento al que pertenece la obra.
        """
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
        """
        Devuelve una representación en cadena de la obra, adecuada para ser impresa en una lista.

        Returns:
            str: Una cadena formateada con la información básica de la obra.
        """
        return (f"ID: {self.id}\n"
                f"Título: {self.titulo}\n"
                f"Artista: {self.nombre_artista} ({self.nacionalidad_artista})\n"
                f"Departamento: {self.departamento}")

    def mostrar_detalles(self):
        """
        Imprime todos los detalles de la obra de arte en la consola.
        """
        print("\n--- Detalles de la Obra ---")
        print(f"ID: {self.id}")
        print(f"Título: {self.titulo}")
        print(f"Artista: {self.nombre_artista}")
        print(f"   Nacionalidad: {self.nacionalidad_artista}")
        print(f"   Fecha de nacimiento: {self.fecha_nacimiento_artista}")
        print(f"   Fecha de muerte: {self.fecha_muerte_artista}")
        print(f"Departamento: {self.departamento}")
        print(f"Tipo: {self.tipo}")
        print(f"Año de creación: {self.anio_creacion}")
        print(f"URL de la imagen: {self.url_imagen}")
        print("--------------------------")

class Departamento:
    """
    Clase para representar un departamento del Met Museum.
    """
    def __init__(self, id, nombre):
        """
        Inicializa una instancia de Departamento.

        Args:
            id (int): El ID único del departamento.
            nombre (str): El nombre del departamento.
        """
        self.id = id
        self.nombre = nombre

    def __str__(self):
        """
        Devuelve una representación en cadena del departamento.

        Returns:
            str: Una cadena formateada con el ID y nombre del departamento.
        """
        return f"ID: {self.id} - Nombre: {self.nombre}"

class MetroArtAPIClient:
    """
    Clase cliente para interactuar con la API pública del Met Museum.
    
    Proporciona métodos para obtener departamentos, buscar obras y obtener sus detalles.
    """
    BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1"

    def conexion_api(self, endpoint):
        """
        Método para realizar solicitudes HTTP a la API del Met Museum.

        Args:
            endpoint (str): El punto final de la API a consultar.

        Returns:
            dict: Los datos JSON de la respuesta o None si ocurre un error.
        """
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API en {url}: {e}")
            return None

    def obtener_apartamentos(self):
        """
        Obtiene una lista de todos los departamentos disponibles en la colección.

        Returns:
            list: Una lista de objetos `Departamento` o una lista vacía si falla.
        """
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
        """
        Obtiene los IDs de las obras de arte con imágenes en un departamento específico.

        Args:
            department_id (int): El ID del departamento.

        Returns:
            list: Una lista de IDs de obras (enteros) o una lista vacía.
        """
        params = {"departmentId": department_id, "hasImages": "true"}
        data = self.conexion_api("/objects", params=params)
        if data and "objectIDs" in data:
            return data["objectIDs"]
        return []
    
    def buscar_objeto_por_id(self, query):
        """
        Realiza una búsqueda general de obras de arte por una palabra clave.

        Args:
            query (str): La palabra clave para buscar obras.

        Returns:
            list: Una lista de IDs de obras (enteros) o una lista vacía.
        """
        
        data = self.conexion_api("/search")
        if data and "objectIDs" in data:
            return data["objectIDs"]
        return []
    def buscar_objeto_por_nacionalidad(self, query):
        """
        Realiza una búsqueda general de obras de arte por nacionalidad del autor.

        Args:
            query (str): La palabra clave para buscar obras.

        Returns:
            list: Una lista de IDs de obras (enteros) o una lista vacía.
        """
        data = self.conexion_api("/search?artistOrCulture=true&q="+query)
        if data and "objectIDs" in data:
            return data["objectIDs"]
        return []
    def buscar_objeto_por_autor(self, query):
        """
        Realiza una búsqueda general de obras de arte por nombre del autor.

        Args:
            query (str): La palabra clave para buscar obras.

        Returns:
            list: Una lista de IDs de obras (enteros) o una lista vacía.
        """
        data = self.conexion_api("/search?artistOrCulture=true&q="+query)
        if data and "objectIDs" in data:
            return data["objectIDs"]
        return []
    
    def obtener_detalles_objeto(self, object_id):
        """
        Obtiene los detalles completos de una obra de arte por su ID.

        Args:
            object_id (int): El ID de la obra de arte.

        Returns:
            ObraDeArte: Un objeto `ObraDeArte` con los detalles o None si no se encuentra.
        """
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
    """
    Permite al usuario buscar y listar obras de arte por departamento.

    Args:
        client (MetroArtAPIClient): Una instancia del cliente de la API.
    """
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
    """
    Permite al usuario buscar y filtrar obras por la nacionalidad del artista.

    Args:
        client (MetroArtAPIClient): Una instancia del cliente de la API.
    """
    nacionalidad = input("Ingrese la nacionalidad del autor: ").strip()
    if not nacionalidad:
        print("Debe ingresar una nacionalidad.")
        return
    nacionalidad_lower = nacionalidad.lower()
    print(f"\nBuscando obras de artistas con nacionalidad '{nacionalidad}'...")
    object_ids = client.buscar_objeto_por_nacionalidad(nacionalidad_lower)
    
    if not object_ids:
        print("No se encontraron obras para esa nacionalidad.")
        return
    print(f"Se encontraron {len(object_ids)} obras. Mostrando las primeras 20:")
    for obra_filtrada in object_ids[:20]:
        filtrado= client.obtener_detalles_objeto(obra_filtrada)
        print("---------------------------------")
        print(filtrado)
    print("-------------------------------")


def buscar_por_autor(client):
    """
    Permite al usuario buscar obras de arte por el nombre del autor.

    Args:
        client (MetroArtAPIClient): Una instancia del cliente de la API.
    """
    autor = input("Ingrese el nombre del autor: ").strip()
    if not autor:
        print("Debe ingresar un nombre de autor.")
        return

    print(f"\nBuscando obras de '{autor}'...")
    object_ids = client.buscar_objeto_por_autor(autor)
    
    if not object_ids:
        print(f"No se encontraron obras para el autor '{autor}'.")
        return

    print(f"Se encontraron {len(object_ids)} obras. Mostrando las primeras 20:")
    for obj_id in object_ids[:20]:
        obra = client.obtener_detalles_objeto(obj_id)
        if obra:
            print("---------------------------------")
            print(obra)
    print("-----------------------" )
    
def mostrar_detalles_obra(client):
    """
    Permite al usuario ver los detalles completos de una obra y su imagen por ID.

    Args:
        client (MetroArtAPIClient): Una instancia del cliente de la API.
    """
    try:
        obra_id = int(input("Ingrese el ID de la obra de arte: "))
        print(f"\nBuscando detalles de la obra con ID {obra_id}...")
        obra = client.obtener_detalles_objeto(obra_id)
        
        if obra:
            obra.mostrar_detalles()
            if obra.url_imagen:
                opcion_imagen = input("¿Desea ver la imagen? (s/n): ").lower()
                if opcion_imagen == 's':
                    nombre_archivo = guardar_imagen_desde_url(obra.url_imagen, f"obra_{obra_id}")
                    if nombre_archivo:
                        mostrar_imagen(nombre_archivo)
            else:
                print("Esta obra no tiene una imagen principal disponible.")
        else:
            print(f"No se encontraron detalles para la obra con ID {obra_id}.")
    except ValueError:
        print("Entrada no válida. Por favor, ingrese un ID numérico.")
    
def mostrar_menu():
    """
    Muestra el menú principal de opciones de la aplicación al usuario.
    """
    print("----------METROART--------")

    print("\n--- Catálogo MetroArt ---")
    print("1. Ver lista de obras por Departamento")
    print("2. Ver lista de obras por Nacionalidad del Autor")
    print("3. Ver lista de obras por Nombre del Autor")
    print("4. Mostrar detalles de una obra por ID")
    print("5. Salir")
    print("--------------------------")

def main():
    """
    La función principal que ejecuta el bucle del programa.
    
    Inicializa el cliente de la API y gestiona la interacción del usuario
    a través del menú principal.
    """
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
            buscar_por_autor(creando_objetos)
            print("")
        elif opcion == '4':
            mostrar_detalles_obra(creando_objetos)
            print("")
        elif opcion == '5':
            print("\nSaliendo del Catálogo MetroArt. Hasta luego, vuelva pronto")
            print("")
            break
        else:
            print("\nSeleccione una opcion valida")

if __name__ == "__main__":
    main()
