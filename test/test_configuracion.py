import PySimpleGUI as sg
from src.pantallas.Configuracion import Configuracion

menu_config = Configuracion()
window = menu_config.crear_ventana()

while True:
    current_window, event, value = sg.read_all_windows()

    if event == sg.WIN_CLOSED:
        current_window.close()
        break
    elif event == '-VOLVER_CONFIG-':
        current_window.close()
        break
    elif event == '-CAMBIOS_CONFIG-':
        menu_config.set_config(value)
