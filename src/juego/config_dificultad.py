import json
import os

from src.pantallas import configuracion as c_pantalla


class Configuracion:
    """Caracteristicas que permite la configuracion del juego segun su dificultad."""

    def __init__(self):
        """Variables para configurar la dificultad el juego"""
        self.__nivel = None
        self.__incorrectas = None
        self.__correctas = None
        self.__rondas = None
        self.__tiempo_u = None

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

    """Setters de la dificultad"""
    def set_datos(self, datos):
        """
        Establecer los valores de las variables de instancia.
        :param datos: el diccionario leido del archivo configuracion.json
        """
        self.__tiempo_u = datos["-TIEMPO_C-"]
        self.__rondas = datos["-RONDAS_C-"]
        self.__correctas = datos["-CORRECTO_C-"]
        self.__incorrectas = datos["-INCORRECTO_C-"]
        self.__nivel = datos["-CARACTERISTICAS_C-"]

    @staticmethod
    def get_config():
        """
        Abrir el archivo configuracion.json y leer los valores, o si no se encontro el archivo,
        crearlo con valores por defecto.
        :return: el diccionario con los datos del archivo configuracion.json
        """
        ruta_completa = os.path.join(os.path.realpath('..'), "recursos", "datos", "configuracion.json")
        try:
            with open(ruta_completa, 'r', encoding='utf-8') as config:
                datos = json.load(config)
            return datos
        except FileNotFoundError:
            # si ocurre el error de que no encontro el archivo, que lo cree con valores default y lo retorne
            datos_d = {
                "-TIEMPO_C-": c_pantalla.cant_tiempos[0],
                "-RONDAS_C-": c_pantalla.cant_rondas[0],
                "-CORRECTO_C-": c_pantalla.cant_correcto[0],
                "-INCORRECTO_C-": c_pantalla.cant_incorrecto[0],
                "-CARACTERISTICAS_C-": c_pantalla.cant_niveles[len(c_pantalla.cant_niveles) - 1]
            }
            with open(ruta_completa, 'w', encoding='utf-8') as config:
                json.dump(datos_d, config, indent=4)
            return datos_d

    @staticmethod
    def set_config(values):
        """
        Reescribir el archivo json con la configuracion que el usuario establezca.
        :param values: valores que establezca el usuario en los sg.Combo() con valores a elegir.
        """
        ruta_completa = os.path.join(os.path.realpath('..'), "recursos", "datos", "configuracion.json")
        with open(ruta_completa, 'w', encoding='utf-8') as config:
            json.dump(values, config, indent=4)
