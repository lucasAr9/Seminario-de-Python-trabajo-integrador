import os
import PySimpleGUI as sg

from src.pantallas import caracteristicas_generales as cg
from src.funcionalidad import dificultad as dificultad
from rutas import IMAGENES_DIR

"""Ruta de las imagenes de la ventana de configuracion"""
ruta_titlebar_icon = os.path.join(IMAGENES_DIR, "cartas_icon.png")
ruta_icon = os.path.join(IMAGENES_DIR, "cartas_icon.ico")

"""tema de las ventanas"""
sg.theme(cg.TEMA)


def layout_configuracion_texto():
    """:return: layout del texto."""
    layout = [
        [sg.Push(),
         sg.Text('CARACTERÍSTICAS', key='-DIFICULTAD_T-',
                 expand_x=True, font='Arial 20', justification='center'),
         sg.Push()],

        [sg.Push(),
         sg.Text('Tiempo límite: ', key='-TIEMPO_T-',
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()],

        [sg.Push(),
         sg.Text('Rondas por funcionalidad: ', key='-RONDAS_T-',
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()],

        [sg.Push(),
         sg.Text('Puntaje por respuesta correcta: ', key='-CORRECTO_T-',
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()],

        [sg.Push(),
         sg.Text('Puntaje por respuesta incorrecta: ', key='-INCORRECTO_T-',
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()],

        [sg.Push(),
         sg.Text('Cantidad de características: ', key='-CARACTERISTICAS_T-',
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()]]
    return layout


def layout_configuracion_nivel(nivel, nombre_nivel):
    """:return: layout con los numeros de cada nivel."""
    layout = [
        [sg.Push(),
         sg.Text(nombre_nivel, key='-DIFICULTAD_T-',
                 expand_x=True, font='Arial 20', justification='center'),
         sg.Push()],

        [sg.Push(),
         sg.Text(str(nivel['-TIEMPO_C-']), key='-TIEMPO_T-',
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()],

        [sg.Push(),
         sg.Text(str(nivel['-RONDAS_C-']), key='-RONDAS_T-',
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()],

        [sg.Push(),
         sg.Text(str(nivel['-CORRECTO_C-']), key='-CORRECTO_T-',
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()],

        [sg.Push(),
         sg.Text(str(nivel['-INCORRECTO_C-']), key='-INCORRECTO_T-',
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()],

        [sg.Push(),
         sg.Text(str(nivel['-CARACTERISTICAS_C-']), key='-CARACTERISTICAS_T-',
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()]]
    return layout


def layour_config_personalizado(nivel):
    """:return: layout con los combos para elegir distintos valores."""
    layout = [
        [sg.Push(),
         sg.Text('PERSONALIZADO', key='-DIFICULTAD_T-',
                 expand_x=True, font='Arial 20', justification='center'),
         sg.Push()],

        [sg.Push(),
         sg.Combo(dificultad.CANT_TIEMPOS, key='-TIEMPO_C-', default_value=nivel['-TIEMPO_C-'],
                  readonly=True, enable_events=True, size=(10, 5), font=cg.FUENTE_BOTONES),
         sg.Push()],

        [sg.Push(),
         sg.Combo(dificultad.CANT_RONDAS, key='-RONDAS_C-', default_value=nivel['-RONDAS_C-'],
                  readonly=True, enable_events=True, size=(10, 5), font=cg.FUENTE_BOTONES),
         sg.Push()],

        [sg.Push(),
         sg.Combo(dificultad.CANT_CORRECTO, key='-CORRECTO_C-', default_value=nivel['-CORRECTO_C-'],
                  readonly=True, enable_events=True, size=(10, 5), font=cg.FUENTE_BOTONES),
         sg.Push()],

        [sg.Push(),
         sg.Combo(dificultad.CANT_INCORRECTO, key='-INCORRECTO_C-', default_value=nivel['-INCORRECTO_C-'],
                  readonly=True, enable_events=True, size=(10, 5), font=cg.FUENTE_BOTONES),
         sg.Push()],

        [sg.Push(),
         sg.Combo(dificultad.CANT_NIVELES, key='-CARACTERISTICAS_C-', default_value=nivel['-CARACTERISTICAS_C-'],
                  readonly=True, enable_events=True, size=(10, 5), font=cg.FUENTE_BOTONES),
         sg.Push()]]
    return layout


def crear_ventana():
    """
    Crea la ventana de configuracion.
    :return: ventana de configuracion.
    """
    datos = dificultad.leer_archivo_json()
    layout_text = layout_configuracion_texto()
    layout_facil = layout_configuracion_nivel(datos['-FACIL-'], 'FÁCIL')
    layout_normal = layout_configuracion_nivel(datos['-NORMAL-'], 'NORMAL')
    layout_dificil = layout_configuracion_nivel(datos['-DIFICIL-'], 'DIFÍCIL')
    layout_personalizado = layour_config_personalizado(datos['-PERSONALIZADO-'])
    crear_layout = [
        [sg.Image(ruta_titlebar_icon, pad=((60, 0), (20, 20))),
         sg.Text("CONFIGURACIÓN", key="-TITULO-", expand_x=True, font='Arial 40', justification='center'),
         sg.Image(ruta_titlebar_icon, pad=((0, 60), (20, 20)))],
        [sg.HSep()],

        [sg.Text(size=(None, 1), )],
        [sg.Push(),
         sg.Col(layout_text, expand_x=True),
         sg.Col(layout_facil, expand_x=True),
         sg.Col(layout_normal, expand_x=True),
         sg.Col(layout_dificil, expand_x=True),
         sg.Col(layout_personalizado, expand_x=True),
         sg.Push()],

        [sg.VPush()],
        [sg.Push(), sg.Button("Confirmar cambios", key="-CONFIRMAR_CAMBIOS-", font=cg.FUENTE_COMBO), sg.Push()],
        [sg.Text(size=(None, 1), )],
        [sg.Button("Volver", key='-VOLVER_CONFIG-', font=cg.FUENTE_COMBO), sg.Push()]
    ]
    window = sg.Window("Configuracion", crear_layout, size=cg.TAM_VENTANA, finalize=True,
                       use_custom_titlebar=True, titlebar_icon=ruta_titlebar_icon, icon=ruta_icon)
    return window
