import PySimpleGUI as sg
import src.pantallas.caracteristicas_generales as cg
from src.pantallas.menu_inicio_juego import crear_menu
from src.pantallas import configuracion as c_pantalla
import src.pantallas.cuentas as cuentas
from src.pantallas import puntajes
from src.pantallas import juego
import time


def abrir_configuracion():
    """"""
    window = c_pantalla.crear_ventana()
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, '-VOLVER_CONFIG-'):
            break
    window.close()
    return


def abrir_puntajes():
    """"""
    window = puntajes.armar_ventana()
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, '-VOLVER_AL_MENU-'):
            break
    window.close()
    return


def abrir_perfiles():
    """"""
    window = cuentas.crear_cuentas({"tam_ventana": cg.TAM_VENTANA, "font_botones": "Verdana 25"})
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, '-VOLVER_PERFILES-'):
            break
    window.close()
    return


def abrir_juego():
    """"""
    window = juego.armar_ventana()
    tiempo_comienzo = time.time()
    while True:
        event, values = window.read(timeout=100)
        if ((event == '-JUEGO_ABANDONAR-') and
                (cg.ventana_chequear_accion('Se darán por perdidas la ronda actual\ny las rondas restantes!\n\n'
                                            'Segurx que querés volver al menú?') == 'Sí')):
            break
        delta_tiempo = time.time() - tiempo_comienzo
        current_time = int(30 - delta_tiempo)
        minutos, segundos = divmod(current_time, 60)
        tiempo = f'{minutos:02d}:{segundos:02d}'
        window['-JUEGO_TIEMPO-'].update(f'{minutos:02d}:{segundos:02d}')
        window['-JUEGO_BARRA-'].update(current_count=delta_tiempo + 1)
    window.close()
    return


def main():
    """"""
    niveles = ['Fácil', 'Medio', 'Difícil', 'Experto']
    conf_cuentas = {"perfiles": cuentas.cargar_perfiles(), "act": 0}
    perfiles = list(map(lambda datos: datos['nombre'], conf_cuentas['perfiles']))
    window = crear_menu(perfiles)
    while True:
        event, values = window.read()
        if (event in (sg.WINDOW_CLOSE_ATTEMPTED_EVENT, '-SALIR-') and
                (cg.ventana_chequear_accion() == 'Sí')):
            break
        elif event == '-USUARIOS-':
            sg.Popup(f"Usuario seleccionado: {window['-USUARIOS-'].Get()}")
        elif event == '-DIFICULTAD-':
            sg.Popup(f"Dificultad seleccionada: {window['-DIFICULTAD-'].Get()}")
        elif event == '-JUGAR-':
            window.hide()
            abrir_juego()
            window.un_hide()
        elif event == '-CONFIGURACION-':
            window.hide()
            abrir_configuracion()
            window.un_hide()
        elif event == '-PUNTAJES-':
            window.hide()
            abrir_puntajes()
            window.un_hide()
        elif event == '-PERFIL-':
            window.hide()
            abrir_perfiles()
            window.un_hide()
            window['-USUARIOS-'].update(values=perfiles)

    window.close()


if __name__ == "__main__":
    main()
