import os
import PySimpleGUI as sg

from src.pantallas import caracteristicas_generales as cg
from src.juego import dificultad as dificultad
from rutas import IMAGENES_DIR

"""Ruta de las imagenes de la ventana de configuracion"""
ruta_titlebar_icon = os.path.join(IMAGENES_DIR, "cartas_icon.png")
ruta_icon = os.path.join(IMAGENES_DIR, "cartas_icon.ico")

"""tema de las ventanas"""
sg.theme(cg.TEMA)

"""
Crear el objeto Dificultad para leer los datos del archivo json con los valores
de la dificultad y el ultimo nivel de dificultad seleccionado por el usuario.
"""
dificultad.cargar_configuracion('-FACIL-')
config = dificultad.Dificultad()


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
    Menu de opciones para la configuracion de las caracteristicas del juego.
    :return: la ventana de configuracion con los niveles de dificultad que se pueden elegir.
    """
    layout = layout_configuracion()
    crear_layout = [
        [sg.Image(ruta_titlebar_icon, pad=((20, 0), (20, 0))),
         sg.Text("CONFIGURACIÓN", key="-TITULO-", expand_x=True, font='Arial 45', justification='center'),
         sg.Image(ruta_titlebar_icon, pad=((0, 20), (20, 0)))],
        [sg.HSep()],

        [sg.Text(size=(None, 2), )],
        [sg.Col(layout, expand_x=True)],
        [sg.Text(size=(None, 2), )],

        [sg.Push(), sg.Text('Ver las caracteristicas de los niveles',
         expand_x=True, font=cg.FUENTE_BOTONES, justification='center'), sg.Push()],
        [sg.Push(), sg.Text('o personalice su dificultád.',
         expand_x=True, font=cg.FUENTE_BOTONES, justification='center'), sg.Push()],

        [sg.VPush()],
        [sg.Button("volver", key='-VOLVER_CONFIG-', font=cg.FUENTE_COMBO), sg.Push()]
    ]
    window = sg.Window("Configuracion", crear_layout, size=cg.TAM_VENTANA, finalize=True,
                       use_custom_titlebar=True, titlebar_icon=ruta_titlebar_icon, icon=ruta_icon)
    return window


def layout_nivel(nivel):
    """
    Con los valores de las variables cant_tiempos, cant_rondas, cant_correcto, cant_incorrecto, cant_niveles,
    se settean los valores que se muestran en los sg.Combo() con los que el usuario puede elegir.
    Y por defecto muestra el ultimo valores seleccionado por el usuario.
    """
    datos = dificultad.leer_configuracion()
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
         sg.Text('Rondas por juego: ' + str(datos[nivel]['-RONDAS_C-']), key='-RONDAS_T-',
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


def dificultad_elegida(nivel):
    """
    Con los valores de las variables de cada nivel predefinidos muestra los valores
    que el usuario puede elegir.
    """
    nivel_elegido = nivel
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


def layout_personalizado():
    """
    :return: layout de la ventana de configuracion personalizada.
    """
    layout = [
        [sg.Push(),
         sg.Text('PERSONALIZADO', key='-DIFICULTAD_T-',
                 expand_x=True, font='Arial 27', justification='center'),
         sg.Push()],

        [sg.Push(),
         sg.Text('Tiempo límite', key='-TIEMPO_T-',
                 expand_x=True, font='Arial 20', justification='center'),
         sg.Push()],
        [sg.Push(),
         sg.Combo(dificultad.cant_tiempos, key='-TIEMPO_C-', default_value=config.tiempo,
                  readonly=True, enable_events=True, size=(10, 5), font=cg.FUENTE_COMBO),
         sg.Push()],

        [sg.Push(),
         sg.Text('Rondas por juego', key='-RONDAS_T-',
                 expand_x=True, font='Arial 20', justification='center'),
         sg.Push()],
        [sg.Push(),
         sg.Combo(dificultad.cant_rondas, key='-RONDAS_C-', default_value=config.rondas,
                  readonly=True, enable_events=True, size=(10, 5), font=cg.FUENTE_COMBO),
         sg.Push()],

        [sg.Push(),
         sg.Text('Puntaje por respuesta correcta', key='-CORRECTO_T-',
                 expand_x=True, font='Arial 20', justification='center'),
         sg.Push()],
        [sg.Push(),
         sg.Combo(dificultad.cant_correcto, key='-CORRECTO_C-', default_value=config.correctas,
                  readonly=True, enable_events=True, size=(10, 5), font=cg.FUENTE_COMBO),
         sg.Push()],

        [sg.Push(),
         sg.Text('Puntaje por respuesta incorrecta', key='-INCORRECTO_T-',
                 expand_x=True, font='Arial 20', justification='center'),
         sg.Push()],
        [sg.Push(),
         sg.Combo(dificultad.cant_incorrecto, key='-INCORRECTO_C-', default_value=config.incorrectas,
                  readonly=True, enable_events=True, size=(10, 5), font=cg.FUENTE_COMBO),
         sg.Push()],

        [sg.Push(),
         sg.Text('Cantidad de características', key='-CARACTERISTICAS_T-',
                 expand_x=True, font='Arial 20', justification='center'),
         sg.Push()],
        [sg.Push(),
         sg.Combo(dificultad.cant_niveles, key='-CARACTERISTICAS_C-', default_value=config.nivel,
                  readonly=True, enable_events=True, size=(10, 5), font=cg.FUENTE_COMBO),
         sg.Push()]]
    return layout


def dificultad_personalizada():
    """
    Con los valores de las variables cant_tiempos, cant_rondas, cant_correcto, cant_incorrecto, cant_niveles,
    se settean los valores que se muestran en los sg.Combo() con los que el usuario puede elegir.
    Y por defecto muestra el ultimo valores seleccionado por el usuario.
    """
    layout = layout_personalizado()
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
