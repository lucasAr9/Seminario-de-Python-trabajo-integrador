import PySimpleGUI as sg
import random
import os
import rutas
from src.pantallas import caracteristicas_generales as cgen


def armar_layout(tarjeta, dificultad_elegida, dataset_elegido, usuario_elegido):
    """Devolver la organización de botones de la ventana de juego."""
    respuestas = tarjeta.get_respuestas()
    pistas = tarjeta.get_pistas()
    resultados = tarjeta.get_resultados()
    datos = tarjeta.get_datos_dificultad()

    columna_izq = [[sg.Frame('Dificultad',
                             [[sg.Text(dificultad_elegida, font=cgen.FUENTE_COMBO)]],
                             expand_x=True)],
                   [sg.Frame('Tema',
                             [[sg.Text(dataset_elegido.title(), font=cgen.FUENTE_OPCIONES),
                               sg.Image(os.path.join(rutas.IMAGENES_DIR, f'{dataset_elegido}.png'))]])],
                   [sg.VPush()],
                   [sg.Button('Abandonar',
                              key='-JUEGO_ABANDONAR-',
                              tooltip='Volver al menú principal',
                              font=cgen.FUENTE_OPCIONES)]
                   ]
    columna_centro = [[sg.Frame('Tiempo restante',
                                [[sg.Text(f'00:00', key='-JUEGO_TIEMPO-',
                                  font=cgen.FUENTE_COMBO),
                                  sg.ProgressBar(datos.tiempo,
                                                 orientation='h',
                                                 size=(18, 20),
                                                 key='-JUEGO_BARRA-')
                                  ]])],
                      [sg.Frame('Tarjeta',
                                [[sg.Text(f'{nombre}: {dato}', font=cgen.FUENTE_OPCIONES)]
                                 for nombre, dato in pistas.items()] +
                                [[sg.Text(f'{respuestas["Titulo"]}: ', pad=5, font=cgen.FUENTE_COMBO)]] +
                                [[sg.Radio(respuestas['Posibles'][i], group_id='respuestas',
                                           font=cgen.FUENTE_OPCIONES, key=respuestas['Posibles'][i])]
                                 for i in range(cgen.CANT_RESPUESTAS)] +
                                [[sg.Button('Confirmar', pad=15, key='-ELECCION-', font=cgen.FUENTE_COMBO),
                                  sg.Push(),
                                  sg.Button('Pasar >', pad=15, key='-JUEGO_PASAR-', font=cgen.FUENTE_COMBO)]],
                                expand_x=True
                                )]
                      ]
    columna_der = [[sg.Frame('Usuario',
                             [[sg.Text(usuario_elegido, font=cgen.FUENTE_COMBO)]],
                             expand_x=True)],
                   [sg.Table(values=list(enumerate(resultados, start=1)),
                             headings=['Pregunta', 'Resultados'], max_col_width=25,
                             auto_size_columns=False, justification='center',
                             num_rows=10, key='-JUEGO_TABLA-',
                             row_height=25, font=cgen.FUENTE_OPCIONES, expand_x=True)]
                   ]

    layout = [[sg.Image(os.path.join(rutas.IMAGENES_DIR, 'titulo_figurace.png'), expand_x=True)],
              [sg.HSep(pad=10)],
              # [sg.Button('Comenzar', key='-JUEGO_COMENZAR-')],
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


def armar_ventana(tarjeta, dificultad_elegida, dataset_elegido, usuario_elegido):
    """Crear y devolver la ventana en la que se juega."""
    window = sg.Window('Juego', armar_layout(tarjeta, dificultad_elegida, dataset_elegido, usuario_elegido),
                       size=cgen.TAM_VENTANA, resizable=True, no_titlebar=True,
                       grab_anywhere=True, finalize=True)
    return window