from src.pantallas import rutas
import csv
import random


def datos_tarjeta(dataset, opciones):
    """"""
    # asi, las opciones = pistas es decir, se van a mostrar tantas pintas como opciones
    with (open(rutas.ruta_datos(dataset), 'r', encoding='utf=8', newline='')) as archivo:
        csv_reader = csv.reader(archivo)
        cabecera, contenido = csv_reader.__next__(), [linea for linea in csv_reader]
    
    linea_dataset = contenido[random.randrange(opciones)]  # si opciones == 3 por ej, se usaran como pistas las 3 primeras columnas.

    respuesta_correcta = linea_dataset[-1]
    x = [linea[-1] for linea in contenido]
    x.remove(respuesta_correcta)
    respuestas_posibles = random.choices(x, k=opciones-1)
    respuestas_posibles.insert(random.randrange(opciones), respuesta_correcta)
    dicc_respuestas = {'Titulo': cabecera[-1], 'Correcta': respuesta_correcta, 'Posibles': respuestas_posibles}

    dicc_pistas = {tipo: dato for tipo, dato in zip(cabecera[:opciones], linea_dataset[:opciones])}

    return dicc_pistas, dicc_respuestas
