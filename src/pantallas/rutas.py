import os

def ruta_imagen(nombre):
    ruta_extra = os.path.join(os.path.realpath('..'), 'recursos', 'imagenes')  # desde test_menu.py
    # ruta_extra = os.path.join('..', '..', 'recursos', 'imagenes') # para que funcionen las imagenes desde puntajes.py
    match nombre:
        case 'volcanes':
            ruta_imagen = os.path.join(os.getcwd(), ruta_extra, 'volcan.png')
        case 'icono_png':
            ruta_imagen = os.path.join(os.getcwd(), ruta_extra, 'cartas_icon.png')
        case 'icono_ico':
            ruta_imagen = os.path.join(os.getcwd(), ruta_extra, 'cartas_icon.ico')
        case 'titulo_menu':
            ruta_imagen = os.path.join(os.getcwd(), ruta_extra, 'titulo_figurace.png')
        case 'logo':
            ruta_imagen = os.path.join(os.getcwd(), ruta_extra, 'imagen_menu_principal.png')
        case _: ruta_imagen = os.getcwd()  # poner ruta a imagen en blanco, con try except?
    return ruta_imagen

def ruta_datos(nombre):
    ruta_extra = os.path.join('..', '..', 'recursos', 'datos')
    match nombre:
        case 'volcanes':
            ruta_datos = os.path.join(os.getcwd(), ruta_extra, 'dataset_erupciones_volcanicas.csv')
        case 'peliculas':
            ruta_datos = os.path.join(os.getcwd(), ruta_extra, 'dataset_peliculas.csv')
        case 'fifa':
            ruta_datos = os.path.join(os.getcwd(), ruta_extra, 'dataset_fifa21.csv')
        case 'spotify':
            ruta_datos = os.path.join(os.getcwd(), ruta_extra, 'dataset_spotify.csv')
        case 'puntajes':
            ruta_datos = os.path.join(os.getcwd(), ruta_extra, 'puntajes.csv')
        case _:
            ruta_datos = os.getcwd()  # sacar y agregar try except?
    return ruta_datos
