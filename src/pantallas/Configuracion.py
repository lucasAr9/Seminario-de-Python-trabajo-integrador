import json
import os
import PySimpleGUI as sg

TAM_VENTANA = (1200, 800)
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
    __tiempos = [x for x in range(5, 31) if (x % 5) == 0]  # del 5 al 30, de 5 en 5
    __rondas = [x for x in range(1, 11)]  # del 1 al 10
    __correcto = [x for x in range(1, 21)]  # del 1 al 20
    __incorrecto = [x for x in range(1, 21)]  # del 1 al 20
    __nivel = [1, 2, 3, 4, 5]

    __titulo = [sg.Push(),
                sg.Text("CONFIGURACIÓN", expand_x=True, font=FONT_TITULO),
                sg.Push()]

    __volver = [sg.Button("volver", key='-VOLVER-', font=FONT_BOTONES), sg.Push()]

    tiempo_u = 0
    rondas = 0
    correctas = 0
    incorrectas = 0
    nivel = 0

    def __layout_opciones(self):
        __layout = [
            [sg.Push(),
             sg.Text('Tiempo límite', key='-TIEMPO_T-',
                     expand_x=True, font=FONT_INDICADOR),
             sg.Push(),
             sg.Combo(self.__tiempos, key='-TIEMPO_C-', default_value=self.tiempo_u,
                      enable_events=True, expand_x=True, font=FONT_COMBO),
             sg.Push()],

            [sg.Push(),
             sg.Text('Rondas por juego', key='-RONDAS_T-',
                     expand_x=True, font=FONT_INDICADOR),
             sg.Push(),
             sg.Combo(self.__rondas, key='-RONDAS_C-', default_value=self.rondas,
                      enable_events=True, expand_x=True, font=FONT_COMBO),
             sg.Push()],

            [sg.Push(),
             sg.Text('Puntaje por respuesta correcta', key='-CORRECTO_T-',
                     expand_x=True, font=FONT_INDICADOR),
             sg.Push(),
             sg.Combo(self.__correcto, key='-CORRECTO_C-', default_value=self.correctas,
                      enable_events=True, expand_x=True, font=FONT_COMBO),
             sg.Push()],

            [sg.Push(),
             sg.Text('Puntaje por respuesta incorrecta', key='-INCORRECTO_T-',
                     expand_x=True, font=FONT_INDICADOR),
             sg.Push(),
             sg.Combo(self.__incorrecto, key='-INCORRECTO_C-', default_value=self.incorrectas,
                      enable_events=True, expand_x=True, font=FONT_COMBO),
             sg.Push()],

            [sg.Push(),
             sg.Text('Cantidad de características', key='-CARACTERISTICAS_T-',
                     expand_x=True, font=FONT_INDICADOR),
             sg.Push(),
             sg.Combo(self.__nivel, key='-CARACTERISTICAS_C-', default_value=self.nivel,
                      enable_events=True, expand_x=True, font=FONT_COMBO),
             sg.Push()]
        ]
        return __layout

    def __set_datos(self, datos):
        self.tiempo_u = datos["tiempo"]
        self.rondas = datos["rondas"]
        self.correctas = datos["correcto"]
        self.incorrectas = datos["incorrecto"]
        self.nivel = datos["nivel"]

    def __get_config(self):
        ruta_completa = os.path.join(os.path.realpath('..'), "recursos", "datos", "configuracion.json")
        try:
            with open(ruta_completa, 'r', encoding='utf-8') as config:
                datos = json.load(config)
        except FileNotFoundError:
            # si ocurre el error de que no encontro el archivo, que lo cree con valores default y lo retorne
            datos_d = {
                "tiempo": self.__tiempos[0],
                "rondas": self.__rondas[0],
                "correcto": self.__correcto[0],
                "incorrecto": self.__incorrecto[0],
                "nivel": self.__nivel[len(self.__nivel)]
            }
            with open(ruta_completa, 'w', encoding='utf-8') as config:
                json.dump(datos_d, config, indent=4)
        return datos

    def __set_config(self):
        pass

    def crear_ventana(self):
        datos = self.__get_config()
        self.__set_datos(datos)
        layout = [
            [self.__titulo],
            [sg.Col(self.__layout_opciones(), expand_x=True)],
            [self.__volver]
        ]
        window = sg.Window(
            "Configuracion", layout, size=TAM_VENTANA, finalize=True, use_custom_titlebar=True
        )
        return window


# para manejar el tiempo
# import time
# tiempo = 10
# for i in range(tiempo):
#     print(i)
#     time.sleep(1)
