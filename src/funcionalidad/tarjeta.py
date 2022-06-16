import PySimpleGUI as sg
import pandas as pd
import os
import csv
import random

import rutas
from src.pantallas import caracteristicas_generales as cgen
from src.funcionalidad.dificultad import Dificultad


class Tarjeta:
    def __init__(self, dataset, dificultad_elegida):
        """
        :param dataset, dificultad_elegida: setado desde el menu_incio_juego
        """
        dataset_ruta = os.path.join(rutas.DATOS_DIR, f'dataset_{dataset}.csv')
        self.data_set = pd.read_csv(dataset_ruta, encoding='utf-8', dtype={"year released": str, "top year": str,
                                                                           "bpm": str, "Year": str,
                                                                           "Volcanic Explosivity Index": str})
        self.datos_dificultad = Dificultad('-' + dificultad_elegida.upper() + '-')

        self.respuesta_correcta = ''
        self.dict_respuestas = {}
        self.dict_pistas = {}
        self.resultados = []
        self.puntos_acumulados = 0

    def set_puntos_acumulados(self, puntos):
        self.puntos_acumulados = puntos

    def cargar_datos(self):
        cabecera = self.data_set.columns
        # Me quedo con los datos de una fila al azar, que será la respuesta correcta. Por lo que serán las pistas
        # de la tarjeta
        pistas = self.data_set.sample()  # elige una fila al azar

        # Me guardo en un dataFrame auxiliar 4 filas al azar (Me queda un DataFrame con 4 filas y las columnas de antes)
        aux = self.data_set.sample(n=4)

        # Me quedo con el dato de la última columna del dataset (donde estaría la respuesta correcta)
        # y lo guardo en una lista de opciones
        opciones = list(aux.iloc[:, 5])

        # Me guardo en formato lista de strings las pistas almacenadas en el DataFrame auxiliar
        # Es decir, el valor de cada columna dentro del DataFrame auxiliar
        pistas = list(pistas.iloc[0, :])

        # Me guardo la respuesta correcta, que se encuentra en la última posición de la lista pistas
        self.respuesta_correcta = pistas[-1]

        # Agrego a la lista de opciones posibles, la respuesta correcta
        opciones.append(self.respuesta_correcta)

        # Reordeno al azar la lista de opciones posibles, para que la respuesta correcta, no siempre este a lo ultimo
        random.shuffle(opciones)

        # Guardo en un diccionario las posibles opciones/respuestas a elegir
        self.dict_respuestas = {
            'Titulo': cabecera[-1],
            'Correcta': self.respuesta_correcta,
            'Posibles': opciones
        }

        # Guardo en un diccionario las pistas de la respuesta correcta, siendo la clave el nombre de la columna y
        # el valor, el dato almacenado en esa columna
        self.dict_pistas = {
            tipo: dato for tipo, dato in zip(cabecera[:self.datos_dificultad.caracteristicas], pistas)
        }

    def analizar_respuesta(self, eleccion):
        """
        Analiza la respuesta seleccionada, si coincide con la respuesta correcta
        se suman los puntos correspondientes. Caso contrario, se restan.
        Se actualiza la lista de resultados y los puntos acumulados
        """
        if eleccion == self.respuesta_correcta:
            self.resultados.append('Bien!')
            self.puntos_acumulados += self.datos_dificultad.correctas
        else:
            self.resultados.append('Mal')
            self.puntos_acumulados -= self.datos_dificultad.incorrectas

    def quedan_rondas(self):
        """Devolver True si quedan rondas por jugar, False si se terminaron las rondas"""
        return len(self.resultados) < self.datos_dificultad.rondas

    def layout_datos(self):
        layout = [sg.Frame('Tarjeta',
                           [[sg.Text(f'{nombre}: {dato}', font=cgen.FUENTE_OPCIONES)]
                            for nombre, dato in self.dict_pistas.items()] +
                           [[sg.Text(f'{self.dict_respuestas["Titulo"]}: ', pad=5, font=cgen.FUENTE_COMBO)]] +
                           [[sg.Radio(
                               self.dict_respuestas['Posibles'][i], group_id='respuestas',
                               font=cgen.FUENTE_OPCIONES, key=self.dict_respuestas['Posibles'][i])]
                               for i in range(cgen.CANT_RESPUESTAS)] +
                           [[sg.Button('Confirmar', pad=15, key='-ELECCION-', font=cgen.FUENTE_COMBO),
                             sg.Push(),
                             sg.Button('Pasar >', pad=15, key='-JUEGO_PASAR-', font=cgen.FUENTE_COMBO)]],
                           expand_x=True
                           )]
        return layout

    def layout_vacio(self):
        layout = [sg.Frame('Tarjeta',
                           [[sg.Text('')]
                            for nombre, dato in self.dict_pistas.items()] +
                           [[sg.Text('')]] +
                           [[sg.Radio('', group_id='respuestas')] for radio in range(5)] +
                           [[sg.Button('Confirmar', pad=15, key='-ELECCION-', font=cgen.FUENTE_COMBO, disabled=True),
                             sg.Push(),
                             sg.Button('Pasar >', pad=15, key='-JUEGO_PASAR-', font=cgen.FUENTE_COMBO, disabled=True)]],
                           expand_x=True
                           )]
        return layout


# para guardar los datos de la partida en un csv ---------------------------------------------------------------------??
def guardar_datos_jugada(datos_jugada):
    """
    Guarda los datos de la jugada en un archivo csv.
    La estructura es:
    marca_tiempo, numero_id, evento, cant_a_adivinar, uruario, estado, respuesta, nivel
    """

    # datos_jugada # aca primero habria que ordenar los datos antes de guardarlos en el csv

    archivo = os.path.join(rutas.DATOS_DIR, 'notebooks', 'datos_de_jugadas.csv')
    with open(archivo, 'a+', encoding='utf-8', newline='') as datos:
        writer = csv.writer(datos, delimiter=',')

        if os.stat(archivo).st_size == 0:
            writer.writerow(['marca_tiempo', 'numero_id', 'evento', 'cant_a_adivinar',
                             'usuario', 'estado', 'respuesta', 'nivel'])

        writer.writerow(datos_jugada)
