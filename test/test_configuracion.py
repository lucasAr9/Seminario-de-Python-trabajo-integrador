import PySimpleGUI as sg

from src.pantallas import configuracion as c_pantalla
from src.juego import config_dificultad as config


c_pantalla.crear_ventana()
dificultad = config.Configuracion()

while True:
    current_window, event, value = sg.read_all_windows()

    if event == sg.WIN_CLOSED:
        current_window.close()
        break
    elif event == '-VOLVER_CONFIG-':
        current_window.close()
        break
    elif event == '-CAMBIOS_CONFIG-':
        dificultad.set_config(value)
