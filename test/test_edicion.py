import PySimpleGUI as sg
import sys
import os
sys.path.append(str(os.path.join(os.path.realpath('..'), "src", "pantallas")))
import Cuentas as ed

edit_cuenta = ed.EdicionPerfiles()
pant_conf = {"tam_ventana": (600, 500), "font_botones": "Verdana 15"}

window = edit_cuenta.crear_pantalla(pant_conf)
perf = []
while True:
    current_window, event, values = sg.read_all_windows()
    perf = edit_cuenta.analisis_event_editar(current_window,event,values, perf)

    if event == sg.WINDOW_CLOSED:
        break

window.close()

