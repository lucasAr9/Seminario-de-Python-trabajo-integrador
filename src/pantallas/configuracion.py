import os
import PySimpleGUI as sg

from src.pantallas import caracteristicas_generales as cg
from src.juego import dificultad as configuracion

"""Ruta de las imagenes de la ventana de configuracion"""
ruta_titlebar_icon = os.path.join(os.path.realpath(''), "recursos", "imagenes", "cartas_icon.png")
ruta_icon = os.path.join(os.path.realpath(''), "recursos", "imagenes", "cartas_icon.ico")

"""
Crear el objeto Dificultad para leer los datos del archivo json con los valores
de la dificultad y el ultimo nivel de dificultad seleccionado por el usuario.
"""
configuracion.cargar_configuracion()
dificultad = configuracion.Dificultad()

"""tema de las ventanas"""
sg.theme(cg.TEMA)


def layout_dificultad():
    """Layout de la ventana de configuracion"""
    layout = [
        [sg.Push(),
         sg.Button("Fácil", key="-FACIL-", size=(12, 1), font=cg.FUENTE_BOTONES),
         sg.Push()],

        [sg.Push(),
         sg.Button("Normal", key="-NORMAL-", size=(12, 1), font=cg.FUENTE_BOTONES),
         sg.Push()],

        [sg.Push(),
         sg.Button("Difícil", key="-DIFICIL-", size=(12, 1), font=cg.FUENTE_BOTONES),
         sg.Push()],

        [sg.Push(),
         sg.Button("Personalizado", key="-CUSTOM-", size=(12, 1), font=cg.FUENTE_BOTONES),
         sg.Push()]]
    return layout


def layout_personalizado():
    """
    Con los valores de las variables cant_tiempos, cant_rondas, cant_correcto, cant_incorrecto, cant_niveles,
    se settean los valores que se muestran en los sg.Combo() con los que el usuario puede elegir.
    Y por defecto muestra el ultimo valores seleccionado por el usuario.
    """
    layout = [
        [sg.Push(),
         sg.Text('PERSONALIZADO', key='-DIFICULTAD_T-',
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()],

        [sg.Push(),
         sg.Text('Tiempo límite', key='-TIEMPO_T-',
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()],
        [sg.Push(),
         sg.Combo(configuracion.cant_tiempos, key='-TIEMPO_C-', default_value=dificultad.tiempo,
                  readonly=True, enable_events=True, size=(10, 5), font=cg.FUENTE_COMBO),
         sg.Push()],

        [sg.Push(),
         sg.Text('Rondas por juego', key='-RONDAS_T-',
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()],
        [sg.Push(),
         sg.Combo(configuracion.cant_rondas, key='-RONDAS_C-', default_value=dificultad.rondas,
                  readonly=True, enable_events=True, size=(10, 5), font=cg.FUENTE_COMBO),
         sg.Push()],

        [sg.Push(),
         sg.Text('Puntaje por respuesta correcta', key='-CORRECTO_T-',
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()],
        [sg.Push(),
         sg.Combo(configuracion.cant_correcto, key='-CORRECTO_C-', default_value=dificultad.correctas,
                  readonly=True, enable_events=True, size=(10, 5), font=cg.FUENTE_COMBO),
         sg.Push()],

        [sg.Push(),
         sg.Text('Puntaje por respuesta incorrecta', key='-INCORRECTO_T-',
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()],
        [sg.Push(),
         sg.Combo(configuracion.cant_incorrecto, key='-INCORRECTO_C-', default_value=dificultad.incorrectas,
                  readonly=True, enable_events=True, size=(10, 5), font=cg.FUENTE_COMBO),
         sg.Push()],

        [sg.Push(),
         sg.Text('Cantidad de características', key='-CARACTERISTICAS_T-',
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()],
        [sg.Push(),
         sg.Combo(configuracion.cant_niveles, key='-CARACTERISTICAS_C-', default_value=dificultad.nivel,
                  readonly=True, enable_events=True, size=(10, 5), font=cg.FUENTE_COMBO),
         sg.Push()]]
    return layout


def crear_ventana():
    """
    Menu de opciones para la configuracion de las caracteristicas del juego.
    :return: la ventana de configuracion con los niveles de dificultad para poder elegir.
    """
    layout = layout_dificultad()
    crear_layout = [
        [sg.Text("CONFIGURACIÓN", key="-TITULO-", expand_x=True, font='Arial 45', justification='center')],
        [sg.HSep()],

        [sg.Text(size=(None, 2), )],
        [sg.Col(layout, expand_x=True)],
        [sg.Text(size=(None, 2), )],

        [sg.Push(),
         sg.Text('Elija una dificultad o personalice su dificultád', key='-TEXTO-',
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()],

        [sg.VPush()],
        [sg.Button("volver", key='-VOLVER_CONFIG-', font=cg.FUENTE_COMBO), sg.Push()]
    ]
    window = sg.Window("Configuracion", crear_layout, size=cg.TAM_VENTANA, finalize=True,
                       use_custom_titlebar=True, titlebar_icon=ruta_titlebar_icon, icon=ruta_icon)
    return window


def dificultad_elegida():
    """
    Menu de opciones para la configuracion de las caracteristicas del juego.
    :return: la ventana de configuracion personalizada.
    """
    layout = layout_personalizado()
    crear_layout = [
        [sg.Text("CONFIGURACIÓN", key="-TITULO-", expand_x=True, font='Arial 45', justification='center')],
        [sg.HSep()],

        [sg.Text(size=(None, 2), )],
        [sg.Col(layout, expand_x=True)],
        [sg.Text(size=(None, 2), )],

        [sg.VPush()],
        [sg.Push(), sg.Button("Confirmar cambios", key="-CAMBIOS_CONFIG-", font=cg.FUENTE_COMBO), sg.Push()],

        [sg.Text(size=(None, 2), )],
        [sg.Button("volver", key='-VOLVER_CUSTOM-', font=cg.FUENTE_COMBO), sg.Push()]
    ]
    window = sg.Window("Configuracion", crear_layout, size=cg.TAM_VENTANA, finalize=True,
                       use_custom_titlebar=True, titlebar_icon=ruta_titlebar_icon, icon=ruta_icon)
    return window
