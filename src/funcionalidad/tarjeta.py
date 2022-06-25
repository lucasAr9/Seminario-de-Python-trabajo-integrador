import PySimpleGUI as sg
import pandas as pd
import os
import random

import rutas
from src.pantallas import caracteristicas_generales as cgen
from src.funcionalidad.dificultad import Dificultad


class Tarjeta:
    """El elemento principal del juego que contiene los datos para adivinar y permite determinar el puntaje"""
    def __init__(self, dataset, dificultad_elegida):
        """
        :param dataset, dificultad_elegida: setado desde el menu_incio_juego
        """
        dataset_ruta = os.path.join(rutas.DATOS_DIR, f'dataset_{dataset}.csv')
        self.data_set = pd.read_csv(dataset_ruta, encoding='utf-8',
                                    keep_default_na=False, dtype={"year released": str, "top year": str,
                                                                  "bpm": str, "Year": str,
                                                                  "Volcanic Explosivity Index": str})
        self.datos_dificultad = Dificultad('-' + dificultad_elegida.upper() + '-')

        self.respuesta_correcta = ''
        self.dict_respuestas = {}
        self.dict_pistas = {}
        self.resultados = {i: '-' for i in range(1, self.datos_dificultad.rondas + 1)}
        self.puntos_acumulados = 0
        self.actual = 1

    def puntos_por_tiempo(self, tiempo, window):
        """Sumar puntos extra si la respuesta es correcta según el tiempo restante"""
        puntos = int(10 / self.datos_dificultad.tiempo * (self.datos_dificultad.tiempo - tiempo))
        window['-PUNTOS_EXTRA-'].update(f'EXTRA: {str(puntos)}', background_color='green')
        self.puntos_acumulados += puntos

    def cargar_datos(self):
        """Procesar los datos del dataset elegido para jugar, para obtener
        las pistas y opciones de respuesta de la tarjeta
        """
        cabecera = self.data_set.columns

        # fila que contiene la respuesta correcta y las pistas elegida al azar
        fila = self.data_set.sample()
        opciones = list(self.data_set.iloc[:, -1].sample(n=4))
        pistas = list(fila.iloc[0, 0:5])

        self.respuesta_correcta = str(fila.iloc[0, -1])

        # agrego la respuesta correcta en una posición al azar entre las opciones
        opciones.insert(random.randrange(cgen.CANT_RESPUESTAS), self.respuesta_correcta)

        self.dict_respuestas = {
            'Titulo': cabecera[-1],
            'Correcta': self.respuesta_correcta,
            'Posibles': opciones
        }

        self.dict_pistas = {
            tipo: dato for tipo, dato in zip(cabecera[:self.datos_dificultad.caracteristicas], pistas)
        }

    def resultados_para_tabla(self):
        """Hacer una lista de listas a partir del diccionario que contiene la tabla de resultados"""
        return [[x, y] for x, y in zip(self.resultados.keys(), self.resultados.values())]

    def analizar_respuesta(self, eleccion, window):
        """
        Analiza la respuesta seleccionada, si coincide con la respuesta correcta
        se suman los puntos correspondientes. Caso contrario, se restan.
        Se actualiza la lista de resultados y los puntos acumulados
        """
        match eleccion:
            case None:
                self.resultados[self.actual] = 'Paso'
                self.puntos_acumulados -= int(self.datos_dificultad.incorrectas / 2)  # resto la mitad de puntos
                window['-CANT_PUNTOS-'].update(f'-{int(self.datos_dificultad.incorrectas / 2)}', background_color='yellow')
            case self.respuesta_correcta:
                self.resultados[self.actual] = 'Bien!'
                self.puntos_acumulados += self.datos_dificultad.correctas
                window['-CANT_PUNTOS-'].update(f'+{self.datos_dificultad.correctas}', background_color='green')
            case _:
                self.resultados[self.actual] = 'Mal'
                if eleccion == 'tiempo':
                    self.resultados[self.actual] += ' (tiempo)'
                self.puntos_acumulados -= self.datos_dificultad.incorrectas
                window['-CANT_PUNTOS-'].update(f'-{self.datos_dificultad.incorrectas}', background_color='red')

        if self.puntos_acumulados < 0:
            self.puntos_acumulados = 0
        window['-PUNTOS_ACUMULADOS-'].update(f'PUNTOS ACUMULADOS: {self.puntos_acumulados}')

    def quedan_rondas(self):
        """Devolver True si quedan rondas por jugar, False si se terminaron las rondas"""
        return self.actual < self.datos_dificultad.rondas

    def layout_datos(self):
        """Devolver la organización de botones de la tarjeta durante el transcurso del juego"""
        layout = [sg.Frame('Tarjeta',
                           [[sg.Image(os.path.join(rutas.IMAGENES_DIR, 'indicador_pista.png')),
                             sg.Text(f'{nombre.upper()}:', font=cgen.FUENTE_OPCIONES, text_color='#FCC314'),
                             sg.Text(f'{dato}', font=cgen.FUENTE_OPCIONES, justification='center',
                                     text_color='#FFDE7D')]
                            for nombre, dato in self.dict_pistas.items()] +
                           [[sg.Text(f'{self.dict_respuestas["Titulo"].upper()}: ', pad=5, font=cgen.FUENTE_COMBO)]] +
                           [[sg.Radio(
                               self.dict_respuestas['Posibles'][i], group_id='respuestas',
                               font=cgen.FUENTE_OPCIONES, key=self.dict_respuestas['Posibles'][i])]
                               for i in range(cgen.CANT_RESPUESTAS)] +
                           [[sg.Button('Confirmar', pad=((15, 0), (1, 3)), key='-ELECCION-', font=cgen.FUENTE_BOTONES),
                             sg.Push(),
                             sg.Button('Pasar >', pad=((0, 15), (1, 3)), key='-JUEGO_PASAR-',
                                       font=cgen.FUENTE_BOTONES)]],
                           expand_x=True, font=cgen.FUENTE_OPCIONES
                           )]
        return layout

    def layout_vacio(self):
        """Devolver la organización de botones de la tarjeta para la pantalla de juego
        antes de comenzar a jugar
        """
        layout = [sg.Frame('Tarjeta',
                           [[sg.Image(os.path.join(rutas.IMAGENES_DIR, 'indicador_pista.png')),
                             sg.Text(f'{nombre.upper()}:', font=cgen.FUENTE_OPCIONES,
                                     text_color='#FCC314'), sg.Text(f'{dato}', visible=False)]
                            for nombre, dato in self.dict_pistas.items()] +
                           [[sg.Text(f'{self.dict_respuestas["Titulo"].upper()}: ', pad=5, font=cgen.FUENTE_COMBO)]] +
                           [[sg.Radio('', group_id='respuestas')] for radio in range(5)] +
                           [[sg.Button('Confirmar', pad=((15, 0), (1, 3)), size=(9, 0), key='-ELECCION-',
                                       font=cgen.FUENTE_BOTONES, disabled=True),
                             sg.Push(),
                             sg.Button('Pasar >', pad=((0, 15), (1, 3)), key='-JUEGO_PASAR-', font=cgen.FUENTE_BOTONES,
                                       disabled=True)]],
                           expand_x=True, font=cgen.FUENTE_OPCIONES
                           )]
        return layout
