import pandas as pd
import rutas
import os
import random
from src.funcionalidad.dificultad import Dificultad


class Tarjeta:
    def __init__(self, dataset, dificultad_elegida):
        dataset_ruta = os.path.join(rutas.DATOS_DIR, f'dataset_{dataset}.csv')
        data_set = pd.read_csv(dataset_ruta, encoding='utf-8')
        self._datos_dificultad = Dificultad('-' + dificultad_elegida.upper() + '-')
        self._cabecera = data_set.columns
        self._pistas = data_set.sample() # elige una fila al azar
        self.__aux = data_set.sample(n=4)
        self._opciones = []
        for i in range(len(self.__aux)):
            self._opciones.append(self.__aux.iloc[i, 5])
        self.__aux = []
        for i in range(6):
            self.__aux.append(str(self._pistas.iloc[0, i]))
        self._pistas = self.__aux
        self._respuesta_correcta = self._pistas[-1]
        self._opciones.append(self._respuesta_correcta)
        # random.shuffle(self._opciones)
        random.shuffle(self._opciones)
        self._dict_respuestas = {'Titulo': self._cabecera[-1], 'Correcta': self._respuesta_correcta,
                                 'Posibles': self._opciones}
        self._dict_pistas = {tipo: dato for tipo, dato in zip(self._cabecera[:self._datos_dificultad.nivel],
                                                              self._pistas)}
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

    def get_datos_dificultad(self):
        return self._datos_dificultad

    def analizar_respuesta(self, eleccion):
        if eleccion == self._respuesta_correcta:
            self._resultados.append('Bien!')
            self._puntos_acumulados += self._datos_dificultad.correctas
        else:
            self._resultados.append('Mal')
            self._puntos_acumulados -= self._datos_dificultad.incorrectas
