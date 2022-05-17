import json
import os
import PySimpleGUI as sg

TAM_VENTANA = (800, 800)
TAM_COLUMNAS = (400, 400)
TAM_COMBO = (20, 50)

FONT_TITULO = 'Verdana 72'
FONT_INDICADOR = 'Verdana 34'
FONT_BOTONES = 'Verdana 30'
FONT_COMBO = 'Verdana 18'


class Configuracion:
    """
    Menu de opciones para la configuracion de las caracteristicas del juego.
    """
    __cant_tiempos = [x for x in range(5, 31) if (x % 5) == 0]  # del 5 al 30, de 5 en 5
    __cant_rondas = [x for x in range(1, 11)]  # del 1 al 10
    __cant_correcto = [x for x in range(1, 21)]  # del 1 al 20
    __cant_incorrecto = [x for x in range(1, 21)]  # del 1 al 20
    __cant_niveles = [1, 2, 3, 4, 5]

    def __int__(self):
        """Variables de la clase que se usan para configurar el juego"""
        self.__tiempo_u = 0
        self.__rondas = 0
        self.__correctas = 0
        self.__incorrectas = 0
        self.__nivel = 0

    # getters de la configuracion
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

    # setters de la configuracion
    def __set_datos(self, datos):
        self.__tiempo_u = datos["-TIEMPO_C-"]
        self.__rondas = datos["-RONDAS_C-"]
        self.__correctas = datos["-CORRECTO_C-"]
        self.__incorrectas = datos["-INCORRECTO_C-"]
        self.__nivel = datos["-CARACTERISTICAS_C-"]

    def __get_config(self):
        ruta_completa = os.path.join(os.path.realpath('..'), "recursos", "datos", "configuracion.json")
        try:
            with open(ruta_completa, 'r', encoding='utf-8') as config:
                datos = json.load(config)
            return datos
        except FileNotFoundError:
            # si ocurre el error de que no encontro el archivo, que lo cree con valores default y lo retorne
            datos_d = {
                "-TIEMPO_C-": self.__cant_tiempos[0],
                "-RONDAS_C-": self.__cant_rondas[0],
                "-CORRECTO_C-": self.__cant_correcto[0],
                "-INCORRECTO_C-": self.__cant_incorrecto[0],
                "-CARACTERISTICAS_C-": self.__cant_niveles[len(self.__cant_niveles) - 1]
            }
            with open(ruta_completa, 'w', encoding='utf-8') as config:
                json.dump(datos_d, config, indent=4)
            return datos_d

    @staticmethod
    def set_config(values):
        ruta_completa = os.path.join(os.path.realpath('..'), "recursos", "datos", "configuracion.json")
        with open(ruta_completa, 'w', encoding='utf-8') as config:
            json.dump(values, config, indent=4)

    def __layout_opciones(self):
        __layout = [
            [sg.Push(),
             sg.Text('Tiempo límite', key='-TIEMPO_T-',
                     expand_x=True, font=FONT_BOTONES, justification='center'),
             sg.Push()],
            [sg.Push(),
             sg.Combo(self.__cant_tiempos, key='-TIEMPO_C-', default_value=self.__tiempo_u,
                      readonly=True, enable_events=True, size=(10, 5), font=FONT_COMBO),
             sg.Push()],

            [sg.Push(),
             sg.Text('Rondas por juego', key='-RONDAS_T-',
                     expand_x=True, font=FONT_BOTONES, justification='center'),
             sg.Push()],
            [sg.Push(),
             sg.Combo(self.__cant_rondas, key='-RONDAS_C-', default_value=self.__rondas,
                      readonly=True, enable_events=True, size=(10, 5), font=FONT_COMBO),
             sg.Push()],

            [sg.Push(),
             sg.Text('Puntaje por respuesta correcta', key='-CORRECTO_T-',
                     expand_x=True, font=FONT_BOTONES, justification='center'),
             sg.Push()],
            [sg.Push(),
             sg.Combo(self.__cant_correcto, key='-CORRECTO_C-', default_value=self.__correctas,
                      readonly=True, enable_events=True, size=(10, 5), font=FONT_COMBO),
             sg.Push()],

            [sg.Push(),
             sg.Text('Puntaje por respuesta incorrecta', key='-INCORRECTO_T-',
                     expand_x=True, font=FONT_BOTONES, justification='center'),
             sg.Push()],
            [sg.Push(),
             sg.Combo(self.__cant_incorrecto, key='-INCORRECTO_C-', default_value=self.__incorrectas,
                      readonly=True, enable_events=True, size=(10, 5), font=FONT_COMBO),
             sg.Push()],

            [sg.Push(),
             sg.Text('Cantidad de características', key='-CARACTERISTICAS_T-',
                     expand_x=True, font=FONT_BOTONES, justification='center'),
             sg.Push()],
            [sg.Push(),
             sg.Combo(self.__cant_niveles, key='-CARACTERISTICAS_C-', default_value=self.__nivel,
                      readonly=True, enable_events=True, size=(10, 5), font=FONT_COMBO),
             sg.Push()]
        ]
        return __layout

    def crear_ventana(self):
        datos = self.__get_config()
        self.__set_datos(datos)
        sg.theme('DarkAmber')
        layout = [
            [sg.Text("CONFIGURACIÓN", key="-TITULO-", expand_x=True, font='Arial 45', justification='center')],
            [sg.Text(size=(None, 2), )],
            [sg.Col(self.__layout_opciones(), expand_x=True)],
            [sg.Text(size=(None, 2), )],
            [sg.Push(), sg.Button("Confirmar cambios", key="-CAMBIOS_CONFIG-", font=FONT_COMBO), sg.Push()],
            [sg.Button("volver", key='-VOLVER_CONFIG-', font=FONT_COMBO), sg.Push()]
        ]
        window = sg.Window("Configuracion", layout, size=TAM_VENTANA, finalize=True, use_custom_titlebar=True)
        return window


# para manejar el tiempo
# import time
# tiempo = 10
# for i in range(tiempo):
#     print(i)
#     time.sleep(1)
