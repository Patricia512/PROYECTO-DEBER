import os  # Importa el módulo os para usar comandos del sistema, como limpiar la terminal.

# DICCIONARIO de colores de consola
COLORES = {  # Crea un diccionario con códigos ANSI para cada color de texto.
    "ROJO": "\033[91m",  # Código ANSI para el color rojo.
    "VERDE": "\033[92m",  # Código ANSI para el color verde.
    "AZUL": "\033[94m",  # Código ANSI para el color azul.
    "AMARILLO": "\033[93m",  # Código ANSI para el color amarillo.
    "CYAN": "\033[96m",  # Código ANSI para el color cyan.
    "BLANCO": "\033[97m",  # Código ANSI para el color blanco.
    "RESET": "\033[0m",  # Código ANSI para volver al color normal de la terminal.
}

# TUPLA: respuestas afirmativas aceptadas
RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")  # Guarda las variantes válidas de respuesta afirmativa.


def limpiar_pantalla():  # Define la función que limpia la consola.
    os.system("clear" if os.name == "posix" else "cls")  # En Linux/macOS usa clear; en Windows usa cls.


def imprimir_color(texto, color):  # Define una función para imprimir texto con color.
    codigo = COLORES.get(color, COLORES["BLANCO"])  # Busca el color solicitado; si no existe, usa blanco.
    print(f"{codigo}{texto}{COLORES['RESET']}")  # Imprime el texto con el color y luego restaura el color original.


def imprimir_titulo(texto):  # Define una función para mostrar un título centrado.
    limpiar_pantalla()  # Limpia la pantalla antes de mostrar el título.
    imprimir_color("=" * 60, "AZUL")  # Dibuja una línea azul larga para decorar el título.
    print(f"  {texto}".center(60))  # Muestra el texto centrado en una línea de 60 caracteres.
    imprimir_color("=" * 60, "AZUL")  # Dibuja otra línea azul al final del título.
    print()  # Deja una línea en blanco después del título.


def imprimir_exito(mensaje):  # Define una función para mostrar mensajes de éxito.
    imprimir_color(f"✓ {mensaje}", "VERDE")  # Muestra un mensaje con un símbolo de éxito en verde.


def imprimir_error(mensaje):  # Define una función para mostrar mensajes de error.
    imprimir_color(f"✗ {mensaje}", "ROJO")  # Muestra un mensaje con un símbolo de error en rojo.


def imprimir_info(mensaje):  # Define una función para mostrar mensajes informativos.
    imprimir_color(f"ℹ {mensaje}", "CYAN")  # Muestra un mensaje con un símbolo de información en cian.


def confirmar(pregunta):  # Define una función para preguntar al usuario si desea confirmar.
    respuesta = input(f"{pregunta} (si/no): ").strip().lower()  # Pide la respuesta, quita espacios y la convierte a minúsculas.
    return respuesta in RESPUESTAS_SI  # Devuelve True si la respuesta es afirmativa y False si no lo es.