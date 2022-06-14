import PySimpleGUI as sg
import os
import rutas

# tamaños de ventanas y botones
ancho, alto = sg.Window.get_screen_size()
ancho_ventana = int(ancho*80/100)
alto_ventana = int(alto*95/100)
TAM_VENTANA = (ancho_ventana, alto_ventana)
TAM_COLUMNAS = (int(ancho_ventana/3), int(alto_ventana/3))
TAM_COMBO = (int(ancho/80), int(alto/80))

# fuentes de los textos y botones (La anterior fuente era Verdana)
FUENTE_TITULO = 'Impact 48'
FUENTE_INDICADOR = 'Impact 28'
FUENTE_BOTONES = 'Impact 26'
FUENTE_COMBO = 'Impact 18'
FUENTE_OPCIONES = 'Impact 12'
FUENTE_POPUP = 'Impact 12'

CANT_RESPUESTAS = 5

# colores
sg.LOOK_AND_FEEL_TABLE['figurace_tema'] = {'BACKGROUND': '#3e206d',
                                           'TEXT': '#FEC260',
                                           'INPUT': '#FEC260',
                                           'TEXT_INPUT': '#000000',
                                           'SCROLL': '#1f1f1f',
                                           'BUTTON': ('#000000', '#D6C5F0'),
                                           'PROGRESS': ('#F58B54', '#F1D6AB'),
                                           'BORDER': 5, 'SLIDER_DEPTH': 0,
                                           'PROGRESS_DEPTH': 5, }
TEMA = 'figurace_tema'

# datasets
datasets = ['volcanes', 'peliculas', 'spotify', 'fifa']


# ventana para chequear salidas
def ventana_chequear_accion(ventana_actual, mensaje='Segurx que querés salir?', imagen='confirmacion.png'):
    """"""
    ruta_imagen = os.path.join(rutas.IMAGENES_DIR, imagen)
    ventana_actual.hide()
    layout_mensaje = [[sg.Push(), sg.T(mensaje, font=FUENTE_POPUP), sg.Push()],
                      [sg.Push(),
                       sg.Button('Sí', s=10), sg.Button('No', s=10),
                       sg.Push()]
                      ]
    layout = [[sg.Col([[sg.Image(ruta_imagen)]]), sg.Col(layout_mensaje)]]
    window = sg.Window('Salir', layout, no_titlebar=True, grab_anywhere=True, keep_on_top=True,)
    event, values = window.read()
    window.close()
    ventana_actual.un_hide()
    return event


def ventana_popup(ventana_actual, mensaje='?', nombre_gif='capoo_aviso.gif'):
    """"""
    ventana_actual.hide()
    gif = os.path.join(rutas.IMAGENES_DIR, nombre_gif)
    layout_aviso = [[sg.Text(mensaje, font=FUENTE_POPUP)], [sg.Push(), sg.Button('OK', key='-OK-', s=10), sg.Push()]]
    layout = [[sg.Col([[sg.Image(gif, key='-GIF-')]]), sg.Col(layout_aviso)]]
    window = sg.Window('Aviso', layout, no_titlebar=True, grab_anywhere=True, keep_on_top=True,
                       element_justification='center')
    while True:
        event, values = window.read(timeout=100)
        if event == '-OK-':
            break
        window['-GIF-'].update_animation(gif, time_between_frames=20)
    window.close()
    ventana_actual.un_hide()
    return event
