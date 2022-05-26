import PySimpleGUI as sg
import sys
import os
sys.path.append(os.getcwd())
import src.pantallas.cuentas as cuentas

conf_cuentas = {"perfiles": cuentas.cargar_perfiles(), "act": 0}
pantalla_cuentas = cuentas.crear_cuentas(conf_cuentas)
nicks_perfiles = [x["nombre"] for x in conf_cuentas["perfiles"]]

while True:
    current_window, event, values = sg.read_all_windows()

    if current_window == pantalla_cuentas:
        if event == "-VOLVER_PERFILES-":
            conf_cuentas["perfiles"] = cuentas.cargar_perfiles()
            nicks_perfiles = [x["nombre"] for x in conf_cuentas["perfiles"]]
            # crear_menu(perfil.perfiles())
            current_window.close()
            # Esto no va en el test_menu
            break

        else: 
            cuentas.analisis_event_cuentas(current_window,event,values,conf_cuentas)

    if event == sg.WINDOW_CLOSED:
        current_window.close()
        break


