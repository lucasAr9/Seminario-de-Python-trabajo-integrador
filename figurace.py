import PySimpleGUI as sg
import time
import uuid
import os
import rutas

from datetime import datetime
from src.pantallas import juego
from src.pantallas import configuracion
from src.pantallas import puntajes
from src.pantallas import cuentas
from src.pantallas import eleccion_dataset
from src.pantallas import instrucciones
from src.pantallas import menu_inicio_juego as menu
from src.pantallas import caracteristicas_generales as cg
from src.funcionalidad import partida as p
from src.funcionalidad import tarjeta as tarje
from src.funcionalidad import dificultad as dificultad


def abrir_instrucciones():
    """
    Crea la ventana de instrucciones y maneja sus eventos
    """
    window = instrucciones.crear_ventana()
    indice = 1  # Para llevar el cambio de imagen en orden
    nro_tutorial = 0  # Para acceder al tutorial correcto
    instrucciones.control_gif(window)  # el gif se corta luego de 4 seg
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, '-VOLVER-'):
            break
        match event:
            case '__TIMEOUT__':
                pass
            case '-SIG-':
                # verifico no salir del rango de cant de imagenes de cada tutorial
                # 0 = la ruta de la imagen, 1 = la cantidad de imagenes
                if indice + 1 <= list(cg.TUTORIALES[nro_tutorial].values())[0][1]:
                    indice += 1
                    # obtengo la ruta de la imagen que sigue, segun el nro de tutorial
                    ruta = os.path.join(rutas.TUTORIALES_DIR, list(cg.TUTORIALES[nro_tutorial].values())[0][0],
                                        f'paso_{indice}.png')
                    window['-IMAGEN_TUTO-'].update(ruta)
            case '-ATRAS-':
                if indice - 1 > 0:
                    indice -= 1
                    # obtengo la ruta de la imagen que antecede, segun el nro de tutorial
                    ruta = os.path.join(rutas.TUTORIALES_DIR, list(cg.TUTORIALES[nro_tutorial].values())[0][0],
                                        f'paso_{indice}.png')
                    window['-IMAGEN_TUTO-'].update(ruta)
            case _:
                # Evento de elegir el tutorial con sus respectivos botones
                indice = 1
                nro_tutorial = instrucciones.obtener_indice(event)
                eleccion = os.path.join(rutas.TUTORIALES_DIR, (cg.TUTORIALES[nro_tutorial][event])[0],
                                        f'paso_{indice}.png')
                window['-IMAGEN_TUTO-'].update(eleccion)

    window.close()


def abrir_configuracion():
    """Crear la ventana de configuración y responder a los eventos en la misma."""
    window_dificultad = configuracion.crear_ventana()
    while True:
        event, values = window_dificultad.read()
        if event in (sg.WIN_CLOSED, '-VOLVER_CONFIG-'):
            break
        elif event == '-CONFIRMAR_CAMBIOS-':
            dificultad.guardar_nivel_personalizado(values)
            cg.ventana_popup(window_dificultad, 'Se guardaron los cambios personalizados.')
    window_dificultad.close()


def abrir_puntajes():
    """Crear la ventana de puntajes y responder a los eventos en la misma."""
    window = puntajes.armar_ventana()
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, '-VOLVER_AL_MENU-'):
            break
    window.close()


def abrir_perfiles():
    """Crear la ventana de perfiles y responder a los eventos en la misma."""
    conf_cuentas = {"perfiles": cuentas.cargar_perfiles(), "act": 0}
    window = cuentas.crear_cuentas(conf_cuentas)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, '-VOLVER_PERFILES-'):
            conf_cuentas["perfiles"] = cuentas.cargar_perfiles()
            nicks_perfiles = [x["nombre"] for x in conf_cuentas["perfiles"]]
            break
        elif event == '-ACEPTAR_PERFIL-':
            cuentas.seleccionar_perfil(window, values, conf_cuentas)
        elif event == '-PERFIL_NUEVO-':
            cuentas.crear_perfil(window)
        elif event == '-BTN_EDITAR-':
            cuentas.editar_perfil(window, conf_cuentas)
        elif event == '-BTN_EDITAR_ELIMINAR-':
            cuentas.eliminar_perfil(window, conf_cuentas)
        elif event == '-BTN_CREAR-':
            cuentas.aceptar_crear(window, values, conf_cuentas)
        elif event == '-BTN_CANCELAR_CREAR-':
            cuentas.cancelar_crear(window)
        elif event == '-BTN_EDITAR_CANCELAR-':
            cuentas.cancelar_edicion(window)
        elif event == '-BTN_APLICAR_EDICION-':
            cuentas.aplicar_edicion(window, values, conf_cuentas)
    window.close()
    return nicks_perfiles


def analizar_siguiente(tarjeta, partida, window, dificultad_elegida, dataset_elegido, usuario_elegido):
    """Realizar las actualizaciones necesarias de acuerdo a si quedan rondas por jugar o no"""
    if tarjeta.quedan_rondas():
        tarjeta.cargar_datos()  # Se actualizan los datos de la tarjeta
        tarjeta.actual += 1
        tiempo_comienzo = time.time()
        window = juego.cambiar_tarjeta(tarjeta, tarjeta.layout_datos(),
                                       window, dificultad_elegida,
                                       dataset_elegido, usuario_elegido)
        # window['-JUEGO_TABLA-'].update(select_rows=(tarjeta.actual - 1,))
        window.refresh()
        return tiempo_comienzo, window, False
    else:
        # Si se terminaron las rondas se termina la partida
        cg.ventana_popup(window, f'SE ACABARON LAS RONDAS!\n\n'
                                 f'TU PUNTAJE TOTAL ES DE: '
                                 f'{tarjeta.puntos_acumulados}')
        partida.eventos(time.time(), "fin", "finalizada", None, None)
        partida.guardar_puntos(str(datetime.now())[:16], dificultad_elegida, cuentas.usuario(usuario_elegido), 
                                tarjeta.puntos_acumulados)
        return None, window, True


def abrir_elegir_dataset():
    """Crear la ventana de elección de temática para jugar y responder a los eventos en la misma."""
    window = eleccion_dataset.eleccion_dataset()
    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, 'Cancelar'):
            break
        else:
            window.close()
            return event
    window.close()
    return None


def abrir_juego(dificultad_elegida, usuario_elegido):
    """Crear la ventana de juego y responder a los eventos en la misma."""
    dataset_elegido = abrir_elegir_dataset()
    if dataset_elegido:
        cg.ventana_de_carga()
        partida = p.Partida()
        tarjeta = tarje.Tarjeta(dataset_elegido, dificultad_elegida)
        tarjeta.cargar_datos()  # Se cargan los primeros datos de la tarjeta a utilizar
        window = juego.armar_ventana(tarjeta, tarjeta.layout_vacio(), dificultad_elegida, dataset_elegido,
                                     usuario_elegido)
        minutos, segundos = divmod(tarjeta.datos_dificultad.tiempo, 60)
        window['-JUEGO_TIEMPO-'].update(f'{minutos:02d}:{segundos:02d}')
        window['-JUEGO_COMENZAR-'].update(visible=True)

        while True:
            event, values = window.read()
            if event == '-JUEGO_ABANDONAR-' and cg.ventana_chequear_accion(window) == 'Sí':
                tarjeta.puntos_acumulados = 0  # si abandona, no suma/resta puntos
                break
            elif event == '-JUEGO_COMENZAR-':
                window_a_cerrar = window
                window = juego.armar_ventana(tarjeta, tarjeta.layout_datos(), dificultad_elegida, dataset_elegido,
                                             usuario_elegido)
                window_a_cerrar.close()
                tiempo_comienzo = time.time()
                partida.comienzo(tiempo_comienzo, uuid.uuid4(), "inicio_partida", cuentas.usuario(usuario_elegido),
                                 dificultad_elegida)

                while True:
                    event, values = window.read(timeout=100)
                    # CONTROL DEL TIEMPO DE LA PARTIDA
                    delta_tiempo = time.time() - tiempo_comienzo
                    tiempo_transcurrido = int(tarjeta.datos_dificultad.tiempo - delta_tiempo)
                    minutos, segundos = divmod(tiempo_transcurrido, 60)
                    window['-JUEGO_TIEMPO-'].update(f'{minutos:02d}:{segundos:02d}')
                    window['-JUEGO_BARRA-'].update(current_count=delta_tiempo + 1)

                    if event == '-JUEGO_ABANDONAR-':
                        if (cg.ventana_chequear_accion(window,
                                                       'Se darán por perdidas la ronda actual\ny las rondas restantes!\n\n'
                                                       'Segurx que querés volver al menú?') == 'Sí'):
                            tarjeta.puntos_acumulados = 0  # si abandona, no suma/resta puntos
                            partida.eventos(time.time(), "fin", "cancelada", None, None)
                            break
                        else:
                            window['-JUEGO_TIEMPO-'].update('00:00')
                            window['-JUEGO_BARRA-'].update(current_count=0)
                            window.refresh()

                    if window['-JUEGO_TIEMPO-'].Get() == '00:00':
                        # Si se acaba el tiempo se pasa de ronda
                        partida.eventos(time.time(), "timeout", "error", None, tarjeta.respuesta_correcta)
                        window['-JUEGO_TIEMPO-'].update(background_color='Red')
                        for respuesta in tarjeta.dict_respuestas['Posibles']:
                            window[respuesta].update(background_color='Red', text_color='Black')
                        tarjeta.analizar_respuesta('tiempo', window)
                        window.refresh()
                        time.sleep(1)
                        tiempo_comienzo, window, cortar = analizar_siguiente(tarjeta, partida,
                                                                             window, dificultad_elegida,
                                                                             dataset_elegido, usuario_elegido)
                        if cortar:
                            break
                    # CONTROL DE LA ELECCIÓN DE RESPUESTA
                    if event in ('-JUEGO_PASAR-', '-ELECCION-'):
                        eleccion = (dict(filter(lambda x: x[1], values.items())))
                        # Si intenta confirmar sin seleccionar respuesta, no ocurre nada
                        try:
                            if event == '-JUEGO_PASAR-':
                                eleccion = None  # Se le asigna None para poder pasar la tarjera sin seleccionar
                                for respuesta in tarjeta.dict_respuestas['Posibles']:
                                    window[respuesta].update(background_color='Yellow', text_color='Black')
                                partida.eventos(time.time(), "pasar", None, None, tarjeta.respuesta_correcta)

                            else:
                                eleccion = (list(eleccion.keys())[0])
                                window[eleccion].update(background_color='Red', text_color='Black')
                                window[tarjeta.respuesta_correcta].update(background_color='Green',
                                                                          text_color='Black')

                                if eleccion == tarjeta.respuesta_correcta:
                                    partida.eventos(time.time(), "intento", "ok", eleccion,
                                                    tarjeta.respuesta_correcta)
                                    tarjeta.puntos_por_tiempo(tiempo_transcurrido, window)
                                else:
                                    partida.eventos(time.time(), "intento", "error", eleccion,
                                                    tarjeta.respuesta_correcta)

                            tarjeta.analizar_respuesta(eleccion, window)
                            window['-JUEGO_TABLA-'].update(values=tarjeta.resultados_para_tabla())
                            window.refresh()
                            time.sleep(1)
                        except IndexError:
                            pass
                        else:
                            tiempo_comienzo, window, cortar = analizar_siguiente(tarjeta, partida,
                                                                                 window, dificultad_elegida,
                                                                                 dataset_elegido, usuario_elegido)
                            if cortar:
                                break
                break
        window.close()


def main():
    """Crear la ventana menú inicial y responder a los eventos en la misma."""
    usuario_elegido = False
    dificultad_elegida = False
    perfiles = cuentas.nombre_perfiles()
    window = menu.crear_menu(perfiles)
    while True:
        event, values = window.read()
        # MANEJO DE SALIDA DEL MENU PRINCIPAL
        if (event in (sg.WINDOW_CLOSE_ATTEMPTED_EVENT, '-SALIR-') and
                (cg.ventana_chequear_accion(window) == 'Sí')):
            break

        # MANEJO DE EVENTOS DEL MENU PRINCIPAL
        match event:
            case '-USUARIOS-':
                usuario_elegido = window['-USUARIOS-'].Get()
            case '-DIFICULTAD-':
                dificultad_elegida = window['-DIFICULTAD-'].Get()
                if dificultad_elegida == 'Personalizado':
                    window['-AVISO_PER-'].update(visible=True)
                else:
                    window['-AVISO_PER-'].update(visible=False)
            case '-JUGAR-':
                if usuario_elegido and dificultad_elegida:
                    window.hide()
                    abrir_juego(dificultad_elegida, usuario_elegido)
                    window.un_hide()
                else:
                    cg.ventana_popup(window,
                                     'Por favor seleccione una dificultad y usuario, antes de comenzar a jugar.')
            case '-CONFIGURACION-':
                window.hide()
                abrir_configuracion()
                window.un_hide()
            case '-PUNTAJES-':
                window.hide()
                abrir_puntajes()
                window.un_hide()
            case '-PERFIL-':
                window.hide()
                perfiles = abrir_perfiles()
                window.un_hide()
                window['-USUARIOS-'].update('Seleccione su usuario', values=perfiles)
                usuario_elegido = ''
            case '-INSTRUCCIONES-':
                window.hide()
                abrir_instrucciones()
                window.un_hide()

    window.close()


if __name__ == "__main__":
    main()
