import PySimpleGUI as sg
import os
import json
import sys

import src.pantallas.caracteristicas_generales as cg
import rutas as ruta


def cargar_perfiles():
    """
    Carga como valor privado de la clase los perfiles.
    :return: Los datos de cada perfil que hay.
    """
    archivo_url = os.path.join(ruta.CONFIG_DIR, "perfiles.json")
    try:
        with open(archivo_url, "r", encoding="utf-8") as arch_perfiles:
            perfiles = json.load(arch_perfiles)
    except FileNotFoundError:
        with open(archivo_url, "w", encoding="utf-8") as arch_perfiles:
            perfiles = []
            json.dump(perfiles, arch_perfiles)
    return perfiles


def actualizar_perfiles(perfiles, nuevo_perfil=None):
    """
    Actualiza el archivo json de perfiles.
    :param 
        perfiles: los datos de todos los perfiles.
        nuevo_perfil: diccionario con la informacion del perfil nuevo ingresada por el usuario.
    :return: los datos actualizados de los perfiles.
    """
    if nuevo_perfil is not None:
        perfiles.append(nuevo_perfil)

    archivo_url = os.path.join(ruta.CONFIG_DIR, "perfiles.json")
    with open(archivo_url, "w", encoding="utf-8") as arch_perfiles:
        json.dump(perfiles, arch_perfiles)
    return perfiles


def comprobar_perfil(window, values, conf):
    """
    Verifica si los datos ingresados son correctos, si lo son carga el perfil, sino envia un mensaje al usuario.
    :param
        window: variable para actualizar el contenido de la pantalla.
        values: variable para acceder a los valores de la pantalla.
        conf: las variables internas de la pantalla configuracion.
    :return: False si la informacion no es correcta, True de lo contrario.
    """
    if not values["-INPUT_EDAD-"] or  values["-INPUT_GENERO-"] == 'Seleccione su género':
        window["-MSJ_EDITAR-"].update(value="*Ingrese todos los datos.")
        return False
    else:
        try:
            int(values["-INPUT_EDAD-"])
            if len(values["-INPUT_EDAD-"]) < 1 or len(values["-INPUT_EDAD-"]) > 2:
                window["-MSJ_EDITAR-"].update(value="*Ingrese una edad correcta.")
                return False
            else:
                conf["perfiles"][conf["act"]]["edad"] = values["-INPUT_EDAD-"]
                conf["perfiles"][conf["act"]]["genero"] = values["-INPUT_GENERO-"]
                conf["perfiles"] = actualizar_perfiles(conf["perfiles"])
                return True
        except ValueError:
            window["-MSJ_EDITAR-"].update(value="*La edad solo puede tener números.")
            return False
    

def comprobar_nuevo(window, values, conf):
    """
    Verifica si los datos ingresados son correctos, si lo son carga el perfil, sino envia un mensaje al usuario.
    :param
        window: variable para actualizar el contenido de la pantalla.
        values: variable para acceder a los valores de la pantalla.
        conf: las variables internas de la pantalla configuracion.
    :return: False si la informacion no es correcta, True de lo contrario.
    """
    if not values["-NUEVO_NOMBRE-"]or not values["-NUEVO_EDAD-"] or values["-NUEVO_GENERO-"] == 'Seleccione su género':
        window["-MSJ_CREAR-"].update(value="*Ingrese todos los datos.")
        return False
    else:
        try:
            int(values["-NUEVO_EDAD-"])
            if len(values["-NUEVO_NOMBRE-"]) > 20:
                window["-MSJ_CREAR-"].update(value="*El nick puede tener hasta 20 caracteres.")
                return False
            elif [x for x in conf["perfiles"] if x["nombre"] == values["-NUEVO_NOMBRE-"]]:
                window["-MSJ_CREAR-"].update(value="*El nick ya existe.")
                return False
            elif len(values["-NUEVO_EDAD-"]) < 1 or len(values["-NUEVO_EDAD-"]) > 2:
                window["-MSJ_CREAR-"].update(value="*Ingrese una edad correcta.")
                return False
            else:
                nuevo_perfil = {
                    "nombre": values["-NUEVO_NOMBRE-"],
                    "edad": values["-NUEVO_EDAD-"],
                    "genero": values["-NUEVO_GENERO-"]
                }
                conf["perfiles"] = actualizar_perfiles(conf["perfiles"], nuevo_perfil)
                return True
        except ValueError:
            window["-MSJ_CREAR-"].update(value="*La edad solo puede tener números.")
            return False
            

def nombre_perfiles():
    """
    Devuelve los nombres de los perfiles.
    :return: Lista con los nombres de los perfiles.
    """
    return list(map(lambda datos: datos['nombre'], cargar_perfiles()))


def crear_cuentas(conf):
    """
    Genera los elementos para la pantalla de creacion/edicion de perfil.
    :return: el sg.Window para ejecutar la pantalla.
    """
    conf["perfiles"] = cargar_perfiles()
    sg.theme('figurace_tema')
    crear = [
        [sg.Text("Ingrese un Nick:    ", font=cg.FUENTE_BOTONES),
            sg.Input("", key="-NUEVO_NOMBRE-", font=cg.FUENTE_BOTONES)],
        [sg.Text("Ingrese su Edad:    ", font=cg.FUENTE_BOTONES),
            sg.Input("", key="-NUEVO_EDAD-", font=cg.FUENTE_BOTONES)],
        [sg.Text("Ingrese su Genero:  ", font=cg.FUENTE_BOTONES),
            sg.Combo(['Masculino', 'Femenino', 'Trans','No Binario', 'Otro'], key="-NUEVO_GENERO-",
                default_value='Seleccione su género', readonly=True, size=cg.TAM_COMBO, font=cg.FUENTE_COMBO)],
        [sg.Text("Ingrese una edad valida", key="-MSJ_CREAR-", visible=False, font=cg.FUENTE_BOTONES)],
        [sg.Text()],
        [sg.Button("Crear", key="-BTN_CREAR-", font=cg.FUENTE_BOTONES),
            sg.Button("Cancelar", key="-BTN_CANCELAR_CREAR-", font=cg.FUENTE_BOTONES)]
    ]

    datos = [
            [sg.Text("Nick:    ", font=cg.FUENTE_BOTONES),
                sg.Text("", key="-NOMBRE_MOSTRAR-", font=cg.FUENTE_BOTONES)],
            [sg.Text("Edad:    ", font=cg.FUENTE_BOTONES),
                sg.Text("", key="-EDAD_MOSTRAR-", font=cg.FUENTE_BOTONES)],
            [sg.Text("Genero:  ", font=cg.FUENTE_BOTONES),
                sg.Text("", key="-GENERO_MOSTRAR-", font=cg.FUENTE_BOTONES)]
    ]

    editar = [
        [sg.pin(sg.Button("Editar", key="-BTN_EDITAR-", font=cg.FUENTE_BOTONES)),
            sg.pin(sg.Button("Eliminar", key="-BTN_EDITAR_ELIMINAR-", font=cg.FUENTE_BOTONES)),
            sg.pin(sg.Button("Cancelar", key="-BTN_EDITAR_CANCELAR-", font=cg.FUENTE_BOTONES)),
            sg.pin(sg.Button("Aplicar", key="-BTN_APLICAR_EDICION-", font=cg.FUENTE_BOTONES))]
    ]

    datos_edit = [
            [sg.Text("Nick:    ", font=cg.FUENTE_BOTONES),
                sg.Text("", key="-INPUT_NOMBRE-", font=cg.FUENTE_BOTONES)],
            [sg.Text("Edad:    ", font=cg.FUENTE_BOTONES),
                sg.Input("", key="-INPUT_EDAD-", font=cg.FUENTE_BOTONES)],
            [sg.Text("Genero:  ", font=cg.FUENTE_BOTONES),
                sg.Combo(['Masculino', 'Femenino', 'Trans','No Binario', 'Otro'], key="-INPUT_GENERO-",
                    default_value='Seleccione su género', readonly=True, size=cg.TAM_COMBO, font=cg.FUENTE_COMBO)],
            [sg.Text("Ingrese una edad valida", key="-MSJ_EDITAR-", visible=False, font=cg.FUENTE_BOTONES)]
    ]

    menu_prin = [
        [sg.Push(), sg.Listbox([a["nombre"] for a in conf["perfiles"]], size=(cg.TAM_COLUMNAS[0]//10,
                                                                              cg.TAM_COLUMNAS[0]//80),
                               key="-PERFILES-", font=cg.FUENTE_BOTONES)],
        [sg.Push(), sg.Button("Aceptar", key="-ACEPTAR_PERFIL-", font=cg.FUENTE_BOTONES),
            sg.Button("Crear Perfil", key="-PERFIL_NUEVO-", font=cg.FUENTE_BOTONES), sg.Push()]
    ]

    layout = [
            [sg.Push(), sg.Text("Editar Perfil", font=cg.FUENTE_TITULO), sg.Push()],
            [sg.HSep()],
            [sg.VPush()],
            [sg.Push(), sg.pin(sg.Col(menu_prin, key="-BTN_PRIN-", visible=True)), sg.Push()],
            [sg.VPush()],
            [sg.pin(sg.Col(crear, key="-NUEVO_USUARIO-", visible=False))],
            [sg.Push(), sg.pin(sg.Col(datos, key="-MOSTRAR_DATOS-", visible=False)), sg.Push(), sg.Push()],
            [sg.pin(sg.Col(datos_edit, key="-EDITAR_DATOS-", visible=False))],
            [sg.VPush()],
            [sg.Push(), sg.Push(), sg.pin(sg.Col(editar, key="-BTNS_EDITAR-", visible=False)), sg.Push()],
            [sg.VPush()],
            [sg.Button("Volver", key='-VOLVER_PERFILES-', font=cg.FUENTE_COMBO), sg.Push()]
        ]
    ruta_titlebar_icon = os.path.join(ruta.IMAGENES_DIR, "cartas_icon.png")
    ruta_icon = os.path.join(ruta.IMAGENES_DIR, "cartas_icon.ico")
    return sg.Window("Figurace - Edición de Perfil", layout, size=cg.TAM_VENTANA, finalize=True,
                     use_custom_titlebar=True, titlebar_icon=ruta_titlebar_icon, icon=ruta_icon)


def crear_perfil(window):
    """
    Abre la interfaz para crear nuevo perfil y oculta las demás interfaces.
    :param window: variable con los elementos de la pantalla.
    """
    window["-NUEVO_USUARIO-"].update(visible=True)
    window["-BTN_PRIN-"].update(visible=False)
    window["-MOSTRAR_DATOS-"].update(visible=False)
    window["-BTNS_EDITAR-"].update(visible=False)
    window["-MSJ_CREAR-"].update(visible=False)
    window["-NUEVO_GENERO-"].update(value='Seleccione su género')



def cancelar_crear(window):
    """
    Cierra la interfaz para crear nuevo perfil y muestra la interfaz principal de la pantalla.
    :param window: variable con los elementos de la pantalla.
    """
    window["-NUEVO_NOMBRE-"].update(value="")
    window["-NUEVO_EDAD-"].update(value="")
    window["-NUEVO_GENERO-"].update(value="")

    window["-NUEVO_USUARIO-"].update(visible=False)
    window["-BTN_PRIN-"].update(visible=True)


def aceptar_crear(window, values, conf):
    """
    Valida el nuevo perfil, lo carga y vuelve a la interfaz principal si está bien, sino muestra un mensaje.
    :param
     window y values: variables para controlar y acceder a los componentes de la pantalla.
     conf: diccionario con los perfiles y numero de perfil usado.
    """
    if comprobar_nuevo(window, values, conf):
        window["-NUEVO_NOMBRE-"].update(value="")
        window["-NUEVO_EDAD-"].update(value="")
        window["-NUEVO_GENERO-"].update(value="")

        window["-NUEVO_USUARIO-"].update(visible=False)
        window["-BTN_PRIN-"].update(visible=True)
        window["-PERFILES-"].update(values=[a["nombre"] for a in conf["perfiles"]])
    else:
        window["-MSJ_CREAR-"].update(visible=True)


def seleccionar_perfil(window, values, conf):
    """
    Busca el perfil seleccionado y muestra sus datos.
    :param
     window y values: variables para controlar y acceder a los componentes de la pantalla.
     conf: diccionario con los perfiles y numero de perfil usado.
    """
    if values["-PERFILES-"]:
        conf["act"] = 0
        while conf["act"] != len(conf["perfiles"]) and \
                conf["perfiles"][conf["act"]]["nombre"] != values["-PERFILES-"][0]:
            conf["act"] += 1
        if conf["perfiles"][conf["act"]]["nombre"] == values["-PERFILES-"][0]:
            window["-MOSTRAR_DATOS-"].update(visible=True)
            window["-BTNS_EDITAR-"].update(visible=True)

            window["-NOMBRE_MOSTRAR-"].update(value=conf["perfiles"][conf["act"]]["nombre"])
            window["-EDAD_MOSTRAR-"].update(value=conf["perfiles"][conf["act"]]["edad"])
            window["-GENERO_MOSTRAR-"].update(value=conf["perfiles"][conf["act"]]["genero"])

            window["-BTN_APLICAR_EDICION-"].update(visible=False)
            window["-BTN_EDITAR_CANCELAR-"].update(visible=False)
            window["-BTN_EDITAR-"].update(visible=True)
            window["-BTN_EDITAR_ELIMINAR-"].update(visible=True)


def editar_perfil(window, conf):
    """
    Muestra la interfaz para editar el perfil seleccionado.
    :param
     window : variables para controlar los componentes de la pantalla.
     conf: diccionario con los perfiles y numero de perfil usado.
    """
    window["-MOSTRAR_DATOS-"].update(visible=False)
    window["-BTN_APLICAR_EDICION-"].update(visible=True)
    window["-BTN_PRIN-"].update(visible=False)
    window["-BTN_EDITAR-"].update(visible=False)
    window["-BTN_EDITAR_CANCELAR-"].update(visible=True)
    window["-BTN_EDITAR_ELIMINAR-"].update(visible=False)
    window["-MSJ_EDITAR-"].update(visible=False)

    window["-INPUT_NOMBRE-"].update(value=conf["perfiles"][conf["act"]]["nombre"])
    window["-INPUT_EDAD-"].update(value=conf["perfiles"][conf["act"]]["edad"])
    window["-INPUT_GENERO-"].update(value=conf["perfiles"][conf["act"]]["genero"])

    window["-BTN_EDITAR_CANCELAR-"].update(visible=True)
    window["-EDITAR_DATOS-"].update(visible=True)


def cancelar_edicion(window):
    """
    Cierra la interfaz para editar el perfil seleccionado y vuelve a la interfaz de los datos.
    :param
     window : variables para controlar los componentes de la pantalla.
    """
    window["-MOSTRAR_DATOS-"].update(visible=True)
    window["-BTN_APLICAR_EDICION-"].update(visible=False)
    window["-BTN_PRIN-"].update(visible=True)
    window["-BTN_EDITAR-"].update(visible=True)
    window["-BTN_EDITAR_ELIMINAR-"].update(visible=True)

    window["-BTN_EDITAR_CANCELAR-"].update(visible=False)
    window["-EDITAR_DATOS-"].update(visible=False)


def aplicar_edicion(window, values, conf):
    """
    Verifica los datos ingresados y actualiza el perfil seleccionado.
    :param
     window y values: variables para controlar y acceder a los componentes de la pantalla.
     conf: diccionario con los perfiles y numero de perfil usado.
    """
    if comprobar_perfil(window, values, conf):
        window["-MOSTRAR_DATOS-"].update(visible=True)
        window["-BTN_APLICAR_EDICION-"].update(visible=False)
        window["-BTN_PRIN-"].update(visible=True)
        window["-BTN_EDITAR-"].update(visible=True)
        window["-BTN_EDITAR_ELIMINAR-"].update(visible=True)

        window["-EDAD_MOSTRAR-"].update(value=conf["perfiles"][conf["act"]]["edad"])
        window["-GENERO_MOSTRAR-"].update(value=conf["perfiles"][conf["act"]]["genero"])

        window["-BTN_EDITAR_CANCELAR-"].update(visible=False)
        window["-EDITAR_DATOS-"].update(visible=False)
    else:
        window["-MSJ_EDITAR-"].update(visible=True)


def eliminar_perfil(window, conf):
    """
    Cierra la interfaz para editar el perfil seleccionado y vuelve a la interfaz de los datos.
    :param
     window : variables para controlar los componentes de la pantalla.
     conf: diccionario con los perfiles y numero de perfil usado.
    """
    if cg.ventana_chequear_accion(window, "¿Está seguro de eliminar este perfil?") == "Sí":
        window["-BTN_APLICAR_EDICION-"].update(visible=True)
        window["-BTN_EDITAR_CANCELAR-"].update(visible=True)
        window["-BTN_EDITAR-"].update(visible=False)
        window["-BTN_EDITAR_ELIMINAR-"].update(visible=False)
        window["-MOSTRAR_DATOS-"].update(visible=False)
        window["-BTNS_EDITAR-"].update(visible=False)

        conf["perfiles"] = [x for x in conf["perfiles"] if x["nombre"] != conf["perfiles"][conf["act"]]["nombre"]]
        conf["perfiles"] = actualizar_perfiles(conf["perfiles"])
        window["-PERFILES-"].update(values=[a["nombre"] for a in conf["perfiles"]])
