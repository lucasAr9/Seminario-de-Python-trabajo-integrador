import PySimpleGUI as sg
import os

import rutas
from src.pantallas import caracteristicas_generales as cgen


def armar_layout(tarjeta, layout_tarjeta, dificultad_elegida, dataset_elegido, usuario_elegido):
    """Devolver la organización de botones de la ventana de juego."""
    datos = tarjeta.datos_dificultad

    columna_izq = [
        [sg.Frame('Dificultad', [[sg.Text(dificultad_elegida, font=cgen.FUENTE_COMBO)]], expand_x=True,
                  font=cgen.FUENTE_OPCIONES)],
        [sg.Frame('Tema', [[sg.Push(), sg.Text(dataset_elegido.title(), font=cgen.FUENTE_OPCIONES), sg.Push()],
                           [sg.Image(os.path.join(rutas.IMAGENES_DIR, f'{dataset_elegido}.png'))]],
                  font=cgen.FUENTE_OPCIONES)],
        [sg.VPush()],
        [sg.Button('Comenzar', key='-JUEGO_COMENZAR-', font=cgen.FUENTE_BOTONES_DESTACADOS, button_color='Green', visible=False)],
        [sg.Button('Abandonar', key='-JUEGO_ABANDONAR-', tooltip='Volver al menú principal', font=cgen.FUENTE_OPCIONES)]
    ]

    columna_centro = [

         layout_tarjeta
    ]

    columna_der = [
        [sg.Frame('Tiempo restante',
                  [[sg.Image(os.path.join(rutas.IMAGENES_DIR, 'indicador_tiempo.png'), pad=((8, 0), (0, 0))),
                    sg.Text(f'00:00', key='-JUEGO_TIEMPO-', font=cgen.FUENTE_COMBO),
                    sg.ProgressBar(datos.tiempo, orientation='h', size=(18, 20), key='-JUEGO_BARRA-')]],
                  font=cgen.FUENTE_OPCIONES)],
        [sg.Frame('Usuario', [[sg.Text(usuario_elegido, font=cgen.FUENTE_COMBO)]], expand_x=True,
                  font=cgen.FUENTE_OPCIONES)],
        [sg.Table(values=tarjeta.resultados_para_tabla(), headings=['Pregunta', 'Resultado'],
                  max_col_width=25, auto_size_columns=False, justification='center', num_rows=10,
                  key='-JUEGO_TABLA-', row_height=25, font=cgen.FUENTE_OPCIONES, expand_x=True,
                  selected_row_colors=('Black', sg.theme_text_color()))],
        [sg.Text(text=f'PUNTOS ACUMULADOS: {tarjeta.puntos_acumulados}',
                 key='-PUNTOS_ACUMULADOS-', font=cgen.FUENTE_OPCIONES, background_color='#D6C5F0', text_color='black'),
         sg.Text(text='-', key='-CANT_PUNTOS-', font=cgen.FUENTE_OPCIONES, background_color='#D6C5F0',
                 text_color='black'), sg.Text('EXTRA: ', key='-PUNTOS_EXTRA-', background_color='#D6C5F0',
                                              text_color='black')]
    ]

    layout = [
        [sg.Image(os.path.join(rutas.IMAGENES_DIR, 'titulo_figurace.png'), expand_x=True)],
        [sg.HSep(pad=10)],

        [sg.Push(),
         sg.Column(columna_izq, expand_y=True),
         sg.Push(),
         sg.Column(columna_centro, expand_y=True),
         sg.Push(),
         sg.Column(columna_der, expand_y=True),
         sg.Push()],
        [sg.Sizegrip()]
    ]

    layout_encuadre = [[sg.Frame('', layout, expand_x=True, expand_y=True)]]

    return layout_encuadre


def armar_ventana(tarjeta, layout_tarjeta, dificultad_elegida, dataset_elegido, usuario_elegido):
    """Crear y devolver la ventana en la que se juega."""
    window = sg.Window('Juego',
                       armar_layout(tarjeta, layout_tarjeta, dificultad_elegida, dataset_elegido, usuario_elegido),
                       size=cgen.TAM_VENTANA, resizable=True, no_titlebar=True, grab_anywhere=True, finalize=True)
    return window


def cambiar_tarjeta(tarjeta, layout_tarjeta, window, dificultad, dataset, usuario):
    nueva_ventana = armar_ventana(tarjeta, layout_tarjeta, dificultad, dataset, usuario)
    window.close()
    return nueva_ventana
