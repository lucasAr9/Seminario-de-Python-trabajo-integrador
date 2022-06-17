import unittest
import json
import os

from src.funcionalidad import dificultad as dificultad
from rutas import CONFIG_DIR

RUTA_JSON = os.path.join(CONFIG_DIR, "configuracion.json")

try:
    with open(RUTA_JSON, 'r', encoding='utf-8') as config:
        leer = json.load(config)
        DATOS_JSON = leer['-NORMAL-']
except (FileNotFoundError, json.decoder.JSONDecodeError):
    print('No se encontro el archivo configuracion.json o esta vacio.')
    exit()


class TestCargarValoresDificultad(unittest.TestCase):
    """Test para probar que los valores de la clase dificultad se cargan correctamente."""

    def test_cargar_facil(self):
        """Comprobar que los valores de dificultad se cargaron y son correctos desde las constantes definidas."""
        datos = dificultad.Dificultad('-FACIL-')
        self.assertEqual(datos.tiempo, dificultad.CANT_TIEMPOS[-1])
        self.assertEqual(datos.rondas, dificultad.CANT_RONDAS[-1])
        self.assertEqual(datos.correctas, dificultad.CANT_CORRECTO[-1])
        self.assertEqual(datos.incorrectas, dificultad.CANT_INCORRECTO[0])
        self.assertEqual(datos.caracteristicas, dificultad.CANT_NIVELES[-1])

    def test_cargar_normal(self):
        """Comprobar que los valores de dificultad se cargaron desde el json."""
        datos = dificultad.Dificultad('-NORMAL-')
        self.assertEqual(datos.tiempo, DATOS_JSON['-TIEMPO_C-'])
        self.assertEqual(datos.rondas, DATOS_JSON['-RONDAS_C-'])
        self.assertEqual(datos.correctas, DATOS_JSON['-CORRECTO_C-'])
        self.assertEqual(datos.incorrectas, DATOS_JSON['-INCORRECTO_C-'])
        self.assertEqual(datos.caracteristicas, DATOS_JSON['-CARACTERISTICAS_C-'])


if __name__ == '__main__':
    unittest.main()
