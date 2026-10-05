from shared.herramientas import (  # Importa las utilidades para mostrar mensajes y confirmar.
    imprimir_titulo,  # Importa la función que presenta títulos.
    imprimir_exito,  # Importa la función que muestra éxitos.
    imprimir_error,  # Importa la función que muestra errores.
    imprimir_info,  # Importa la función que muestra información.
    confirmar  # Importa la función que solicita confirmación.
)  # Cierra la lista de utilidades importadas.
from views import ClienteController  # Importa el controlador de clientes.
from views_estudiante import EstudianteController  # NUEVO: importa el controlador de estudiantes.


class MenuClientes:  # Define la vista del menú de clientes.
    """VISTA: muestra, pide y presenta. No decide reglas del negocio."""  # Describe la responsabilidad de la vista.

    TITULO = "SISTEMA DE GESTIÓN DE CLIENTES"  # Guarda el título del menú.
    ANCHO = 85  # Define el ancho de las líneas de la tabla.

    def __init__(self, controlador=ClienteController):  # Inicializa el menú con su controlador.
        # CAMBIO: __controlador, __activo y __opciones pasaron a un solo guion bajo (_); ahora la subclase puede accederlos.
        # para que la subclase MenuEstudiantes pueda usarlos. Este comentario original se conserva.
        self._controlador = controlador  # Guarda el controlador recibido.
        self._activo = True  # Indica que el menú debe seguir activo.
        self._opciones = {  # Asocia cada tecla con su acción.
            "1": ("Crear", self.crear),  # CAMBIO: antes decía "Crear cliente"; muestra la opción para crear.
            "2": ("Ver todos", self.listar),  # Asocia la opción de listar registros.
            "3": ("Buscar", self.buscar),  # Asocia la opción de buscar registros.
            "4": ("Ver por id", self.ver_por_id),  # Asocia la opción de consultar por identificador.
            "5": ("Actualizar", self.actualizar),  # Asocia la opción de actualizar registros.
            "6": ("Eliminar", self.eliminar),  # Asocia la opción de eliminar registros.
            "7": ("Estadísticas", self.estadisticas),  # Asocia la opción de mostrar estadísticas.
            "0": ("Salir", self.salir),  # Asocia la opción de salir.
        }  # Finaliza el diccionario de opciones.

    @staticmethod  # Declara un método que no necesita la instancia.
    def pausa():  # Define la pausa entre acciones.
        input("\nPresione Enter para continuar...")  # Espera que el usuario presione Enter.

    @staticmethod  # Declara un método independiente de la instancia.
    def pedir_entero(etiqueta):  # Solicita un valor entero.
        try:  # Intenta convertir la entrada a entero.
            return int(input(etiqueta))  # Devuelve el número ingresado.
        except ValueError:  # Atiende entradas que no son números enteros.
            return None  # Indica que la conversión falló.

    @staticmethod  # Declara un método independiente de la instancia.
    def mostrar_resultado(exito, mensaje):  # Presenta el resultado de una operación.
        if exito:  # Comprueba si la operación fue exitosa.
            imprimir_exito(mensaje)  # Muestra el mensaje de éxito.
        else:  # Atiende el caso de operación fallida.
            imprimir_error(mensaje)  # Muestra el mensaje de error.

    def mostrar_tabla(self, clientes):  # Define cómo mostrar clientes en tabla.
        print(f"{'ID':<5}{'NOMBRE':<25}{'EMAIL':<28}{'CIUDAD':<15}{'TELÉFONO':<12}")  # Imprime los encabezados.
        print("-" * self.ANCHO)  # Dibuja la línea superior de la tabla.
        for cliente in clientes:  # Recorre los clientes recibidos.
            print(f"{cliente.id:<5}{cliente.nombre_completo:<25}"  # Imprime el identificador y nombre.
                  f"{cliente.email:<28}{cliente.ciudad:<15}{cliente.telefono:<12}")  # Completa los datos de la fila.
        print("-" * self.ANCHO)  # Dibuja la línea inferior de la tabla.
        imprimir_info(f"Total: {len(clientes)} cliente(s)")  # Informa cuántos clientes hay.

    def crear(self):  # Define el proceso de creación.
        imprimir_titulo("CREAR NUEVO REGISTRO")  # CAMBIO: texto genérico (antes "CREAR NUEVO CLIENTE"); presenta el formulario.
        datos = {}  # Prepara el diccionario con los datos ingresados.
        for campo in self._controlador.MODELO.CAMPOS:  # CAMBIO: self._controlador (un guion); solicita cada campo del modelo.
            datos[campo] = input(f"{campo.capitalize()}: ")  # Guarda el valor digitado para el campo.
        exito, mensaje = self._controlador.crear(datos)  # CAMBIO: self._controlador; solicita crear el registro.
        self.mostrar_resultado(exito, mensaje)  # Muestra el resultado de la creación.
        self.pausa()  # Espera antes de volver al menú.

    def listar(self):  # Define la consulta de todos los registros.
        imprimir_titulo("LISTA DE REGISTROS")  # CAMBIO: texto genérico; muestra el encabezado de la lista.
        registros = self._controlador.listar()  # CAMBIO: variable "registros" y self._controlador; obtiene todos los registros.
        if not registros:  # Comprueba si no hay registros.
            imprimir_info("Todavía no hay registros. Use la opción 1 para crear el primero.")  # CAMBIO: texto genérico; informa que la lista está vacía.
        else:  # Atiende el caso en que sí hay registros.
            self.mostrar_tabla(registros)  # Presenta los registros en una tabla.
        self.pausa()  # Espera antes de volver al menú.

    def buscar(self):  # Define la búsqueda de registros.
        imprimir_titulo("BUSCAR")  # CAMBIO: texto genérico; presenta la búsqueda.
        termino = input("Término de búsqueda: ")  # CAMBIO: texto genérico; solicita el término.
        encontrados = self._controlador.buscar(termino)  # CAMBIO: self._controlador; obtiene las coincidencias.
        if not encontrados:  # Comprueba si no hubo coincidencias.
            imprimir_info(f"Nada coincide con '{termino}'.")  # CAMBIO: texto genérico; informa que no hay resultados.
        else:  # Atiende cuando existen coincidencias.
            self.mostrar_tabla(encontrados)  # Presenta los resultados encontrados.
        self.pausa()  # Espera antes de volver al menú.

    def ver_por_id(self):  # Define la consulta de un cliente por identificador.
        imprimir_titulo("VER CLIENTE POR ID")  # Presenta el título de la consulta.
        id_cliente = self.pedir_entero("Id del cliente: ")  # Solicita el identificador del cliente.
        if id_cliente is None:  # Comprueba si el identificador no es válido.
            imprimir_error("El id debe ser un número entero")  # Informa el formato requerido.
            return self.pausa()  # Pausa y termina esta acción.

        cliente = self._controlador.obtener(id_cliente)  # CAMBIO: self._controlador; obtiene el cliente solicitado.
        if cliente is None:  # Comprueba si el cliente no existe.
            imprimir_error(f"No existe un cliente con id {id_cliente}")  # Informa que no se encontró.
        else:  # Atiende cuando el cliente sí existe.
            for clave, valor in cliente.a_diccionario().items():  # Recorre los atributos del cliente.
                print(f"  {clave.capitalize():<12}: {valor}")  # Imprime cada atributo y su valor.
            imprimir_info(f"Dominio del email: {cliente.dominio_email}")  # Muestra el dominio de su correo.
        self.pausa()  # Espera antes de volver al menú.

    def actualizar(self):  # Define la modificación de un registro.
        imprimir_titulo("ACTUALIZAR")  # CAMBIO: texto genérico; presenta la actualización.
        id_registro = self.pedir_entero("Id: ")  # CAMBIO: variable id_registro (antes id_cliente); solicita el identificador.
        if id_registro is None:  # Comprueba si el identificador no es válido.
            imprimir_error("El id debe ser un número entero")  # Informa el formato requerido.
            return self.pausa()  # Pausa y termina esta acción.

        objeto = self._controlador.obtener(id_registro)  # CAMBIO: variable "objeto" (antes "cliente"); busca el registro.
        if objeto is None:  # Comprueba si el registro no existe.
            imprimir_error(f"No existe un registro con id {id_registro}")  # CAMBIO: texto genérico; informa que no se encontró.
            return self.pausa()  # Pausa y termina esta acción.

        imprimir_info(f"Editando a {objeto.nombre_completo}")  # Indica qué registro se modificará.
        print("Deje en blanco el campo que no quiera cambiar.\n")  # Explica cómo omitir campos.

        cambios = {}  # Prepara los valores que se modificarán.
        for campo in self._controlador.MODELO.CAMPOS:  # CAMBIO: self._controlador; recorre los campos editables.
            actual = getattr(objeto, campo)  # Obtiene el valor actual del campo.
            nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()  # Solicita el nuevo valor.
            if nuevo:  # Comprueba si se ingresó un valor.
                cambios[campo] = nuevo  # Guarda el cambio solicitado.

        self.mostrar_resultado(*self._controlador.actualizar(id_registro, cambios))  # CAMBIO: self._controlador; actualiza y muestra el resultado.
        self.pausa()  # Espera antes de volver al menú.

    def eliminar(self):  # Define la eliminación de un registro.
        imprimir_titulo("ELIMINAR")  # CAMBIO: texto genérico; presenta la eliminación.
        id_registro = self.pedir_entero("Id: ")  # CAMBIO: variable id_registro; solicita el identificador.
        if id_registro is None:  # Comprueba si el identificador no es válido.
            imprimir_error("El id debe ser un número entero")  # Informa el formato requerido.
            return self.pausa()  # Pausa y termina esta acción.

        objeto = self._controlador.obtener(id_registro)  # CAMBIO: variable "objeto"; busca el registro a eliminar.
        if objeto is None:  # Comprueba si el registro no existe.
            imprimir_error(f"No existe un registro con id {id_registro}")  # CAMBIO: texto genérico; informa que no se encontró.
            return self.pausa()  # Pausa y termina esta acción.

        imprimir_info(f"Se eliminará: {objeto}")  # Muestra el registro seleccionado.
        if confirmar("¿Confirma la eliminación?"):  # Solicita confirmación antes de borrar.
            self.mostrar_resultado(*self._controlador.eliminar(id_registro))  # CAMBIO: self._controlador; elimina y muestra el resultado.
        else:  # Atiende cuando el usuario cancela.
            imprimir_info("Operación cancelada")  # Informa que no se eliminó el registro.
        self.pausa()  # Espera antes de volver al menú.

    def estadisticas(self):  # Define la consulta de estadísticas.
        imprimir_titulo("ESTADÍSTICAS")  # Presenta el título de las estadísticas.
        datos = self._controlador.estadisticas()  # CAMBIO: self._controlador; obtiene los datos estadísticos.
        print(f"  Clientes registrados : {datos['total']}")  # Imprime el total de clientes.
        print(f"  Ciudades distintas   : {len(datos['ciudades'])} -> {', '.join(datos['ciudades'])}")  # Imprime las ciudades distintas.
        print(f"  Dominios de email    : {', '.join(datos['dominios'])}")  # Imprime los dominios de correo.
        print(f"  Sin teléfono         : {len(datos['sin_telefono'])}")  # Imprime cuántos clientes no tienen teléfono.
        self.pausa()  # Espera antes de volver al menú.

    def salir(self):  # Define la acción para salir.
        self._activo = False  # CAMBIO: self._activo (un guion); detiene el ciclo del menú.
        imprimir_info("¡Hasta luego! 👋")  # Despide al usuario.

    def mostrar_menu(self):  # Define la presentación de las opciones.
        imprimir_titulo(self.TITULO)  # Imprime el título del menú.
        for tecla, (texto, _metodo) in self._opciones.items():  # CAMBIO: self._opciones; recorre las opciones registradas.
            print(f"  {tecla}. {texto}")  # Muestra la tecla y su descripción.
        print()  # Añade una línea en blanco.

    def ejecutar(self):  # Define el ciclo principal del menú.
        while self._activo:  # CAMBIO: self._activo; repite mientras el menú siga activo.
            self.mostrar_menu()  # Presenta las opciones disponibles.
            tecla = input("Seleccione una opción: ").strip()  # Lee y limpia la opción ingresada.

            if tecla not in self._opciones:  # CAMBIO: self._opciones; valida que la opción exista.
                imprimir_error("Opción no válida")  # Informa que la opción no es reconocida.
                self.pausa()  # Espera antes de repetir el menú.
                continue  # Inicia la siguiente iteración del ciclo.

            _texto, metodo = self._opciones[tecla]  # CAMBIO: self._opciones; obtiene la acción seleccionada.
            metodo()  # Ejecuta la acción elegida.


# ======================================================================  # Separa visualmente las secciones del archivo.
# NUEVO: toda la clase MenuEstudiantes; define el menú especializado de estudiantes.
# ======================================================================  # Cierra el separador visual.
class MenuEstudiantes(MenuClientes):  # NUEVO: hereda de MenuClientes; reutiliza sus acciones comunes.
    """VISTA de estudiantes: hereda el menú y cambia/agrega lo suyo."""  # Describe el menú especializado.

    TITULO = "SISTEMA DE GESTIÓN DE ESTUDIANTES"  # NUEVO: cambia el título (punto 6 del enunciado); identifica este menú.

    def __init__(self, controlador=EstudianteController):  # NUEVO: usa el controlador de estudiantes; inicializa el menú.
        super().__init__(controlador)  # NUEVO: ejecuta el __init__ del padre; configura opciones comunes.
        salir = self._opciones.pop("0")  # NUEVO: saca "Salir" para ponerlo al final; conserva su acción.
        self._opciones["8"] = ("Agregar nota", self.agregar_nota)  # NUEVO: opción 8; registra agregar notas.
        self._opciones["9"] = ("Ver promedio", self.ver_promedio)  # NUEVO: opción 9; registra consultar promedios.
        self._opciones["10"] = ("Materias en común", self.materias_en_comun)  # NUEVO: opción 10; registra comparar materias.
        self._opciones["0"] = salir  # NUEVO: "Salir" vuelve al final; restaura la opción de salida.

    # NUEVO: sobrescribe la tabla (carnet, promedio y estado en vez de ciudad y teléfono); personaliza sus columnas.
    def mostrar_tabla(self, estudiantes):  # Define la tabla de estudiantes.
        print(f"{'ID':<5}{'NOMBRE':<25}{'CARNET':<14}{'PROMEDIO':<10}{'ESTADO'}")  # Imprime los encabezados.
        print("-" * 65)  # Dibuja la línea superior de la tabla.
        for e in estudiantes:  # Recorre los estudiantes recibidos.
            print(f"{e.id:<5}{e.nombre_completo:<25}{e.carnet:<14}"  # Imprime identificador, nombre y carnet.
                  f"{e.promedio:<10}{e.estado}")  # Completa la fila con promedio y estado.
        print("-" * 65)  # Dibuja la línea inferior de la tabla.
        imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")  # Informa cuántos estudiantes hay.

    # NUEVO: sobrescribe ver_por_id (Estudiante no tiene dominio_email); evita consultar un atributo inexistente.
    def ver_por_id(self):  # Define la consulta de estudiante por identificador.
        imprimir_titulo("VER ESTUDIANTE POR ID")  # Presenta el título de la consulta.
        id_est = self.pedir_entero("Id del estudiante: ")  # Solicita el identificador.
        if id_est is None:  # Comprueba si el identificador no es válido.
            imprimir_error("El id debe ser un número entero")  # Informa el formato requerido.
            return self.pausa()  # Pausa y termina esta acción.

        est = self._controlador.obtener(id_est)  # Busca el estudiante solicitado.
        if est is None:  # Comprueba si el estudiante no existe.
            imprimir_error(f"No existe un estudiante con id {id_est}")  # Informa que no se encontró.
        else:  # Atiende cuando el estudiante sí existe.
            for clave, valor in est.a_diccionario().items():  # Recorre sus atributos.
                print(f"  {clave.capitalize():<10}: {valor}")  # Imprime cada atributo y su valor.
            imprimir_info(f"Promedio: {est.promedio} - Estado: {est.estado}")  # Muestra su promedio y estado.
        self.pausa()  # Espera antes de volver al menú.

    # NUEVO: sobrescribe estadisticas (aprobados/reprobados y materias ofertadas); adapta los datos al estudiante.
    def estadisticas(self):  # Define las estadísticas de estudiantes.
        imprimir_titulo("ESTADÍSTICAS")  # Presenta el título de las estadísticas.
        estudiantes = self._controlador.listar()  # Obtiene todos los estudiantes.
        aprobados = [e for e in estudiantes if e.estado == "Aprobado"]  # Filtra los estudiantes aprobados.
        materias = self._controlador.materias_ofertadas()  # Obtiene las materias disponibles.
        print(f"  Estudiantes registrados : {len(estudiantes)}")  # Imprime el total de estudiantes.
        print(f"  Aprobados / Reprobados  : {len(aprobados)} / {len(estudiantes) - len(aprobados)}")  # Imprime aprobados y reprobados.
        print(f"  Materias ofertadas      : {', '.join(sorted(materias)) or 'ninguna'}")  # Imprime las materias ofertadas.
        self.pausa()  # Espera antes de volver al menú.

    # NUEVO: opción 8, Agregar nota; permite registrar una calificación.
    def agregar_nota(self):  # Define el registro de una nota.
        imprimir_titulo("AGREGAR NOTA")  # Presenta el título de la acción.
        id_est = self.pedir_entero("Id del estudiante: ")  # Solicita el identificador del estudiante.
        if id_est is None:  # Comprueba si el identificador no es válido.
            imprimir_error("El id debe ser un número entero")  # Informa el formato requerido.
            return self.pausa()  # Pausa y termina esta acción.

        materia = input("Materia: ")  # Solicita el nombre de la materia.
        try:  # Intenta leer la nota como número decimal.
            nota = float(input("Nota (0-20): "))  # input da texto: aquí se convierte a número y se guarda la nota.
        except ValueError:  # Atiende una entrada que no es numérica.
            imprimir_error("La nota debe ser un número")  # Informa el formato de nota requerido.
            return self.pausa()  # Pausa y termina esta acción.

        self.mostrar_resultado(*self._controlador.agregar_nota(id_est, materia, nota))  # Registra la nota y muestra el resultado.
        self.pausa()  # Espera antes de volver al menú.

    # NUEVO: opción 9, Ver promedio; permite consultar el resultado académico.
    def ver_promedio(self):  # Define la consulta del promedio.
        imprimir_titulo("VER PROMEDIO")  # Presenta el título de la consulta.
        id_est = self.pedir_entero("Id del estudiante: ")  # Solicita el identificador.
        est = self._controlador.obtener(id_est) if id_est is not None else None  # Busca solo si el identificador es válido.
        if est is None:  # Comprueba si no se encontró al estudiante.
            imprimir_error("Estudiante no encontrado")  # Informa que no existe.
        else:  # Atiende cuando se encontró al estudiante.
            imprimir_info(f"{est.nombre_completo}: {est.promedio} ({est.estado})")  # Muestra nombre, promedio y estado.
        self.pausa()  # Espera antes de volver al menú.

    # NUEVO: opción 10, Materias en común; compara los cursos de dos estudiantes.
    def materias_en_comun(self):  # Define la comparación de materias.
        imprimir_titulo("MATERIAS EN COMÚN")  # Presenta el título de la consulta.
        a = self.pedir_entero("Id del primer estudiante: ")  # Solicita el primer identificador.
        b = self.pedir_entero("Id del segundo estudiante: ")  # Solicita el segundo identificador.
        if a is None or b is None:  # Comprueba si alguno de los identificadores no es válido.
            imprimir_error("Los ids deben ser números enteros")  # Informa el formato requerido.
            return self.pausa()  # Pausa y termina esta acción.

        exito, resultado = self._controlador.materias_en_comun(a, b)  # Obtiene las materias compartidas.
        if exito:  # Comprueba si la consulta se completó correctamente.
            imprimir_info(", ".join(sorted(resultado)) or "No comparten materias")  # Muestra las materias coincidentes.
        else:  # Atiende el fallo de la consulta.
            imprimir_error(resultado)  # Muestra el motivo del error.
        self.pausa()  # Espera antes de volver al menú.


if __name__ == "__main__":  # Ejecuta el bloque solo al iniciar directamente este archivo.
    try:  # Controla la interrupción manual del programa.
        print("1. Clientes\n2. Estudiantes")  # CAMBIO: ahora se elige el sistema; muestra las opciones iniciales.
        if input("Elija el sistema: ").strip() == "2":  # CAMBIO: solicita y comprueba el sistema elegido.
            MenuEstudiantes().ejecutar()  # NUEVO: abre el menú de estudiantes.
        else:  # Atiende cualquier opción distinta de estudiantes.
            MenuClientes().ejecutar()  # Inicia el menú de clientes.
    except KeyboardInterrupt:  # Atiende la interrupción del teclado.
        print("\nPrograma interrumpido por el usuario.")  # Informa que el programa fue interrumpido.