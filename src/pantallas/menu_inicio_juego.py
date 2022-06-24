import PySimpleGUI as sg
import os

import rutas
from src.pantallas import caracteristicas_generales as cg


def _layout_op_principales():
    """
    :return: el layout que contendra las funciones principales del menu de inicio.
    """
    ruta_imagen = os.path.join(rutas.IMAGENES_DIR, 'indicador_perfil.png')
    layout = [
        [sg.Text(size=(None, 2), )],
        [sg.Text("Menú", justification='center', expand_x=True, font=cg.FUENTE_INDICADOR, size=(14, None), )],
        [sg.Button("Jugar", key='-JUGAR-', expand_x=True, font=cg.FUENTE_BOTONES_DESTACADOS)],
        [sg.Button("Configuración", key='-CONFIGURACION-', expand_x=True, font=cg.FUENTE_BOTONES),
         sg.Button("Puntajes", key='-PUNTAJES-', expand_x=True, font=cg.FUENTE_BOTONES)],
        [sg.Button("Perfiles", key='-PERFIL-', expand_x=True, font=cg.FUENTE_BOTONES),
         sg.Button("Instrucciones", key='-INSTRUCCIONES-', expand_x=True, font=cg.FUENTE_BOTONES)],
        [sg.Push(), sg.Image(ruta_imagen), sg.Push()],
        [sg.VPush()],
        [sg.Button("Salir", key='-SALIR-', font=cg.FUENTE_COMBO, pad=((0, 0), (10, 0))), sg.Push()]
    ]
    return layout


def _layout_usuario_dificultad(usuarios):
    """
    :return: el layout que contendra la selccion de usuario y dificultad
    """
    # ruta para la imagen
    ruta_imagen = os.path.join(rutas.IMAGENES_DIR, 'imagen_menu_principal.png')
    ruta_imagen_aviso = os.path.join(rutas.IMAGENES_DIR, 'tip_personalizado.png')
    # layout
    layout = [
        [sg.Combo(usuarios, key='-USUARIOS-', default_value="Seleccione su usuario", enable_events=True,
                  readonly=True, size=cg.TAM_COMBO, font=cg.FUENTE_BOTONES, pad=((0, 0), (100, 5)))],
        [sg.Combo(['Facil', 'Normal', 'Dificil', 'Personalizado'], key='-DIFICULTAD-',
                  default_value='Seleccione la dificultad', enable_events=True, readonly=True, size=cg.TAM_COMBO,
                  font=cg.FUENTE_BOTONES)],
        [sg.Image(ruta_imagen)],
        [sg.Image(ruta_imagen_aviso, key='-AVISO_PER-', visible=False)]
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
    # rutas para las imágenes
    ruta_icon_png = os.path.join(rutas.IMAGENES_DIR, 'cartas_icon.png')
    ruta_icon_ico = os.path.join(rutas.IMAGENES_DIR, 'cartas_icon.ico')
    ruta_image_titulo = os.path.join(rutas.IMAGENES_DIR, 'titulo_figurace.png')
    # layouts
    l_principal = _layout_op_principales()
    l_user_dif = _layout_usuario_dificultad(usuarios)
    layout = [[sg.Frame('', [
        [sg.Push(), sg.Image(ruta_image_titulo), sg.Push()],
        [sg.Push(), sg.Col(l_principal, size=cg.TAM_COLUMNAS, expand_y=True), sg.Col(l_user_dif,  size=cg.TAM_COLUMNAS,
                                                                                     expand_y=True,
                                                                                     element_justification='center'),
         sg.Push()]
    ], expand_y=True, expand_x=True)]]
    window = sg.Window("Figurace", layout, size=cg.TAM_VENTANA, finalize=True, use_custom_titlebar=True,
                       titlebar_icon=ruta_icon_png, icon=ruta_icon_ico, enable_close_attempted_event=True,
                       margins=(20, 20))
    return window
