import PySimpleGUI as sg
import csv
import os

import rutas
from src.pantallas import caracteristicas_generales as cgen


def enumerar(lista):
    """Insertar numeración ordenada a cada elemento de la lista de listas recibida como parámetro"""
    return list(map(lambda x, y: x.insert(0, y), lista, list(range(1, 21))))


def ordenar_y_cortar(lista, num):
    """Devolver la lista recibida ordenada y con 'num' cantidad de elementos"""
    return sorted(lista, key=lambda x: int(x[1]), reverse=True)[:num]


def procesar_dificultad(contenido, nivel):
    """Procesar la lista de listas recibida para devolver los 20 puntajes más altos del nivel recibido."""
    lista = [linea[2:4] for linea in contenido if linea[1] == list(cgen.NIVELES.keys())[nivel]]
    lista = ordenar_y_cortar(lista, 20)
    enumerar(lista)
    return lista


def promedio(lista):
    """Devolver el valor promedio entre los valores de la lista recibida como parámetro"""
    return round(sum([int(num) for num in lista]) / len(lista), 2)


def procesar_promedios(contenido, nivel):
    """Procesar la lista de listas recibida para devolver los 20 promedios más altos del nivel recibido."""
    nombres = set([contenido[i][2] for i in range(len(contenido)) if contenido[i][1] == list(cgen.NIVELES.keys())[nivel]])
    # dicc = {}
    lista = []
    for nombre in nombres:
        # dicc[nombre] = [contenido[i][3] for i in range(len(contenido)) if contenido[i][2] == nombre]
        lista.append([nombre, [contenido[i][3] for i in range(len(contenido)) if contenido[i][2] == nombre and contenido[i][1] == list(cgen.NIVELES.keys())[nivel]]])
    # dicc = {clave: promedio(lista) for clave, lista in dicc.items()}
    lista = [[nombre, promedio(puntajes)] for nombre, puntajes in lista]
    lista = ordenar_y_cortar(lista, 20)
    enumerar(lista)
    return lista


def procesar_archivo():
    """
    Tomar el contenido del archivo de puntajes y devolver en listas los mejores puntajes por nivel.
    En caso de no existir el archivo devolver listas vacías.
    """
    try:
        with(open(os.path.join(rutas.REGISTROS_DIR, 'puntajes.csv'), 'r', encoding='utf-8', newline='')) as archivo:
            csv_reader = csv.reader(archivo, delimiter=',')
            cabecera, contenido = csv_reader.__next__(), [linea for linea in csv_reader]
    except FileNotFoundError:
        sg.popup('No existe registro de puntajes,\njugá al menos una vez para crearlo',
                 no_titlebar=True, grab_anywhere=True, keep_on_top=True, font=cgen.FUENTE_POPUP,
                 image=os.path.join(rutas.IMAGENES_DIR, 'indicador_pista.png'),)
        puntajes_mas_altos = [[] for i in range(len(cgen.NIVELES))]
        promedios_mas_altos = [[] for i in range(len(cgen.NIVELES))]
        print(puntajes_mas_altos)
        print(promedios_mas_altos)
    else:
        puntajes_mas_altos = [procesar_dificultad(contenido, i) for i in range(4)]
        promedios_mas_altos = [procesar_promedios(contenido, i) for i in range(4)]
    return puntajes_mas_altos, promedios_mas_altos


def layouts_pestanias(puntajes, promedios):
    """Devolver la estructura de tabla en la que se muestran los puntajes del juego."""
    titulos = [['Puesto', 'Nick', 'Puntaje'], ['Puesto', 'Nick', 'Promedio']]    # mejorar
    layout = [[sg.Table(values=puntajes, headings=titulos[0],
                        max_col_width=25, auto_size_columns=True,
                        justification='center', key='-JUEGO_TABLA-',
                        row_height=25, expand_x=True, expand_y=True,
                        font=cgen.FUENTE_OPCIONES),
               sg.Table(values=promedios, headings=titulos[1],
                        max_col_width=25, auto_size_columns=True,
                        justification='center', key='-JUEGO_TABLA-',
                        row_height=25, expand_x=True, expand_y=True,
                        font=cgen.FUENTE_OPCIONES)]
              ]
    return layout


def armar_layout():
    """Devolver la organización de botones de una ventana de puntajes."""
    puntajes_por_nivel, promedios_por_nivel = procesar_archivo()
    tab_group = sg.TabGroup([[sg.Tab(list(cgen.NIVELES.keys())[i],
                                     layouts_pestanias(puntajes_por_nivel[i], promedios_por_nivel[i]),
                                     key=f'-PANTALLA_TAB{str(i)}-')] for i in range(4)],
                            expand_y=True, expand_x=True, pad=30, font=cgen.FUENTE_COMBO)

    layout = [[sg.Push(), sg.Image(os.path.join(rutas.IMAGENES_DIR, 'e_puntajes.png'), pad=10), sg.Push(),
               sg.Column([[sg.Image(os.path.join(rutas.IMAGENES_DIR, "t_puntajes.png"))],
                          [sg.Text('Los 20 mejores puntajes y promedios por nivel',
                                   font=cgen.FUENTE_COMBO, justification='c', expand_x=True)]]),
               sg.Push(), sg.Image(os.path.join(rutas.IMAGENES_DIR, 'e_puntajes.png'), pad=10), sg.Push()],
              [sg.HSep()],
              [tab_group],
              [sg.VPush()],
              [sg.Button('Volver', key='-VOLVER_AL_MENU-', font=cgen.FUENTE_COMBO,
                         tooltip='Volver al menú principal', pad=((50, 0), (0, 5))), sg.Push(), sg.Sizegrip()]
              ]

    layout_marco = [[sg.Frame("", layout, expand_x=True, expand_y=True)]]
    return layout_marco


def armar_ventana():
    """Crear y devolver la ventana que mostrará los puntajes del juego."""
    sg.theme(cgen.TEMA)
    window = sg.Window('Puntajes', armar_layout(), finalize=True,
                       size=cgen.TAM_VENTANA, grab_anywhere=True,
                       margins=(20, 20), resizable=True,
                       use_custom_titlebar=True,
                       titlebar_icon=os.path.join(rutas.IMAGENES_DIR, 'cartas_icon.png'))
    return window

