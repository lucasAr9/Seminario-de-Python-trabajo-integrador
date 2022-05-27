import PySimpleGUI as sg

# ancho, alto = sg.Window.get_screen_size()
# tamaños de ventanas y botones
ancho = 700
alto = 680
TAM_VENTANA = (ancho, alto)
TAM_COLUMNAS = (int(ancho/4), int(alto/2))
TAM_COMBO = (int(ancho/80), int(alto/80))

# fuentes de los textos y botones
FUENTE_TITULO = 'Verdana 48'
FUENTE_INDICADOR = 'Verdana 28'
FUENTE_BOTONES = 'Verdana 26'
FUENTE_COMBO = 'Verdana 18'

# colores
sg.LOOK_AND_FEEL_TABLE['figurace_tema'] = {'BACKGROUND': '#1f1f1f',
                                           'TEXT': '#d7d0b7',
                                           'INPUT': '#6d6552',
                                           'TEXT_INPUT': '#eeeeee',
                                           'SCROLL': '#9b9b9b',
                                           'BUTTON': ('#eeeeee', '#6897bb'),
                                           'PROGRESS': ('#eeeeee', '#eeeeee'),
                                           'BORDER': 2, 'SLIDER_DEPTH': 0,
                                           'PROGRESS_DEPTH': 0, }
TEMA = 'figurace_tema'


# ventana para chequear salidas
def ventana_chequear_accion(mensaje='Segurx que querés salir?'):
    """"""
    fondo = 'Black'
    layout = [[sg.T(mensaje, background_color=fondo, text_color='White')],
              [sg.Push(background_color=fondo),
               sg.Button('Sí', s=10), sg.Button('No', s=10),
               sg.Push(background_color=fondo)]
              ]
    window = sg.Window('Salir', layout, no_titlebar=True, grab_anywhere=True,
                       background_color=fondo, keep_on_top=True,)
    event, values = window.read()
    window.close()
    return event
