import pandas as pd
import rutas
import os
import random
import PySimpleGUI as sg
from src.pantallas import caracteristicas_generales as cgen
from src.funcionalidad.dificultad import Dificultad


class Tarjeta:
    def __init__(self, dataset, dificultad_elegida):
        """
        :param dataset, dificultad_elegida: setado desde el menu_incio_juego
        """
        dataset_ruta = os.path.join(rutas.DATOS_DIR,  f'dataset_{dataset}.csv')
        self._data_set = pd.read_csv(dataset_ruta, encoding='utf-8')
        self._datos_dificultad = Dificultad('-' + dificultad_elegida.upper() + '-')
        self._respuesta_correcta = ''
        self._dict_respuestas = {}
        self._dict_pistas = {}
        self._resultados = []
        self._puntos_acumulados = 0

    def get_respuestas(self):
        return self._dict_respuestas

    def get_pistas(self):
        return self._dict_pistas

    def get_resultados(self):
        return self._resultados

    def get_puntos_acumulados(self):
        return self._puntos_acumulados

    def set_puntos_acumulados(self, puntos):
        self._puntos_acumulados = puntos

    def get_datos_dificultad(self):
        return self._datos_dificultad

    def cargar_datos(self):
        cabecera = self._data_set.columns
        # Me quedo con los datos de una fila al azar, que será la respuesta correcta. Por lo que serán las pistas
        # de la tarjeta
        pistas = self._data_set.sample()  # elige una fila al azar

        # Me guardo en un dataFrame auxiliar 4 filas al azar (Me queda un DataFrame con 4 filas y las columnas de antes)
        aux = self._data_set.sample(n=4)
        opciones = []

        # Me quedo con el dato de la última columna del dataset (donde estaría la respuesta correcta)
        # y lo guardo en una lista de opciones
        for i in range(len(aux)):
            opciones.append(aux.iloc[i, 5])

        # Me guardo en formato lista de strings las pistas almacenadas en el DataFrame auxiliar
        # Es decir, el valor de cada columna dentro del DataFrame auxiliar
        aux = []  # reutilizo la variable aux, esta vez para una lista
        for i in range(6):
            aux.append(str(pistas.iloc[0, i]))
        pistas = aux

        # Me guardo la respuesta correcta, que se encuentra en la última posición de la lista pistas
        self._respuesta_correcta = pistas[-1]

        # Agrego a la lista de opciones posibles, la respuesta correcta
        opciones.append(self._respuesta_correcta)

        # Reordeno al azar la lista de opciones posibles, para que la respuesta correcta, no siempre este a lo ultimo
        random.shuffle(opciones)

        # Guardo en un diccionario las posibles opciones/respuestas a elegir
        self._dict_respuestas = {'Titulo': cabecera[-1], 'Correcta': self._respuesta_correcta,
                                 'Posibles': opciones}

        # Guardo en un diccionario las pistas de la respuesta correcta, siendo la clave el nombre de la columna y
        # el valor, el dato almacenado en esa columna
        self._dict_pistas = {tipo: dato for tipo, dato in
                             zip(cabecera[:self._datos_dificultad.get_caracteristicas()],
                                 pistas)}

    def analizar_respuesta(self, eleccion):
        """
        Analiza la respuesta seleccionada, si coincide con la respuesta correcta
        se suman los puntos correspondientes. Caso contrario, se restan.
        Se actualiza la lista de resultados y los puntos acumulados
        """
        if eleccion == self._respuesta_correcta:
            self._resultados.append('Bien!')
            self._puntos_acumulados += self._datos_dificultad.get_correctas()
        else:
            self._resultados.append('Mal')
            self._puntos_acumulados -= self._datos_dificultad.get_incorrectas()

        # Si No quedan más rondas, se retorna el string correspondiente para detener la partida en el manejo
        # del figurace
        if len(self._resultados) == self._datos_dificultad.get_rondas():
            return 'TERMINO_LAS_RONDAS'
        else:
            return 'SIGUE'

    def layout_datos(self):
        layout = [sg.Frame('Tarjeta',
                  [[sg.Text(f'{nombre}: {dato}', font=cgen.FUENTE_OPCIONES)]
                   for nombre, dato in self._dict_pistas.items()] +
                  [[sg.Text(f'{self._dict_respuestas["Titulo"]}: ', pad=5, font=cgen.FUENTE_COMBO)]] +
                  [[sg.Radio(self._dict_respuestas['Posibles'][i], group_id='respuestas',
                             font=cgen.FUENTE_OPCIONES, key=self._dict_respuestas['Posibles'][i])]
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
                   for nombre, dato in self._dict_pistas.items()] +
                  [[sg.Text('')]] +
                  [[sg.Radio(['', '', '', '', ''], group_id='respuestas')]] +
                  [[sg.Button('Confirmar', pad=15, key='-ELECCION-', font=cgen.FUENTE_COMBO, disabled=True),
                    sg.Push(),
                    sg.Button('Pasar >', pad=15, key='-JUEGO_PASAR-', font=cgen.FUENTE_COMBO, disabled=True)]],
                  expand_x=True
                  )]
        return layout
