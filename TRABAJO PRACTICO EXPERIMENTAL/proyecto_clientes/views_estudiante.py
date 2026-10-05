from models import Estudiante  # Importa el modelo de estudiante.
from shared.json_manager import GestorJSON  # Importa la herramienta para guardar datos JSON.
from views import ClienteController  # Importa el controlador base de clientes.


class EstudianteController(ClienteController):  # Define el controlador de estudiantes.
    """Hereda las operaciones de ClienteController. Solo cambia la configuración."""  # Explica qué hereda la clase.

    MODELO = Estudiante  # Indica qué modelo usa el controlador.
    ARCHIVO = "data/estudiantes.json"  # Define dónde se guardan los estudiantes.
    CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")  # Define los campos de búsqueda.
    _gestor = GestorJSON(ARCHIVO)  # Crea el gestor para leer y guardar datos.

    @classmethod  # Permite usar el método desde la clase.
    def carnets_registrados(cls, excepto_id=None):  # Define la consulta de carnets existentes.
        return {  # Devuelve un conjunto de carnets.
            r["carnet"].upper()  # Convierte cada carnet a mayúsculas.
            for r in cls._registros()  # Recorre los registros guardados.
            if r["id"] != excepto_id  # Omite el estudiante indicado, si lo hay.
        }  # Termina el conjunto de carnets.

    @classmethod  # Permite usar el método desde la clase.
    def crear(cls, datos):  # Define la creación de un estudiante.
        carnet = str(datos.get("carnet", "")).strip().upper()  # Limpia y normaliza el carnet.
        if carnet and carnet in cls.carnets_registrados():  # Comprueba si el carnet ya está usado.
            return False, "Ese carnet ya está registrado"  # Rechaza el carnet repetido.
        return super().crear(datos)  # Usa la creación heredada del controlador base.

    @classmethod  # Permite usar el método desde la clase.
    def actualizar(cls, id_registro, cambios):  # Define la actualización de un estudiante.
        if "carnet" in cambios:  # Comprueba si se está cambiando el carnet.
            nuevo = str(cambios["carnet"]).strip().upper()  # Limpia y normaliza el nuevo carnet.
            if nuevo in cls.carnets_registrados(excepto_id=id_registro):  # Comprueba si otro estudiante ya lo usa.
                return False, "Ese carnet ya lo usa otro estudiante"  # Rechaza el carnet repetido.
        return super().actualizar(id_registro, cambios)  # Usa la actualización del controlador base.

    @classmethod  # Permite usar el método desde la clase.
    def agregar_nota(cls, id_estudiante, materia, nota):  # Define cómo guardar una nota.
        try:  # Intenta realizar la operación.
            estudiante = cls.obtener(id_estudiante)  # Busca al estudiante por su identificador.
            if estudiante is None:  # Comprueba si no existe el estudiante.
                return False, f"No existe un estudiante con id {id_estudiante}"  # Informa que no se encontró.

            estudiante.agregar_nota(materia, nota)  # Agrega la nota a la materia indicada.

            registros = cls._registros()  # Carga todos los registros guardados.
            for i, r in enumerate(registros):  # Recorre registros con su posición.
                if r["id"] == id_estudiante:  # Busca el registro del estudiante.
                    registros[i] = estudiante.a_diccionario()  # Actualiza sus datos en la lista.
                    break  # Detiene la búsqueda al encontrarlo.
            cls._gestor.guardar(registros)  # Guarda los registros actualizados.
            return True, f"Nota {nota} agregada en {materia}"  # Confirma que la nota se guardó.
        except ValueError as error:  # Atiende errores de validación de la nota.
            return False, str(error)  # Devuelve el mensaje del error.

    @classmethod  # Permite usar el método desde la clase.
    def materias_ofertadas(cls):  # Define la consulta de materias disponibles.
        todas = set()  # Crea un conjunto vacío para evitar duplicados.
        for estudiante in cls.listar():  # Recorre todos los estudiantes.
            todas |= estudiante.materias  # Agrega sus materias al conjunto.
        return todas  # Devuelve las materias reunidas.

    @classmethod  # Permite usar el método desde la clase.
    def materias_en_comun(cls, id_a, id_b):  # Define la búsqueda de materias compartidas.
        a, b = cls.obtener(id_a), cls.obtener(id_b)  # Busca a los dos estudiantes.
        if a is None or b is None:  # Comprueba si alguno no fue encontrado.
            return False, "Alguno de los dos estudiantes no existe"  # Informa que falta un estudiante.
        return True, a.materias_en_comun(b)  # Devuelve las materias que comparten.