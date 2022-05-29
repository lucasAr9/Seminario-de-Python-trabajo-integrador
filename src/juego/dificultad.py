import json
import os

"""Rango de valores de la pantalla de la configuracion"""
cant_tiempos = [x for x in range(5, 31, 5)]  # del 5 al 30, de 5 en 5
cant_rondas = [x for x in range(1, 11)]  # del 1 al 10
cant_correcto = [x for x in range(1, 21)]  # del 1 al 20
cant_incorrecto = [x for x in range(1, 21)]  # del 1 al 20
cant_niveles = [1, 2, 3, 4, 5]  # del 1 al 5

"""Ruta del archivo de configuraciones.json con los ultimos valores guardados"""
RUTA_JSON = os.path.join(os.path.realpath(''), "recursos", "datos", "configuracion.json")


class Dificultad:
    """Caracteristicas que permite la configuracion del juego segun su dificultad."""

    """Variables para configurar la dificultad el juego."""
    __dificultad = None
    __tiempo_u = None
    __rondas = None
    __correctas = None
    __incorrectas = None
    __nivel = None

    """Getters de la dificultad"""
    @property
    def dificultad(self):
        return self.__dificultad

    @property
    def tiempo(self):
        return self.__tiempo_u

    @property
    def rondas(self):
        return self.__rondas

    @property
    def correctas(self):
        return self.__correctas

    @property
    def incorrectas(self):
        return self.__incorrectas

    @property
    def nivel(self):
        return self.__nivel

    """setters de la dificultad"""
    @dificultad.setter
    def dificultad(self, dificultad):
        self.__dificultad = dificultad

    @tiempo.setter
    def tiempo(self, tiempo):
        self.__tiempo_u = tiempo

    @rondas.setter
    def rondas(self, rondas):
        self.__rondas = rondas

    @correctas.setter
    def correctas(self, correctas):
        self.__correctas = correctas

    @incorrectas.setter
    def incorrectas(self, incorrectas):
        self.__incorrectas = incorrectas

    @nivel.setter
    def nivel(self, nivel):
        self.__nivel = nivel


def cargar_configuracion():
    """Lee los valores del archivo configuracion.json y los guarda en las variables de la clase."""
    try:
        datos = leer_configuracion()
        Dificultad.dificultad = datos["-DIFICULTAD-C"]
        Dificultad.tiempo_u = datos["-TIEMPO_C-"]
        Dificultad.rondas = datos["-RONDAS_C-"]
        Dificultad.correctas = datos["-CORRECTO_C-"]
        Dificultad.incorrectas = datos["-INCORRECTO_C-"]
        Dificultad.nivel = datos["-CARACTERISTICAS_C-"]
    except KeyError:
        datos = crear_configuracion()
        Dificultad.dificultad = datos["-DIFICULTAD-C"]
        Dificultad.tiempo_u = datos["-TIEMPO_C-"]
        Dificultad.rondas = datos["-RONDAS_C-"]
        Dificultad.correctas = datos["-CORRECTO_C-"]
        Dificultad.incorrectas = datos["-INCORRECTO_C-"]
        Dificultad.nivel = datos["-CARACTERISTICAS_C-"]


def leer_configuracion():
    """
    Abrir el archivo configuracion.json y leer los valores, si no se encontro el archivo,
    lo crea con valores por defecto.
    :return: el diccionario con los datos del archivo configuracion.json
    """
    try:
        with open(RUTA_JSON, 'r', encoding='utf-8') as config:
            datos = json.load(config)
        return datos
    except FileNotFoundError:
        # si ocurre el error de que no se encontro alguna key en el archivo, que lo cree con valores default
        datos = crear_configuracion()
        return datos


def settear_ultima_seleccion(event):
    datos = {}
    if event == "FACIL":
        datos["-DIFICULTAD-C"] = '-FACIL-'
        datos["-TIEMPO_C-"] = cant_tiempos[len(cant_tiempos)]
        datos["-RONDAS_C-"] = cant_rondas[len(cant_rondas)]
        datos["-CORRECTO_C-"] = cant_correcto[len(cant_correcto)]
        datos["-INCORRECTO_C-"] = cant_incorrecto[len(cant_incorrecto)]
        datos["-CARACTERISTICAS_C-"] = cant_niveles[len(cant_niveles) - 1]
        guardar_configuracion(datos)
    elif event == "NOEMAL":
        datos["-DIFICULTAD-C"] = '-NORMAL-'
        datos["-TIEMPO_C-"] = cant_tiempos[len(cant_tiempos) // 2]
        datos["-RONDAS_C-"] = cant_rondas[len(cant_rondas) // 2]
        datos["-CORRECTO_C-"] = cant_correcto[len(cant_correcto) // 2]
        datos["-INCORRECTO_C-"] = cant_incorrecto[len(cant_incorrecto) // 2]
        datos["-CARACTERISTICAS_C-"] = cant_niveles[len(cant_niveles) // 2]
        guardar_configuracion(datos)
    elif event == "-DFICIL-":
        datos["-DIFICULTAD-C"] = '-DIFICIL-'
        datos["-TIEMPO_C-"] = cant_tiempos[0]
        datos["-RONDAS_C-"] = cant_rondas[0]
        datos["-CORRECTO_C-"] = cant_correcto[0]
        datos["-INCORRECTO_C-"] = cant_incorrecto[0]
        datos["-CARACTERISTICAS_C-"] = cant_niveles[0]
        guardar_configuracion(datos)


def guardar_configuracion(values):
    """
    Reescribir el archivo json con la configuracion que el usuario establezca.
    :param values: valores que establezca el usuario en los sg.Combo() con valores a elegir.
    """
    with open(RUTA_JSON, 'w', encoding='utf-8') as config:
        json.dump(values, config, indent=4)
    cargar_configuracion()


def crear_configuracion():
    """
    Crear el archivo configuracion.json con valores por defecto.
    :return: el diccionario con los datos del archivo configuracion.json
    """
    datos_d = {
        "-DIFICULTAD-C": "FACIL",
        "-TIEMPO_C-": cant_tiempos[0],
        "-RONDAS_C-": cant_rondas[0],
        "-CORRECTO_C-": cant_correcto[0],
        "-INCORRECTO_C-": cant_incorrecto[0],
        "-CARACTERISTICAS_C-": cant_niveles[len(cant_niveles) - 1]
    }
    with open(RUTA_JSON, 'w', encoding='utf-8') as config:
        json.dump(datos_d, config, indent=4)
    return datos_d
