import PySimpleGUI as sg
from src.pantallas import caracteristicas_generales as cgen
from src.pantallas import rutas
import csv


niveles = ['Fácil', 'Medio', 'Difícil', 'Personalizado']  # definir cómo recibe el dato


def procesar_dificultad(puntajes_ordenados, nivel):
    nivel = [linea[2:4] for linea in puntajes_ordenados if linea[1] == niveles[nivel]]
    list(map(lambda x, y: x.insert(0, y), nivel, list(range(1, 21))))
    nivel = nivel[:20]
    return nivel


def procesar_archivo():
    try:
        with(open(rutas.ruta_datos('puntajes'), 'r', encoding='utf-8', newline='')) as archivo:
            csv_reader = csv.reader(archivo)
            cabecera, contenido = csv_reader.__next__(), [linea for linea in csv_reader]
    except FileNotFoundError:
        sg.popup('No existe registro de puntajes, juegue al menos una vez para crearlo',
                 no_titlebar=True, grab_anywhere=True, keep_on_top=True)
        nivel_facil, nivel_medio, nivel_dificil, nivel_experto = [], [], [], []
    else:
        puntajes_ordenados = sorted(contenido, key=lambda x: int(x[3]), reverse=True)
        nivel_facil, nivel_medio, nivel_dificil, nivel_experto = [procesar_dificultad(puntajes_ordenados, i)
                                                                  for i in range(4)]
    return nivel_facil, nivel_medio, nivel_dificil, nivel_experto


def layouts_pestanias(num, mejores_puntajes):
    """"""
    titulos = ['Puesto', 'Nick', 'Puntaje']
    match num:
        case 0:
            layout = [[sg.Table(values=mejores_puntajes, headings=titulos,
                                max_col_width=25, auto_size_columns=True,
                                justification='center', key='-JUEGO_TABLA-',
                                row_height=25, expand_x=True, expand_y=True,
                                font=cgen.FUENTE_OPCIONES)]]
        case 1:
            layout = [[sg.Table(values=mejores_puntajes, headings=titulos,
                                max_col_width=25, auto_size_columns=True,
                                justification='center', key='-JUEGO_TABLA-',
                                row_height=25, expand_x=True, expand_y=True,
                                font=cgen.FUENTE_OPCIONES)]]
        case 2:
            layout = [[sg.Table(values=mejores_puntajes, headings=titulos,
                                max_col_width=25, auto_size_columns=True,
                                justification='center', key='-JUEGO_TABLA-',
                                row_height=25, expand_x=True, expand_y=True,
                                font=cgen.FUENTE_OPCIONES)]]
        case 3:
            layout = [[sg.Table(values=mejores_puntajes, headings=titulos,
                                max_col_width=25, auto_size_columns=True,
                                justification='center', key='-JUEGO_TABLA-',
                                row_height=25, expand_x=True, expand_y=True,
                                font=cgen.FUENTE_OPCIONES)]]
        case _:
            layout = [[]]
    return layout


def armar_layout():
    mejores_por_nivel = procesar_archivo()
    tab_group = sg.TabGroup([[sg.Tab(niveles[i],
                                     layouts_pestanias(i, mejores_por_nivel[i]),
                                     key=f'-PANTALLA_TAB{str(i)}-')] for i in range(4)],
                            expand_y=True, expand_x=True, pad=30, font=cgen.FUENTE_COMBO)

    layout = [[sg.Push(), sg.Image(rutas.ruta_imagen('puntaje'), pad=10), sg.Push(),
               sg.Column([[sg.Text('Puntajes', font=cgen.FUENTE_TITULO, justification='c', expand_x=True)],
                          [sg.Text('Los 20 mejores puntajes por nivel',
                                   font=cgen.FUENTE_COMBO, justification='c', expand_x=True)]]),
               sg.Push(), sg.Image(rutas.ruta_imagen('puntaje'), pad=10), sg.Push()],
              [sg.HSep()],
              [tab_group],
              [sg.VPush()],
              [sg.Button('Volver', key='-VOLVER_AL_MENU-', font=cgen.FUENTE_COMBO,
                         tooltip='Volver al menú principal', pad=5), sg.Push(), sg.Sizegrip()]
              ]

    layout_marco = [[sg.Frame("", layout, expand_x=True, expand_y=True)]]
    return layout_marco


def armar_ventana():
    sg.theme(cgen.TEMA)
    window = sg.Window("Puntajes", armar_layout(), finalize=True,
                       size=cgen.TAM_VENTANA, grab_anywhere=True,
                       margins=(20, 20), resizable=True,
                       use_custom_titlebar=True,
                       titlebar_icon=rutas.ruta_imagen('icono_png'))
    return window

