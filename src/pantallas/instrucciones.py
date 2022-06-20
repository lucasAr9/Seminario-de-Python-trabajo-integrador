import PySimpleGUI as sg
import os
import rutas
import src.pantallas.caracteristicas_generales as cg


def obtener_indice(event):
    indice = 0
    for nombre in cg.TUTORIALES:
        if list(nombre.keys())[0] == event:
            break
        else:
            indice += 1
    return indice


def crear_ventana():
    """
    return: La ventana de instrucciones/Tutoriales
    """
    ruta_imagen = os.path.join(rutas.TUTORIALES_DIR, list(cg.TUTORIALES[0].values())[0][0], 'paso_1.png')

    layout_botones = [[sg.Button(f'{list(tutorial.keys())[0]}', key=f'{list(tutorial.keys())[0]}',
                                 pad=10, font=cg.FUENTE_OPCIONES)]
                      for tutorial in cg.TUTORIALES]

    layout_navegar = [[sg.Push(), sg.Image(ruta_imagen, key='-IMAGEN_TUTO-'), sg.Push()],
                      [sg.Push(),
                       sg.Button('<', key='-ATRAS-', font=cg.FUENTE_BOTONES),
                       sg.Button('>', key='-SIG-', font=cg.FUENTE_BOTONES),
                       sg.Push()
                       ]]

    layout = [[sg.Text('Tutoriales :', font=cg.FUENTE_INDICADOR)],
              [sg.Col(layout_botones, expand_x=True, expand_y=True),
               sg.Col(layout_navegar, expand_x=True, expand_y=True)],
              [sg.Button('VOLVER', key='-VOLVER-', font=cg.FUENTE_BOTONES)]
              ]

    window = sg.Window('TUTORIALES', layout, size=cg.TAM_VENTANA, finalize=True, no_titlebar=True)

    return window
