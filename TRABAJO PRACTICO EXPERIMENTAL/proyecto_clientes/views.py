from models import Cliente  # Importa el modelo de clientes.
from shared.json_manager import GestorJSON  # Importa la herramienta para guardar datos JSON.


class ClienteController:  # Define el controlador de clientes.
    """CONTROLADOR: las cinco operaciones. No imprime ni pide datos."""  # Describe la función de esta clase.

    # ===== ATRIBUTOS DE CLASE: toda la configuración junta =====
    MODELO = Cliente  # Define el modelo que usará el controlador.
    ARCHIVO = "data/clientes.json"  # Indica dónde se guardan los clientes.
    CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "telefono", "ciudad")  # Define los campos para buscar.
    _gestor = GestorJSON(ARCHIVO)  # Crea una vez la herramienta para manejar el archivo.

    # ===== AYUDAS =====
    @classmethod  # Permite llamar este método desde la clase.
    def _registros(cls):  # Define la lectura de los registros.
        """LISTA de diccionarios, tal como está en el archivo."""  # Describe el formato de los datos.
        return cls._gestor.leer()  # Lee y devuelve los registros guardados.

    @classmethod  # Permite llamar este método desde la clase.
    def emails_registrados(cls, excepto_id=None):  # Obtiene los emails ya registrados.
        """CONJUNTO de emails ya usados: permite detectar duplicados al instante."""  # Explica para qué sirve el método.
        return {  # Devuelve los emails en un conjunto.
            registro["email"].lower()  # Convierte cada email a minúsculas.
            for registro in cls._registros()  # Recorre todos los registros.
            if registro["id"] != excepto_id  # Omite el registro indicado, si se especificó.
        }  # Termina el conjunto de emails.

    @classmethod  # Permite llamar este método desde la clase.
    def siguiente_id(cls):  # Define cómo obtener el siguiente identificador.
        ids = [registro["id"] for registro in cls._registros()]  # Reúne los identificadores actuales.
        return max(ids) + 1 if ids else 1  # Devuelve el siguiente número o empieza en 1.

    @staticmethod  # Declara un método que no necesita la clase.
    def _coincide(registro, termino, campos):  # Comprueba si un registro coincide con la búsqueda.
        """Estático: no necesita la clase, solo compara textos."""  # Describe el método.
        for campo in campos:  # Recorre los campos que se pueden buscar.
            if termino in str(registro.get(campo, "")).lower():  # Busca el texto sin distinguir mayúsculas.
                return True  # Indica que encontró una coincidencia.
        return False  # Indica que no hubo coincidencias.

    # ===== C · CREATE =====
    @classmethod  # Permite llamar este método desde la clase.
    def crear(cls, datos):  # Define la creación de un cliente.
        """datos: diccionario. Devuelve la TUPLA (exito, mensaje)."""  # Describe la entrada y el resultado.
        try:  # Intenta crear el cliente.
            faltantes = [  # Reúne los campos obligatorios que faltan.
                campo for campo in cls.MODELO.OBLIGATORIOS  # Recorre los campos obligatorios del modelo.
                if not str(datos.get(campo, "")).strip()  # Detecta los valores vacíos.
            ]  # Termina la lista de campos faltantes.
            if faltantes:  # Comprueba si faltan datos necesarios.
                return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"  # Informa qué campos faltan.

            email = str(datos.get("email", "")).strip().lower()  # Limpia y normaliza el email.
            if email in cls.emails_registrados():  # Comprueba si el email ya está en uso.
                return False, "Ese email ya está registrado"  # Rechaza el email duplicado.

            valores = {campo: datos.get(campo, "") for campo in cls.MODELO.CAMPOS}  # Conserva solo los campos del modelo.

            # cls.MODELO es la clase: aquí nace el objeto y sus setters validan todo
            objeto = cls.MODELO(cls.siguiente_id(), **valores)  # Crea el cliente con un nuevo identificador.

            registros = cls._registros()  # Carga los registros actuales.
            registros.append(objeto.a_diccionario())  # Agrega el nuevo cliente a la lista.
            if not cls._gestor.guardar(registros):  # Guarda la lista y comprueba si hubo error.
                return False, "No se pudo escribir el archivo"  # Informa que no se pudo guardar.

            return True, f"{objeto.nombre_completo} creado con id {objeto.id}"  # Confirma la creación del cliente.

        except ValueError as error:  # Atiende errores de validación del modelo.
            # Los setters del Modelo lanzan ValueError con el mensaje ya listo
            return False, str(error)  # Devuelve el mensaje del error.

    # ===== R · READ =====
    @classmethod  # Permite llamar este método desde la clase.
    def listar(cls):  # Define la consulta de todos los clientes.
        """LISTA de objetos del Modelo."""  # Describe el tipo de resultado.
        return [cls.MODELO.desde_diccionario(r) for r in cls._registros()]  # Convierte y devuelve cada registro como objeto.

    @classmethod  # Permite llamar este método desde la clase.
    def obtener(cls, id_registro):  # Busca un cliente por identificador.
        for objeto in cls.listar():  # Recorre los clientes guardados.
            if objeto.id == id_registro:  # Comprueba si coincide el identificador.
                return objeto  # Devuelve el cliente encontrado.
        return None  # Indica que no existe ese cliente.

    # ===== S · SEARCH =====
    @classmethod  # Permite llamar este método desde la clase.
    def buscar(cls, termino):  # Define la búsqueda de clientes.
        termino = str(termino).strip().lower()  # Limpia y normaliza el texto buscado.
        if not termino:  # Comprueba si el término está vacío.
            return []  # Devuelve una lista vacía.
        return [  # Devuelve los registros que coinciden.
            cls.MODELO.desde_diccionario(registro)  # Convierte cada coincidencia en objeto.
            for registro in cls._registros()  # Recorre los registros guardados.
            if cls._coincide(registro, termino, cls.CAMPOS_BUSCABLES)  # Filtra por los campos buscables.
        ]  # Termina la lista de resultados.

    # ===== U · UPDATE =====
    @classmethod  # Permite llamar este método desde la clase.
    def actualizar(cls, id_registro, cambios):  # Define la actualización de un cliente.
        try:  # Intenta aplicar los cambios.
            # DIFERENCIA DE CONJUNTOS: ¿mandaron campos que no existen?
            desconocidos = set(cambios) - set(cls.MODELO.CAMPOS)  # Encuentra campos que no existen en el modelo.
            if desconocidos:  # Comprueba si se enviaron campos inválidos.
                return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"  # Informa cuáles no son válidos.
            if not cambios:  # Comprueba si no se indicó ningún cambio.
                return False, "No se indicó ningún cambio"  # Informa que no hay cambios por aplicar.

            objeto = cls.obtener(id_registro)  # Busca el cliente que se desea modificar.
            if objeto is None:  # Comprueba si el cliente no existe.
                return False, f"No existe un registro con id {id_registro}"  # Informa que no se encontró.

            if "email" in cambios:  # Comprueba si se está cambiando el email.
                nuevo = str(cambios["email"]).strip().lower()  # Limpia y normaliza el nuevo email.
                if nuevo in cls.emails_registrados(excepto_id=id_registro):  # Comprueba si otro registro ya lo usa.
                    return False, "Ese email ya lo usa otro registro"  # Rechaza el email duplicado.

            # setattr le asigna a la PROPIEDAD, así que cada setter valida el valor
            for campo, valor in cambios.items():  # Recorre cada campo que se quiere modificar.
                setattr(objeto, campo, valor)  # Asigna el valor y activa su validación.

            registros = cls._registros()  # Carga los registros actuales.
            for indice, registro in enumerate(registros):  # Recorre registros junto con su posición.
                if registro["id"] == id_registro:  # Busca el registro que se actualiza.
                    registros[indice] = objeto.a_diccionario()  # Reemplaza sus datos por los nuevos.
                    break  # Termina la búsqueda al encontrarlo.

            cls._gestor.guardar(registros)  # Guarda la lista actualizada.
            return True, f"Registro {id_registro} actualizado ({len(cambios)} campo/s)"  # Confirma los cambios.

        except ValueError as error:  # Atiende errores de validación.
            return False, str(error)  # Devuelve el mensaje del error.

    # ===== D · DELETE =====
    @classmethod  # Permite llamar este método desde la clase.
    def eliminar(cls, id_registro):  # Define la eliminación de un cliente.
        registros = cls._registros()  # Carga los registros actuales.
        # Lista nueva sin ese registro: nunca se borra mientras se recorre
        quedan = [r for r in registros if r["id"] != id_registro]  # Conserva los registros con otro identificador.

        if len(quedan) == len(registros):  # Comprueba si no se eliminó ningún registro.
            return False, f"No existe un registro con id {id_registro}"  # Informa que el cliente no existe.

        cls._gestor.guardar(quedan)  # Guarda la lista sin el cliente eliminado.
        return True, f"Registro {id_registro} eliminado"  # Confirma la eliminación.

    # ===== EXTRA =====
    @classmethod  # Permite llamar este método desde la clase.
    def estadisticas(cls):  # Define el cálculo de estadísticas.
        registros = cls._registros()  # Carga los registros guardados.
        ciudades = {r.get("ciudad", "") for r in registros if r.get("ciudad")}  # Reúne las ciudades no vacías.
        dominios = {r["email"].split("@")[1] for r in registros if "@" in r["email"]}  # Reúne los dominios de email.
        sin_telefono = [r["nombre"] for r in registros if not r.get("telefono")]  # Lista clientes sin teléfono.
        return {  # Devuelve las estadísticas calculadas.
            "total": len(registros),  # Incluye el total de registros.
            "ciudades": sorted(ciudades),  # Incluye las ciudades ordenadas.
            "dominios": sorted(dominios),  # Incluye los dominios ordenados.
            "sin_telefono": sin_telefono,  # Incluye los nombres sin teléfono.
        }  # Termina el diccionario de estadísticas.
