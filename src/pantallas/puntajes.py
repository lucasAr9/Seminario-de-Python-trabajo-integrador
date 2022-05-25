import PySimpleGUI as sg
import caracteristicas_generales as cgen
import rutas
import csv

sg.theme(cgen.TEMA)

niveles = ['Fácil', 'Medio', 'Difícil', 'Experto']


def procesar_archivo():
    with(open(rutas.ruta_datos('puntajes'), 'r', encoding='utf-8', newline='')) as archivo:
        csv_reader = csv.reader(archivo)
        cabecera, contenido = csv_reader.__next__(), [linea for linea in csv_reader]
    puntajes_ordenados = sorted(contenido, key=lambda x:int(x[3]), reverse=True)
    nivel_facil = [linea[2:4] for linea in puntajes_ordenados if linea[1] == 'Fácil']
    list(map(lambda x, y: x.insert(0, y), nivel_facil, list(range(1, 21))))
    nivel_medio = [linea[2:4] for linea in puntajes_ordenados if linea[1] == 'Medio']
    list(map(lambda x, y: x.insert(0, y), nivel_medio, list(range(1, 21))))
    nivel_dificil = [linea[2:4] for linea in puntajes_ordenados if linea[1] == 'Difícil']
    list(map(lambda x, y: x.insert(0, y), nivel_dificil, list(range(1, 21))))
    nivel_experto = [linea[2:4] for linea in puntajes_ordenados if linea[1] == 'Experto']
    list(map(lambda x, y: x.insert(0, y), nivel_experto, list(range(1, 21))))

    return nivel_facil[:20], nivel_medio[:20], nivel_dificil[:20], nivel_experto[:20]


def layouts_pestanias(num):
    """"""
    mejores_nivel1, mejores_nivel2, mejores_nivel3, mejores_nivel4 = procesar_archivo()
    titulos = ['Puesto', 'Nick', 'Puntaje']
    match num:
        case 0:
            layout = [[sg.Table(values=mejores_nivel1, headings=titulos,
                                max_col_width=25, auto_size_columns=True,
                                justification='center', key='-JUEGO_TABLA-',
                                row_height=25, expand_x=True, expand_y=True)]]
        case 1:
            layout = [[sg.Table(values=mejores_nivel2, headings=titulos,
                                max_col_width=25, auto_size_columns=True,
                                justification='center', key='-JUEGO_TABLA-',
                                row_height=25, expand_x=True, expand_y=True)]]
        case 2:
            layout = [[sg.Table(values=mejores_nivel3, headings=titulos,
                                max_col_width=25, auto_size_columns=True,
                                justification='center', key='-JUEGO_TABLA-',
                                row_height=25, expand_x=True, expand_y=True)]]
        case 3:
            layout = [[sg.Table(values=mejores_nivel4, headings=titulos,
                                max_col_width=25, auto_size_columns=True,
                                justification='center', key='-JUEGO_TABLA-',
                                row_height=25, expand_x=True, expand_y=True)]]
        case _:
            layout = [[]]
    return layout


def armar_layout():
    tab_group = sg.TabGroup([[sg.Tab(niveles[i],
                                     layouts_pestanias(i),
                                     key=f'-PANTALLA_TAB{str(i)}-')] for i in range(4)],
                            expand_y=True, expand_x=True, pad=30, enable_events=True)

    layout = [[sg.Image(rutas.ruta_imagen('icono_png'), pad=((20, 0),(20, 0))),
               sg.Text('Puntajes', font=cgen.FUENTE_TITULO, justification='c', expand_x=True),
               sg.Image(rutas.ruta_imagen('icono_png'), pad=((0, 20),(20, 0)))],
              [sg.Text('Los 20 mejores puntajes por nivel',
                       font=cgen.FUENTE_INDICADOR, justification='c', expand_x=True)],
              [sg.HSep()],
              [tab_group],
              [sg.VPush()],
              [sg.Button('Volver', key='-PUNTAJES_VOLVER-',
                         tooltip='Volver al menú principal', pad=5), sg.Push(), sg.Sizegrip()]
              ]

    layout_marco = [[sg.Frame("", layout, expand_x=True, expand_y=True)]]
    return layout_marco


def armar_ventana():
    window = sg.Window("Puntajes", armar_layout(), finalize=True,
                       size=cgen.TAM_VENTANA, enable_close_attempted_event=True,
                       no_titlebar=False, grab_anywhere=True, margins=(20, 20),
                       resizable=True, use_custom_titlebar=True, titlebar_icon=rutas.ruta_imagen('icono_png'))
    return window


window = armar_ventana()
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT and \
            (cgen.ventana_chequear_accion() == 'Sí'):
        break
    if event == '-PUNTAJES_VOLVER-':
        break

window.close()
