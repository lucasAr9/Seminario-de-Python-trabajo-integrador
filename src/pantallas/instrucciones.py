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
    ruta_adya_imagen = os.path.join(rutas.TUTORIALES_DIR, 'adya_boton.png')
    ruta_titulo = os.path.join(rutas.TUTORIALES_DIR, 'tutorial_titulo.png')
    ruta_gif_tuto = os.path.join(rutas.TUTORIALES_DIR, 'gif_tutorial.gif')

    layout_botones = [[sg.Image(ruta_adya_imagen),
                       sg.Button(f'{list(tutorial.keys())[0]}', key=f'{list(tutorial.keys())[0]}'
                                 , font=cg.FUENTE_OPCIONES, expand_x=True), sg.Image(ruta_adya_imagen)]
                      for tutorial in cg.TUTORIALES]
    layout_botones.append([sg.Push(), sg.Image(ruta_gif_tuto, key='-GIF_TUTO-'), sg.Push()])
    layout_botones.insert(0, [sg.Push(), sg.Image(ruta_titulo), sg.Push()])

    layout_navegar = [[sg.Push(), sg.Image(ruta_imagen, key='-IMAGEN_TUTO-'), sg.Push()],
                      [sg.Push(),
                       sg.Button('<', key='-ATRAS-', font=cg.FUENTE_BOTONES),
                       sg.Button('>', key='-SIG-', font=cg.FUENTE_BOTONES),
                       sg.Push()
                       ]]

    layout = [[sg.VPush()], [sg.Push(), sg.Col(layout_botones, expand_x=True, expand_y=True), sg.Push(),
                             sg.Col(layout_navegar, expand_x=True, expand_y=True)],
              [sg.Button('Volver', key='-VOLVER-', font=cg.FUENTE_BOTONES, pad=((50, 0), (0, 5)))]]

    window = sg.Window('TUTORIALES', layout, size=cg.TAM_VENTANA, finalize=True, grab_anywhere=True, no_titlebar=True)

    return window
