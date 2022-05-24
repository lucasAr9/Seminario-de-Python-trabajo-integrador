import os
import PySimpleGUI as sg

from src.pantallas import caracteristicas_generales as fs
from src.juego import config_dificultad as config


def crear_ventana():
    """
    Menu de opciones para la configuracion de las caracteristicas del juego.

    Establecer las rutas de iconos, cargar los valores del archivo de configuracion.json y el tema del juego.
    :return: la ventana de configuracion con los ultimos valores de configuracion ingresados.
    """
    ruta_titlebar_icon = os.path.join(os.path.realpath('..'), "recursos", "imagenes", "cartas_icon.png")
    ruta_icon = os.path.join(os.path.realpath('..'), "recursos", "imagenes", "cartas_icon.ico")

    crear_layout = [
        [sg.Text("CONFIGURACIÓN", key="-TITULO-", expand_x=True, font='Arial 45', justification='center')],
        [sg.HSep()],
        [sg.Text(size=(None, 2), )],
        [sg.Col(layout, expand_x=True)],
        [sg.Text(size=(None, 2), )],
        [sg.Push(), sg.Button("Confirmar cambios", key="-CAMBIOS_CONFIG-", font=fs.FUENTE_COMBO), sg.Push()],
        [sg.Button("volver", key='-VOLVER_CONFIG-', font=fs.FUENTE_COMBO), sg.Push()]
    ]
    window = sg.Window("Configuracion", crear_layout, size=fs.TAM_VENTANA, finalize=True, use_custom_titlebar=True,
                       titlebar_icon=ruta_titlebar_icon, icon=ruta_icon)
    return window


"""Rango de valores de la pantalla de la configuracion"""
cant_tiempos = [x for x in range(5, 31, 5)]  # del 5 al 30, de 5 en 5
cant_rondas = [x for x in range(1, 11)]  # del 1 al 10
cant_correcto = [x for x in range(1, 21)]  # del 1 al 20
cant_incorrecto = [x for x in range(1, 21)]  # del 1 al 20
cant_niveles = [1, 2, 3, 4, 5]  # del 1 al 5

"""Crear el objeto config_dificultas para leer los datos del archivo json con los valores de la dificultad"""
dificultad = config.Configuracion()
datos = dificultad.get_config()
dificultad.set_datos(datos)

"""tema de las ventanas"""
sg.theme(fs.TEMA)

"""
Con los valores privados de la clase
    cant_tiempos
    cant_rondas
    cant_correcto
    cant_incorrecto
    cant_niveles
se settean los valores que se muestran en los sg.Combo() con los que el usuario puede elegir.
"""
layout = [
    [sg.Push(),
     sg.Text('Tiempo límite', key='-TIEMPO_T-',
             expand_x=True, font=fs.FUENTE_BOTONES, justification='center'),
     sg.Push()],
    [sg.Push(),
     sg.Combo(cant_tiempos, key='-TIEMPO_C-', default_value=dificultad.tiempo,
              readonly=True, enable_events=True, size=(10, 5), font=fs.FUENTE_COMBO),
     sg.Push()],

    [sg.Push(),
     sg.Text('Rondas por juego', key='-RONDAS_T-',
             expand_x=True, font=fs.FUENTE_BOTONES, justification='center'),
     sg.Push()],
    [sg.Push(),
     sg.Combo(cant_rondas, key='-RONDAS_C-', default_value=dificultad.rondas,
              readonly=True, enable_events=True, size=(10, 5), font=fs.FUENTE_COMBO),
     sg.Push()],

    [sg.Push(),
     sg.Text('Puntaje por respuesta correcta', key='-CORRECTO_T-',
             expand_x=True, font=fs.FUENTE_BOTONES, justification='center'),
     sg.Push()],
    [sg.Push(),
     sg.Combo(cant_correcto, key='-CORRECTO_C-', default_value=dificultad.correctas,
              readonly=True, enable_events=True, size=(10, 5), font=fs.FUENTE_COMBO),
     sg.Push()],

    [sg.Push(),
     sg.Text('Puntaje por respuesta incorrecta', key='-INCORRECTO_T-',
             expand_x=True, font=fs.FUENTE_BOTONES, justification='center'),
     sg.Push()],
    [sg.Push(),
     sg.Combo(cant_incorrecto, key='-INCORRECTO_C-', default_value=dificultad.incorrectas,
              readonly=True, enable_events=True, size=(10, 5), font=fs.FUENTE_COMBO),
     sg.Push()],

    [sg.Push(),
     sg.Text('Cantidad de características', key='-CARACTERISTICAS_T-',
             expand_x=True, font=fs.FUENTE_BOTONES, justification='center'),
     sg.Push()],
    [sg.Push(),
     sg.Combo(cant_niveles, key='-CARACTERISTICAS_C-', default_value=dificultad.nivel,
              readonly=True, enable_events=True, size=(10, 5), font=fs.FUENTE_COMBO),
     sg.Push()]]
