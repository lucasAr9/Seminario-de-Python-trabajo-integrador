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


def layout_configuracion():
    """:return: layout de la ventana de configuracion"""
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
         sg.Button("Personalizado", key="-PERSONALIZADO-", size=(12, 1), font=cg.FUENTE_BOTONES),
         sg.Push()]]
    return layout


def crear_ventana():
    """
    Menu de opciones para la configuracion de las caracteristicas del funcionalidad.
    :return: la ventana de configuracion con los niveles de dificultad que se pueden elegir.
    """
    layout = layout_configuracion()
    crear_layout = [
        [sg.Image(ruta_titlebar_icon, pad=((60, 0), (20, 20))),
         sg.Text("CONFIGURACIÓN", key="-TITULO-", expand_x=True, font='Arial 45', justification='center'),
         sg.Image(ruta_titlebar_icon, pad=((0, 60), (20, 20)))],
        [sg.HSep()],

        [sg.Text(size=(None, 1), )],
        [sg.Col(layout, expand_x=True)],

        [sg.Push(), sg.Text('Vea las características de los niveles',
         expand_x=True, font=cg.FUENTE_COMBO, justification='center'), sg.Push()],
        [sg.Push(), sg.Text('o personalice su dificultad.',
         expand_x=True, font=cg.FUENTE_COMBO, justification='center'), sg.Push()],

        [sg.VPush()],
        [sg.Button("Volver", key='-VOLVER_CONFIG-', font=cg.FUENTE_COMBO), sg.Push()]
    ]
    window = sg.Window("Configuracion", crear_layout, size=cg.TAM_VENTANA, finalize=True,
                       use_custom_titlebar=True, titlebar_icon=ruta_titlebar_icon, icon=ruta_icon)
    return window


def layout_nivel(nivel):
    """
    Con los valores de las variables CANT_TIEMPOS, CANT_RONDAS, CANT_CORRECTO, CANT_INCORRECTO, CANT_NIVELES,
    se settean los valores que se muestran en los sg.Combo() con los que el usuario puede elegir.
    Y por defecto muestra el ultimo valores seleccionado por el usuario.
    """
    datos = dificultad.leer_archivo_json()
    layout = [
        [sg.Push(),
         sg.Text(nivel, key='-DIFICULTAD_T-',  # aca va una variable que cambia segun el nivel
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()],

        [sg.Push(),
         sg.Text('Tiempo límite: ' + str(datos[nivel]['-TIEMPO_C-']), key='-TIEMPO_T-',
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()],

        [sg.Push(),
         sg.Text('Rondas por funcionalidad: ' + str(datos[nivel]['-RONDAS_C-']), key='-RONDAS_T-',
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()],

        [sg.Push(),
         sg.Text('Puntaje por respuesta correcta: ' + str(datos[nivel]['-CORRECTO_C-']), key='-CORRECTO_T-',
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()],

        [sg.Push(),
         sg.Text('Puntaje por respuesta incorrecta: ' + str(datos[nivel]['-INCORRECTO_C-']), key='-INCORRECTO_T-',
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()],

        [sg.Push(),
         sg.Text('Cantidad de características: ' + str(datos[nivel]['-CARACTERISTICAS_C-']), key='-CARACTERISTICAS_T-',
                 expand_x=True, font=cg.FUENTE_BOTONES, justification='center'),
         sg.Push()]]
    return layout


def nivel_elegida(nivel):
    """
    Con los valores de las variables de cada nivel predefinidos muestra los valores
    que el usuario puede elegir.
    """
    layout = layout_nivel(nivel)
    crear_layout = [
        [sg.Text(size=(None, 2), )],
        [sg.Col(layout, expand_x=True)],
        [sg.Text(size=(None, 2), )],

        [sg.VPush()],
        [sg.Button("volver", key='-VOLVER_VALORES-', font=cg.FUENTE_COMBO), sg.Push()]
    ]
    window = sg.Window("Configuracion", crear_layout, size=cg.TAM_VENTANA, finalize=True,
                       use_custom_titlebar=True, titlebar_icon=ruta_titlebar_icon, icon=ruta_icon)
    return window


def layout_personalizado(nivel):
    """
    :return: layout de la ventana de configuracion personalizada.
    """
    datos = dificultad.leer_archivo_json()
    layout = [
        [sg.Push(),
         sg.Text('-PERSONALIZADO-', key='-DIFICULTAD_T-',
                 expand_x=True, font='Arial 27', justification='center'),
         sg.Push()],

        [sg.Push(),
         sg.Text('Tiempo límite', key='-TIEMPO_T-',
                 expand_x=True, font='Arial 20', justification='center'),
         sg.Push()],
        [sg.Push(),
         sg.Combo(dificultad.CANT_TIEMPOS, key='-TIEMPO_C-', default_value=datos[nivel]['-TIEMPO_C-'],
                  readonly=True, enable_events=True, size=(10, 5), font=cg.FUENTE_COMBO),
         sg.Push()],

        [sg.Push(),
         sg.Text('Rondas por funcionalidad', key='-RONDAS_T-',
                 expand_x=True, font='Arial 20', justification='center'),
         sg.Push()],
        [sg.Push(),
         sg.Combo(dificultad.CANT_RONDAS, key='-RONDAS_C-', default_value=datos[nivel]['-RONDAS_C-'],
                  readonly=True, enable_events=True, size=(10, 5), font=cg.FUENTE_COMBO),
         sg.Push()],

        [sg.Push(),
         sg.Text('Puntaje por respuesta correcta', key='-CORRECTO_T-',
                 expand_x=True, font='Arial 20', justification='center'),
         sg.Push()],
        [sg.Push(),
         sg.Combo(dificultad.CANT_CORRECTO, key='-CORRECTO_C-', default_value=datos[nivel]['-CORRECTO_C-'],
                  readonly=True, enable_events=True, size=(10, 5), font=cg.FUENTE_COMBO),
         sg.Push()],

        [sg.Push(),
         sg.Text('Puntaje por respuesta incorrecta', key='-INCORRECTO_T-',
                 expand_x=True, font='Arial 20', justification='center'),
         sg.Push()],
        [sg.Push(),
         sg.Combo(dificultad.CANT_INCORRECTO, key='-INCORRECTO_C-', default_value=datos[nivel]['-INCORRECTO_C-'],
                  readonly=True, enable_events=True, size=(10, 5), font=cg.FUENTE_COMBO),
         sg.Push()],

        [sg.Push(),
         sg.Text('Cantidad de características', key='-CARACTERISTICAS_T-',
                 expand_x=True, font='Arial 20', justification='center'),
         sg.Push()],
        [sg.Push(),
         sg.Combo(dificultad.CANT_NIVELES, key='-CARACTERISTICAS_C-', default_value=datos[nivel]['-CARACTERISTICAS_C-'],
                  readonly=True, enable_events=True, size=(10, 5), font=cg.FUENTE_COMBO),
         sg.Push()]]
    return layout


def dificultad_personalizada():
    """
    Con los valores de las variables CANT_TIEMPOS, CANT_RONDAS, CANT_CORRECTO, CANT_INCORRECTO, CANT_NIVELES,
    se settean los valores que se muestran en los sg.Combo() con los que el usuario puede elegir.
    Y por defecto muestra el ultimo valores seleccionado por el usuario.
    """
    layout = layout_personalizado('-PERSONALIZADO-')
    crear_layout = [
        [sg.Text(size=(None, 2), )],
        [sg.Col(layout, expand_x=True)],
        [sg.Text(size=(None, 2), )],

        [sg.VPush()],
        [sg.Push(), sg.Button("Confirmar cambios", key="-CAMBIOS_CONFIRMADOS-", font=cg.FUENTE_COMBO), sg.Push()],

        [sg.Text(size=(None, 2), )],
        [sg.Button("volver", key='-VOLVER_PERSONALIZADO-', font=cg.FUENTE_COMBO), sg.Push()]
    ]
    window = sg.Window("Configuracion", crear_layout, size=cg.TAM_VENTANA, finalize=True,
                       use_custom_titlebar=True, titlebar_icon=ruta_titlebar_icon, icon=ruta_icon)
    return window
