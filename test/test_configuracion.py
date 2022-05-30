import PySimpleGUI as sg

from src.pantallas import configuracion as c_pantalla
from src.juego import dificultad as dificultad


def nivel(window_dificultad, elegido):
    window_otra = c_pantalla.nivel_elegida(elegido)
    window_dificultad.hide()
    event, values = window_otra.read()
    if event == '-VOLVER_VALORES-':
        window_otra.close()
    window_dificultad.un_hide()


window_dificultad = c_pantalla.crear_ventana()
while True:
    event, values = window_dificultad.read()
    if event in (sg.WIN_CLOSED, '-VOLVER_CONFIG-'):
        break
    if event == '-FACIL-':
        nivel(window_dificultad, '-FACIL-')
    elif event == '-NORMAL-':
        nivel(window_dificultad, '-NORMAL-')
    elif event == '-DIFICIL-':
        nivel(window_dificultad, '-DIFICIL-')

    elif event == '-PERSONALIZADO-':
        window_otra = c_pantalla.dificultad_personalizada()
        window_dificultad.hide()
        while True:
            event, values2 = window_otra.read()
            if event in (sg.WIN_CLOSED, '-VOLVER_PERSONALIZADO-'):
                break
            if event == '-CAMBIOS_CONFIRMADOS-':
                dificultad.guardar_nivel_personalizado(values2)
        if event == '-VOLVER_PERSONALIZADO-':
            window_otra.close()
        window_dificultad.un_hide()
window_dificultad.close()
