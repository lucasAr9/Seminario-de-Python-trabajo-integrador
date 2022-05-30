import PySimpleGUI as sg
import random
from src.pantallas import caracteristicas_generales as cgen
from src.juego import dificultad as config
from src.pantallas import rutas
from src.juego import tarjeta


def obtener_datos():
    cant_pistas = 5
    valores = config.leer_configuracion()
    opciones = valores['-CARACTERISTICAS_C-']
    seg_por_respuesta = valores['-TIEMPO_C-']
    rondas_por_juego = valores['-RONDAS_C-']
    dataset_elegido = random.choice(cgen.datasets)
    pistas, respuestas = tarjeta.datos_tarjeta(dataset_elegido, opciones)
    datos = dict(zip(['seg_por_respuesta', 'rondas_por_juego', 'dataset_elegido', 'pistas', 'respuestas', 'opciones'],
                     [seg_por_respuesta, rondas_por_juego, dataset_elegido, pistas, respuestas, opciones]))
    return datos


def armar_layout(datos):
    """"""

    titulos = ['Pregunta', 'Resultado']
    resultados = ['Bien', 'Mal', 'Bien', 'Mal', 'Bien', 'Mal', 'Bien', 'Mal', 'Bien', 'Mal']

    columna_izq = [[sg.Frame('Tema',
                             [[sg.Text(datos['dataset_elegido'].title()),
                               sg.Image(rutas.ruta_imagen(datos['dataset_elegido']))]])],
                   [sg.Table(values=list(enumerate(resultados, start=1)),
                             headings=titulos,
                             max_col_width=25,
                             auto_size_columns=True,
                             # display_row_numbers=True,
                             justification='center',
                             num_rows=datos['rondas_por_juego'],
                             key='-JUEGO_TABLA-',
                             row_height=25)],
                   [sg.VPush()],
                   [sg.Button('Abandonar',
                              key='-JUEGO_ABANDONAR-',
                              tooltip='Volver al menú principal')]
                   ]
    columna_der = [[sg.Frame('Dificultad', [[sg.Text('Fácil')]])],
                   [sg.Frame('Tiempo restante', [[sg.Text(f'00:00', key='-JUEGO_TIEMPO-'),
                                                  sg.ProgressBar(datos['seg_por_respuesta'],
                                                                 orientation='h',
                                                                 size=(20, 20),
                                                                 key='-JUEGO_BARRA-')
                                                  ]])],
                   [sg.Frame('Tarjeta',
                             [[sg.Text(f'{nombre}: {dato}')]
                              for nombre, dato in datos['pistas'].items()] +
                             [[sg.Text(f'{datos["respuestas"]["Titulo"]}: ', pad=5, font=cgen.FUENTE_COMBO)]] +
                             [[sg.Radio(datos['respuestas']['Posibles'][i], group_id='respuestas',
                                        key=f'-JUEGO_RESPUESTA{str(i)}-')]
                              for i in range(datos['opciones'])] +
                             [[sg.Ok(pad=15), sg.Push(), sg.Button('Pasar >', pad=15, key='-JUEGO_PASAR-')]]
                             )],
                   [sg.Push(), sg.Sizegrip()]
                   ]

    layout = [[sg.Text('FiguRace', justification='c', expand_x=True, font=cgen.FUENTE_TITULO)],
              [sg.HSep(pad=10)],
              # [sg.Button('Comenzar', key='-JUEGO_COMENZAR-')],
              [sg.Column(columna_izq, expand_x=True, expand_y=True),
               sg.Column(columna_der, element_justification='l', expand_x=True, expand_y=True)],
              ]

    layout_encuadre = [[sg.Frame('', layout, expand_x=True)]]

    return layout_encuadre


def armar_ventana():
    sg.theme(cgen.TEMA)
    datos = obtener_datos()
    window = sg.Window('Juego', armar_layout(datos),
                       size=cgen.TAM_VENTANA, resizable=True, no_titlebar=True,
                       grab_anywhere=True, keep_on_top=True, finalize=True)
    return window


# if __name__ == '__main__':
#     window = armar_ventana()
#     tiempo_comienzo = time.time()
#     while True:
#          event, values = window.read(timeout=1000)
#          if ((event == '-JUEGO_ABANDONAR-') and
#              (cgen.ventana_chequear_accion('Se darán por perdidas la ronda actual\ny las rondas restantes!\n\n'
#                                           'Segurx que querés volver al menú?') == 'Sí')):
#              break
#          delta_tiempo = time.time() - tiempo_comienzo
#          current_time = int(seg_por_respuesta - delta_tiempo)
#          minutos, segundos = divmod(current_time, 60)
#          tiempo = f'{minutos:02d}:{segundos:02d}'
#          window['-JUEGO_TIEMPO-'].update(f'{minutos:02d}:{segundos:02d}')
#          window['-JUEGO_BARRA-'].update(current_count=delta_tiempo+1)
#
#     window.close()
