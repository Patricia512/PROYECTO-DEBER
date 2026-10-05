import json  # Importa la librería para trabajar con archivos JSON.
import os  # Importa la librería para manejar rutas, carpetas y archivos del sistema.


class GestorJSON:  # Define una clase que se encarga de leer y guardar datos en formato JSON.
    """Lee y guarda una lista de diccionarios. Es la única parte que toca el disco."""  # Explica que esta clase es la encargada de interactuar con el archivo en disco.

    def __init__(self, ruta):  # Constructor: se ejecuta al crear un objeto de la clase.
        self.__ruta = ruta  # Guarda la ruta del archivo JSON en un atributo privado.
        carpeta = os.path.dirname(ruta)  # Obtiene la carpeta donde se almacenará el archivo.
        if carpeta and not os.path.exists(carpeta):  # Si la carpeta no existe, la crea.
            os.makedirs(carpeta)  # Crea la carpeta automáticamente.

    @property  # Decorador que permite acceder al valor de la ruta como si fuera un atributo.
    def ruta(self):  # Método que devuelve la ruta del archivo JSON.
        # Solo lectura: nadie puede cambiar el archivo de un gestor ya creado
        return self.__ruta  # Devuelve la ruta almacenada anteriormente.

    def leer(self):  # Método para leer el contenido del archivo JSON.
        if not os.path.exists(self.__ruta):  # Si el archivo no existe, no intenta leerlo.
            return []  # Devuelve una lista vacía para evitar errores.
        try:  # Intenta ejecutar esta parte y manejar errores si algo falla.
            with open(self.__ruta, "r", encoding="utf-8") as archivo:  # Abre el archivo en modo lectura con codificación UTF-8.
                datos = json.load(archivo)  # Carga el contenido JSON del archivo en una variable.
            return datos if isinstance(datos, list) else []  # Si el contenido es una lista, lo devuelve; si no, devuelve una lista vacía.
        except (json.JSONDecodeError, OSError):  # Si el archivo está corrupto o falla la lectura, captura el error.
            return []  # Devuelve una lista vacía para evitar que el programa falle.

    def guardar(self, datos):  # Método para guardar datos en el archivo JSON.
        try:  # Intenta guardar y maneja errores si algo falla.
            with open(self.__ruta, "w", encoding="utf-8") as archivo:  # Abre el archivo en modo escritura con codificación UTF-8.
                json.dump(datos, archivo, ensure_ascii=False, indent=2)  # Guarda los datos en JSON con formato legible y sin convertir caracteres especiales.
            return True  # Si la escritura fue exitosa, devuelve True.
        except (TypeError, OSError):  # Si los datos o el archivo tienen un problema, captura el error.
            return False  # Devuelve False para indicar que la escritura falló.