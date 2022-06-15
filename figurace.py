import PySimpleGUI as sg
import time
import uuid

from src.pantallas import caracteristicas_generales as cg, juego_ver_2
from src.funcionalidad import dificultad as dificultad
from src.pantallas.menu_inicio_juego import crear_menu
from src.pantallas import configuracion as c_pantalla
from src.pantallas import cuentas as cuentas
from src.pantallas import puntajes
from src.funcionalidad import tarjeta_ver_2
from src.pantallas import eleccion_dataset


def abrir_configuracion():
    """Crear la ventana de configuración y responder a los eventos en la misma."""
    window_dificultad = c_pantalla.crear_ventana()
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


def abrir_juego(dificultad_elegida, usuario_elegido):
    """Crear la ventana de juego y responder a los eventos en la misma."""
    dataset_elegido = eleccion_dataset.eleccion_dataset()
    if dataset_elegido:
        # guardar los datos de la partida ----------------------------------------------------------------------------??
        datos_de_partida = []

        tarjeta = tarjeta_ver_2.Tarjeta(dataset_elegido, dificultad_elegida)
        window = juego_ver_2.armar_ventana(tarjeta, tarjeta.layout_vacio(), dificultad_elegida,
                                           dataset_elegido, usuario_elegido)
        window['-JUEGO_COMENZAR-'].update(visible=True)

        # generar un id unico para cada partida ----------------------------------------------------------------------??
        id = uuid.uuid4()
        datos_de_partida.append(id)

        while True:
            event, values = window.read()
            if event == '-JUEGO_ABANDONAR-' and cg.ventana_chequear_accion(window) == 'Sí':
                tarjeta.set_puntos_acumulados(0)  # si abandona, no suma/resta puntos
                break
            elif event == '-JUEGO_COMENZAR-':
                tarjeta.cargar_datos()  # Se cargan los primeros datos de la tarjeta
                window_a_cerrar = window
                window = juego_ver_2.armar_ventana(tarjeta, tarjeta.layout_datos(), dificultad_elegida,
                                                   dataset_elegido, usuario_elegido)
                window_a_cerrar.close()
                tiempo_comienzo = time.time()

                while True:
                    event, values = window.read(timeout=100)
                    # CONTROL DEL TIEMPO DE LA PARTIDA
                    delta_tiempo = time.time() - tiempo_comienzo
                    tiempo_transcurrido = int(tarjeta.get_datos_dificultad().get_tiempo() - delta_tiempo)
                    minutos, segundos = divmod(tiempo_transcurrido, 60)
                    window['-JUEGO_TIEMPO-'].update(f'{minutos:02d}:{segundos:02d}')
                    window['-JUEGO_BARRA-'].update(current_count=delta_tiempo + 1)

                    if event == '-JUEGO_ABANDONAR-':
                        if (cg.ventana_chequear_accion(window,
                                                       'Se darán por perdidas la ronda actual\ny las rondas restantes!\n\n'
                                                       'Segurx que querés volver al menú?') == 'Sí'):
                            tarjeta.set_puntos_acumulados(0)  # si abandona, no suma/resta puntos
                            break
                        else:
                            window['-JUEGO_TIEMPO-'].update('00:00')
                            window['-JUEGO_BARRA-'].update(current_count=0)
                            window.refresh()

                    if window['-JUEGO_TIEMPO-'].Get() == '00:00':
                        # Si se acaba el tiempo de termina la partida
                        cg.ventana_popup(window, f'SE ACABO EL TIEMPO!. PASASTE TODAS LAS RONDAS!. '
                                                 f'TU PUNTAJE TOTAL ES DE:{tarjeta.get_puntos_acumulados()}')
                        break
                    # CONTROL DE LA ELECCIÓN DE RESPUESTA

                    match event:
                        case '-JUEGO_PASAR-' | '-ELECCION-':
                            eleccion = (dict(filter(lambda x: x[1], values.items())))
                            # Si intenta confirmar sin seleccionar respuesta, no ocurre nada
                            try:
                                if event == '-JUEGO_PASAR-':
                                    eleccion = None  # Se le asigna un valor None para poder pasar la tarjera sin seleccionar
                                    for respuesta in tarjeta.get_respuestas()['Posibles']:
                                        window[respuesta].update(background_color='Red', text='COBARDE')
                                else:
                                    eleccion = (list(eleccion.keys())[0])
                                    window[eleccion].update(background_color='Red')
                                    window[tarjeta.get_respuesta_correcta()].update(background_color='Green')
                                tarjeta.analizar_respuesta(eleccion)
                                window['-JUEGO_TABLA-'].update(
                                    values=list(enumerate(tarjeta.get_resultados(), start=1)))
                                window.refresh()
                                time.sleep(2)
                            except IndexError:
                                pass
                            else:
                                if tarjeta.quedan_rondas():
                                    tarjeta.cargar_datos()  # Se actualizan los datos de la tarjeta
                                    tiempo_comienzo = time.time()

                                    # guardar el tiempo de comienzo --------------------------------------------------??
                                    datos_de_partida.append(tiempo_comienzo)

                                    window = juego_ver_2.cambiar_tarjeta(tarjeta, tarjeta.layout_datos(),
                                                                         window, dificultad_elegida,
                                                                         dataset_elegido, usuario_elegido)
                                else:
                                    # Si se terminaron las rondas se termina la partida
                                    cg.ventana_popup(window, f'PASASTE TODAS LAS RONDAS!. '
                                                             f'TU PUNTAJE TOTAL ES DE:{tarjeta.get_puntos_acumulados()}')
                                    break
                    # despues con los datos que almacena la tarjeta y este loop hay que armar el csv de la partida
                    # el tema de el cambio de pantallas no me quedo muy bien
                break

        # enviar los datos a la funcion para que guarde en un csv los datos de la partida ----------------------------??
        print(datos_de_partida)
        tarjeta_ver_2.guardar_datos_jugada(datos_de_partida)

        window.close()


def main():
    """Crear la ventana menú inicial y responder a los eventos en la misma."""
    usuario_elegido = False
    dificultad_elegida = False
    indicador_visible = False
    niveles = ['Fácil', 'Medio', 'Difícil', 'Experto']
    perfiles = cuentas.nombre_perfiles()
    window = crear_menu(perfiles)
    while True:
        event, values = window.read(timeout=100)
        if (event in (sg.WINDOW_CLOSE_ATTEMPTED_EVENT, '-SALIR-') and
                (cg.ventana_chequear_accion(window) == 'Sí')):
            break
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
        # Control de indicador_perfiles
        if not perfiles and not indicador_visible:
            window['-INDICADOR-'].update(visible=True)
            indicador_visible = True
        elif perfiles:
            window['-INDICADOR-'].update(visible=False)
            indicador_visible = False

    window.close()


if __name__ == "__main__":
    main()
