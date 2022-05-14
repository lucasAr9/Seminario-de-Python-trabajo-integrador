# Menú de inicio del juego
import PySimpleGUI as sg
import os
# constantes de tamaños y fuentes
TAM_VENTANA = (800, 800)
TAM_COLUMNAS = (415, 400)
TAM_COMBO = (20, 50)
FONT_TITULO = 'Verdana 72'
FONT_INDICADOR = 'Verdana 34'
FONT_BOTONES = 'Verdana 30'
FONT_COMBO = 'Verdana 18'


class MenuInicio:
    def __init__(self, usuarios=['user1', 'user2']):
        """
        :param usuarios: es la lista que genera la ventana de 'Pantalla de creación/edición de perfil'.
        """
        self._lista_usuarios = usuarios

    @property
    def lista_usuarios(self, usuarios):
        self._lista_usuarios = usuarios

    def _layout_op_principales(self):
        """
        :return: el layout que contendra las funciones principales del menu de inicio.
        """
        layout = [
            [sg.Text(size=(None, 2), )],
            [sg.Text("Menu", justification=('center'), expand_x=True,
                     font=FONT_INDICADOR, size=(14, None),)],
            [sg.Button("Jugar", key='-JUGAR-',
                       expand_x=True, font=FONT_BOTONES)],
            [sg.Button("Configuración", key='-CONFIGURACION-',
                       expand_x=True, font=FONT_BOTONES)],
            [sg.Button("Puntajes", key='-PUNTAJES-',
                       expand_x=True, font=FONT_BOTONES)],
            [sg.Button("Perfil", key='-PERFIL-',
                       expand_x=True, font=FONT_BOTONES)]
        ]
        return layout

    def _layout_usuario_dificultad(self):
        """
        :return: el layout que contendra la selccion de usuario y dificultad
        """
        layout = [
            [
                sg.Combo(
                    self._lista_usuarios,
                    key='-USUARIOS-',
                    default_value="Seleccione su usuario",
                    enable_events=True,
                    size=TAM_COMBO,
                    font=FONT_COMBO,
                )
            ],
            [
                sg.Combo(
                    ['Facíl', 'Normal', 'Difícil', 'Experto'],
                    key='-DIFICULTAD-',
                    default_value='Seleccione la dificultad',
                    enable_events=True,
                    size=TAM_COMBO,
                    font=FONT_COMBO,
                )
            ],
            ruta_imagen =
            [
                sg.Image("juego-de-cartas.png")
            ]

        ]
        return layout

    def crear_menu(self):
        """
        Creacion de la ventana de menu de inicio.
        Su layout contiene un Texto principal,
        dos columnas con (_layout_op_principales(self) y
        _layout_usuario_dificultad(self)) y
        un Boton con el cual se cierra la ventana.
        """
        sg.theme('DarkAmber')
        l_principal = self._layout_op_principales()
        l_user_dif = self._layout_usuario_dificultad()
        layout = [
            [sg.Push(),
             sg.Text("FIGURACE", justification='center',
                     expand_x=True, font=FONT_TITULO),
             sg.Push()],

            [sg.Push(),
             sg.Col(l_principal,
                    size=TAM_COLUMNAS, expand_y=True),
             sg.Col(l_user_dif,  size=TAM_COLUMNAS, expand_y=True,
                    element_justification='center'),
             sg.Push()],

            [sg.Push(),
             sg.Button("Salir", key='-SALIR-',
                       font=FONT_BOTONES),
             sg.Push()]
        ]
        window = sg.Window(
            "Figurace", layout, size=TAM_VENTANA, finalize=True,

            use_custom_titlebar=True, titlebar_icon=("cartas_icon.png"),
            icon=("cartas_icon.ico")
        )
        return window
