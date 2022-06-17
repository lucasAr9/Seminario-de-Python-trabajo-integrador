import json
import os

from rutas import CONFIG_DIR

"""Rango de valores de la pantalla de la configuracion"""
CANT_TIEMPOS = [x for x in range(5, 31)]  # del 5 al 30, de 5 en 5
CANT_RONDAS = [x for x in range(5, 11)]  # del 1 al 10
CANT_CORRECTO = [x for x in range(1, 11)]  # del 1 al 20
CANT_INCORRECTO = [x for x in range(1, 11)]  # del 1 al 20
CANT_NIVELES = [1, 2, 3, 4, 5]  # del 1 al 5

"""Ruta del archivo de configuraciones.json con los ultimos valores guardados"""
RUTA_JSON = os.path.join(CONFIG_DIR, "configuracion.json")


class Dificultad:
    """Caracteristicas que permite la configuracion de la funcionalidad segun su dificultad."""

    def __init__(self, dificultad_actual):
        """
        Llama a la funcion que lee los datos de configuracion.json
        y lo settea a las variables de la clase para poder usarse en la pantalla de funcionalidad.
        :param dificultad_actual: la clave de la dificultad a settear.
        """
        self.tiempo = None
        self.rondas = None
        self.correctas = None
        self.incorrectas = None
        self.caracteristicas = None
        try:
            datos = leer_archivo_json()
            actuales = datos[dificultad_actual]
            self.settear_dificultad_elegida(actuales)
        except KeyError:
            # si ocurre el error de que no se encontro alguna key en el archivo, que lo cree con valores por defecto.
            datos = establecer_dificultades()
            actuales = datos[dificultad_actual]
            self.settear_dificultad_elegida(actuales)

    def settear_dificultad_elegida(self, actuales):
        """
        Settear los valores de la clase Dificultad con los valores del archivo configuracion.json.
        :param actuales: el diccionario con los datos de la dificultad elegida.
        """
        self.tiempo = actuales['-TIEMPO_C-']
        self.rondas = actuales['-RONDAS_C-']
        self.correctas = actuales['-CORRECTO_C-']
        self.incorrectas = actuales['-INCORRECTO_C-']
        self.caracteristicas = actuales['-CARACTERISTICAS_C-']


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
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        # si ocurre el error de que no se encontro el archivo, que lo cree con valores por defecto.
        datos = establecer_dificultades()
        return datos


def establecer_dificultades():
    """
    Configuraciones por defecto para el archivo configuracion.json.
    :return: los datos por defecto en un diccionario.
    """
    datos = {'-FACIL-': {
        '-TIEMPO_C-': CANT_TIEMPOS[-1],
        '-RONDAS_C-': CANT_RONDAS[-1],
        '-CORRECTO_C-': CANT_CORRECTO[-1],
        '-INCORRECTO_C-': CANT_INCORRECTO[0],
        '-CARACTERISTICAS_C-': CANT_NIVELES[-1]
    }, '-NORMAL-': {
        '-TIEMPO_C-': CANT_TIEMPOS[len(CANT_TIEMPOS) // 2],
        '-RONDAS_C-': CANT_RONDAS[len(CANT_RONDAS) // 2],
        '-CORRECTO_C-': CANT_CORRECTO[len(CANT_CORRECTO) // 2],
        '-INCORRECTO_C-': CANT_INCORRECTO[len(CANT_INCORRECTO) // 2],
        '-CARACTERISTICAS_C-': CANT_NIVELES[len(CANT_NIVELES) // 2]
    }, '-DIFICIL-': {
        '-TIEMPO_C-': CANT_TIEMPOS[0],
        '-RONDAS_C-': CANT_RONDAS[0],
        '-CORRECTO_C-': CANT_CORRECTO[0],
        '-INCORRECTO_C-': CANT_INCORRECTO[-1],
        '-CARACTERISTICAS_C-': CANT_NIVELES[0]
    }, '-PERSONALIZADO-': {
        '-TIEMPO_C-': CANT_TIEMPOS[-1],
        '-RONDAS_C-': CANT_RONDAS[-1],
        '-CORRECTO_C-': CANT_CORRECTO[-1],
        '-INCORRECTO_C-': CANT_INCORRECTO[0],
        '-CARACTERISTICAS_C-': CANT_NIVELES[-1]
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
