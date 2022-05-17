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
        """Variables de instancia de la clase que se usan para configurar el juego"""
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
        """
        Establecer los valores de las variables de instancia.
        :param datos: el diccionario leido del archivo configuracion.json
        """
        self.__tiempo_u = datos["-TIEMPO_C-"]
        self.__rondas = datos["-RONDAS_C-"]
        self.__correctas = datos["-CORRECTO_C-"]
        self.__incorrectas = datos["-INCORRECTO_C-"]
        self.__nivel = datos["-CARACTERISTICAS_C-"]

    def __get_config(self):
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
        """
        Reescribir el archivo json con la configuracion que el usuario establezca.
        :param values: valores que establezca el usuario en los sg.Combo() con valores a elegir.
        """
        ruta_completa = os.path.join(os.path.realpath('..'), "recursos", "datos", "configuracion.json")
        with open(ruta_completa, 'w', encoding='utf-8') as config:
            json.dump(values, config, indent=4)

    def __layout_opciones(self):
        """
        Con los valores privados de la clase
            __cant_tiempos
            __cant_rondas
            __cant_correcto
            __cant_incorrecto
            __cant_niveles
        se settean los valores que se muestran en los sg.Combo() con los que el usuario puede elegir.
        :return: la configuracion del layout de los botones de la ventana
        """
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
        """
        Establecer las rutas de iconos, cargar los valores del archivo de configuracion.json y el tema del juego.
        :return: la ventana de configuracion con los ultimos valores de configuracion ingresados.
        """
        datos = self.__get_config()
        self.__set_datos(datos)

        ruta_titlebar_icon = os.path.join(os.path.realpath('..'), "recursos", "imagenes", "cartas_icon.png")
        ruta_icon = os.path.join(os.path.realpath('..'), "recursos", "imagenes", "cartas_icon.ico")

        sg.theme('DarkAmber')
        layout = [
            [sg.Text("CONFIGURACIÓN", key="-TITULO-", expand_x=True, font='Arial 45', justification='center')],
            [sg.Text(size=(None, 2), )],
            [sg.Col(self.__layout_opciones(), expand_x=True)],
            [sg.Text(size=(None, 2), )],
            [sg.Push(), sg.Button("Confirmar cambios", key="-CAMBIOS_CONFIG-", font=FONT_COMBO), sg.Push()],
            [sg.Button("volver", key='-VOLVER_CONFIG-', font=FONT_COMBO), sg.Push()]
        ]
        window = sg.Window("Configuracion", layout, size=TAM_VENTANA, finalize=True, use_custom_titlebar=True,
                           titlebar_icon=ruta_titlebar_icon, icon=ruta_icon)
        return window


# para manejar el tiempo
# import time
# tiempo = 10
# for i in range(tiempo):
#     print(i)
#     time.sleep(1)
