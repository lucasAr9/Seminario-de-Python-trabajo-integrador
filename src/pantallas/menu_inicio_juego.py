# Menú de inicio del juego
import PySimpleGUI as sg
from src.pantallas import font_size as fz
from src.pantallas import cuentas
import os


def _layout_op_principales():
    """
    :return: el layout que contendra las funciones principales del menu de inicio.
    """
    layout = [
        [sg.Text(size=(None, 2), )],
        [sg.Text("Menu", justification=('center'), expand_x=True, font=fz.FONT_INDICADOR, size=(14, None),)],
        [sg.Button("Jugar", key='-JUGAR-', expand_x=True, font=fz.FONT_BOTONES)],
        [sg.Button("Configuración", key='-CONFIGURACION-', expand_x=True, font=fz.FONT_BOTONES)],
        [sg.Button("Puntajes", key='-PUNTAJES-', expand_x=True, font=fz.FONT_BOTONES)],
        [sg.Button("Perfil", key='-PERFIL-', expand_x=True, font=fz.FONT_BOTONES)]
    ]
    return layout


def _layout_usuario_dificultad(usuarios=('',)):
    """
    :return: el layout que contendra la selccion de usuario y dificultad
    """
    # ruta para la imagen
    ruta_imagen = os.path.join(os.path.realpath('..'), "recursos", "imagenes", "imagen_menu_principal.png")
    # layout
    layout = [
        [sg.Combo(usuarios, key='-USUARIOS-', default_value="Seleccione su usuario", enable_events=True,
                readonly=True, size=fz.TAM_COMBO, font=fz.FONT_COMBO)],
        [sg.Combo(['Facíl', 'Normal', 'Difícil', 'Experto'], key='-DIFICULTAD-',
                default_value='Seleccione la dificultad', enable_events=True, readonly=True, size=fz.TAM_COMBO,
                font=fz.FONT_COMBO)],
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
    sg.theme('DarkAmber')
    # rutas para las imagenes
    ruta_titlebar_icon = os.path.join(os.path.realpath('..'), "recursos", "imagenes", "cartas_icon.png")
    ruta_icon = os.path.join(os.path.realpath('..'), "recursos", "imagenes", "cartas_icon.ico")
    ruta_image_titulo = os.path.join(os.path.realpath('..'), "recursos", "imagenes", "titulo_figurace.png")
    # layouts
    l_principal = _layout_op_principales()
    l_user_dif = _layout_usuario_dificultad(usuarios)
    layout = [
        [sg.Push(), sg.Image(ruta_image_titulo), sg.Push()],
        [sg.Push(), sg.Col(l_principal, size=fz.TAM_COLUMNAS, expand_y=True), sg.Col(l_user_dif,  size=fz.TAM_COLUMNAS,
        expand_y=True, element_justification='center'), sg.Push()],
        [sg.Push(), sg.Button("Salir", key='-SALIR-', font=fz.FONT_BOTONES), sg.Push()]
    ]
    window = sg.Window("Figurace", layout, size=fz.TAM_VENTANA, finalize=True, use_custom_titlebar=True,
    titlebar_icon=ruta_titlebar_icon, icon=ruta_icon)
    return window


if __name__ == '__main__':
    crear_menu()
