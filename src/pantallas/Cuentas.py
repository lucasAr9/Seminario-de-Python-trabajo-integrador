import PySimpleGUI as sg
import os
import json


class Perfiles:
    def __init__(self):
        return

    def __cargar_perfiles(self):
        """
        Carga como valor privado de la clase los perfiles.
        """
        archivo_url = os.path.join(os.path.realpath('..'), "recursos", "datos", "perfiles.json")
        try:
            with open(archivo_url, "r", encoding="utf-8") as arch_perfiles:
                self.__perfiles = json.load(arch_perfiles)
        except FileNotFoundError:
            with open(archivo_url, "w", encoding="utf-8") as arch_perfiles:
                self.__perfiles = []
                json.dump(self.__perfiles, arch_perfiles)

    def __actualizar_perfiles(self, nuevo_perfil=[]):
        """
        Actualiza el archivo json de perfiles.
        :param nuevo_perfil: diccionario con la informacion del perfil nuevo ingresada por el usuario.
        """
        archivo_url = os.path.join(os.path.realpath('..'), "recursos", "datos" , "perfiles.json")

        if nuevo_perfil != []:
            self.__perfiles.append(nuevo_perfil)
        
        with open(archivo_url, "w", encoding="utf-8") as arch_perfiles:
            json.dump(self.__perfiles, arch_perfiles)

    def __comprobar_y_cargar(self, window, values, op):
        """
        Verifica si los datos ingresados son correctos, si lo son carga el perfil, sino envia un mensaje al usuario.
        :param 
            window: variable para actualizar el contenido de la pantalla.
            values: variable para acceder a los valores de la pantalla.
            op: variable que indica si la llamada proviende de la creacion o edicion de un perfil.
        :return: False si la informacion no es correcta, True de lo contrario.
        """
        if op == 1:
            if values["-INPUT_EDAD-"] == "" or values["-INPUT_GENERO-"] == "":
                window["-MSJ_EDITAR-"].update(value="*Ingrese todos los datos.")
                return False
            elif values["-INPUT_EDAD-"] <= "0" or values["-INPUT_EDAD-"] >= "9":
                window["-MSJ_EDITAR-"].update(value="*La edad no es correcta.")
                return False
            else:
                self.__perfiles[self.__act]["edad"] = values["-INPUT_EDAD-"]
                self.__perfiles[self.__act]["genero"] = values["-INPUT_GENERO-"]
                self.__actualizar_perfiles()
                return True
        elif op == 2:
            if values["-NUEVO_NOMBRE-"] == "" or values["-NUEVO_EDAD-"] == "" or values["-NUEVO_GENERO-"] == "":
                window["-MSJ_CREAR-"].update(value="*Ingrese todos los datos.")
                return False
            elif values["-NUEVO_EDAD-"] <= "0" or values["-NUEVO_EDAD-"] >= "9":
                window["-MSJ_CREAR-"].update(value="*La edad no es correcta.")
                return False
            else:
                nuevo_perfil = {
                    "nombre": values["-NUEVO_NOMBRE-"],
                    "edad": values["-NUEVO_EDAD-"],
                    "genero": values["-NUEVO_GENERO-"]
                }
                self.__actualizar_perfiles(nuevo_perfil)
                return True

    def crear_pantalla(self, pant_conf={"tam_ventana": (600, 500), "font_botones": "Verdana 15"}):
        """
        Genera los elementos para la pantalla de creacion/edicion de perfil.
        :param pant_conf: diccionario con las especificaciones de la pantalla (tamaños y fuentes).
        :return: el sg.Window para ejecutar la pantalla.
        """
        self.pant_conf = pant_conf
        self.__cargar_perfiles()
        sg.theme('DarkAmber')
        crear = [
            [sg.Text("Ingrese un Nick:    ", font=pant_conf["font_botones"]),
                sg.InputText("", key="-NUEVO_NOMBRE-", font=pant_conf["font_botones"])],
            [sg.Text("Ingrese su Edad:    ", font=pant_conf["font_botones"]),
                sg.InputText("", key="-NUEVO_EDAD-", font=pant_conf["font_botones"])],
            [sg.Text("Ingrese su Genero:  ", font=pant_conf["font_botones"]),
                sg.InputText("", key="-NUEVO_GENERO-", font=pant_conf["font_botones"])],
            [sg.Text("Ingrese una edad valida", key="-MSJ_CREAR-", visible=False, font=pant_conf["font_botones"])],
            [sg.Text()],
            [sg.Button("Crear", key="-BTN_CREAR-", font=pant_conf["font_botones"]), 
                sg.Button("Cancelar", key="-BTN_CANCELAR_CREAR-", font=pant_conf["font_botones"])]
        ]

        datos = [
                [sg.Text("Nick:    ", font=pant_conf["font_botones"]),
                    sg.Text("", key="-NOMBRE_MOSTRAR-", font=pant_conf["font_botones"])],
                [sg.Text("Edad:    ", font=pant_conf["font_botones"]),
                    sg.Text("", key="-EDAD_MOSTRAR-", font=pant_conf["font_botones"])],
                [sg.Text("Genero:  ", font=pant_conf["font_botones"]),
                    sg.Text("", key="-GENERO_MOSTRAR-", font=pant_conf["font_botones"])]
        ]
        
        editar = [
            [sg.pin(sg.Button("Editar", key="-BTN_EDITAR-", font=pant_conf["font_botones"])),
                sg.pin(sg.Button("Cancelar", key="-BTN_EDITAR_CANCELAR-", font=pant_conf["font_botones"])),
                sg.Button("Aplicar", key="-BTN_APLICAR_EDICION-", font=pant_conf["font_botones"])]
        ]
        
        datos_edit = [
                [sg.Text("Nick:    ", font=pant_conf["font_botones"]),
                    sg.Text("", key="-INPUT_NOMBRE-", font=pant_conf["font_botones"])],
                [sg.Text("Edad:    ", font=pant_conf["font_botones"]),
                    sg.InputText("", key="-INPUT_EDAD-", font=pant_conf["font_botones"])],
                [sg.Text("Genero:  ", font=pant_conf["font_botones"]),
                    sg.InputText("", key="-INPUT_GENERO-", font=pant_conf["font_botones"])],
                [sg.Text("Ingrese una edad valida", key="-MSJ_EDITAR-", visible=False, font=pant_conf["font_botones"])]
        ]

        menu_prin = [
            [sg.Push(), sg.Listbox([a["nombre"] for a in self.__perfiles], size=(7, 4), key="-PERFILES-",
                                   font=pant_conf["font_botones"]),
                sg.Push(), sg.Button("Aceptar", key="-ACEPTAR_PERFIL-", font=pant_conf["font_botones"]),
                sg.Button("Crear Perfil", key="-PERFIL_NUEVO-", font=pant_conf["font_botones"]), sg.Push()]
        ]

        layout = [
                [sg.Push(), sg.Text("Editar Perfil", font="Verdana 35"), sg.Push()],
                [sg.VPush()],
                [sg.Push(), sg.pin(sg.Col(menu_prin, key="-BTN_PRIN-", visible=True)), sg.Push()],
                [sg.VPush()],
                [sg.pin(sg.Col(crear, key="-NUEVO_USUARIO-", visible=False))],
                [sg.Push(),sg.pin(sg.Col(datos, key="-MOSTRAR_DATOS-", visible=False)), sg.Push(), sg.Push()],
                [sg.pin(sg.Col(datos_edit, key="-EDITAR_DATOS-", visible=False))],
                [sg.VPush()],
                [sg.Push(), sg.Push(), sg.pin(sg.Col(editar, key="-BTNS_EDITAR-", visible=False)), sg.Push()],
                [sg.VPush()],
                [sg.Button("Volver", key='-VOLVER_PERFILES-', font=pant_conf["font_botones"]), sg.Push()]
            ]
        ruta_titlebar_icon = os.path.join(os.path.realpath('..'), "recursos", "imagenes", "cartas_icon.png")
        ruta_icon = os.path.join(os.path.realpath('..'), "recursos", "imagenes", "cartas_icon.ico")
        return sg.Window("FiguRace - Edición de Perfil", layout, size=pant_conf["tam_ventana"], finalize=True,
                         use_custom_titlebar=True, titlebar_icon=ruta_titlebar_icon, icon=ruta_icon)

    def analisis_event_editar(self, window, event, values):
        """
        Verifica los eventos y ejecuta los cambios correspondientes
        :param 
            window, event y values: variables para controlar y acceder a los componentes de la pantalla.
        :return: variable perf si no se cierra la pantalla, lo contrario una lista con los nombres de los perfiles.
        """
        if event == "-PERFIL_NUEVO-":
            window["-NUEVO_USUARIO-"].update(visible=True)
            window["-BTN_PRIN-"].update(visible=False)
            window["-MOSTRAR_DATOS-"].update(visible=False)
            window["-BTNS_EDITAR-"].update(visible=False)

        elif event == "-BTN_CANCELAR_CREAR-":
            window["-NUEVO_NOMBRE-"].update(value="")
            window["-NUEVO_EDAD-"].update(value="")
            window["-NUEVO_GENERO-"].update(value="")

            window["-NUEVO_USUARIO-"].update(visible=False)
            window["-BTN_PRIN-"].update(visible=True)
            window["-MSJ_CREAR-"].update(visible=False)

        elif event == "-BTN_CREAR-":
            if self.__comprobar_y_cargar(window, values, 2):
                window["-NUEVO_NOMBRE-"].update(value="")
                window["-NUEVO_EDAD-"].update(value="")
                window["-NUEVO_GENERO-"].update(value="")

                window["-NUEVO_USUARIO-"].update(visible=False)
                window["-BTN_PRIN-"].update(visible=True)
                window["-PERFILES-"].update(values=[a["nombre"] for a in self.__perfiles])
            else:
                window["-MSJ_CREAR-"].update(visible=True)
        
        elif event == "-ACEPTAR_PERFIL-":
            if len(values["-PERFILES-"]) == 1:
                self.__act = 0
                while self.__act != len(self.__perfiles) and \
                        self.__perfiles[self.__act]["nombre"] != values["-PERFILES-"][0]:
                    self.__act += 1
                if self.__perfiles[self.__act]["nombre"] == values["-PERFILES-"][0]:
                    window["-MOSTRAR_DATOS-"].update(visible=True)
                    window["-BTNS_EDITAR-"].update(visible=True)

                    window["-NOMBRE_MOSTRAR-"].update(value= self.__perfiles[self.__act]["nombre"])
                    window["-EDAD_MOSTRAR-"].update(value= self.__perfiles[self.__act]["edad"])
                    window["-GENERO_MOSTRAR-"].update(value= self.__perfiles[self.__act]["genero"])

                    window["-BTN_APLICAR_EDICION-"].update(disabled=True)
                    window["-BTN_EDITAR_CANCELAR-"].update(visible=False)

        elif event == "-BTN_EDITAR-":
            window["-MOSTRAR_DATOS-"].update(visible=False)
            window["-BTN_APLICAR_EDICION-"].update(disabled=False)
            window["-BTN_PRIN-"].update(visible=False)
            window["-BTN_EDITAR-"].update(visible=False)

            window["-INPUT_NOMBRE-"].update(value= self.__perfiles[self.__act]["nombre"])
            window["-INPUT_EDAD-"].update(value= self.__perfiles[self.__act]["edad"])
            window["-INPUT_GENERO-"].update(value= self.__perfiles[self.__act]["genero"])
           
            window["-BTN_EDITAR_CANCELAR-"].update(visible=True)
            window["-EDITAR_DATOS-"].update(visible=True)

        elif event == "-BTN_EDITAR_CANCELAR-":
            window["-MOSTRAR_DATOS-"].update(visible=True)
            window["-BTN_APLICAR_EDICION-"].update(disabled=True)
            window["-BTN_PRIN-"].update(visible=True)
            window["-BTN_EDITAR-"].update(visible=True)
           
            window["-BTN_EDITAR_CANCELAR-"].update(visible=False)
            window["-EDITAR_DATOS-"].update(visible=False)
            window["-MSJ_EDITAR-"].update(visible=False)

        elif event == "-BTN_APLICAR_EDICION-":
            if self.__comprobar_y_cargar(window, values, 1):
                window["-MOSTRAR_DATOS-"].update(visible=True)
                window["-BTN_APLICAR_EDICION-"].update(disabled=True)
                window["-BTN_PRIN-"].update(visible=True)
                window["-BTN_EDITAR-"].update(visible=True)

                window["-EDAD_MOSTRAR-"].update(value= self.__perfiles[self.__act]["edad"])
                window["-GENERO_MOSTRAR-"].update(value= self.__perfiles[self.__act]["genero"])

                window["-BTN_EDITAR_CANCELAR-"].update(visible=False)
                window["-EDITAR_DATOS-"].update(visible=False)
            else:
                window["-MSJ_EDITAR-"].update(visible=True)

    def perfiles(self):
            return [a["nombre"] for a in self.__perfiles]





