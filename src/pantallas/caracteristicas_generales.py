import PySimpleGUI as sg


# tamaños de ventanas y botones
ancho, alto = sg.Window.get_screen_size()
ancho_ventana = int(ancho*80/100)
alto_ventana = int(alto*95/100)
TAM_VENTANA = (ancho_ventana, alto_ventana)
TAM_COLUMNAS = (int(ancho_ventana/3), int(alto_ventana/3))
TAM_COMBO = (int(ancho/80), int(alto/80))

# fuentes de los textos y botones
FUENTE_TITULO = 'Verdana 48'
FUENTE_INDICADOR = 'Verdana 28'
FUENTE_BOTONES = 'Verdana 26'
FUENTE_COMBO = 'Verdana 18'
FUENTE_OPCIONES = 'Verdana 12'
FUENTE_POPUP = 'Verdana 10'

CANT_RESPUESTAS = 5

# colores
sg.LOOK_AND_FEEL_TABLE['figurace_tema'] = {'BACKGROUND': '#3A1F5D',
                                           'TEXT': '#F1D6AB',
                                           'INPUT': '#F58B54',
                                           'TEXT_INPUT': '#000000',
                                           'SCROLL': '#1f1f1f',
                                           'BUTTON': ('#000000', '#F9D276'),
                                           'PROGRESS': ('#F58B54', '#F1D6AB'),
                                           'BORDER': 2, 'SLIDER_DEPTH': 0,
                                           'PROGRESS_DEPTH': 0, }
TEMA = 'figurace_tema'

# datasets
datasets = ['volcanes', 'peliculas', 'spotify', 'fifa']


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
