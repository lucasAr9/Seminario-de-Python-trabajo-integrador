import PySimpleGUI as sg
from src.pantallas import caracteristicas_generales as cgen
from src.pantallas import rutas
from src.juego import tarjeta


# definir cómo recibe los datos, dataset por random?
seg_por_respuesta = 30
cant_pistas = 5
rondas_por_juego = 5
dataset_elegido = 'spotify'  # 'fifa' 'peliculas' 'spotify' 'volcanes'


def armar_layout(dataset_elegido, cant_pistas, seg_por_respuesta, rondas_por_juego):
    """"""
    pistas, respuestas = tarjeta.datos_tarjeta(dataset_elegido, cant_pistas)

    titulos = ['Pregunta', 'Resultado']
    resultados = ['Bien', 'Mal', 'Bien', 'Mal', 'Bien', 'Mal', 'Bien', 'Mal', 'Bien', 'Mal']

    columna_izq = [[sg.Frame('Tema',
                             [[sg.Text(dataset_elegido.title()),
                               sg.Image(rutas.ruta_imagen(dataset_elegido))]])],
                   [sg.Table(values=list(enumerate(resultados, start=1)),
                             headings=titulos,
                             max_col_width=25,
                             auto_size_columns=True,
                             # display_row_numbers=True,
                             justification='center',
                             num_rows=rondas_por_juego,
                             key='-JUEGO_TABLA-',
                             row_height=25)],
                   [sg.VPush()],
                   [sg.Button('Abandonar',
                              key='-JUEGO_ABANDONAR-',
                              tooltip='Volver al menú principal')]
                   ]
    columna_der = [[sg.Frame('Dificultad', [[sg.Text('Fácil')]])],
                   [sg.Frame('Tiempo restante', [[sg.Text(f'00:00', key='-JUEGO_TIEMPO-'),
                                                  sg.ProgressBar(seg_por_respuesta,
                                                                 orientation='h',
                                                                 size=(20, 20),
                                                                 key='-JUEGO_BARRA-')
                                                  ]])],
                   [sg.Frame('Tarjeta',
                             [[sg.Text(f'{nombre}: {dato}')]
                              for nombre, dato in pistas.items()] +
                             [[sg.Text(f'{respuestas["Titulo"]}: ', pad=5, font=cgen.FUENTE_COMBO)]] +
                             [[sg.Radio(respuestas['Posibles'][i],
                                        group_id='respuestas',
                                        key=f'-JUEGO_RESPUESTA{str(i)}-')]
                              for i in range(5)] +
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
    window = sg.Window('Juego', armar_layout(dataset_elegido,
                                             cant_pistas,
                                             seg_por_respuesta,
                                             rondas_por_juego),
                       size=cgen.TAM_VENTANA, resizable=True, no_titlebar=True,
                       grab_anywhere=True, keep_on_top=True, finalize=True)
    return window


# window = armar_ventana()
# tiempo_comienzo = time.time()
# while True:
#     event, values = window.read(timeout=1000)
#     if ((event == '-JUEGO_ABANDONAR-') and
#         (cgen.ventana_chequear_accion('Se darán por perdidas la ronda actual\ny las rondas restantes!\n\n'
#                                      'Segurx que querés volver al menú?') == 'Sí')):
#         break
#     delta_tiempo = time.time() - tiempo_comienzo
#     current_time = int(seg_por_respuesta - delta_tiempo)
#     minutos, segundos = divmod(current_time, 60)
#     tiempo = f'{minutos:02d}:{segundos:02d}'
#     window['-JUEGO_TIEMPO-'].update(f'{minutos:02d}:{segundos:02d}')
#     window['-JUEGO_BARRA-'].update(current_count=delta_tiempo+1)
#
# window.close()
