import PySimpleGUI as sg

ancho, alto = sg.Window.get_screen_size()
# tamaños de ventanas y botones
    # ancho = 700
    # alto = 680
TAM_VENTANA = (ancho, alto)
TAM_COLUMNAS = (int(ancho/4), int(alto/2))
TAM_COMBO = (int(ancho/80), int(alto/80))

# fuentes de los textos y botones
FUENTE_TITULO = 'Verdana 48'
FUENTE_INDICADOR = 'Verdana 28'
FUENTE_BOTONES = 'Verdana 26'
FUENTE_COMBO = 'Verdana 18'

# colores
    # sg.LOOK_AND_FEEL_TABLE['figurace_tema'] = {'BACKGROUND': '#A02800',
    #                                            'TEXT': '#F4E3B2',
    #                                            'INPUT': '#CF5C36',
    #                                            'TEXT_INPUT': '#F1EEE9',
    #                                            'SCROLL': '#99CC99',
    #                                            'BUTTON': ('#CF0036', '#E8C65E'),
    #                                            'PROGRESS': ('#D1826B', '#E8C65E'),
    #                                            'BORDER': 2, 'SLIDER_DEPTH': 0,
    #                                            'PROGRESS_DEPTH': 0, }
    #  TEMA = 'figurace_tema'
TEMA = 'DarkAmber'


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