# Menú de inicio del juego
import PySimpleGUI as sg
from src.pantallas import caracteristicas_generales as cg
from src.pantallas import rutas


def _layout_op_principales():
    """
    :return: el layout que contendra las funciones principales del menu de inicio.
    """
    layout = [
        [sg.Text(size=(None, 2), )],
        [sg.Text("Menu", justification='center', expand_x=True, font=cg.FUENTE_INDICADOR, size=(14, None), )],
        [sg.Button("Jugar", key='-JUGAR-', expand_x=True, font=cg.FUENTE_BOTONES)],
        [sg.Button("Configuración", key='-CONFIGURACION-', expand_x=True, font=cg.FUENTE_BOTONES)],
        [sg.Button("Puntajes", key='-PUNTAJES-', expand_x=True, font=cg.FUENTE_BOTONES)],
        [sg.Button("Perfil", key='-PERFIL-', expand_x=True, font=cg.FUENTE_BOTONES)]
    ]
    return layout


def _layout_usuario_dificultad(usuarios=('',)):
    """
    :return: el layout que contendra la selccion de usuario y dificultad
    """
    # ruta para la imagen
    ruta_imagen = rutas.ruta_imagen('logo')
    # layout
    layout = [
        [sg.Combo(usuarios, key='-USUARIOS-', default_value="Seleccione su usuario", enable_events=True,
                  readonly=True, size=cg.TAM_COMBO, font=cg.FUENTE_COMBO)],
        [sg.Combo(['Facíl', 'Normal', 'Difícil', 'Experto'], key='-DIFICULTAD-',
                  default_value='Seleccione la dificultad', enable_events=True, readonly=True, size=cg.TAM_COMBO,
                  font=cg.FUENTE_COMBO)],
        [sg.Image(ruta_imagen)]
    ]
    return layout


def crear_menu(usuarios=("",)):
    """
    Creacion de la ventana de menu de inicio.
    Su layout contiene un Texto principal,
    dos columnas con (_layout_op_principales(self) y
    _layout_usuario_dificultad(self)) y
    un Boton con el cual se cierra la ventana.
    :return: la ventana del menu principal
    """
    sg.theme(cg.TEMA)
    # rutas para las imagenes
    ruta_icon_png = rutas.ruta_imagen('icono_png')
    ruta_icon_ico = rutas.ruta_imagen('icono_ico')
    ruta_image_titulo = rutas.ruta_imagen('titulo_menu')
    # layouts
    l_principal = _layout_op_principales()
    l_user_dif = _layout_usuario_dificultad(usuarios)
    layout = [
        [sg.Push(), sg.Image(ruta_image_titulo), sg.Push()],
        [sg.Push(), sg.Col(l_principal, size=cg.TAM_COLUMNAS, expand_y=True), sg.Col(l_user_dif,  size=cg.TAM_COLUMNAS,
                                                                                     expand_y=True,
                                                                                     element_justification='center'),
         sg.Push()],
        [sg.Push(), sg.Button("Salir", key='-SALIR-', font=cg.FUENTE_BOTONES), sg.Push()]
    ]
    window = sg.Window("Figurace", layout, size=cg.TAM_VENTANA, finalize=True, use_custom_titlebar=True,
                       titlebar_icon=ruta_icon_png, icon=ruta_icon_ico, enable_close_attempted_event=True)
    return window


if __name__ == '__main__':
    crear_menu()
