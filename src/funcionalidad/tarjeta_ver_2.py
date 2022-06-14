import pandas as pd
import rutas
import os
import random
from src.funcionalidad.dificultad import Dificultad


class Tarjeta:
    def __init__(self, dataset, dificultad_elegida):
        dataset_ruta = os.path.join(rutas.DATOS_DIR,  f'dataset_{dataset}.csv')
        self._data_set = pd.read_csv(dataset_ruta, encoding='utf-8')
        self._dificultad_elegida = dificultad_elegida
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
        pistas = self._data_set.sample()  # elige una fila al azar
        aux = self._data_set.sample(n=4)
        opciones = []
        for i in range(len(aux)):
            opciones.append(aux.iloc[i, 5])
        aux = []
        for i in range(6):
            aux.append(str(pistas.iloc[0, i]))
        pistas = aux
        self._respuesta_correcta = pistas[-1]
        opciones.append(self._respuesta_correcta)
        random.shuffle(opciones)
        self._dict_respuestas = {'Titulo': cabecera[-1], 'Correcta': self._respuesta_correcta,
                                 'Posibles': opciones}
        self._dict_pistas = {tipo: dato for tipo, dato in
                             zip(cabecera[:self._datos_dificultad.get_caracteristicas()],
                                 pistas)}

    def analizar_respuesta(self, eleccion):
        if eleccion == self._respuesta_correcta:
            self._resultados.append('Bien!')
            self._puntos_acumulados += self._datos_dificultad.get_correctas()
        else:
            self._resultados.append('Mal')
            self._puntos_acumulados -= self._datos_dificultad.get_incorrectas()

        if len(self._resultados) == self._datos_dificultad.get_rondas():
            return 'TERMINO_LAS_RONDAS'
        else:
            return 'SIGUE'

