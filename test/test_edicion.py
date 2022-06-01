import PySimpleGUI as sg
import src.pantallas.cuentas as cuentas

conf_cuentas = {"perfiles": cuentas.cargar_perfiles(), "act": 0}
window = cuentas.crear_cuentas(conf_cuentas)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, '-VOLVER_PERFILES-'):
        conf_cuentas["perfiles"] = cuentas.cargar_perfiles()
        nicks_perfiles = [x["nombre"] for x in conf_cuentas["perfiles"]]
        break
    elif event == '-ACEPTAR_PERFIL-':
        cuentas.seleccionar_perfil(window, values, conf_cuentas)
    elif event == '-PERFIL_NUEVO-':
        cuentas.crear_perfil(window)
    elif event == '-BTN_EDITAR-':
        cuentas.editar_perfil(window, conf_cuentas)
    elif event == '-BTN_EDITAR_ELIMINAR-':
        cuentas.eliminar_perfil(window, conf_cuentas)
    elif event == '-BTN_CREAR-':
        cuentas.aceptar_crear(window, values, conf_cuentas)
    elif event == '-BTN_CANCELAR_CREAR-':
        cuentas.cancelar_crear(window)
    elif event == '-BTN_EDITAR_CANCELAR-':
        cuentas.cancelar_edicion(window)
    elif event == '-BTN_APLICAR_EDICION-':
        cuentas.aplicar_edicion(window, values, conf_cuentas)
window.close()
