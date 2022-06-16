import csv
import os

import rutas


class Partida:
    """El registro de todos los eventos de cada partida que se guardan en un archivo csv"""
    def __init__(self):
        self.timestamp = None
        self.id = None
        self.evento = None
        self.nombre_jugador = None
        self.edad_jugador = None
        self.sexo_jugador = None
        self.estado = None
        self.texto_ingresado = None
        self.respuesta = None
        self.nivel = None

    def get_todos_datos(self):
        """:return: todos los datos de la jugada."""
        return [self.timestamp, self.id, self.evento, self.nombre_jugador, self.edad_jugador,
                self.sexo_jugador, self.estado, self.texto_ingresado, self.respuesta, self.nivel]

    def comienzo(self, timestamp, id, evento, jugador, nivel):
        """
        Setea los datos de la jugada.
        :param timestamp: tiempo de la partida en cada momento.
        :param id: de la partida
        :param evento: actual de la partida (inicio_partida, intento, fin)
        :param jugador: nombre, edad y sexo del jugador actual.
        :param nivel: la dificultad de la partida (facil, normal, dificil, personalizado)
        Guardar los nuevos datos en un archivo csv.
        """
        self.timestamp = timestamp
        self.id = id
        self.evento = evento
        self.nombre_jugador = jugador["nombre"]
        self.edad_jugador = jugador["edad"]
        self.sexo_jugador = jugador["genero"]
        self.nivel = nivel
        self.guardar_datos_jugada()

    def eventos(self, timestamp, evento, estado, texto_ingresado, respuesta):
        """
        Setea los datos de la jugada.
        :param timestamp: tiempo de la partida en cada momento.
        :param evento: actual de la partida (inicio_partida, intento, fin)
        :param estado: estado de la partida (error, ok, finalizada)
        :param texto_ingresado: texto ingresado por el jugador.
        :param respuesta: respuesta del sistema.
        Guardar los nuevos datos en un archivo csv.
        """
        self.timestamp = timestamp
        self.evento = evento
        self.estado = estado
        self.texto_ingresado = texto_ingresado
        self.respuesta = respuesta
        self.guardar_datos_jugada()

    def guardar_datos_jugada(self):
        """
        Guarda los datos de la jugada en un archivo csv.
        La estructura es:
        marca_tiempo, numero_id, evento, cant_a_adivinar, uruario, estado, respuesta, nivel
        """
        archivo = os.path.join(rutas.DATOS_DIR, 'notebooks', 'datos_de_jugadas.csv')
        with open(archivo, 'a+', encoding='utf-8', newline='') as datos:
            writer = csv.writer(datos, delimiter=',')

            if os.stat(archivo).st_size == 0:
                writer.writerow(['timestamp', 'id', 'evento', 'nombre_jugador', 'edad_jugador',
                                 'sexo_jugador', 'estado', 'texto_ingresado', 'respuesta', 'nivel'])

            writer.writerow(self.get_todos_datos())
