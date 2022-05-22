import PySimpleGUI as sg
from src.pantallas.menu_inicio_juego import MenuInicio  # no se como hacer que ande este import :C
from src.pantallas.Configuracion import Configuracion
from src.pantallas.Cuentas import Perfiles

TAM_VENTANAS = (800, 800)
FONT_TEXTOS = 'Arial 40'
FONT_BOTONES = 'Arial 20'


def accion_usuario(usuario):
    sg.Popup(f"Usuario seleccionado: {usuario}")


def accion_dificultad(dificultad):
    sg.Popup(f"Dificultad seleccionada: {dificultad}")


def accion_jugar():
    layout = [
        [sg.Text('ACA SE JUEGA :)', font=FONT_TEXTOS)],
        [sg.Button("SALIR", key='-VOLVER_AL_MENU-', font=FONT_BOTONES)]
    ]
    return sg.Window("Ventana de juego", layout, finalize=True)


def accion_configuracion():
    config = Configuracion()
    window = config.crear_ventana()
    return window


def accion_puntajes():
    layout = [
        [sg.Text('ACA SE PUNTUA B)', font=FONT_TEXTOS)],
        [sg.Button("SALIR", key='-VOLVER_AL_MENU-', font=FONT_BOTONES)]
    ]
    return sg.Window("Ventana de juego", layout, finalize=True)


def accion_perfil(perfil):
    return perfil.crear_pantalla({"tam_ventana": TAM_VENTANAS, "font_botones": "Verdana 25"})


usuarios = ["Anto", "Vero", "Lucas", "Tomás"]
menu = MenuInicio(usuarios)
perfil = Perfiles()
window = menu.crear_menu()

while True:
    current_window, event, values = sg.read_all_windows()

    if event == sg.WIN_CLOSED:
        current_window.close()
        break
    elif event == '-SALIR-':
        current_window.close()
        break
    elif event == '-USUARIOS-':
        accion_usuario(current_window['-USUARIOS-'].Get())
    elif event == '-DIFICULTAD-':
        accion_dificultad(current_window['-DIFICULTAD-'].Get())
    elif event == '-JUGAR-':
        accion_jugar()
        current_window.close()
    elif event == '-CONFIGURACION-':
        accion_configuracion()
        current_window.close()
    elif event == '-PUNTAJES-':
        accion_puntajes()
        current_window.close()
    elif event == '-PERFIL-':
        accion_perfil(perfil)
        current_window.close()
    elif event == '-VOLVER_AL_MENU-':
        menu.crear_menu()
        current_window.close()

    elif event == '-VOLVER_CONFIG-':
        menu.crear_menu()
        current_window.close()

    elif event == "-VOLVER_PERFILES-":
        menu.lista_usuarios = perfil.perfiles()
        menu.crear_menu()
        current_window.close()

    perfil.analisis_event_editar(current_window, event, values)
