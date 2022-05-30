import PySimpleGUI as sg

from src.pantallas import configuracion as c_pantalla
from src.juego import dificultad as dificultad


window_dificultad = c_pantalla.crear_ventana()
while True:
    event, values = window_dificultad.read()
    if event in (sg.WIN_CLOSED, '-VOLVER_CONFIG-'):
        break
    if event == '-FACIL-':
        window_otra = c_pantalla.dificultad_elegida('-FACIL-')
        window_dificultad.un_hide()
        event, values = window_otra.read()
        if event == '-VOLVER_VALORES-':
            window_otra.close()
        window_dificultad.un_hide()
    elif event == '-NORMAL-':
        window_otra = c_pantalla.dificultad_elegida('-NORMAL-')
        window_dificultad.un_hide()
        event, values = window_otra.read()
        if event == '-VOLVER_VALORES-':
            window_otra.close()
        window_dificultad.un_hide()
    elif event == '-DIFICIL-':
        window_otra = c_pantalla.dificultad_elegida('-DIFICIL-')
        window_dificultad.un_hide()
        event, values = window_otra.read()
        if event == '-VOLVER_VALORES-':
            window_otra.close()
        window_dificultad.un_hide()
    elif event == '-PERSONALIZADO-':
        window_otra = c_pantalla.dificultad_personalizada()
        window_dificultad.un_hide()
        event, values2 = window_otra.read()
        while True:
            if event in (sg.WIN_CLOSED, '-VOLVER_PERSONALIZADO-'):
                break
            if event == '-CAMBIOS_CONFIRMADOS-':
                dificultad.guardar_nivel_personalizado(values2)
        if event == '-VOLVER_PERSONALIZADO-':
            window_otra.close()
        window_dificultad.un_hide()
window_dificultad.close()
