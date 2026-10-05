class Cliente:  # Define la clase Cliente, que representa a un cliente válido del sistema.
    """MODELO: un cliente válido. Si los datos están mal, el objeto no se crea."""  # Explica la regla de validación del modelo.

    # ===== ATRIBUTOS DE CLASE (estáticos): existen una sola vez =====
    CAMPOS = ("nombre", "apellido", "email", "telefono", "ciudad", "direccion")  # Nombres de los campos que tiene el cliente.
    OBLIGATORIOS = ("nombre", "apellido", "email")  # Campos que deben venir completos para crear un cliente válido.
    total_creados = 0  # Cuenta cuántos clientes se han creado en total.

    def __init__(self, id_cliente, nombre, apellido, email,
                 telefono="", ciudad="", direccion=""):  # Constructor del cliente con sus datos iniciales.
        self.__id = id_cliente  # Guarda el identificador privado del cliente.
        # Asignamos por las PROPIEDADES para que la validación corra también al crear
        self.nombre = nombre  # Asigna y valida el nombre.
        self.apellido = apellido  # Asigna y valida el apellido.
        self.email = email  # Asigna y valida el email.
        self.telefono = telefono  # Asigna y valida el teléfono.
        self.ciudad = ciudad  # Asigna y normaliza la ciudad.
        self.direccion = direccion  # Asigna y normaliza la dirección.
        Cliente.total_creados += 1  # Incrementa el contador global de clientes creados.

    # ===== MÉTODOS ESTÁTICOS: reglas que no dependen de ningún cliente =====
    @staticmethod  # Define un método estático que no recibe self ni cls.
    def limpiar(texto):  # Quita espacios vacíos al inicio y al final del texto.
        return str(texto).strip()  # Convierte a texto y elimina espacios extras.

    @staticmethod  # Define una regla general sin depender de una instancia.
    def es_email_valido(texto):  # Verifica si un email tiene el formato correcto.
        texto = str(texto).strip()  # Normaliza el texto antes de validar.
        if texto.count("@") != 1:  # Debe tener exactamente un arroba.
            return False  # Si no, devuelve False.
        usuario, dominio = texto.split("@")  # Separa usuario y dominio.
        return len(usuario) > 0 and "." in dominio and not dominio.endswith(".")  # Revisa usuario, punto y dominio final.

    # ===== PROPIEDADES =====
    @property  # Permite leer el valor como si fuera un atributo.
    def id(self):  # Devuelve el ID del cliente.
        # SOLO LECTURA: no tiene setter, así que cliente.id = 5 lanza AttributeError
        return self.__id  # Retorna el valor privado del ID.

    @property  # Lee el nombre usando la propiedad.
    def nombre(self):  # Devuelve el nombre del cliente.
        return self.__nombre  # Retorna el nombre guardado internamente.

    @nombre.setter  # Define cómo asignar el nombre.
    def nombre(self, valor):  # Guarda el nombre con validación.
        valor = Cliente.limpiar(valor)  # Quita espacios y normaliza.
        if not valor:  # Si está vacío, falla.
            raise ValueError("El nombre es obligatorio")  # Lanza error si falta el nombre.
        self.__nombre = valor.title()  # Guarda el nombre con primera letra mayúscula.

    @property  # Lee el apellido.
    def apellido(self):  # Devuelve el apellido del cliente.
        return self.__apellido  # Retorna el apellido guardado.

    @apellido.setter  # Define la asignación del apellido.
    def apellido(self, valor):  # Guarda el apellido con validación.
        valor = Cliente.limpiar(valor)  # Quita espacios vacíos.
        if not valor:  # Si no hay valor, falla.
            raise ValueError("El apellido es obligatorio")  # Lanza error.
        self.__apellido = valor.title()  # Guarda el apellido capitalizado.

    @property  # Lee el email.
    def email(self):  # Devuelve el correo del cliente.
        return self.__email  # Retorna el email guardado.

    @email.setter  # Define la asignación del email.
    def email(self, valor):  # Guarda el email validado.
        valor = Cliente.limpiar(valor)  # Elimina espacios extras.
        if not Cliente.es_email_valido(valor):  # Verifica si el email es válido.
            raise ValueError(f"Email inválido: '{valor}'")  # Lanza error si no es válido.
        self.__email = valor.lower()  # Guarda el correo en minúsculas.

    @property  # Lee el teléfono.
    def telefono(self):  # Devuelve el teléfono del cliente.
        return self.__telefono  # Retorna el teléfono guardado.

    @telefono.setter  # Define la asignación del teléfono.
    def telefono(self, valor):  # Guarda el teléfono validado.
        valor = Cliente.limpiar(valor)  # Quita espacios.
        if valor and not valor.isdigit():  # Si se puso algo, debe ser numérico.
            raise ValueError("El teléfono solo puede tener números")  # Lanza error si hay letras.
        self.__telefono = valor  # Guarda el teléfono.

    @property  # Lee la ciudad.
    def ciudad(self):  # Devuelve la ciudad del cliente.
        return self.__ciudad  # Retorna la ciudad guardada.

    @ciudad.setter  # Define la asignación de la ciudad.
    def ciudad(self, valor):  # Guarda la ciudad normalizada.
        self.__ciudad = Cliente.limpiar(valor).title()  # Limpia y capitaliza la ciudad.

    @property  # Lee la dirección.
    def direccion(self):  # Devuelve la dirección del cliente.
        return self.__direccion  # Retorna la dirección guardada.

    @direccion.setter  # Define la asignación de la dirección.
    def direccion(self, valor):  # Guarda la dirección limpia.
        self.__direccion = Cliente.limpiar(valor)  # Elimina espacios y guarda la dirección.

    # PROPIEDADES CALCULADAS: no guardan nada, se calculan al leerlas
    @property  # Crea una propiedad calculada.
    def nombre_completo(self):  # Devuelve nombre y apellido juntos.
        return f"{self.__nombre} {self.__apellido}"  # Concatena nombre y apellido.

    @property  # Crea una propiedad calculada.
    def dominio_email(self):  # Devuelve el dominio del email, por ejemplo gmail.com.
        return self.__email.split("@")[1]  # Divide el email y toma la parte después del @.

    # ===== MÉTODOS DE INSTANCIA: necesitan los datos de ESTE cliente =====
    def a_diccionario(self):  # Convierte el cliente en un diccionario para guardar.
        return {  # Devuelve un diccionario con todos los datos.
            "id": self.__id,  # Guarda el ID.
            "nombre": self.__nombre,  # Guarda el nombre.
            "apellido": self.__apellido,  # Guarda el apellido.
            "email": self.__email,  # Guarda el email.
            "telefono": self.__telefono,  # Guarda el teléfono.
            "ciudad": self.__ciudad,  # Guarda la ciudad.
            "direccion": self.__direccion,  # Guarda la dirección.
        }

    def __str__(self):  # Define cómo se ve el cliente en texto.
        return f"[{self.__id}] {self.nombre_completo} - {self.__email}"  # Muestra ID, nombre y email.

    # ===== MÉTODO DE CLASE: fabrica un objeto a partir de un diccionario =====
    @classmethod  # Define un método de clase que recibe cls.
    def desde_diccionario(cls, datos):  # Crea un cliente desde un diccionario.
        # cls es la clase. Si mañana existe ClienteVIP(Cliente),
        # ClienteVIP.desde_diccionario(d) devolverá un ClienteVIP.
        return cls(  # Retorna una nueva instancia de la clase actual.
            datos["id"],  # ID del cliente.
            datos["nombre"],  # Nombre del cliente.
            datos["apellido"],  # Apellido del cliente.
            datos["email"],  # Email del cliente.
            datos.get("telefono", ""),  # Teléfono opcional.
            datos.get("ciudad", ""),  # Ciudad opcional.
            datos.get("direccion", ""),  # Dirección opcional.
        )


class Estudiante:  # Define la clase Estudiante, que maneja notas y materias.
    """MODELO: un estudiante con sus materias (set) y sus notas (dict de listas)."""  # Describe el comportamiento del estudiante.

    CAMPOS = ("nombre", "apellido", "email", "carnet")  # Campos que forman un estudiante.
    OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")  # Campos obligatorios.
    NOTA_MINIMA = 0  # Nota mínima permitida.
    NOTA_MAXIMA = 20  # Nota máxima permitida.
    total_creados = 0  # Cuenta cuántos estudiantes se crean.

    def __init__(self, id_estudiante, nombre, apellido, email, carnet,
                 notas=None, materias=None):  # Constructor del estudiante.
        self.__id = id_estudiante  # Guarda el ID del estudiante.
        self.nombre = nombre  # Asigna y valida el nombre.
        self.apellido = apellido  # Asigna y valida el apellido.
        self.email = email  # Asigna y valida el email.
        self.carnet = carnet  # Asigna y valida el carnet.
        self.__notas = dict(notas) if notas else {}  # Guarda las notas por materia como un diccionario de listas.
        self.__materias = set(materias) if materias else set()  # Guarda las materias en un conjunto sin duplicados.
        Estudiante.total_creados += 1  # Incrementa el contador de estudiantes creados.

    # ===== ESTÁTICOS =====
    @staticmethod  # Define un método sin depender de una instancia.
    def limpiar(texto):  # Quita espacios al inicio y final del texto.
        return str(texto).strip()  # Convierte a string y elimina espacios.

    @staticmethod  # Define una regla general para validar notas.
    def es_nota_valida(nota):  # Comprueba si una nota cae dentro del rango válido.
        # No usa self ni cls: es una regla suelta, por eso es estático
        return isinstance(nota, (int, float)) and \
            Estudiante.NOTA_MINIMA <= nota <= Estudiante.NOTA_MAXIMA  # Devuelve True si la nota está en el rango.

    # ===== PROPIEDADES =====
    @property  # Permite leer el ID como atributo.
    def id(self):  # Devuelve el ID del estudiante.
        return self.__id  # Retorna el identificador interno.

    @property  # Lee el nombre.
    def nombre(self):  # Devuelve el nombre del estudiante.
        return self.__nombre  # Retorna el nombre guardado.

    @nombre.setter  # Define asignación del nombre.
    def nombre(self, valor):  # Guarda el nombre con validación.
        valor = Estudiante.limpiar(valor)  # Quita espacios.
        if not valor:  # Si está vacío, falla.
            raise ValueError("El nombre es obligatorio")  # Lanza error.
        self.__nombre = valor.title()  # Guarda el nombre capitalizado.

    @property  # Lee el apellido.
    def apellido(self):  # Devuelve el apellido.
        return self.__apellido  # Retorna el apellido guardado.

    @apellido.setter  # Define la asignación del apellido.
    def apellido(self, valor):  # Guarda el apellido validado.
        valor = Estudiante.limpiar(valor)  # Quita espacios.
        if not valor:  # Si está vacío, falla.
            raise ValueError("El apellido es obligatorio")  # Lanza error.
        self.__apellido = valor.title()  # Guarda el apellido capitalizado.

    @property  # Lee el email.
    def email(self):  # Devuelve el correo.
        return self.__email  # Retorna el email guardado.

    @email.setter  # Define la asignación del email.
    def email(self, valor):  # Guarda el email validado.
        valor = Estudiante.limpiar(valor)  # Quita espacios.
        if "@" not in valor:  # Debe tener arroba.
            raise ValueError(f"Email inválido: '{valor}'")  # Lanza error si no es válido.
        self.__email = valor.lower()  # Guarda el email en minúsculas.

    @property  # Lee el carnet.
    def carnet(self):  # Devuelve el carnet del estudiante.
        return self.__carnet  # Retorna el carnet guardado.

    @carnet.setter  # Define la asignación del carnet.
    def carnet(self, valor):  # Guarda el carnet validado.
        valor = Estudiante.limpiar(valor).upper()  # Elimina espacios y lo pone en mayúsculas.
        if len(valor) < 4:  # Debe tener al menos 4 caracteres.
            raise ValueError("El carnet debe tener al menos 4 caracteres")  # Lanza error si es demasiado corto.
        self.__carnet = valor  # Guarda el carnet final.

    @property  # Lee la lista de materias.
    def materias(self):  # Devuelve una copia del conjunto de materias.
        # Devolvemos una COPIA: así nadie modifica el conjunto interno desde afuera
        return set(self.__materias)  # Retorna una copia del conjunto para proteger los datos internos.

    @property  # Lee el nombre completo.
    def nombre_completo(self):  # Devuelve nombre y apellido juntos.
        return f"{self.__nombre} {self.__apellido}"  # Concatena ambos nombres.

    @property  # Calcula el promedio del estudiante.
    def promedio(self):  # Devuelve el promedio de todas las notas.
        # CALCULADA: recorre el diccionario de listas cada vez que se lee
        todas = []  # Acumula todas las notas de todas las materias.
        for lista_notas in self.__notas.values():  # Recorre cada lista de notas.
            todas.extend(lista_notas)  # Agrega esas notas a la lista total.
        return round(sum(todas) / len(todas), 2) if todas else 0  # Calcula el promedio o devuelve 0 si no hay notas.
    
    #agregado
    @property  # Permite consultar estado como atributo.
    def estado(self):  # Define el estado académico.
        return "Aprobado" if self.promedio >= 14 else "Reprobado"  # Aprueba con promedio de 14 o más.

    # ===== MÉTODOS DE INSTANCIA =====
    def inscribir_materia(self, materia):  # Agrega una materia al estudiante.
        materia = Estudiante.limpiar(materia).title()  # Normaliza y capitaliza la materia.
        if not materia:  # Si la materia queda vacía, falla.
            raise ValueError("La materia no puede estar vacía")  # Lanza error.
        self.__materias.add(materia)  # Agrega la materia al conjunto, sin duplicados.
        return materia  # Devuelve la materia ya normalizada.

    def agregar_nota(self, materia, nota):  # Añade una nota a una materia.
        if not Estudiante.es_nota_valida(nota):  # Verifica si la nota es válida.
            raise ValueError(
                f"La nota debe estar entre {Estudiante.NOTA_MINIMA} y {Estudiante.NOTA_MAXIMA}"
            )  # Lanza error si la nota está fuera del rango.
        materia = self.inscribir_materia(materia)  # Asegura que la materia exista.
        self.__notas.setdefault(materia, []).append(nota)  # Guarda la nota en la lista de esa materia.

    def notas_de(self, materia):  # devuelve las notas de una materia concreta.
        return list(self.__notas.get(Estudiante.limpiar(materia).title(), []))  # Retorna una copia de la lista.

    def materias_en_comun(self, otro):  # Compara materias con otro estudiante.
        # INTERSECCIÓN de conjuntos
        return self.__materias & otro.materias  # Devuelve las materias compartidas.

    def a_diccionario(self):  # Convierte el estudiante en un diccionario para guardar.
        return {  # Devuelve un diccionario con toda la información.
            "id": self.__id,  # Guarda el ID.
            "nombre": self.__nombre,  # Guarda el nombre.
            "apellido": self.__apellido,  # Guarda el apellido.
            "email": self.__email,  # Guarda el email.
            "carnet": self.__carnet,  # Guarda el carnet.
            "notas": self.__notas,  # Guarda el diccionario de notas.
            "materias": sorted(self.__materias),  # JSON no guarda sets
        }

    def __str__(self):  # Define cómo se muestra el estudiante por texto.
        return f"[{self.__carnet}] {self.nombre_completo} - Promedio: {self.promedio}"  # Muestra carnet, nombre y promedio.

    # ===== MÉTODO DE CLASE =====
    @classmethod  # Define un constructor alternativo para la clase.
    def desde_diccionario(cls, datos):  # Crea un estudiante desde un diccionario.
        return cls(  # Retorna una nueva instancia usando los datos.
            datos["id"], datos["nombre"], datos["apellido"], datos["email"],  # ID, nombre, apellido, email.
            datos["carnet"],  # Carnet del estudiante.
            notas=datos.get("notas", {}),  # Carga notas si existen.
            materias=set(datos.get("materias", [])),  # lista -> conjunto otra vez
        )

#PRUEBA
from models import Cliente

ana = Cliente(1, "  ana  ", "pérez", "ANA@Ejemplo.com", "0987654321", "guayaquil", "Av. 1")

print(ana.nombre)            # 'Ana'              -> el setter limpió y capitalizó
print(ana.email)             # 'ana@ejemplo.com'  -> en minúsculas
print(ana.nombre_completo)   # 'Ana Pérez'        -> propiedad calculada, sin paréntesis
print(ana.dominio_email)     # 'ejemplo.com'
print(Cliente.total_creados) # 1                  -> atributo de clase

ana.ciudad = "quito"         # pasa por el setter
print(ana.ciudad)            # 'Quito'

# ana.id = 99                -> AttributeError: property has no setter
# ana.email = "roto"         -> ValueError: Email inválido: 'roto'
# print(ana.__nombre)        -> AttributeError: es privado
print(ana._Cliente__nombre)  # 'Ana'  <- así lo renombra Python por dentro