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

def mostrar_menu():
    """
    METROART
    """
    print("\n--- Catálogo---")
    print("1. Buscar obras por Departamento")
    print("2. Buscar obras por Nacionalidad del Autor")
    print("3. Buscar obras por Nombre del Autor")
    print("4. Mostrar detalles de una obra por ID")
    print("5. Salir")
    print("--------------------------")


mostrar_menu()
