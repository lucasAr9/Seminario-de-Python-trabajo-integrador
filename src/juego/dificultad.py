import json
import os

from rutas import CONFIG_DIR

"""Rango de valores de la pantalla de la configuracion"""
cant_tiempos = [x for x in range(5, 31, 5)]  # del 5 al 30, de 5 en 5
cant_rondas = [x for x in range(1, 11)]  # del 1 al 10
cant_correcto = [x for x in range(1, 21)]  # del 1 al 20
cant_incorrecto = [x for x in range(1, 21)]  # del 1 al 20
cant_niveles = [1, 2, 3, 4, 5]  # del 1 al 5

"""Ruta del archivo de configuraciones.json con los ultimos valores guardados"""
RUTA_JSON = os.path.join(CONFIG_DIR, "configuracion.json")


class Dificultad:
    """Caracteristicas que permite la configuracion del juego segun su dificultad."""
    __tiempo_u = None
    __rondas = None
    __correctas = None
    __incorrectas = None
    __nivel = None

    def __init__(self, dificultad_actual):
        """
        Llama a la funcion que lee los datos de configuracion.json
        y lo settea a las variables de la clase para poder usarse en la pantalla de juego.
        :param dificultad_actual: la clave de la dificultad a settear.
        """
        try:
            datos = leer_archivo_json()
            actuales = datos[dificultad_actual]
            self.settear_dificultad_elegida(actuales)
        except KeyError:
            # si ocurre el error de que no se encontro alguna key en el archivo, que lo cree con valores por defecto.
            datos = establecer_dificultades()
            actuales = datos[dificultad_actual]
            self.settear_dificultad_elegida(actuales)

    """Getters de la dificultad"""
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

    @staticmethod
    def settear_dificultad_elegida(actuales):
        """
        Settear los valores de la clase Dificultad con los valores del archivo configuracion.json.
        :param actuales: el diccionario con los datos de la dificultad elegida.
        """
        __tiempo = actuales['-TIEMPO_C-']
        __rondas = actuales['-RONDAS_C-']
        __correctas = actuales['-CORRECTO_C-']
        __incorrectas = actuales['-INCORRECTO_C-']
        __nivel = actuales['-CARACTERISTICAS_C-']


def leer_archivo_json():
    """
    Abrir el archivo configuracion.json y leer los valores, si no se encontro el archivo,
    lo crea con valores por defecto.
    :return: el diccionario con los datos del archivo configuracion.json.
    """
    try:
        with open(RUTA_JSON, 'r', encoding='utf-8') as config:
            datos = json.load(config)
        return datos
    except FileNotFoundError:
        # si ocurre el error de que no se encontro el archivo, que lo cree con valores por defecto.
        datos = establecer_dificultades()
        return datos


def establecer_dificultades():
    """
    Configuraciones por defecto para el archivo configuracion.json.
    :return: los datos por defecto en un diccionario.
    """
    datos = {'-FACIL-': {
        '-TIEMPO_C-': cant_tiempos[len(cant_tiempos) - 1],
        '-RONDAS_C-': cant_rondas[len(cant_rondas) - 1],
        '-CORRECTO_C-': cant_correcto[len(cant_correcto) - 1],
        '-INCORRECTO_C-': cant_incorrecto[0],
        '-CARACTERISTICAS_C-': cant_niveles[len(cant_niveles) - 1]
    }, '-NORMAL-': {
        '-TIEMPO_C-': cant_tiempos[len(cant_tiempos) // 2],
        '-RONDAS_C-': cant_rondas[len(cant_rondas) // 2],
        '-CORRECTO_C-': cant_correcto[len(cant_correcto) // 2],
        '-INCORRECTO_C-': cant_incorrecto[len(cant_incorrecto) // 2],
        '-CARACTERISTICAS_C-': cant_niveles[len(cant_niveles) // 2]
    }, '-DIFICIL-': {
        '-TIEMPO_C-': cant_tiempos[0],
        '-RONDAS_C-': cant_rondas[0],
        '-CORRECTO_C-': cant_correcto[0],
        '-INCORRECTO_C-': cant_incorrecto[len(cant_incorrecto) - 1],
        '-CARACTERISTICAS_C-': cant_niveles[0]
    }, '-PERSONALIZADO-': {
        '-TIEMPO_C-': cant_tiempos[len(cant_tiempos) - 1],
        '-RONDAS_C-': cant_rondas[len(cant_rondas) - 1],
        '-CORRECTO_C-': cant_correcto[len(cant_correcto) - 1],
        '-INCORRECTO_C-': cant_incorrecto[0],
        '-CARACTERISTICAS_C-': cant_niveles[len(cant_niveles) - 1]
    }}
    guardar_en_json(datos)
    return datos


def guardar_en_json(valores):
    """
    Reescribir el archivo json con la configuracion que el usuario establezca.
    :param valores: valores que establezca el usuario en los sg.Combo() con valores a elegir.
    """
    with open(RUTA_JSON, 'w', encoding='utf-8') as config:
        json.dump(valores, config, indent=4)


def guardar_nivel_personalizado(valores):
    """
    Guarda en el archivo configuracion.json los valores que el usuario establezca en los sg.Combo()
    con valores a elegir para la dificultad personalizada.
    """
    datos = leer_archivo_json()
    datos['-PERSONALIZADO-'] = valores
    guardar_en_json(datos)
