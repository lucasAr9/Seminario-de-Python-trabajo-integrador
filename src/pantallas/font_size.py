import PySimpleGUI as sg

ancho, alto = sg.Window.get_screen_size()
# tamaños de ventanas y botones
TAM_VENTANA = (ancho, alto)
TAM_COLUMNAS = (int(ancho/4), int(alto/2))
TAM_COMBO = (int(ancho/80), int(alto/80))

# fuentes de los textos y botones
FONT_TITULO = 'Verdana 72'
FONT_INDICADOR = 'Verdana 34'
FONT_BOTONES = 'Verdana 30'
FONT_COMBO = 'Verdana 18'
